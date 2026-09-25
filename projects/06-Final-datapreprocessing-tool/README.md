# Automated Data Preprocessing Tool

An automated data preprocessing tool built with Python and Streamlit.
This tool helps users prepare datasets for machine learning by automatically identifying and handling common data preprocessing issues.

## Project Overview

Data preprocessing is an important step before applying machine learning models.
This tool allows users to upload a CSV dataset and perform several preprocessing tasks through a simple web interface.

### Main Workflow

**Upload CSV → Data Profiling → Preprocessing → Final Dataset → Final Profiling Report**

## Features

### 1. Data Profiling

The tool analyzes the uploaded dataset and provides information about:

* Dataset shape
* Data types
* Missing values
* Duplicated values
* Numerical variables
* Categorical variables
* Histograms
* Boxplots

A profiling report can also be generated and downloaded.

### 2. Remove Unnecessary Columns

Users can select unnecessary columns that are not required for data analysis or machine learning.

Selected columns will be automatically deleted from the dataset.

### 3. Missing Value Handling

The tool handles missing values based on predefined rules.

**Option 1**

* Remove missing values

**Option 2**

* If the variable is numerical, impute missing values with the median.
* If the variable is categorical, impute missing values with the mode.

### 4. Duplicated Value Handling

The tool identifies duplicated rows and allows users to remove duplicated values from the dataset.

### 5. Outlier Handling

The tool identifies possible outliers in numerical variables using the IQR method.

Users can review the distribution using:

* Histogram
* Boxplot

Available preprocessing options include:

* Keep
* Remove
* Transform using log1p
* Remove the column

### 6. Categorical Variable Encoding

The tool provides different encoding methods depending on the characteristics of the variable.

#### Label Encoding

If the target variable is categorical, use Label Encoding.

#### One-Hot Encoding

One-Hot Encoding can be used for categorical variables without a meaningful order.

#### Binary Encoding

If the variable has two categories, use Binary Encoding.

#### Ordinal Encoding

If the variable has an inherent order, use Ordinal Encoding.

#### Skip

Keep the categorical variable without applying encoding.

#### Remove Column

Remove the selected categorical variable from the dataset.

The tool also displays the encoding result so users can check how the categorical variable was transformed.

## Technology Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Streamlit
* YData Profiling

## Project Structure

```text
06-Final-datapreprocessing-tool/
│
├── app.py
├── preprocessing.py
├── profiling.py
├── README.md
└── ...
```

## How to Run

Install the required Python packages:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit ydata-profiling
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in a web browser.

## Input

The tool accepts:

```text
CSV file (.csv)
```

## Output

The tool provides:

* Processed dataset as a CSV file
* Initial data profiling report
* Final data profiling report
* Encoding results
* Outlier visualizations

## Project Goal

The goal of this project is to simplify common data preprocessing tasks for beginners and reduce repetitive preprocessing work before machine learning.

## Future Improvements

Possible future improvements include:

* More advanced outlier detection methods
* Additional encoding methods
* More customizable preprocessing rules
* Improved profiling reports
* Support for additional file formats
* Machine learning model integration

## Author

Yuna Bae
