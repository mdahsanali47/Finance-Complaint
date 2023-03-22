variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "model_bucket_name" {
  type    = string
  default = "finance-cat-service"
}

variable "aws_account_id" {
  type    = string
  default = "272281124872"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}

variable "iam_policy_principal_type" {
  type    = string
  default = "AWS"
}

variable "iam_role_name" {
  type    = string
  default = "my_iam_role"
}

