variable "upload_bucket_name" {
  description = "The name of the S3 bucket to store the uploaded files."
  type        = string
  
}
variable "queue_arn" {
  description = "The ARN of the SQS queue"
  type        = string
  
}
variable "queue_name" {
  description = "The SQS queue"
  type        = string
  
}
variable "queue_policy" {

  description = "The policy for the SQS queue"
  type        = string
  
}