terraform init

if [ -z "$1" ]
then
  #terraform plan
  terraform apply -auto-approve
else
  #terraform plan -var "account_id=$1"
  terraform apply -auto-approve -var "account_id=$1"
fi

