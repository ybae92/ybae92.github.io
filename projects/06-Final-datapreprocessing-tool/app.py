import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

from profiling import (
    profile_data,
    generate_profile_report
)

from preprocessing import (
    preprocess_missing_values,
    remove_column,
    get_outlier_bounds,
    keep_outlier,
    remove_outlier,
    transform_outlier,
    label_encoding,
    one_hot_encoding,
    ordinal_encoding,
    binary_encoding
)

# =========================================================
# Settings
# =========================================================

BASE_DIR = Path(__file__).parent

REPORT_PATH = (BASE_DIR / "profiling_report.html")

st.set_page_config(
    page_title="Automated Data Preprocessing Tool",
    layout="wide"
)

# =========================================================
# Session State
# =========================================================

if "df" not in st.session_state:
    st.session_state.df = None

if "processed_df" not in st.session_state:
    st.session_state.processed_df = None

if "profile_result" not in st.session_state:
    st.session_state.profile_result = None

if "report_generated" not in st.session_state:
    st.session_state.report_generated = False

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "encoding_result" not in st.session_state:
    st.session_state.encoding_result = None

# =========================================================
# Title
# =========================================================

st.title("Automated Data Preprocessing Tool")

st.write(
    "Upload a CSV file and automatically "
    "analyze and preprocess your data."
)

st.divider()

# =========================================================
# 1. Upload CSV
# =========================================================

st.header("1. Upload CSV")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    if (uploaded_file.name != st.session_state.uploaded_file_name):
        df = pd.read_csv(uploaded_file)

        st.session_state.df = df
        st.session_state.processed_df = None
        st.session_state.encoding_result = None
        st.session_state.profile_result = None
        st.session_state.report_generated = False
        st.session_state.uploaded_file_name = (uploaded_file.name)

    else:
        df = st.session_state.df

    st.success(
        f"{uploaded_file.name} "
        "uploaded successfully!"
    )

# =========================================================
# Uploaded Data
# =========================================================

if st.session_state.df is not None:
    df = st.session_state.df

    with st.expander(
        "📋 View Uploaded Data",
        expanded=False
    ):
        
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        st.dataframe(df.head(20), use_container_width=True)

# =========================================================
# 2. Data Profiling
# =========================================================

if st.session_state.df is not None:
    st.header(
        "2. Data Profiling"
    )
    if st.button("Run Profiling", type="primary"):

        with st.spinner("Analyzing your data..."):

            profile_result = profile_data(st.session_state.df)

        st.session_state.profile_result = (profile_result)

        st.session_state.report_generated = False
        st.success("Data profiling completed!")

# =========================================================
# Profiling Results
# =========================================================

if st.session_state.profile_result is not None:
    profile_result = (st.session_state.profile_result)

    # =====================================================
    # Missing
    # =====================================================

    with st.expander(
        "🔍 Missing Values",
        expanded=False
    ):

        missing = profile_result["missing"]

        if missing.empty:
            st.success("No missing values found.")

        else:
            st.dataframe(missing, use_container_width=True)

    # =====================================================
    # Duplicates
    # =====================================================

    with st.expander(
        "🔁 Duplicated Rows",
        expanded=False
    ):

        duplicate_count = (profile_result["duplicate_count"])

        if duplicate_count == 0:
            st.success("No duplicated rows found.")

        else:
            st.warning(
                f"{duplicate_count} "
                "duplicated rows found."
            )

    # =====================================================
    # Variables
    # =====================================================

    with st.expander(
        "🔢 Numerical Variables",
        expanded=False
    ):
        st.write(
            f"Numerical variables: "
            f"{len(profile_result['numerical_columns'])}"
        )
        st.write(profile_result["numerical_columns"])
        

    with st.expander(
        "🔤 Categorical Variables",
        expanded=False
    ):
        st.write(
            f"Categorical variables: "
            f"{len(profile_result['categorical_columns'])}"
        )
        st.write(profile_result["categorical_columns"])

    # =====================================================
    # 3. Visualization
    # =====================================================
    st.header("3. Visualization")

    figures = profile_result["figures"]

    with st.expander(
        "📈 View Distribution & Outliers",
        expanded=False
    ):

        if figures:
            for col, fig in figures.items():
                st.subheader(col)

                st.pyplot(fig, clear_figure=False)

        else:
            st.write(
                "No numerical variables "
                "to visualize."
            )

    # =====================================================
    # 4. Profiling Report
    # =====================================================

    st.header("4. Profiling Report")

    with st.expander(
        "📄 Generate Profiling Report",
        expanded=True
    ):

        if not st.session_state.report_generated:
            if st.button(
                "Generate Profiling Report",
                type="primary"
            ):

                progress_bar = st.progress(0, text="Preparing report...")
                progress_bar.progress(30, text="Analyzing dataset...")

                with st.spinner("Generating profiling report..."):

                    generate_profile_report(
                        st.session_state.df,
                        REPORT_PATH
                    )

                progress_bar.progress(100, text="Report generation completed!")

                st.session_state.report_generated = True
                st.success("Profiling report generated!")
                st.rerun()

        if (
            st.session_state.report_generated
            and REPORT_PATH.exists()
        ):

            st.success("Your profiling report is ready.")

            with open(
                REPORT_PATH,
                "rb"
            ) as file:

                st.download_button(
                    "⬇️ Download Profiling Report",
                    data=file,
                    file_name="profiling_report.html",
                    mime="text/html"
                )

# =========================================================
# 5. Data Preprocessing
# =========================================================

if st.session_state.profile_result is not None:
    st.header(
        "5. Data Preprocessing"
    )

    with st.expander(
        "🛠️ Preprocessing Options",
        expanded=True
    ):
        # =================================================
        # Current Dataset
        # =================================================

        if (
            st.session_state.processed_df
            is not None
        ):
            df = (st.session_state.processed_df)

        else:
            df = st.session_state.df

        # =====================================================
        # 5-0 Remove Unnecessary Columns
        # =====================================================

        st.subheader("1️⃣ Remove Unnecessary Columns")

        st.write(
            "Select columns that are not needed for data analysis "
            "or machine learning."
        )

        columns_to_remove = st.multiselect(
            "Select columns to remove",
            options=df.columns.tolist(),
            key="columns_to_remove"
        )

        # if columns_to_remove:
        #     st.write("**Selected columns:**")
        #     st.write(columns_to_remove)

        if st.button(
            "Remove Selected Columns",
            type="primary",
            key="remove_columns"
        ):

            if not columns_to_remove:
                st.warning("Please select at least one column.")

            else:
                processed_df = remove_column(df, columns_to_remove)

                st.session_state.processed_df = processed_df
                st.success(
                    f"Removed {len(columns_to_remove)} column(s) successfully."
                )

        # =================================================
        # 5-1. Missing Values
        # =================================================

        st.subheader("2️⃣ Missing Values")

        missing_columns = df.columns[df.isna().any()].tolist()

        if not missing_columns:
            st.success("No missing values found.")

        else:
            selected_column = st.selectbox(
                "Select column",
                missing_columns,
                key="missing_column"
            )

            missing_count = (df[selected_column].isna().sum())
            missing_percentage = (df[selected_column].isna().mean()* 100)

            st.info(
                f"**{selected_column}**: "
                f"{missing_count} missing values "
                f"({missing_percentage:.2f}%)"
            )

            # ---------------------------------------------
            # > 20%
            # ---------------------------------------------

            if missing_percentage > 20:

                st.warning(
                    f'"{selected_column}" has '
                    "more than 20% missing values."
                )

                st.write(
                    "According to your preprocessing "
                    "rule, this column can be deleted."
                )

                if st.button(
                    "Delete Column",
                    type="primary",
                    key="delete_column"
                ):
                    processed_df, message = (
                        preprocess_missing_values(df, selected_column, "Delete Column")
                    )

                    st.session_state.processed_df = (processed_df)
                    st.success(message)

                    st.rerun()


            # ---------------------------------------------
            # <= 20%
            # ---------------------------------------------

            else:
                method = st.radio(
                    "Select method",
                    [
                        "Delete Missing Rows",
                        "Imputation"
                    ],
                    key="missing_method"
                )

                if method == "Imputation":

                    if pd.api.types.is_numeric_dtype(df[selected_column]):

                        st.info(
                            "Numerical column → "
                            "Median Imputation"
                        )
                    else:
                        st.info(
                            "Categorical column → "
                            "Mode Imputation"
                        )

                if st.button(
                    "Apply Missing Value Treatment",
                    type="primary",
                    key="apply_missing"
                ):

                    processed_df, message = (
                        preprocess_missing_values(df, selected_column, method)
                    )

                    st.session_state.processed_df = (processed_df)
                    st.success(message)
                    st.rerun()
        st.divider()

        # =================================================
        # 5-2. Outlier
        # =================================================

        st.subheader("3️⃣ Outlier Handling")

        numerical_columns = (
            df.select_dtypes(include="number").columns.tolist()
        )

        if not numerical_columns:

            st.info(
                "No numerical columns "
                "available."
            )

        else:
            outlier_column = st.selectbox(
                "Select numerical column",
                numerical_columns,
                key="outlier_column"
            )

            lower, upper = get_outlier_bounds(df, outlier_column)

            outlier_mask = ((df[outlier_column] < lower) | (df[outlier_column] > upper))

            outlier_count = outlier_mask.sum()

            st.info(f"Possible outliers: **{outlier_count}**")
            # ---------------------------------------------
            # Graph
            # ---------------------------------------------

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4, 2))

            sns.histplot(data=df, x=outlier_column, ax=ax1)
            ax1.set_title(f"{outlier_column} Histogram", fontsize=6)
            ax1.set_xlabel(outlier_column, fontsize=6)
            ax1.set_ylabel("Count", fontsize=6)
            ax1.tick_params(axis="both", labelsize=6)

            sns.boxplot(data=df, x=outlier_column, ax=ax2)
            ax2.set_title(f"{outlier_column} Boxplot", fontsize=6)
            ax2.set_xlabel(outlier_column, fontsize=6)
            ax2.tick_params(axis="both", labelsize=6)

            plt.tight_layout()

            st.pyplot(fig, clear_figure=True)

            outlier_method = st.radio(
                "Select outlier treatment",
                [
                    "Remove outliers",
                    "Transform",
                    "Remove Column"
                ],
                key="outlier_method"
            )

            if st.button(
                "Apply Outlier Treatment",
                type="primary",
                key="apply_outlier"
            ):

                if outlier_method == "Remove outliers":
                    (processed_df, removed) = remove_outlier(df, outlier_column)

                    message = (
                        f"{removed} outlier rows "
                        f"were removed."
                    )

                elif outlier_method == "Transform":
                    (processed_df, transform_method) = transform_outlier(df, outlier_column)

                    message = (
                        f'"{outlier_column}" '
                        f"was transformed using "
                        f"{transform_method}."
                    )

                else:
                    processed_df = (remove_column(df, outlier_column))
                    message = (f'"{outlier_column} column was removed.')

                st.session_state.processed_df = (processed_df)
                st.success(message)

                st.rerun()
        st.divider()

        # =================================================
        # 5-3. Encoding
        # =================================================

        
        st.subheader("4️⃣ Encoding")

        categorical_columns = (
            df.select_dtypes(include=["object", "category"]).columns.tolist()
            )

        if not categorical_columns:

            st.info("No categorical columns available for encoding.")

            # Show the last encoding result
            if st.session_state.encoding_result is not None:

                result = st.session_state.encoding_result

                st.divider()
                st.subheader("Last Encoding Result")

                st.write(f"**Column:** `{result['column']}`")
                st.write(f"**Method:** `{result['method']}`")

                before_df = result["before"]
                after_df = result["after"]
                column = result["column"]

                # One-Hot Encoding
                if result["method"] == "One-Hot Encoding":

                    new_columns = [
                        col
                        for col in after_df.columns
                        if col not in before_df.columns
                    ]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Before Encoding**")
                        st.dataframe(
                            before_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )
                        st.caption(
                            f"dtype: {before_df[column].dtype}"
                        )

                    with col2:
                        st.write("**After Encoding**")

                        if new_columns:
                            st.dataframe(
                                after_df[new_columns].head(20),
                                use_container_width=True,
                                hide_index=True
                            )

                            st.caption(
                                "dtype: " +
                                ", ".join(
                                    f"{col} → {after_df[col].dtype}"
                                    for col in new_columns
                                )
                            )

                # Label / Ordinal / Binary
                elif result["method"] in [
                    "Label Encoding",
                    "Ordinal Encoding",
                    "Binary Encoding"
                ]:

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Before Encoding**")
                        st.dataframe(
                            before_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )
                        st.caption(
                            f"dtype: {before_df[column].dtype}"
                        )

                    with col2:
                        st.write("**After Encoding**")
                        st.dataframe(
                            after_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )
                        st.caption(
                            f"dtype: {after_df[column].dtype}"
                        )

                # Skip
                elif result["method"] == "Skip":

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Before Encoding**")
                        st.dataframe(
                            before_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )

                    with col2:
                        st.write("**After Encoding**")
                        st.dataframe(
                            after_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )
                        st.info("No changes were made.")

                # Remove Column
                elif result["method"] == "Remove Column":

                    st.info(
                        f"`{column}` was removed from the dataset."
                    )

        else:
            target_column = st.selectbox(
                "Select Target Variable",
                ["None"] + categorical_columns,
                key="target_column"
            )

            encoding_column = st.selectbox(
                "Select categorical column",
                categorical_columns,
                key="encoding_column"
            )
           
            # ---------------------------------------------
            # Unique Values
            # ---------------------------------------------

            unique_values = df[encoding_column].dropna().unique()

            st.write(
                f"**Unique values in `{encoding_column}`:** "
                f"{len(unique_values)}"
            )

            unique_df = pd.DataFrame({
                encoding_column: unique_values
            })

            st.dataframe(
                unique_df,
                use_container_width=True,
                hide_index=True
            )

            # ---------------------------------------------
            # Target → Label
            # ---------------------------------------------

            if (
                target_column != "None"
                and encoding_column == target_column
            ):
                st.info(
                    f'"{encoding_column}" is the '
                    "target variable. "
                    "Label Encoding will be applied."
                )
                encoding_method = ("Label Encoding")

            else:
                encoding_method = st.selectbox(
                    "Select encoding method",
                    [
                        "One-Hot Encoding",
                        "Ordinal Encoding",
                        "Binary Encoding",
                        "Skip",
                        "Remove Column"
                    ],
                    key="encoding_method"
                )

            # ---------------------------------------------
            # Ordinal
            # ---------------------------------------------

            categories = None

            if (encoding_method == "Ordinal Encoding"):
                st.caption("Example: Low, Medium, High")

                category_input = st.text_input(
                    "Enter categories in order",
                    key="ordinal_categories"
                )

                if category_input:
                    categories = [
                        x.strip()
                        for x in category_input.split(",")
                    ]

            # ---------------------------------------------
            # Binary
            # ---------------------------------------------

            if (encoding_method == "Binary Encoding"):
                unique_categories = (df[encoding_column].dropna().unique())

                if len(unique_categories) != 2:
                    st.warning(
                        "Binary Encoding requires "
                        "exactly 2 categories."
                    )

            # ---------------------------------------------
            # Apply Encoding
            # ---------------------------------------------

            if st.button(
                "Apply Encoding",
                type="primary",
                key="apply_encoding"
            ):
                actual_method = encoding_method
                # Target
                if (
                    target_column != "None" and encoding_column == target_column
                ):

                    processed_df = (label_encoding(df, encoding_column))
                    actual_method = "Label Encoding"
                    message = (f'"{encoding_column}" → Label Encoding')

                elif (encoding_method == "One-Hot Encoding"):
                    processed_df = (one_hot_encoding(df, encoding_column))
                    message = (f'"{encoding_column} → One-Hot Encoding')

                elif (encoding_method == "Ordinal Encoding"):

                    if not categories:
                        st.error(
                            "Please enter "
                            "the categories."
                        )
                        st.stop()

                    unique_values = set(
                        df[encoding_column].dropna().astype(str)
                    )

                    entered_values = set(categories)


                    if (unique_values != entered_values):

                        st.error(
                            "Entered categories "
                            "do not match the "
                            "column values."
                        )

                        st.stop()

                    processed_df = (
                        ordinal_encoding(df, encoding_column, categories)
                    )

                    message = (
                        f'"{encoding_column}" → Ordinal Encoding'
                    )

                elif (encoding_method == "Binary Encoding"):

                    unique_categories = (
                        df[encoding_column].dropna().unique()
                    )

                    if len(unique_categories) != 2:

                        st.error(
                            "Binary Encoding "
                            "requires exactly "
                            "2 categories."
                        )

                        st.stop()

                    processed_df = (binary_encoding(df, encoding_column))
                    message = (
                        f'"{encoding_column}" '
                        "→ Binary Encoding"
                    )

                elif (encoding_method == "Skip"):

                    processed_df = df.copy()
                    message = (
                        f'"{encoding_column}" '
                        "was skipped."
                    )

                else:
                    processed_df = (remove_column(df, encoding_column))

                    message = (
                        f'"{encoding_column}" '
                        "column was removed."
                    )

                # Save encoding information
                st.session_state.encoding_result = {
                    "column": encoding_column,
                    "method": actual_method,
                    "before": df,
                    "after": processed_df
                }

                st.session_state.processed_df = processed_df
                st.success(message)
                st.rerun()

            # =================================================
            # Encoding Result
            # =================================================
            

            if st.session_state.encoding_result is not None:

                result = st.session_state.encoding_result

                st.divider()

                st.subheader("🔤 Encoding Result")

                st.write(
                    f"**Column:** `{result['column']}`"
                )

                st.write(
                    f"**Method:** `{result['method']}`"
                )

                before_df = result["before"]
                after_df = result["after"]
                column = result["column"]

                # =================================================
                # Before / After
                # =================================================

                if result["method"] == "One-Hot Encoding":

                    # Find newly created columns
                    new_columns = [
                        col
                        for col in after_df.columns
                        if col not in before_df.columns
                    ]

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write("**Before Encoding**")

                        st.dataframe(
                            before_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )

                        st.caption(
                            f"dtype: {before_df[column].dtype}"
                        )

                    with col2:

                        st.write("**After Encoding**")

                        st.dataframe(
                            after_df[new_columns].head(20),
                            use_container_width=True,
                            hide_index=True
                        )

                        if new_columns:
                            st.caption(
                                "dtype: "
                                + ", ".join(
                                    f"{col} → {after_df[col].dtype}"
                                    for col in new_columns
                                )
                            )

                elif result["method"] in [
                    "Label Encoding",
                    "Ordinal Encoding",
                    "Binary Encoding"
                ]:

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write("**Before Encoding**")

                        st.dataframe(
                            before_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )

                        st.caption(
                            f"dtype: {before_df[column].dtype}"
                        )

                    with col2:

                        st.write("**After Encoding**")

                        st.dataframe(
                            after_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )

                        st.caption(
                            f"dtype: {after_df[column].dtype}"
                        )

                elif result["method"] == "Skip":

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write("**Before Encoding**")

                        st.dataframe(
                            before_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )

                    with col2:

                        st.write("**After Encoding**")

                        st.dataframe(
                            after_df[[column]].head(20),
                            use_container_width=True,
                            hide_index=True
                        )

                        st.info("No changes were made.")

                elif result["method"] == "Remove Column":

                    st.info(
                        f"`{column}` was removed from the dataset."
                    )

        # =================================================
        # Current Processed Dataset
        # =================================================

        # =========================================================
        # 6. Final Results
        # =========================================================

        if st.session_state.processed_df is not None:

            final_df = st.session_state.processed_df
            remaining_categorical = (
                final_df
                .select_dtypes(include=["object", "category"])
                .columns
                .tolist()
            )

            if not remaining_categorical:
                st.divider()
                st.header("6. Final Results")

                # =====================================================
                # Final Dataset
                # =====================================================

                st.subheader("📊 Final Processed Dataset")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Rows",
                        final_df.shape[0]
                    )

                with col2:
                    st.metric(
                        "Columns",
                        final_df.shape[1]
                    )

                st.dataframe(
                    final_df.head(20),
                    use_container_width=True
                )

                # =====================================================
                # Download Processed CSV
                # =====================================================

                st.subheader("📥 Download Processed Data")

                csv_data = (
                    final_df
                    .to_csv(index=False)
                    .encode("utf-8")
                )

                st.download_button(
                    label="⬇️ Download Processed CSV",
                    data=csv_data,
                    file_name="processed_data.csv",
                    mime="text/csv",
                    key="download_processed_csv"
                )

                st.divider()

                # =====================================================
                # Final Profiling Report
                # =====================================================

                st.subheader("📄 Final Profiling Report")

                st.write(
                    "Generate a new profiling report based on "
                    "the processed dataset."
                )

                FINAL_REPORT_PATH = (
                    BASE_DIR / "final_profiling_report.html"
                )
                if st.button(
                    "Generate Final Profiling Report",
                    type="primary",
                    key="generate_final_report"
                ):
                    with st.spinner("Generating final profiling report..."):

                        generate_profile_report(
                            final_df,
                            FINAL_REPORT_PATH
                        )

                    st.success("Final profiling report generated!")

                    with open(FINAL_REPORT_PATH, "rb") as file:
                        st.download_button(
                            "Download Final Profiling Report",
                            file,
                            file_name="final_profiling_report.html",
                            mime="text/html",
                            key="download_final_report"
                        )
              
                # =====================================================
                # Download Final Report
                # =====================================================
            
            