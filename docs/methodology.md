# Methodology

## Objective

Evaluate whether supervised machine learning models can select stock portfolios that outperform the Ibovespa benchmark on a risk-adjusted basis.

---

## Investment Universe

### Source

* Source: B3 – Ações por Índice
* URL: https://www.b3.com.br
* Access date: 2026-06-03
* Downloaded file: AcoesIndices_2026-06-03.csv

### Universe Definition

The investment universe consists of all assets belonging to the Ibovespa (IBOV) portfolio available on the B3 website on 2026-06-03.

The resulting universe contains:

* 79 assets

### Universe Type

A fixed universe is adopted throughout the entire study period.

### Justification

Using a fixed universe improves experiment reproducibility and simplifies portfolio comparison across different machine learning models.

### Limitation

The use of a fixed universe may introduce survivorship bias because the historical composition of the Ibovespa is not reconstructed over time.

---

## Historical Data

### Source

* Yahoo Finance
* Accessed through the yfinance Python library

### Period

* Start date: 2015-01-01
* End date: 2025-12-31

### Frequency

* Daily observations

### Download Result

* 79 assets successfully downloaded
* 193,007 observations
* No download failures

---

## Price Series

### Selected Variable

Adjusted Close (Adj Close)

### Justification

Adjusted Close incorporates corporate actions such as:

* dividends
* stock splits
* reverse splits
* bonus issues

This provides a more accurate representation of the economic return obtained by investors.

---

## Assets with Partial History

Assets with incomplete historical series are maintained in the dataset.

Examples include companies that:

* performed IPOs after 2015;
* entered the market during the study period;
* changed corporate structure during the analysis window.

### Justification

Removing these assets would reduce the representativeness of the current Ibovespa universe.

The model will use only the observations available for each asset.

No minimum-history filter will be applied.

---

## Benchmark

* Benchmark: Ibovespa (^BVSP)

---

## Prediction Horizon

* 1 month

### Justification

A monthly horizon is consistent with portfolio rebalancing strategies commonly used by institutional and individual investors.

---

## Rebalancing Frequency

* Monthly

---

## Prediction Target

The target variable is defined as:

target = future_stock_return − future_ibovespa_return

where:

* future_stock_return = asset return over the prediction horizon
* future_ibovespa_return = benchmark return over the same horizon

The target therefore represents the future excess return relative to the benchmark.

---

## Portfolio Construction

### Main Portfolio

* Top 10 assets ranked by predicted score

### Robustness Analysis

Additional portfolios will be evaluated using:

* Top 15 assets
* Top 20 assets

---

## Models

The following supervised machine learning models will be evaluated:

* Decision Tree Regressor
* Random Forest Regressor
* XGBoost Regressor

---

## Data Architecture

The project follows a simplified medallion-inspired structure:

* external: official external sources
* raw: downloaded market data
* processed: cleaned and transformed data
* curated: modeling-ready datasets

This structure improves reproducibility, traceability and maintainability.
