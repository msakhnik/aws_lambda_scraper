provider "aws" {
  region = var.region
}

terraform {
  backend "s3" {
    bucket         = "market-analytic-terraform-state"
    key            = "global/s3/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "market-analytic-terraform-locks"
    encrypt        = true
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../src/"
  output_path = "lambda_function.zip"
}


resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = "layers/lambda-layer.zip"
  layer_name = "lambda_layer_2"
}


resource "aws_kinesis_stream" "test_stream" {
  name             = "market_data-kinesis-stream"
  shard_count      = 1
  retention_period = 48

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]

  tags = {
    Environment = "test"
  }
}

resource "aws_lambda_function" "test_lambda" {
  filename         = "lambda_function.zip"
  function_name    = var.lambda_name
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "lambda_handler.handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
  timeout          = 300
  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.example,
    aws_efs_mount_target.mount_target_az1,
    aws_efs_mount_target.mount_target_az2,
  ]
  layers = [aws_lambda_layer_version.lambda_layer.arn]
  environment {
    variables = {
      LOGLEVEL        = "DEBUG"
      MAX_ITEM_NUMBER = 10
      REQUEST_TIMEOUT = 100
      OUTPUT_KINESIS  = aws_kinesis_stream.test_stream.name
      XDG_CACHE_HOME  = "/tmp/.cache"
      PYPPETEER_HOME  = "/mnt/efs/"
    }
  }
    vpc_config {
    subnet_ids         = [
      "${aws_subnet.private_subnet_1.id}",
      "${aws_subnet.private_subnet_2.id}",
    ]
    security_group_ids = ["${aws_default_security_group.default.id}"]
  }

  file_system_config {
    arn              = "${aws_efs_access_point.access_point_lambda.arn}"
    local_mount_path = "/mnt/efs"
  }
}

resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${var.lambda_name}"
  retention_in_days = 14
}


resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}
