echo "AWS Account: $1"
echo "aws cloudformation package --template-file sam.json --s3-bucket standard-update-checker-builds --output-template-file packaged.yml --profile tcc-td-puc-minas-admin"
aws cloudformation package --template-file sam.json --s3-bucket standard-update-checker-builds --output-template-file packaged.yml --profile tcc-td-puc-minas-admin