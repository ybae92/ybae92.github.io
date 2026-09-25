import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import PowerTransformer

df = pd.read_csv("D:\\ybae92.github.io\\projects\\06-Final-datapreprocessing-tool\\titanic_data.csv")
image_dir = Path(
    "D:\\ybae92.github.io\\projects\\06-Final-datapreprocessing-tool\\profile_images"
)

# =========================================================
# 3. Encoding
# =========================================================

# ---------------------------------------------------------
# 3-1. Label Encoding
# ---------------------------------------------------------

def label_encoding(df, col):

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(
        df[col].astype(str)
    )

    print(f'"{col}" → Label Encoding')
    print("After Encoding -> ")
    print(df[col].head())

    return df


# ---------------------------------------------------------
# 3-2. One-Hot Encoding
# ---------------------------------------------------------

def one_hot_encoding(df, col):

    df = pd.get_dummies(
        df,
        columns=[col],
        dtype=int
    )

    print(f'"{col}" → One-Hot Encoding')
    print("After Encoding -> ")
    print(df[col].head())

    return df


# ---------------------------------------------------------
# 3-3. Ordinal Encoding
# ---------------------------------------------------------

def ordinal_encoding(df, col, categories):

    encoder = OrdinalEncoder(
        categories=[categories]
    )

    df[col] = encoder.fit_transform(
        df[[col]]
    )

    print(f'"{col}" → Ordinal Encoding')
    print("After Encoding -> ")
    print(df[col].head())

    return df


# ---------------------------------------------------------
# 3-4. Binary Encoding
# ---------------------------------------------------------

def binary_encoding(df, col):

    categories = df[col].unique()

    mapping = {
        categories[0]: 0,
        categories[1]: 1
    }

    df[col] = df[col].map(mapping)

    print(f'"{col}" → Binary Encoding')
    print("After Encoding -> ")
    print(df[col])

    return df


def handle_encoding(df, target_col):

    categorical_columns = df.select_dtypes( include=["object", "category"]).columns

    for col in categorical_columns:
        # Target → Label Encoding
        if col == target_col:
            df = label_encoding(df, col)
            print(f'"{col}" is target → Label Encoding')
            print(f'Unique of this {col} : {df[col].unique}')

        # Feature → user selection
        else:
            # print("=" * 50)
            # print(f'Encoding for "{col}"')
            # print("=" * 50)
            # print()
            # print(f'Unique of this {col} : {df[col].unique}')
            # print()

            while True:
                print("=" * 50)
                print(f'Encoding for "{col}"')
                print("=" * 50)
                print()
                print(f'Unique of this {col} : {df[col].unique}')
                print()
                print("1. One-Hot Encoding")
                print("2. Ordinal Encoding")
                print("3. Binary Encoding (only for two categories)")
                print("4. Skip Encoding")
                print("5. Remove Column")
                print()
                way = input("Select (1, 2, 3, 4 or 5) : ")
                if way == "1":
                    df = one_hot_encoding(df, col)
                    break

                elif way == "2":
                    print("Example: Low, Medium, High")

                    categories = input(
                        "Enter categories in order "
                        "(comma separated): "
                    ).split(",")

                    categories = [
                        x.strip()
                        for x in categories
                    ]

                    df = ordinal_encoding(
                        df,
                        col,
                        categories
                    )
                    break

                elif way == "3":
                    categories = df[col].unique()
                
                    if len(categories) != 2:
                        print(f'"{col}" has {len(categories)} categories.')
                        print("======= Warning =======")
                        print("Binary Encoding is only available for 2 categories.")
                        print("="*30)
                        print("!!Select another Option!!")
                        continue
                
                    df = binary_encoding(df, col)
                    break

                elif way == "4":
                    break

                elif way == "5":
                    while True:
                        print(f"WARNING: {col} column will be removed. Please be careful")
                        print(f"Do you really want to drop this {col}column?")
                        drop_way = input("1. Yes, 2. No \nSelect (1 or 2) : ")
                        if drop_way == "1":
                            print("Remove column")
                            #df = remove_column(df, col)
                            break
                        elif drop_way == "2":
                            print(f"\n{col} Column will NOT be removed.")
                            print("Please select an option again.")
                            break
                        else: 
                            print('Please input "1" or "2".')

                else:
                    print('Please input "1", "2", "3", "4" or "5".')

    return df

handle_encoding(df, "a")

# =========================================================
# 2. Outlier Detection
# =========================================================

# def get_outlier_bounds(df, col):

#     Q1 = df[col].quantile(0.25)
#     Q3 = df[col].quantile(0.75)

#     IQR = Q3 - Q1

#     lower = Q1 - 1.5 * IQR
#     upper = Q3 + 1.5 * IQR

#     return lower, upper

# # =========================================================
# # 2-1. Keep Outlier
# # =========================================================

# def keep_outlier(df, col):
#     print(f'"{col}" outliers were kept.')

#     return df


# # =========================================================
# # 2-2. Remove Outlier
# # =========================================================

# def remove_outlier(df, col):
#     lower, upper = get_outlier_bounds(df, col)
#     before = len(df)

#     df = df[(df[col] >= lower) & (df[col] <= upper)]

#     removed = before - len(df)
#     print(
#         f'"{col}" outliers were removed. '
#         f'{removed} rows deleted.'
#     )

#     return df


# # =========================================================
# # 2-3. Transform Outlier
# # =========================================================

# def transform_outlier(df, col):
#     # Check negative values
#     if (df[col] < 0).any():
#         print(f'Negative values detected in "{col}".')
#         print('Yeo-Johnson transformation will be applied.')

#         transformer = PowerTransformer(method="yeo-johnson")
#         df[col] = transformer.fit_transform(df[[col]]).ravel()

#     else:
#         print(f'No negative values in "{col}".')
#         print('Log1p transformation will be applied.')
#         df[col] = np.log1p(df[col])

#     return df


# # =========================================================
# # 2-4. Outlier Menu
# # =========================================================

# def handle_outliers(df, image_dir):

#     numerical_columns = df.select_dtypes(include="number").columns

#     print("\n==============================")
#     print("       Outlier Handling")
#     print("==============================")

#     for i, col in enumerate(numerical_columns, start=1):
#         print(f"{i}. {col}")

#     while True:
#         choice = input(
#             "\nSelect column number: "
#         )
#         if choice.isdigit():
#             choice = int(choice)
#             if 1 <= choice <= len(numerical_columns):
#                 col = numerical_columns[choice - 1]
#                 break

#         print("Please select a valid column.")

#     # Find image of selected column
#     image_path = image_dir / f"{col}.png"

#     print(f"\nSelected column: {col}")
#     print(f"Profile image: {image_path}")

#     # Outlier 확인
#     lower, upper = get_outlier_bounds(df, col)
#     outlier_count = (
#         (df[col] < lower) | (df[col] > upper)).sum()

#     print(f"\nPossible outliers: {outlier_count}")

#     print("\n[Outlier Handling]")
#     print("1. Keep")
#     print("2. Remove (IQR)")
#     print("3. Transform")

#     while True:
#         way = input("Select (1, 2 or 3): ")

#         if way == "1":
#             df = keep_outlier(df, col)
#             break

#         elif way == "2":
#             df = remove_outlier(df, col)
#             break

#         elif way == "3":
#             df = transform_outlier(df, col)
#             break

#         else:
#             print('Please input "1", "2" or "3".')
#     return df







# missing = pd.DataFrame({
#     "Column" : df.columns,
#     "Missing Count" : df.isna().sum(),
#     "Missing %" : df.isna().mean()* 100,
#     "Type" : df.dtypes
# })

# print(missing[missing["Missing Count"] > 0])

# auto_m_clean = missing[missing["Missing Count"] > 0].sort_values("Missing Count", ascending=0)
# print(auto_m_clean)
# print()

# for row in auto_m_clean.index:
#     missing_pct = auto_m_clean.loc[row,'Missing %']
#     if  missing_pct > 20:
#         print(f'"{row}" has missing value over 20%. The value is {missing_pct:.2f} \n This column will be deleted\n')
#         #auto_m_clean.drop(column=row, inplace=True)
#     else:
#         print("===============")
#         print(f'Clean the missing Value of "{row}" having {missing_pct:.2f}%')
#         print('[Select Way]')
#         print('**Notice**\nIf you select "2. Imputation(i)", The missing value will be imputed with median value.\n')

#         while True:
#             way = input('1. Delete(d), 2. Imputation(i) \n Select (1 or 2) : ')
#             if way == "1":
#                 print(way)
#                 break
#                 #auto_m_clean.dropna(subset=[row], inplace=True)
#             elif way == "2":
#                 print(way)
#                 if auto_m_clean.loc[row,'Type']  == 'object':
#                     print(f'{row} is Object Value. It will be imputed mode value')
#                 else: print(f'{row} is Numerical Value. It will be imputed median value')
#                 break
#                 #auto_m_clean.fillna(auto_m_clean[row].median())
#             else:
#                 print('Please input "1 or 2"')
        