# Data Sources

## Stock universe

The investment universe used in this study is based on the official B3 file "Ações por Índice".

- Source: B3 - Ações por Índice
- URL: https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices/acoes-por-indice/
- Downloaded file: `data/external/AcoesIndices_2026-06-03.csv`
- B3 update date: 2026-06-03
- Access date: 2026-06-03
- Portfolio period shown by B3: May-August 2026
- Selected index: IBOV

The fixed investment universe contains all assets whose index membership includes `IBOV`, resulting in 79 assets.

## Methodological note

A fixed universe was adopted to improve reproducibility and simplify the experimental design. This choice may introduce survivorship bias, since the historical composition of the Ibovespa is not reconstructed month by month. This limitation will be explicitly reported in the final study.