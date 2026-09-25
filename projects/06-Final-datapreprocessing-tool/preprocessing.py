import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import PowerTransformer

# =========================================================
# Missing Values - Streamlit
# =========================================================

def preprocess_missing_values(df, column, method):

    df_clean = df.copy()
    # 1. Delete Column
    if method == "Delete Column":
        df_clean = df_clean.drop(columns=[column])

        return (
            df_clean,
            f'"{column}" column was deleted.'
        )


    # 2. Delete Rows with Missing Value
    elif method == "Delete Missing values":

        before = len(df_clean)
        df_clean = df_clean.dropna(subset=[column])

        removed = before - len(df_clean)

        return (
            df_clean,
            f'{removed} rows were deleted because '
            f'"{column}" had missing values.'
        )


    # 3. Imputation
    elif method == "Imputation":
        if pd.api.types.is_numeric_dtype(
            df_clean[column]
        ):
            median_value = df_clean[column].median()

            df_clean[column] = df_clean[column].fillna(median_value)

            return (
                df_clean,
                f'Missing values in "{column}" '
                f'were imputed with median '
                f'({median_value:.2f}).'
            )

        else:
            mode_value = df_clean[column].mode()[0]
            df_clean[column] = df_clean[column].fillna(mode_value)

            return (
                df_clean,
                f'Missing values in "{column}" '
                f'were imputed with mode '
                f'({mode_value}).'
            )

    return df_clean, "No changes were made."

# =========================================================
# 1. Column
# =========================================================

def remove_column(df, col):

    df = df.copy()
    df.drop(columns=col, inplace=True)

    return df


# =========================================================
# 1-1. Original CLI Missing Value Function
# =========================================================

def handle_missing_values(df):

    # Make a copy of the original data
    df_clean = df.copy()
    # ==============================
    # 1. Remove Duplicates
    # ==============================

    print("== Drop duplicated data ==")
    df_clean = df_clean.drop_duplicates()

    # ==============================
    # 2. Handle Missing Values
    # ==============================

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": df.isna().sum(),
        "Missing %": df.isna().mean() * 100,
        "Type": df.dtypes
    })

    print(
        missing[
            missing["Missing Count"] > 0
        ]
    )
    auto_m_clean = (
        missing[
            missing["Missing Count"] > 0
        ]
        .sort_values("Missing Count", ascending=False)
    )

    print(auto_m_clean)
    print()

    for row in auto_m_clean.index:

        missing_pct = (auto_m_clean.loc[row, "Missing %"])

        if missing_pct > 20:
            print(
                f'"{row}" has missing value over 20%. '
                f'The value is {missing_pct:.2f} '
                f'\nThis column will be deleted\n'
            )

        else:
            print("=" * 30)
            print(
                f'Clean the missing Value of '
                f'"{row}" having {missing_pct:.2f}%'
            )

            print("[Select Way]")

            print(
                "**Notice**\n"
                "If you select "
                '"2. Imputation", '
                "the missing value will be "
                "imputed with median value.\n"
            )

            while True:
                way = input(
                    "1. Delete  "
                    "2. Imputation"
                    "\nSelect (1 or 2): "
                )

                if way == "1":
                    print(way)
                    break

                elif way == "2":
                    print(way)
                    if (
                        auto_m_clean.loc[row, "Type"] == "object"):

                        print(
                            f'{row} is Object Value. '
                            'It will be imputed '
                            'mode value'
                        )
                    else:
                        print(
                            f'{row} is Numerical Value. '
                            'It will be imputed '
                            'median value'
                        )

                    break
                else:
                    print('Please input "1 or 2"')
    return df

# =========================================================
# 2. Outlier Detection
# =========================================================

def get_outlier_bounds(df, col):

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    return lower, upper

# =========================================================
# 2-1. Keep Outlier
# =========================================================

def keep_outlier(df, col):

    print(f'"{col}" outliers were kept.')

    return df.copy()

# =========================================================
# 2-2. Remove Outlier
# =========================================================

def remove_outlier(df, col):

    df = df.copy()

    lower, upper = get_outlier_bounds(df, col)

    before = len(df)

    df = df[(df[col] >= lower) & (df[col] <= upper)]

    removed = before - len(df)

    print(
        f'"{col}" outliers were removed. '
        f'{removed} rows deleted.'
    )

    return df, removed


# =========================================================
# 2-3. Transform Outlier
# =========================================================

def transform_outlier(df, col):

    df = df.copy()

    # Check negative values
    if (df[col] < 0).any():

        print(f'Negative values detected in "{col}".')

        print(
            "Yeo-Johnson transformation "
            "will be applied."
        )
        transformer = PowerTransformer(method="yeo-johnson")
        df[col] = (transformer.fit_transform(df[[col]]).ravel())

        method = "Yeo-Johnson"

    else:
        print(f'No negative values in "{col}".')

        print(
            "Log1p transformation "
            "will be applied."
        )
        df[col] = np.log1p(df[col])
        method = "Log1p"

    return df, method


# =========================================================
# 2-4. Original CLI Outlier Function
# =========================================================

def handle_outliers(df, image_dir):

    numerical_columns = (
        df.select_dtypes(include="number").columns)

    print("\n==============================")
    print("       Outlier Handling")
    print("==============================")

    for i, col in enumerate(numerical_columns, start=1):
        print(f"{i}. {col}")

    while True:
        choice = input("\nSelect column number: ")
        if choice.isdigit():
            choice = int(choice)
            if (1 <= choice <= len(numerical_columns)):
                col = numerical_columns[choice - 1]
                break

        print("Please select a valid column.")

    image_path = (image_dir / f"{col}.png")

    print(f"\nSelected column: {col}")
    print(f"Profile image: {image_path}")

    lower, upper = get_outlier_bounds(df, col)

    outlier_count = ((df[col] < lower) | (df[col] > upper)).sum()

    print(
        f"\nPossible outliers: "
        f"{outlier_count}"
    )

    print("\n[Outlier Handling]")

    print("1. Keep")
    print("2. Remove (IQR)")
    print("3. Transform")
    print("4. Remove Column")

    while True:
        way = input("Select (1, 2, 3 or 4): ")

        if way == "1":
            df = keep_outlier(df, col)
            break

        elif way == "2":

            df, removed = remove_outlier(df, col)
            break

        elif way == "3":
            df, method = transform_outlier(df, col)
            break

        elif way == "4":
            while True:
                print(f"WARNING: {col} column will be removed.")

                drop_way = input(
                    "1. Yes, 2. No, "
                    "Select 1 or 2: "
                )

                if drop_way == "1":
                    df = remove_column(df, col)
                    break

                elif drop_way == "2":
                    print(
                        "\nColumn will NOT "
                        "be removed."
                    )

                    break

                else:
                    print('Please input "1" or "2".')
            break

        else:
            print(
                'Please input '
                '"1", "2", "3" or "4".'
            )

    return df

# =========================================================
# 3. Encoding
# =========================================================

# ---------------------------------------------------------
# 3-1. Label Encoding
# ---------------------------------------------------------

def label_encoding(df, col):

    df = df.copy()

    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col].astype(str))

    print( f'"{col}" → Label Encoding')
    print("After Encoding -> ")
    print(df[col].head())

    return df


# ---------------------------------------------------------
# 3-2. One-Hot Encoding
# ---------------------------------------------------------

def one_hot_encoding(df, col):

    df = df.copy()
    df = pd.get_dummies(
        df,
        columns=[col],
        dtype=int
    )
    print(f'"{col}" → One-Hot Encoding')

    return df


# ---------------------------------------------------------
# 3-3. Ordinal Encoding
# ---------------------------------------------------------

def ordinal_encoding(df, col, categories):

    df = df.copy()

    encoder = OrdinalEncoder(categories=[categories])

    df[col] = encoder.fit_transform(df[[col]])

    print(f'"{col}" → Ordinal Encoding')
    print( "After Encoding -> ")
    print(df[col].head())

    return df

# ---------------------------------------------------------
# 3-4. Binary Encoding
# ---------------------------------------------------------

def binary_encoding(df, col):

    df = df.copy()

    categories = (df[col].dropna().unique())

    if len(categories) != 2:

        raise ValueError(
            "Binary Encoding is only "
            "available for 2 categories."
        )

    mapping = {
        categories[0]: 0,
        categories[1]: 1
    }

    df[col] = df[col].map(mapping)

    print(f'"{col}" → Binary Encoding')
    print("After Encoding -> ")
    print(df[col])

    return df


# =========================================================
# 3-5. Original CLI Encoding Function
# =========================================================

def handle_encoding(df, target_col):

    categorical_columns = (
        df.select_dtypes(include=["object", "category"]).columns
    )

    for col in categorical_columns:
        # Target → Label Encoding
        if col == target_col:

            df = label_encoding(df, col)

            print(
                f'"{col}" is target '
                '→ Label Encoding'
            )

        # Feature → user selection

        else:
            while True:
                print("=" * 50)
                print(f'Encoding for "{col}"')
                print("=" * 50)

                print(
                    f'Unique of this {col}: '
                    f'{df[col].unique()}'
                )

                print()
                print("1. One-Hot Encoding")
                print("2. Ordinal Encoding")
                print("3. Binary Encoding (only for two categories)")
                print("4. Skip Encoding")
                print("5. Remove Column")
                print()

                way = input("Select (1, 2, 3, 4 or 5): ")

                if way == "1":
                    df = one_hot_encoding(df, col)
                    break

                elif way == "2":
                    print(
                        "Example: "
                        "Low, Medium, High"
                    )
                    categories = input(
                        "Enter categories in order "
                        "(comma separated): "
                    ).split(",")

                    categories = [x.strip() for x in categories]

                    df = ordinal_encoding(df, col, categories)
                    break

                elif way == "3":
                    categories = (df[col].unique())
                    if len(categories) != 2:

                        print(
                            f'"{col}" has '
                            f'{len(categories)} categories.'
                        )

                        print(
                            "Binary Encoding "
                            "is only available "
                            "for 2 categories."
                        )
                        continue

                    df = binary_encoding(df, col)
                    break

                elif way == "4":
                    break

                elif way == "5":
                    confirm = input(
                        f'Do you really want '
                        f'to remove "{col}"? '
                        '(y/n): '
                    )

                    if confirm.lower() == "y":
                        df = remove_column(df, col)
                        break
                    else:
                        print("Column was not removed.")

                else:
                    print('Please input "1", "2", "3", "4" or "5".')
    return df
