# Air Quality Index (AQI) Prediction

This repository contains code for predicting the Air Quality Index (AQI) using various machine learning and time series forecasting techniques. The AQI is an index used to communicate how polluted the air is and what associated health effects might be a concern for the general population. The prediction models utilize data collected from air quality monitoring stations, including parameters such as PM2.5, PM10, NO2, SO2, CO, O3, and others.

## Table of Contents
1. [Introduction](#introduction)
2. [Data](#data)
3. [Methods](#methods)
4. [Results](#results)
5. [Contributing](#contributing)
6. [License](#license)

## Introduction
The quality of the air we breathe is a critical factor in public health, and accurate prediction of the AQI can help individuals and authorities take preventive measures to mitigate the health risks associated with air pollution. This project aims to develop models capable of forecasting the AQI based on historical air quality data.

## Data
The dataset used in this project contains the following columns:
- StationId: ID or code assigned to the air quality monitoring station.
- Date: Date and possibly time when the data was recorded.
- PM2.5, PM10: Particulate Matter concentrations with diameters of 2.5 and 10 micrometers or smaller.
- NO, NO2, NOx: Nitric Oxide, Nitrogen Dioxide, and Nitrogen Oxides concentrations.
- NH3: Ammonia concentration.
- CO: Carbon Monoxide concentration.
- SO2: Sulfur Dioxide concentration.
- O3: Ozone concentration.
- Benzene, Toluene, Xylene: Concentrations of benzene, toluene, and xylene.
- AQI: Air Quality Index, a numerical scale indicating the level of air pollution.
- AQI_Bucket: Qualitative description of the air quality based on the AQI value.

## Methods
The project employs several techniques for AQI prediction, including:
- ARIMA (AutoRegressive Integrated Moving Average)
- SARIMAX (Seasonal AutoRegressive Integrated Moving Average with eXogenous factors)
- LSTM (Long Short-Term Memory) neural networks

## Results
The performance of each prediction model is evaluated using metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R-squared (R2) score. The results are visualized to assess the accuracy of the predictions.

## Contributing
Contributions to this project are welcome! To contribute, please follow these steps:
1. Fork the repository to your GitHub account.
2. Clone the forked repository to your local machine.
3. Create a new branch for your feature or bug fix.
4. Make your changes and commit them to your branch.
5. Push your changes to your forked repository.
6. Create a pull request from your branch to the main repository's master branch.
7. Provide a clear description of your changes in the pull request.
8. Wait for feedback and incorporate any requested changes.
