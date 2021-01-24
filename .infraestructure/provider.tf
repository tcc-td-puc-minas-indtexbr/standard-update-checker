provider "aws" {
    profile =                 "tcc-td-puc-minas-admin"
    shared_credentials_file = "~/.aws/credentials"
    region =                  "${var.aws_region}"
}