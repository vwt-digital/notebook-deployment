echo "Project ID: $1"
echo "Deployment name: $2"

# Check if deployment exists
gcloud deployment-manager deployments describe "$2" --project="$1" >/dev/null 2>&1
result=$?


if [ $result -ne 0 ]; then
	gcloud deployment-manager deployments create "$2" --config config.yaml --project="$1"
else
	gcloud deployment-manager deployments update "$2" --config config.yaml --project="$1"
fi

gsutil cp notebook-deployment/notebook-vm/startup-script.sh gs://"$1"-data-stg/

export INSTANCE_NAME="$2"
export VM_IMAGE_PROJECT="deeplearning-platform-release"
export VM_IMAGE_FAMILY="common-cpu"
export MACHINE_TYPE="n1-standard-1"
export LOCATION="europe-west1-b"
export NETWORK="$1"-vn
export STARTUP_SCRIPT=gs://"$1"-data-stg/startup-script.sh
export SERVICE_ACCOUNT=data-science@"$1".iam.gserviceaccount.com

RES=$(gcloud beta notebooks instances list \
  --location=$LOCATION \
  --format 'value(name)'
  )
if [[ "$RES" == *"$INSTANCE_NAME"* ]]; then
  echo "vm $INSTANCE_NAME already exists"
else
  echo "creating vm " "$INSTANCE_NAME"
  gcloud beta notebooks instances create "$INSTANCE_NAME" \
    --vm-image-project="$VM_IMAGE_PROJECT" \
    --vm-image-family="$VM_IMAGE_FAMILY" \
    --machine-type="$MACHINE_TYPE" \
    --location="$LOCATION" \
    --network="$NETWORK" \
    --post-startup-script="$STARTUP_SCRIPT" \
    --service-account="$SERVICE_ACCOUNT"
fi



