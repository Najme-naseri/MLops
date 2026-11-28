# Release Notes

## Current Champion — churn v4

### Model, Version, and Aliases

- **Model:** `churn`
- **Version:** `4`
- **Aliases:** `@champion`, `@challenger`
- **Run:** `fc908d6b`

### Changes from the Previous Champion

The previous champion was **churn v3**.

The model parameter `C` was changed from `0.01` to `10`.

- **Model:** `LogisticRegression`
- **C:** `0.01 → 10`
- **Threshold:** `0.5 → 0.5` (unchanged)

### Metrics and Changes

| Metric | Previous Champion v3 | Current Champion v4 | Change |
|---|---:|---:|---:|
| ROC-AUC | 0.7489 | 0.7490 | +0.0001 |
| F1 | 0.7033 | 0.7365 | +0.0332 |

ROC-AUC improved slightly, while F1 improved significantly.

### Data and Code Commit

- **Data MD5:** `e0be77bd`
- **Git commit:** `ee228ae`
- **Run:** `fc908d6b`

### Gate Result

Version 4 successfully passed the evaluation gate and was promoted to `@champion`.

The following rules were checked:

- `min_roc_auc = 0.745`
- `min_f1 = 0.69`
- `max_roc_auc_drop = 0.001`
- `max_f1_drop = 0.0`

Results:

- ROC-AUC = `0.749` ≥ `0.745` → **passed**
- F1 = `0.7365` ≥ `0.69` → **passed**
- ROC-AUC did not drop by more than `0.001` compared with the previous champion → **passed**
- F1 did not drop compared with the previous champion → **passed**

### Known Limitations

The ROC-AUC improvement over the previous champion is very small (`+0.0001`). Therefore, this small change alone does not demonstrate a meaningful improvement in the model's overall ranking ability.

The evaluation is also based on the current dataset and configuration. Evaluation on independent or newly collected data would be needed to verify the model's generalization.

### Rollback

Rollback is performed by moving the `@champion` alias to a previous healthy model version. No new model version is required.

Since version 3 was the previous champion, version 3 can be restored as the champion if version 4 causes problems:

```bash
uv run python -c 'from mlflow import MlflowClient; MlflowClient().set_registered_model_alias("churn", "champion", 3)'
```

The same operation can also be performed through the MLflow UI using the edit icon next to the aliases.
