
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
# Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env
# using your lab credentials; never commit .env.
# Ensure S3_ENDPOINT_URL=http://localhost:8333 is set in .env.
set -a
source .env
set +a
uv run aws --endpoint-url "$S3_ENDPOINT_URL" s3 mb s3://dvc
uv run aws --endpoint-url "$S3_ENDPOINT_URL" s3 mb s3://mlflow
make s3-ls
## Contributing

- **Branch naming:** Use `feature/...` for new features, `fix/...` for bug fixes, and `docs/...` for documentation changes.
- **Commit messages:** Follow [Conventional Commits](https://www.conventionalcommits.org/), e.g. `feat: add churn rate test`.
- **Pull Requests:** Ensure all tests pass, include before-and-after metrics in the description, and never commit datasets, trained models, or secrets/passwords.
- **Before pushing:** Run `make lint` and `make test` and make sure both commands pass.
