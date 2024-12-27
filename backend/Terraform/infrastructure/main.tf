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
