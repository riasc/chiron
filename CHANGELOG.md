# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [0.11.0] - 2024-08-13

## Features

- Added counts of Structural Variants (SVs) - for certain genes (e.g., APOB) - as features to the model
- Removed features that showed no effect in the model (SHAP)
- Also print the SHAP values for the features to file

# [0.10.0] - 2024-08-08

## Features

- Changed the model of HLA typing (combined alleles into one and added the genotype as a feature)

# [0.9.0] - 2024-08-07

## Features

- Added methylation data as features to the model
- Added parameters for search space optimization

# [0.8.1] - 2024-08-06

## Fix

- Added environment.yml file to the repository (to ensure easy installation of the required packages using conda/mamba)

# [0.8.0] - 2024-08-05

## Features

- Added Ancestry, Telomeric Content as features to the model

# [0.7.0] - 2024-08-02

## Features
- Added the Polygenic Score as a feature to the model

# [0.6.0] - 2024-07-26

## Features

- Changed to native XGBoost implementation

# [0.5.0] - 2024-07-24

## Features

- merged family history of diseases from the survey data (e.g., Y/N)
- added family history of cancer as a feature (e.g., Y/N)

# [0.4.0] - 2024-07-23

- Changed model optimization to use the optuna package

# [0.3.0] - 2024-07-23

- Changed hypertuning to Bayesian Optimization

# [0.2.0] - 2024-07-22

## Features
- Implemented Gradient Boost approach (XGBoost) that is currently (only) based on the survey (Health and Exposure)
- Exluded fields that have missing data (>20%) and probably not interesting for the prediction

# [0.1.2] - 2024-07-13

## Fix

- Changed Dockerfile to python-based image (which allows to install packages using pip seamlessly)

# [0.1.1] - 2024-07-13

## Fix

- Changed the input format such that it now accepts the full data path instead of individual files

# [0.1.0] - 2024-07-13

## Features

- Initial release (that only randomly assign probabilities) for testing the submission
