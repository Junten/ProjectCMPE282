resource "aws_iam_role" "lambda_rds" {
  name        = "Lambda_RDS"
  description = "Allows Lambda functions to call RDS"

  tags = {
    CMPE282 = "API"
  }

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
