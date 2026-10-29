# Universal Data Analyzer

An interactive Streamlit app for exploring almost any tabular dataset.

## ✨ What it does

- Upload **CSV, Excel, JSON, or Parquet** files
- Preview the data and inspect rows, columns, missing values, and duplicates
- View descriptive statistics
- Explore numeric distributions and categorical frequencies
- Detect date columns and plot daily time trends
- Download the uploaded data as CSV

## 🚀 Run locally

```bash
git clone https://github.com/AkhilBarman/Universal-Data-Analyzer.git
cd Universal-Data-Analyzer
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit, upload a dataset, and use the selectors to interact with the charts.

<details>
<summary>Supported file formats</summary>

| Format | Extension |
|---|---|
| Comma-separated values | `.csv` |
| Excel workbook | `.xlsx`, `.xls` |
| JSON records | `.json` |
| Apache Parquet | `.parquet` |

</details>

> **Privacy:** Uploaded files are processed by the running app. Sample CSV data is intentionally not included in this repository.
