terraform init

if [ -z "$1" ]
then
  terraform plan
else
  terraform plan -var "account_id=$1"
fi


