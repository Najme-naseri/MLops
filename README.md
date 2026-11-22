
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
Note: The .env file is not committed to Git because it may contain local configuration, credentials, and secrets that should not be shared publicly.
## Contributing

- **Branch naming:** Use `feature/...` for new features, `fix/...` for bug fixes, and `docs/...` for documentation changes.
- **Commit messages:** Follow [Conventional Commits](https://www.conventionalcommits.org/), e.g. `feat: add churn rate test`.
- **Pull Requests:** Ensure all tests pass, include before-and-after metrics in the description, and never commit datasets, trained models, or secrets/passwords.
- **Before pushing:** Run `make lint` and `make test` and make sure both commands pass.
### Troubleshooting

| Command | Error Message | Cause and Solution |
|---|---|---|
| `AWS_SECRET_ACCESS_KEY=wrong uv run aws --endpoint-url "$S3_ENDPOINT_URL" s3 ls` | `SignatureDoesNotMatch` | The access key or secret key does not match the credentials configured in SeaweedFS. Make sure `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` match the credentials defined in `compose/seaweedfs/s3.json`. |
| `uv run aws --endpoint-url http://localhost:8334 s3 ls` | `Could not connect to the endpoint URL` | The S3 endpoint or port is incorrect, or the service is not available on that port. Check the configured endpoint; in this project, it is `http://localhost:8333`. |
## Dataset version comparison

| Tag | Rows | Churn rate | MD5 (first 8 chars) | ROC AUC | F1 |
|---|---:|---:|---|---:|---:|
| `data-v1` | 8,000 | 0.523625 | `e0be77bd` | 0.7493 | 0.7318 |
| `data-v2` | 5,000 | 0.3606 | `79921313` | 0.8020 | 0.6682 |
| `data-v3` | 5,000 | 0.3548 | `f61e9dc2` | 0.7825 | 0.5733 |

These metrics should not be compared as a fair benchmark because the datasets were generated with different random seeds and may have different churn distributions, which can affect both the training and test splits and consequently the evaluation results.
## Troubleshooting: intentional failures

The following failures were intentionally reproduced to verify the DVC remote configuration and document common configuration mistakes.

| What I did | Error message | What it means | Solution |
|---|---|---|---|
| Changed the DVC `endpointurl` from port `8333` to the incorrect port `8334` and ran `uv run dvc push`. | `ERROR: unexpected error - Could not connect to the endpoint URL: "http://localhost:8334/dvc/store/files/md5/06/910cf17d38a01ab3ead6e70bec63a2.dir"` | DVC cannot connect to the S3-compatible SeaweedFS service because the configured endpoint port is incorrect. | Restore the endpoint to `http://localhost:8333` (or the value of `S3_ENDPOINT_URL` in `.env`). |
| Removed the local `access_key_id` with `uv run dvc remote modify --local storage --unset access_key_id` and ran `uv run dvc pull`. | `ERROR: failed to connect to s3 (dvc/store/files/md5) - Partial credentials found in explicit, missing: aws_access_key_id` followed by `ERROR: failed to pull data from the cloud - 5 files failed to download` | DVC has a secret key configured but no AWS access key, so the S3 credentials are incomplete. | Restore the access key from the local `.env` using `uv run dvc remote modify --local storage access_key_id "$AWS_ACCESS_KEY_ID"`. |
