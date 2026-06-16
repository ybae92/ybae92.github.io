# 🌍 World Happiness Analysis

## 📌 Project Overview
This project analyzes the World Happiness dataset using correlation analysis and hypothesis testing.  
In particular, an A/B testing framework was used to compare different data collection approaches and evaluate which method produces more reliable data compared to real-world observations.

- Presentation: https://canva.link/64nwg76o8taqt1b

---

## 🎯 Problem Statement
- What factors are most strongly associated with happiness scores?
- How do different data collection methods affect data quality?
- Which approach (manual vs ML-based) produces results closer to real-world data?

---

## 📊 Dataset
- Source: World Happiness Report (Kaggle / public dataset)
- Features: GDP per capita, social support, life expectancy, freedom, generosity, corruption perception, happiness score, etc.
- Type: Cross-country socio-economic dataset

---

## 🔗 Correlation Analysis
- Analyzed relationships between happiness score and key socio-economic factors
- Identified strong positive and negative correlations
- Visualized relationships using correlation matrix and heatmaps

---

## 🧪 A/B Testing (Data Collection Comparison)

### Objective
To evaluate which data collection approach produces more reliable and realistic results:

- **Group A:** Manual data collection approach  
- **Group B:** Machine Learning-based data collection approach  

### Method
- Defined null hypothesis: no difference in data accuracy between methods
- Compared both approaches against real-world reference data
- Measured deviation (error gap) from actual observed data

### Evaluation
- Calculated difference between predicted/collected values and real data
- Assessed which method minimizes deviation

---

## 🔍 Key Insights
- Socio-economic factors such as GDP and social support are strongly correlated with happiness
- Data collection method impacts accuracy and consistency of results
- One method showed lower deviation from real-world data, indicating higher reliability
- Not all differences between methods were statistically significant

---

## 📈 Statistical Approach
- Correlation analysis
- Hypothesis testing (A/B testing framework)
- Error/deviation comparison against real data
- Null hypothesis significance testing (NHST)

---

## 🛠 Tech Stack
- Python
- Pandas
- NumPy
- Ydata_profiling
- SciPy / Statsmodels
- Matplotlib
- Seaborn

---

## 👤 My Role
- Data cleaning and preprocessing (handling missing values, feature engineering)
- Exploratory data analysis (EDA)
- Designed A/B testing framework for data collection comparison
- Defined hypothesis and evaluation metrics
- Measured deviation from real-world data
- Performed statistical analysis and interpretation
- Built visualizations for insights
