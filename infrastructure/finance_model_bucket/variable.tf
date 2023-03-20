variable "aws_regioin" {
    type    = string
    default = "us-east-1"
}

variable "model_bucket_name" {
    type    = string
    default = "finance-complaint-service"
}

variable "aws_account_id" {
    type    = string
    default = "272281124872"
}

variable "destroy_bucket_byforce" {
    type    = bool
    default = true
}

variable "iam_policy_principal_type" {
    type    = string
    default = "AWS"
}