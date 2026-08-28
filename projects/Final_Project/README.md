📱 Mobile Price Classification — Research Paper Reproduction

📌 Project Overview

This project reproduces the machine learning experiments presented in the research paper “Mobile Price Classification” using the publicly available Mobile Price Classification dataset.

The study focuses on predicting mobile phone price ranges based on hardware and technical specifications. The original experimental approach was reproduced and extended by comparing different machine learning models and hyperparameter optimization methods.

Research Paper: https://www.mdpi.com/2079-9292/14/11/2173

Dataset: Mobile Price Classification Dataset

🎯 Problem Statement

* Can mobile phone price ranges be accurately classified based on technical specifications?
* How well does the baseline SVM model perform?
* Can hyperparameter optimization improve model performance?
* How does SVM compare with Logistic Regression?
* How do Hyperopt and Optuna affect model performance?
* How closely can the reproduced results match the original research paper?

📊 Dataset

Source: Kaggle — Mobile Price Classification Dataset

Size: 2,000 observations, 21 columns

Target Variable: price_range

The target variable represents four mobile phone price categories:

* 0 — Low price
* 1 — Medium-low price
* 2 — Medium-high price
* 3 — High price

Main Features:

* Battery power
* Bluetooth
* Clock speed
* Dual SIM
* Front camera
* Internal memory
* Mobile depth
* Mobile weight
* Number of cores
* Primary camera
* Pixel height
* Pixel width
* RAM
* Screen height
* Screen width
* Talk time
* 3G / 4G
* Touch screen
* Wi-Fi

🔄 Research Reproduction Workflow

1. Data Preparation

* Loaded the Mobile Price Classification dataset
* Inspected dataset structure and feature types
* Checked for missing values and potential data quality issues

2. Data Preprocessing

* Checked missing values
* Reviewed feature distributions
* Converted RAM from KB to MB
* Applied feature scaling using StandardScaler

3. Data Splitting / Cross-Validation

A 5-fold Stratified Cross-Validation approach was used:

StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

Stratification was used to maintain a similar distribution of the four price categories across folds.

4. Model Training

The following models were implemented:

* Baseline SVM
* SVM + Hyperopt
* SVM + Optuna
* Baseline Logistic Regression
* Logistic Regression + Hyperopt
* Logistic Regression + Optuna

5. Hyperparameter Optimization

Two optimization frameworks were used to investigate whether optimized hyperparameters could improve model performance.

Hyperopt

Used to search for optimal model parameters based on validation performance.

Optuna

Used for automated hyperparameter optimization with a defined search space.

6. Model Evaluation

Models were evaluated using:

* Accuracy
* Precision
* Recall
* F1-score

Macro-averaged metrics were used to evaluate performance across the four price categories.

7. Performance Comparison

The performance of all six approaches was compared:

Model	Optimization
SVM	Baseline
SVM	Hyperopt
SVM	Optuna
Logistic Regression	Baseline
Logistic Regression	Hyperopt
Logistic Regression	Optuna

The comparison focuses on whether hyperparameter optimization provides measurable improvements over baseline models.

📈 Experimental Approach

The reproduction follows the general methodology described in the research paper:

Dataset → Preprocessing → Cross-Validation → Model Training → Hyperparameter Optimization → Evaluation → Performance Comparison

The reproduced experiments were then compared with the methodology and reported results from the original paper.

🔍 Key Insights

* Mobile phone price ranges can be effectively classified using hardware and technical specifications.
* SVM provides a strong baseline for the multi-class classification problem.
* Logistic Regression was implemented as an additional baseline model for comparison.
* Hyperparameter optimization allows the models to explore parameter combinations beyond their default configurations.
* Hyperopt and Optuna provide different optimization approaches and can produce different model configurations.
* Cross-validation provides a more robust estimate of model performance than relying on a single train/test split.
* The final comparison helps identify which model and optimization strategy provides the best classification performance.

📊 Models Compared

SVM

Support Vector Machine was selected as the primary classification model and reproduced as a baseline before optimization.

SVM + Hyperopt

Hyperopt was used to optimize SVM hyperparameters such as:

* C
* gamma
* kernel
* decision_function_shape

SVM + Optuna

Optuna was used to perform automated hyperparameter optimization over a predefined search space.

Logistic Regression
Logistic Regression was added as an additional classification model to provide a comparison with SVM.

Logistic Regression + Hyperopt
Hyperopt was used to search for suitable Logistic Regression hyperparameters.

Logistic Regression + Optuna
Optuna was used to optimize Logistic Regression parameters and compare the resulting performance with the baseline and Hyperopt models.

📉 Evaluation Metrics

The following metrics were used:

* Accuracy — Overall classification performance
* Precision — Proportion of positive predictions that were correct
* Recall — Proportion of actual positives correctly identified
* F1-score — Harmonic mean of precision and recall

Because this is a four-class classification problem, macro averaging was used to give equal importance to each price category.

🛠 Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Hyperopt
* Optuna
* Matplotlib
* Seaborn
* Jupyter Notebook

👤 My Role

* Reproduced the methodology from the research paper
* Performed data cleaning and preprocessing
* Conducted exploratory data analysis (EDA)
* Implemented 5-fold Stratified Cross-Validation
* Implemented baseline SVM
* Implemented SVM with Hyperopt
* Implemented SVM with Optuna
* Implemented baseline Logistic Regression
* Implemented Logistic Regression with Hyperopt
* Implemented Logistic Regression with Optuna
* Defined and evaluated model performance metrics
* Compared model performance across different optimization approaches
* Created visualizations for model and data analysis
* Analyzed differences between the reproduced experiments and the original research paper

📚 Reference

Research Paper:
Mobile Price Classification, Electronics, MDPI

https://www.mdpi.com/2079-9292/14/11/2173

Dataset:
Mobile Price Classification — Kaggle
