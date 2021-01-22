provider "aws" {
    profile =                 "tcc-td-puc-minas-admin"
    shared_credentials_file = "~/.aws/credentials"
//    region =                  "sa-east-1"
    region =                  "${var.aws_region}"
}