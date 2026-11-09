import pandas as pd

from make_dataset import make

EXPECTED_COLUMNS = {
    "tenure_months",
    "monthly_charges",
    "contract",
    "internet_service",
    "payment_method",
    "support_calls",
    "churn",
}


def test_dataset_schema():
    df = make(rows=200, seed=1)
    assert set(df.columns) == EXPECTED_COLUMNS
    assert len(df) == 200
    assert set(df["churn"].unique()) <= {0, 1}


def test_dataset_is_reproducible():
    pd.testing.assert_frame_equal(make(200, seed=42), make(200, seed=42))


def test_tenure_months_are_non_negative():
    df = make(rows=200, seed=1)
    assert (df["tenure_months"] >= 0).all()


def test_churn_rate_is_valid():
    df = make(rows=200, seed=1)

    churn_rate = df["churn"].mean()

    assert 0 <= churn_rate <= 1
    assert 0 in df["churn"].values
    assert 1 in df["churn"].values
