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
        print(f"Error generating presigned URL: {str(e)}")
        return jsonify({"error": "Failed to generate presigned URL"}), 500

def process_sqs_message():
    # Receive message from SQS
    response = sqs_client.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    messages = response.get("Messages", [])
    if not messages:
        print("No messages in the queue")
        return

    # Parse message
    sqs_message = messages[0]
    receipt_handle = sqs_message["ReceiptHandle"]
    message_body = json.loads(sqs_message["Body"])
    records = message_body.get("Records", [])

    if not records:
        print("No S3 event records found")
        return

    # Extract bucket and object key
    s3_record = records[0]["s3"]
    bucket_name = s3_record["bucket"]["name"]
    object_key = s3_record["object"]["key"]

    print(f"Received file: {object_key} from bucket: {bucket_name}")

    # Download file from S3
    try:
        local_path = f"/tmp/{object_key}"
        s3_client.download_file(bucket_name, object_key, local_path)
        print(f"File downloaded to: {local_path}")
        return local_path
    except Exception as e:
        print(f"Error processing file: {e}")
        return


@app.route('/process', methods=['POST'])
def process_model():
    from ids_logic import models, preprocess

    try:
        # Process the incoming SQS message (download the dataset)
        local_path = process_sqs_message()
        if not local_path:
            return jsonify({"error": "Failed to download the file from S3."}), 500
        
        print(f"File downloaded to {local_path}")

        # Preprocess the data
        processed_data, status = preprocess(local_path)
        if processed_data is None:
            return jsonify({"error": "Preprocessing failed"}), 500

        # Process the model
        result = models(processed_data)
        if result is None:
            return jsonify({"error": "Model processing failed"}), 500

        # Successfully processed and returned predictions
        return jsonify({"result": result}), 200
    
    except Exception as e:
        print(f"Error processing model: {str(e)}")
        return jsonify({"error": f"Failed to process model: {str(e)}"}), 500
    
    try:
        sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
        print("Message deleted from queue")

    except KeyError as e:
        print(f"KeyError in SQS message: {e}")
        return None, None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None, None, None
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None, None, None


if __name__ == "__main__":
    app.run(debug=True)
