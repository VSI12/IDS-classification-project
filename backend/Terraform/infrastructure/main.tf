terraform {
  required_version = ">= 1.9.4"
  backend "s3" {
    bucket         = "ids-classification-tf-state"
    key            = "tf-state/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "ids-classification-tf-lock"
    encrypt        = true
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.50.0"
    }
  }
}

module "s3" {
  source = "./modules/s3"
  upload_bucket_name = local.upload_bucket_name
  queue_arn = module.sqs.sqs_queue_arn
  
}

module "sqs" {
  source = "./modules/sqs"
  queue_name = local.queue_name
  upload_bucket_arn = module.s3.bucket_arn
}