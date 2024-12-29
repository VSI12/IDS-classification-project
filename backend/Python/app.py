import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, methods=["GET", "POST", "OPTIONS"])
# Fetch environment variables
load_dotenv()  
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
SQS_QUEUE_URL = os.getenv("SQS_URL")

# Initialize the S3 and SQS client
s3_client = boto3.client("s3", region_name=AWS_REGION)
sqs_client = boto3.client("sqs", region_name=AWS_REGION)

@app.route('/generate-presigned-url', methods=['POST'])
def generate_presigned_url():
    try:
        data = request.json
        file_name = data.get("file_name")
        file_type = data.get("file_type")
        
        if not file_name or not file_type:
            return jsonify({"error": "Missing file_name or file_type"}), 400
        
        # Generate the presigned URL for PUT
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': file_name,
                'ContentType': file_type
            },
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return jsonify({"url": presigned_url})
    except ClientError as e:

def receive_message_from_queue():
    try:
        # Receive messages from the queue
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,  # Number of messages to retrieve
            WaitTimeSeconds=10      # Long polling duration
        )

        messages = response.get("Messages", [])
        if messages:
            message = messages[0]
            receipt_handle = message["ReceiptHandle"]

            # Parse the message body
            body = json.loads(message["Body"])

            # Extract bucket and key details from the message
            s3_info = json.loads(body["Message"])  # SNS message might wrap the actual info
            bucket_name = s3_info["Records"][0]["s3"]["bucket"]["name"]
            file_key = s3_info["Records"][0]["s3"]["object"]["key"]
            download_path = f"/tmp/{file_key.split('/')[-1]}"

            # Delete the message from the queue after processing
            sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)

            return bucket_name, file_key, download_path

        else:
            print("No messages in the queue.")
            return None, None

    except Exception as e:
        print(f"Error receiving message: {str(e)}")
        return None, None

def download_file_from_s3(bucket_name, file_key, download_path):
    try:
        s3_client.download_file(Bucket=bucket_name, Key=file_key, Filename=download_path)
        print(f"File downloaded to {download_path}")
        return download_path
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return None

@app.route('/process', methods=['POST'])
def process_model():
    from ids_logic import models
    receive_message_from_queue()
    download_file_from_s3(bucket_name, file_key, download_path)
    dataset = download_path
    models(dataset)

if __name__ == "__main__":
    app.run(debug=True)
