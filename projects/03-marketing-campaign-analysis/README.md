# 📈 Marketing Campaign Analysis

## 📌 Project Overview
This project analyzes marketing-related data by building a data pipeline using PostgreSQL and PL/pgSQL.  
A structured VIEW was created in the database layer, and the processed data was imported into Python using psycopg2 for visualization and analysis.
- Presentation: https://canva.link/2apkpvj3c1kso7m

---

## 🎯 Problem Statement
What factors influence customer behavior and marketing performance?

---

## 📊 Dataset
- Source: Kaggle / public marketing dataset
- Size: 10,000 rows, 11 features
- Features: Channel, Impressions, Clicks, Cost_USD, Revenue_USD, ROI etc.

---

## 🧹 Data Processing (SQL Layer)
- Data preprocessing performed in PostgreSQL using SQL and PL/pgSQL
- Created a reusable VIEW to structure and clean raw marketing data
- Applied filtering and transformation logic at the database level
- Queried the final VIEW from Python using psycopg2

---

## 📊 Analysis & Visualization (Python Layer)
- Imported processed data from PostgreSQL into Python
- Conducted exploratory data analysis (EDA)
- Built visualizations to identify customer patterns and marketing insights

---

## 🔍 Key Insights
- Certain customer segments show significantly higher engagement rates
- Marketing campaign effectiveness varies across demographics
- Spending behavior is strongly correlated with campaign response

---

## 🛠 Tech Stack
- PostgreSQL (PL/pgSQL)
- Python
- psycopg2
- Pandas
- Ydata_Profiling
- Matplotlib
- Seaborn

---

## 👤 My Role
- Designed and implemented SQL queries and PL/pgSQL views
- Built data pipeline between PostgreSQL and Python using psycopg2
- Performed EDA and visualization
- Extracted key marketing insights from the dataset
