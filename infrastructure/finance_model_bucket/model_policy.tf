provider "aws" {
  region = "ap-south-1"
}

data "aws_iam_policy_document" "allow_full_access" {
  statement {
    actions   = ["s3:*"]
    effect   = "Allow"
    resources = [
        aws_s3_bucket.model_bucket.arn,
        "${aws_s3_bucket.model_bucket.arn}/*",
     ]
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.aws_account_id}:role/${var.iam_role_name}"]
    }
  }
}

resource "aws_s3_bucket_policy" "allow_full_access" {
  bucket = aws_s3_bucket.model_bucket.id
  policy = data.aws_iam_policy_document.allow_full_access.json
}