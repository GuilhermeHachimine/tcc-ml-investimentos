# Experiments Log

## Experiment 001 - Data acquisition and validation

### Date

2026-06-03

### Description

Initial data acquisition and validation.

### Decisions

- Fixed IBOV universe selected.
- 79 assets identified from B3 official source.
- Historical period defined from 2015-01-01 to 2025-12-31.
- Adjusted Close selected as the primary price series.
- Assets with partial history retained.
- Monthly prediction horizon selected.
- Monthly rebalancing selected.

### Results

- 193,007 stock observations downloaded.
- No stock download failures.
- Ibovespa benchmark successfully downloaded.

### Status

Completed.

---

## Experiment 002 - Simple temporal split model comparison

### Date

2026-06-03

### Description

Three supervised regression models were trained using a simple temporal split.

- Training period: 2015-01-01 to 2020-12-31
- Test period: 2021-01-01 to 2025-12-31
- Target: one-month future excess return over Ibovespa
- Main portfolio: Top 10 assets
- Rebalancing: monthly, using the last available trading day of each month

### Models

- Decision Tree Regressor
- Random Forest Regressor
- XGBoost Regressor

### Main Results - Top 10 Portfolio

| Model | Portfolio total return | Portfolio Sharpe | Hit rate |
|---|---:|---:|---:|
| Decision Tree | 113.53% | 0.6885 | 61.02% |
| Random Forest | 150.79% | 0.7513 | 50.85% |
| XGBoost | 65.88% | 0.4907 | 50.85% |

### Benchmark

| Benchmark | Total return |
|---|---:|
| Ibovespa | 43.02% |

### Status

Completed.

---

## Experiment 003 - Portfolio size sensitivity analysis

### Date

2026-06-03

### Description

Sensitivity analysis was performed by varying the number of selected assets.

Portfolio sizes tested:

- Top 10
- Top 15
- Top 20

### Results

| Model | Top N | Portfolio total return | Portfolio Sharpe | Hit rate |
|---|---:|---:|---:|---:|
| Decision Tree | 10 | 113.53% | 0.6885 | 61.02% |
| Decision Tree | 15 | 70.18% | 0.5434 | 50.85% |
| Decision Tree | 20 | 75.30% | 0.5840 | 54.24% |
| Random Forest | 10 | 150.79% | 0.7513 | 50.85% |
| Random Forest | 15 | 89.36% | 0.6001 | 50.85% |
| Random Forest | 20 | 57.41% | 0.4735 | 50.85% |
| XGBoost | 10 | 65.88% | 0.4907 | 50.85% |
| XGBoost | 15 | 56.01% | 0.4638 | 50.85% |
| XGBoost | 20 | 31.16% | 0.3387 | 47.46% |

### Preliminary Interpretation

The Top 10 portfolios presented stronger performance than the Top 15 and Top 20 portfolios, especially for Random Forest. This suggests that model concentration may be relevant for portfolio construction, since adding lower-ranked assets diluted performance.

### Status

Completed.

---

## Experiment 004 - Feature importance analysis

### Date

2026-06-03

### Description

Feature importance was calculated for Random Forest and XGBoost using the training period.

### Main Findings

Both models assigned greater importance to medium-term momentum and volatility variables.

### Random Forest - Top features

| Feature | Importance |
|---|---:|
| return_63d | 26.85% |
| volatility_63d | 23.22% |
| volatility_21d | 18.63% |
| distance_to_ma_63d | 11.25% |
| return_21d | 10.57% |

### XGBoost - Top features

| Feature | Importance |
|---|---:|
| return_63d | 17.85% |
| distance_to_ma_63d | 13.65% |
| volatility_21d | 13.32% |
| volatility_63d | 13.10% |
| return_21d | 11.96% |

### Preliminary Interpretation

The results indicate that medium-term return, volatility and distance from moving averages were more relevant than one-day return. This is consistent with the idea that medium-term price behavior may contain more useful information for ranking assets than very short-term movements.

### Status

Completed.