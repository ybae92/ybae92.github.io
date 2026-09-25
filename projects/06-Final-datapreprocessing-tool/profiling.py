from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport
import webbrowser


def generate_profile_report(df, output_path):
    df = df.copy()
    profile = ProfileReport(
        df,
        title="Data Profiling Report",
        vars={
            "num": {"low_categorical_threshold": 0}
        }
    )

    profile.to_file(output_path)

    return output_path

def profile_data(df):
    # BASE_DIR = Path(__file__).parent
    # print(BASE_DIR)

    # # Import CSV File
    # df = pd.read_csv(BASE_DIR / 'titanic_data.csv')
    # profile = ProfileReport(df, title="Before preprocessing")
    # profile.to_file(image_dir / "profiling_report.html")

    # Information
    print("== Data Shape ==")
    print(df.shape)
    print("\n== Data Information ==")
    df.info()
    print("\n== Missing Values ==")
    print(df.isna().mean()*100)

    #######ADD!!###
    print("\n== Delete Seires variable ==\n")
    print("Select from web form")
    print(df.head(10))

    print("\n== Select Target Variable ==\n")
    print('If there is no target variable on the dataset, Please select "None"')
    #####ADD!!###

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": df.isna().sum(),
        "Missing %": df.isna().mean() * 100
    })

    missing = missing[missing["Missing Count"] > 0]

    print(missing)

    print("\n== Duplicated Values ==")
    print(df.duplicated().sum())

    # Outliers
    print("\n== Outliers ==")

    df_num = df.select_dtypes(include="number")
    df_obj = df.select_dtypes(exclude="number")

    num_cols = df_num.columns
    obj_cols = df_obj.columns

    print("\n==== Numerical variables ===")
    print(num_cols, "\n", len(num_cols))
    print("\n==== Categorical variables ===")
    print(obj_cols, "\n", len(obj_cols))

    figures = {}

    for col in df_num.columns:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4, 2))
        ax1.set_title(f"{col} Histogram", fontsize=6)
        ax1.set_xlabel(col, fontsize=6)
        ax1.set_ylabel("Count", fontsize=6)
        ax1.tick_params(axis="both", labelsize=6)
        sns.histplot(x=col, data=df, ax=ax1)
        ax2.set_title(f"{col} Boxplot", fontsize=6)
        ax2.set_xlabel(col, fontsize=6)
        ax2.tick_params(axis="both", labelsize=6)
        sns.boxplot(x=col, data=df, ax=ax2)
        plt.tight_layout()
        figures[col] = fig

    return {
        "missing": missing,
        "duplicate_count": df.duplicated().sum(),
        "numerical_columns": list(df_num.columns),
        "categorical_columns": list(df_obj.columns),
        "figures": figures
    }
    

        
