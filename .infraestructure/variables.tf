variable "aws_profile" {
  type    = string
  default = "tcc-td-puc-minas-admin"
}

variable "aws_region" {
  type    = string
  default = "sa-east-1"
}

variable "aws_lambda_function_name" {
  type    = string
  default = "standard-update-checker"
}

variable "aws_lambda_handler" {
  type    = string
  default = "app.index"
}

variable "aws_lambda_runtime" {
  type    = string
  default = "python3.8"
}

variable "aws_lambda_filename" {
  type    = string
  default = "../dist/deployment.zip"
}

variable "aws_lambda_source_dir" {
  type    = string
  default = "../"
}