echo "AWS Account: $1"
echo "aws cloudformation describe-stack-events --stack-name standard-update-checker-dynamodb  --region sa-east-1 --profile tcc-td-puc-minas-admin"
aws cloudformation describe-stack-events --stack-name standard-update-checker-dynamodb  --region sa-east-1 --profile tcc-td-puc-minas-admin
