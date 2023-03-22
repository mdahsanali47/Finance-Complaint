terraform {
  backend "s3" {
    bucket = "finance-model-bucket"
    key    = "tf_state"
    region = "ap-south-1"
    # Specify your AWS profile name
    # profile = "default"
    # Optionally, specify a session token value
    # session_token = "your-value-here"
  }
}

module "finance_artifact_repository" {
  source = "./finance_artifact_repository"
}

module "finance_model_bucket" {
  source = "./finance_model_bucket"
}

module "finance_virtual_machine" {
  source = "./finance_virtual_machine"
}