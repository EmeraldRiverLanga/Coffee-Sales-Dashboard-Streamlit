# Coffee Sales Dashboard — Streamlit

## Overview

An interactive Streamlit dashboard for analyzing coffee sales data. The
app loads transactional sales records from a CSV file, lets the user filter
them by date range and product category, and presents the results through
three visualizations, a simple next-month revenue forecast, and an
AI-generated business summary.

The project demonstrates a complete small data-analysis tool: data loading
and cleaning, interactive filtering, visualization, a basic forecast, and an
optional AI integration — built iteratively with the Cline AI assistant.

## Technologies Used

- **Python** — core language
- **Streamlit** — interactive web dashboard framework
- **Pandas** — data loading, cleaning, and aggregation
- **Plotly Express** — interactive charts (line, bar, pie)
- **NumPy** — numeric arrays for the forecast model
- **scikit-learn** — LinearRegression for revenue forecasting
- **Requests** — HTTP calls to the OpenRouter API
- **OpenRouter API** — LLM backend for the AI summary
- **VS Code + Cline** — AI-assisted development environment

## Setup

### Requirements

- Python 3.11 or newer
- An OpenRouter API key (free key available at openrouter.ai) — only needed
  for the optional AI summary feature

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add your API key

The AI summary feature reads its key from Streamlit secrets. Create a file at
`.streamlit/secrets.toml` and add your key:

```toml
OPENROUTER_API_KEY = "your-openrouter-api-key-here"
```

The `secrets.toml` file is listed in `.gitignore`, so the key never reaches
the repository. The dashboard works fully without a key — only the AI summary
button requires it.

### Run the app

```bash
streamlit run app.py
```

The dashboard opens automatically in your browser at `http://localhost:8501`.

## Project Structure
Coffee-Sales-Dashboard-Streamlit/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── cline_log.md            # Log of AI (Cline) prompts and iterations
├── data/
│   └── index_1.csv         # Coffee sales dataset
└── utils/
├── init.py         # Makes utils an importable package
└── data_loader.py      # Data loading and column preparation

## Features

### Interactive Filters
- **Date range filter** — select a start and end date
- **Category filter** — select one or more product categories
- All charts, metrics, and the forecast update automatically based on the filters

### Visualizations
| Chart | Description |
|---|---|
| Line chart | Monthly revenue over time |
| Bar chart | Top 10 products by revenue |
| Pie chart | Revenue share by category |

### Revenue Forecast
A simple next-month revenue estimate using scikit-learn LinearRegression on
the monthly revenue trend. The forecast is shown together with an R-squared
score so the user can judge how well the linear trend fits the data, and a
warning is displayed when there is too little data for a reliable estimate.

### AI Data Summary
A "Generate AI Summary" button computes key statistics from the filtered data,
sends them to the OpenRouter API, and displays a plain-English business
summary. The call is wrapped in error handling so the app stays stable if the
API is unavailable.

## Key Design Decisions

### 1. The AI rephrases numbers, it does not calculate them

The app computes all statistics (total revenue, top product, best month) in
Python first, then sends those finished numbers to the model and asks only for
a plain-English summary. The model never does the arithmetic. This guarantees
the numbers in the summary are exact — the AI only puts them into words. If the
model were asked to calculate from raw data, it could make mistakes that are
hard to detect.

### 2. Column renaming happens in code, not in the CSV

The dataset uses lowercase column names (`date`, `money`, `coffee_name`). Rather
than editing the source CSV, the `load_data()` function renames them to the
schema the rest of the app expects (`Date`, `Amount`, `Product`). The source
data stays untouched, the transformation is visible in code, and the same file
can be reloaded at any time with identical results.

### 3. The API key is never in the source code

The OpenRouter key is read from `st.secrets`, not hard-coded. The
`.streamlit/secrets.toml` file is listed in `.gitignore` from the start, so the
key never reaches the repository.

## Dataset

| Column | Description |
|---|---|
| date | Transaction date |
| money | Transaction amount |
| coffee_name | Product sold |

The loader renames these to `Date`, `Amount`, and `Product`, and adds a
`Category` column (a copy of the product name) used for filtering and the pie
chart.

## AI-Assisted Development

This project was built using AI-assisted "vibe coding" with the Cline assistant
in VS Code. Each feature was generated, tested, and refined through follow-up
prompts. The full prompt history and the iterations behind each fix are
documented in `cline_log.md`.

## Challenges & Solutions

| Problem | Solution |
|---|---|
| First dataset had artificially duplicated data (one year copied three times) | Verified data quality by inspecting transactions per month, then switched to a clean coffee sales dataset |
| Dates were in day/month/year format and caused a parse error | Added `dayfirst=True` to `pd.to_datetime()` |
| Amount column was stored as text with "$" and "," characters | Cleaned and converted to numeric inside `load_data()`, leaving the source CSV untouched |
| AI summary returned a 404 error (the named free model was retired) | Switched to the `openrouter/free` auto-routing model |
| Cline placed the AI section above where `filtered_data` is created | Moved the section to the end of the file so it runs after filtering |

## Scope and Limitations

This is an educational and portfolio project. It works and is honest about what
it does not do:

- **The forecast is a simple linear trend.** LinearRegression fits a straight
  line and does not account for seasonality or short-term fluctuation. It gives
  a rough estimate, not a reliable business projection — which is why the
  R-squared score is shown alongside it.
- **"Category" equals "Product".** This dataset has no separate category column,
  so the coffee name serves as both product and category. A richer dataset would
  have a true product hierarchy.
- **The forecast rests on limited data** (13 months). More history would make
  the trend more meaningful.
- **The AI summary depends on a free model**, which can be slow or temporarily
  unavailable. The feature is optional and fails gracefully; the rest of the
  dashboard does not depend on it.

## Possible Improvements

- Use a forecasting method that accounts for seasonality (e.g. moving average or seasonal decomposition)
- Add a keyword search box to filter the data table
- Add a dark/light theme toggle
- Add more product-level metrics and breakdowns

## Dataset

The dataset ("Coffee Sales") contains coffee sales transactions from a
vending machine, sourced from
[Kaggle](https://www.kaggle.com/datasets/ihelon/coffee-sales) by the author
`ihelon`.
