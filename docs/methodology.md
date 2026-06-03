# Methodology

## Objective

Evaluate whether supervised machine learning models can select stock portfolios that outperform the Ibovespa benchmark on a risk-adjusted basis.

---

## Investment Universe

- Source: B3 - Ações por Índice
- Access date: 2026-06-03
- Selected index: IBOV
- Universe size: 79 assets
- Universe type: Fixed

### Limitation

A fixed universe was adopted to improve reproducibility. This choice may introduce survivorship bias because the historical composition of the Ibovespa is not reconstructed through time.

---

## Benchmark

- Benchmark: Ibovespa (^BVSP)

---

## Prediction Target

The target variable is defined as:

future_stock_return - future_ibovespa_return

where:

- future_stock_return = asset return over the prediction horizon
- future_ibovespa_return = benchmark return over the same period

The target represents the future excess return relative to the benchmark.

---

## Prediction Horizon

- Horizon: 1 month

---

## Rebalancing

- Frequency: Monthly

---

## Portfolio Construction

### Main Portfolio

- Top 10 assets ranked by predicted score

### Robustness Analysis

- Top 15 assets
- Top 20 assets

---

## Models

- Decision Tree Regressor
- Random Forest Regressor
- XGBoost Regressor

---

## Data Source

- Yahoo Finance
- Daily frequency

---

## Price Series

Adjusted Close (Adj Close)

### Justification

Adjusted Close incorporates corporate actions such as dividends, stock splits and reverse splits, providing a more accurate representation of the economic return obtained by investors.