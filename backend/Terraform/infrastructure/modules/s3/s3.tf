resource "aws_s3_bucket" "upload_bucket" {
  bucket = var.upload_bucket_name
  lifecycle {
    prevent_destroy = true # Prevents the S3 bucket from being destroyed
  }

}

resource "aws_s3_bucket_versioning" "terraform_bucket_versioning" {
  bucket = aws_s3_bucket.upload_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_crypto_conf" {
  bucket = aws_s3_bucket.upload_bucket.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
