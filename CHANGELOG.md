# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
