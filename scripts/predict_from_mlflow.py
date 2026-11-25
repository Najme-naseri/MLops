import argparse
import os
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd


def main():
    parser = argparse.ArgumentParser(
        description="Load a model from MLflow and predict churn probabilities."
    )
    parser.add_argument(
        "--model-id",
        required=True,
        help="MLflow logged model ID, e.g. m-xxxxxxxx",
    )
    parser.add_argument(
        "--data",
        default="data/processed/test.csv",
        help="Path to the test CSV file.",
    )
    args = parser.parse_args()

    # Connect to MLflow
    tracking_uri = os.getenv(
        "MLFLOW_TRACKING_URI",
        "http://localhost:5050",
    )
    mlflow.set_tracking_uri(tracking_uri)

    # Load the logged model
    model_uri = f"models:/{args.model_id}"
    print(f"Loading model: {model_uri}")

    model = mlflow.sklearn.load_model(model_uri)

    # Load test data
    data_path = Path(args.data)
    df = pd.read_csv(data_path)

    if "churn" not in df.columns:
        raise ValueError("The test dataset must contain a 'churn' column.")

    # Select first five rows and remove target column
    X = df.drop(columns=["churn"]).head(5)

    # Predict churn probabilities
    probabilities = model.predict_proba(X)[:, 1]

    # Display results
    results = pd.DataFrame(
        {
            "row": X.index,
            "churn_probability": probabilities,
        }
    )

    print("\nChurn probabilities:")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
