# RSEF Supplemental Material

Supplemental files for the RSEF building-energy forecasting manuscript.

The CSV files contain aggregate values reported in the manuscript. They are transcribed summaries, not reconstructed run-level observations. No raw UCI or BDG2 observations, per-window predictions, or trained checkpoints are included.

## Contents

| File | Contents |
|---|---|
| `Table_S1_component_ablations.csv` | Three-seed component-ablation MAE and RMSE summaries |
| `Table_S2_dropout_spectrum.csv` | Indoor and outdoor channel-dropout MAE summaries across dropout rates |
| `Table_S3_interval_calibration.csv` | Uncalibrated and calibrated interval coverage, width, and score |
| `Table_S4_semisynthetic_response.csv` | Reported synthetic response-operator diagnostic |
| `Fig_S1_dropout_spectrum.svg` | Mean MAE and sample SD across stochastic dropout rates; generated from Table S2 |
| `Fig_S2_interval_coverage.svg` | Mean empirical coverage and sample SD before and after calibration; generated from Table S3 |
| `generate_figures.py` | Script used to render Figures S1 and S2 from the CSV files |

## Reproducibility

The associated code, frozen experiment configurations, and split metadata are available in the [RSEF code repository](https://github.com/Hajimi-Sudo/rsef-building-energy-forecasting). Raw datasets remain available from the UCI Machine Learning Repository and the Building Data Genome Project 2 release under their original terms. The manuscript reports the BDG2 analysis as feature-adapted external validation, not zero-shot transfer.
