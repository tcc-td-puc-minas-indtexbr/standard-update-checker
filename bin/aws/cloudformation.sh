echo "AWS Account: $1"
echo "cloudformation deploy --template-file packaged.yml --stack-name standard-update-checker-stack --region sa-east-1 --profile tcc-td-puc-minas-admin"
aws cloudformation deploy --template-file packaged.yml --stack-name standard-update-checker-stack --region sa-east-1 --profile tcc-td-puc-minas-admin
