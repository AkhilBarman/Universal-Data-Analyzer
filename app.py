import os

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Dataset Analyzer", layout="wide")
st.title("Dataset Analyzer")
st.write("Upload a dataset to view its summary and graphs.")


def read_file(file):
    """Read the uploaded file based on its extension."""
    extension = os.path.splitext(file.name)[1].lower()

    if extension == ".csv":
        return pd.read_csv(file)
    if extension in [".xlsx", ".xls"]:
        return pd.read_excel(file)
    if extension == ".json":
        return pd.read_json(file)
    if extension == ".parquet":
        return pd.read_parquet(file)

    return None


file = st.file_uploader(
    "Upload a file",
    type=["csv", "xlsx", "xls", "json", "parquet"],
)

if file is not None:
    try:
        data = read_file(file)

        if data is None:
            st.error("This file type is not supported.")
        elif data.empty:
            st.warning("The uploaded file is empty.")
        else:
            st.success("File uploaded successfully.")

            st.subheader("Dataset preview")
            st.dataframe(data.head(20), use_container_width=True)

            st.subheader("Dataset information")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows", len(data))
            col2.metric("Columns", len(data.columns))
            col3.metric("Missing values", int(data.isna().sum().sum()))
            col4.metric("Duplicate rows", int(data.duplicated().sum()))

            st.subheader("Statistics")
            st.dataframe(data.describe(include="all").T, use_container_width=True)

            numeric_columns = list(data.select_dtypes(include="number").columns)
            if numeric_columns:
                st.subheader("Numeric graph")
                numeric_column = st.selectbox(
                    "Choose a numeric column",
                    numeric_columns,
                )

                figure, axis = plt.subplots()
                axis.hist(data[numeric_column].dropna(), bins=20, color="steelblue")
                axis.set_title("Distribution of " + numeric_column)
                axis.set_xlabel(numeric_column)
                axis.set_ylabel("Count")
                st.pyplot(figure)
                plt.close(figure)
            else:
                st.info("No numeric columns were found.")

            text_columns = list(
                data.select_dtypes(include=["object", "string", "category", "bool"]).columns
            )
            if text_columns:
                st.subheader("Category graph")
                text_column = st.selectbox("Choose a category column", text_columns)
                counts = data[text_column].fillna("Missing").value_counts().head(15)

                figure, axis = plt.subplots()
                counts.sort_values().plot.barh(ax=axis, color="orange")
                axis.set_title("Values in " + text_column)
                axis.set_xlabel("Count")
                st.pyplot(figure)
                plt.close(figure)

            date_columns = []
            for column in data.columns:
                dates = pd.to_datetime(data[column], errors="coerce")
                if dates.notna().mean() >= 0.8:
                    date_columns.append(column)

            if date_columns and numeric_columns:
                st.subheader("Time analysis")
                date_column = st.selectbox("Choose a date column", date_columns)
                value_column = st.selectbox("Choose a value column", numeric_columns)

                dates = pd.to_datetime(data[date_column], errors="coerce")
                values = pd.to_numeric(data[value_column], errors="coerce")
                time_data = pd.DataFrame({"date": dates, "value": values}).dropna()
                time_data = time_data.sort_values("date")

                if not time_data.empty:
                    daily_values = (
                        time_data.set_index("date")["value"]
                        .resample("D")
                        .mean()
                        .dropna()
                    )

                    st.write(
                        "Showing",
                        len(daily_values),
                        "data points from",
                        daily_values.index.min().strftime("%Y-%m-%d"),
                        "to",
                        daily_values.index.max().strftime("%Y-%m-%d"),
                    )

                    figure, axis = plt.subplots(figsize=(10, 4))
                    axis.plot(
                        daily_values.index,
                        daily_values.values,
                        marker="o",
                        color="blue",
                    )
                    axis.set_title(value_column + " over time")
                    axis.set_xlabel(date_column)
                    axis.set_ylabel(value_column)
                    axis.grid(True)
                    figure.autofmt_xdate()
                    st.pyplot(figure)
                    plt.close(figure)
                else:
                    st.warning("No valid date and value data was found.")

            st.subheader("Download data")
            st.download_button(
                "Download CSV",
                data.to_csv(index=False),
                file_name="analyzed_data.csv",
                mime="text/csv",
            )
    except (ValueError, TypeError, ImportError, pd.errors.ParserError) as error:
        st.error("Could not read this file: " + str(error))
else:
    st.info("Upload a file to start.")
