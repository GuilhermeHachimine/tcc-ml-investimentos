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

## Experiment 003 - Simple split portfolio size sensitivity analysis

### Date

2026-06-03

### Portfolio sizes tested

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

The Top 10 portfolios presented stronger performance than the Top 15 and Top 20 portfolios, especially for Random Forest. This suggests that concentration may be relevant for portfolio construction, since adding lower-ranked assets diluted performance.

### Status

Completed.

---

## Experiment 004 - Feature importance analysis

### Date

2026-06-03

### Description

Feature importance was calculated for Random Forest and XGBoost using the training period.

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

---

## Experiment 005 - Walk-forward validation

### Date

2026-06-04

### Description

The models were evaluated using expanding-window walk-forward validation.

For each test year:

- the model was trained using all previous years;
- predictions were generated only for the test year;
- predictions were concatenated across the full test period.

### Main Results - Top 10 Portfolio

| Model | Portfolio total return | Portfolio Sharpe | Hit rate |
|---|---:|---:|---:|
| Decision Tree | 40.90% | 0.4022 | 50.85% |
| Random Forest | 94.50% | 0.5972 | 54.24% |
| XGBoost | 95.37% | 0.6152 | 50.85% |

### Benchmark

| Benchmark | Total return |
|---|---:|
| Ibovespa | 43.02% |

### Preliminary Interpretation

Walk-forward validation reduced the extreme performance observed in the simple split, especially for Decision Tree and Random Forest. However, Random Forest and XGBoost still outperformed the benchmark in cumulative return. XGBoost improved substantially under walk-forward validation, suggesting that this model benefits from periodic retraining.

### Status

Completed.

---

## Experiment 006 - Walk-forward portfolio size sensitivity analysis

### Date

2026-06-04

### Portfolio sizes tested

- Top 10
- Top 15
- Top 20

### Results

| Model | Top N | Portfolio total return | Portfolio Sharpe | Hit rate |
|---|---:|---:|---:|---:|
| Decision Tree | 10 | 40.90% | 0.4022 | 50.85% |
| Decision Tree | 15 | 58.52% | 0.5214 | 50.85% |
| Decision Tree | 20 | 68.93% | 0.5890 | 49.15% |
| Random Forest | 10 | 94.50% | 0.5972 | 54.24% |
| Random Forest | 15 | 61.66% | 0.4884 | 50.85% |
| Random Forest | 20 | 46.51% | 0.4259 | 49.15% |
| XGBoost | 10 | 95.37% | 0.6152 | 50.85% |
| XGBoost | 15 | 75.32% | 0.5702 | 49.15% |
| XGBoost | 20 | 58.11% | 0.4980 | 54.24% |

### Preliminary Interpretation

Under walk-forward validation, Random Forest and XGBoost maintained stronger performance with Top 10 portfolios, while Decision Tree benefited from greater diversification. This suggests that the more robust ensemble models were better able to rank the highest-scoring assets, whereas the simpler tree model produced rankings that benefited from diversification.

### Status

Completed.