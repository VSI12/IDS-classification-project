variable "upload_bucket_name" {
  description = "The name of the S3 bucket to store the uploaded files."
  type        = string
  
}

variable "queue_name" {
  description = "The name of the SQS queue"
  type        = string
}