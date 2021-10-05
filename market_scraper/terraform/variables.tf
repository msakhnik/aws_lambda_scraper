variable "region" {
  description = "The name of the AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "lambda_name" {
  default = "test_lambda"
}
