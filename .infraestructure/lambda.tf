//locals {
//  lambda_filename = "../dist/deployment.zip"
//}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.lambda_role.id

  policy = "${file("policies/iam/aws_lambda_policy.json")}"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = "${file("policies/iam/aws_lambda_role.json")}"
}

//data "archive_file" "lambda_file" {
//  output_path = "${local.lambda_filename}"
//  source_dir = ""
//  type = "zip"
//}

resource "aws_lambda_function" "test_lambda" {
  function_name = "${var.aws_lambda_function_name}"
  handler = "${var.aws_lambda_handler}"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "${var.aws_lambda_runtime}"
  filename = "${var.aws_lambda_filename}"
}