resource "aws_sqs_queue" "file_upload_queue" {
  name = var.queue_name
}