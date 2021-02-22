terraform init

if [ -z "$1" ]
then
  terraform plan -out $2.binary
else
  terraform plan -var "account_id=$1" -out $2.binary
fi

terraform show -json $2.binary > $2
