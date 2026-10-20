
# Churn MLOps

## Local storage

This project uses SeaweedFS as an S3-compatible local object storage service.
The `dvc` and `mlflow` buckets are used for DVC data storage and MLflow artifacts.

### 1. Start SeaweedFS

Run the following commands from the lab Compose directory.

```bash
cd ~/mlops-lab/compose
docker compose up -d seaweedfs
docker compose ps
cd ~/work/churn-mlops
cp ~/mlops-lab/compose/.env.example .env
cat >> .env <<'ENV'
AWS_ACCESS_KEY_ID=$S3_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=$S3_SECRET_KEY
S3_ENDPOINT_URL=http://localhost:8333
ENV
set -a
source .env
set +a
uv run aws --endpoint-url "$S3_ENDPOINT_URL" s3 mb s3://dvc
uv run aws --endpoint-url "$S3_ENDPOINT_URL" s3 mb s3://mlflow
make s3-ls
