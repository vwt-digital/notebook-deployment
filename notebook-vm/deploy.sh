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

