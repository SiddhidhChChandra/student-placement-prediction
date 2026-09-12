# 🏠 House Price Prediction

An end-to-end Machine Learning regression project for predicting house prices from property characteristics.

## Project Workflow

- Data understanding and cleaning
- Exploratory Data Analysis (EDA)
- Univariate, bivariate and multivariate analysis
- Train/test split
- One-Hot Encoding
- Standardization
- ColumnTransformer and Pipeline
- Linear Regression baseline
- Ridge Regression with GridSearchCV
- Lasso Regression with GridSearchCV
- 5-Fold Cross Validation
- Ablation study using the `area` feature
- Feature engineering
- Final model comparison

## Dataset

`Housing.csv` contains 545 observations and 13 columns. The target variable is `price`.

## Models

1. Linear Regression
2. Ridge Regression
3. Lasso Regression
4. Feature-engineered Linear Regression

## How to Run

Open `House-Price-Prediction.ipynb` in Google Colab or Jupyter and keep `Housing.csv` in the same folder as the notebook.

## Libraries

See `requirements.txt`.