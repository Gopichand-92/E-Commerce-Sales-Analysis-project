# E-Commerce Sales Analysis

## Project Overview

This project focuses on analyzing e-commerce sales data using Python, Pandas, NumPy, and MySQL.

The objective is to extract meaningful business insights from sales data by calculating key performance indicators (KPIs), identifying top-performing products and states, analyzing revenue trends, and understanding customer retention patterns.

The project uses a MySQL database as its data source and Python for data processing, analysis, and visualization.

## Technologies Used

- **Python 3.13** – Programming language
- **MySQL** – Database management system
- **Pandas** – Data loading, cleaning, manipulation, and analysis
- **NumPy** – Vectorized numerical calculations
- **Matplotlib** – Data visualization
- **Seaborn** – Statistical visualization and cohort retention heatmap
- **Visual Studio Code** – Development environment

## Project Features

### 1. Core KPI Analysis
- Gross Merchandise Value (GMV)
- Net Revenue
- Total Delivered Orders
- Average Order Value (AOV)

### 2. Vectorized Sales Calculations
- Calculate gross sales using quantity and unit price.
- Calculate discounts using NumPy.
- Calculate net sales after discounts.
- Include shipping fees in net revenue calculations.

### 3. Top Performers Analysis
- Identify the Top 10 products by net revenue.
- Identify the Top 5 states by net revenue.

### 4. Revenue Trend Analysis
- Analyze daily revenue trends.
- Calculate a 7-day moving average.
- Calculate cumulative Year-to-Date (YTD) revenue.

### 5. Customer Cohort Retention Analysis
- Identify customer acquisition cohorts based on first purchase month.
- Calculate monthly returning customers.
- Generate a customer retention percentage matrix.

### 6. Data Visualization
- Top 10 Products bar chart.
- Top 5 States bar chart.
- Daily Revenue Trend line chart.
- Customer Cohort Retention heatmap.


## Database Structure

The project uses a MySQL database named `ecommerce` containing six tables:

| Table Name | Description |
|---|---|
| customers | Stores customer information |
| categories | Stores product categories |
| products | Stores product details and prices |
| orders | Stores customer order information |
| order_items | Stores individual products in each order |
| payments | Stores payment details and statuses |

These tables provide the data required for sales analysis, revenue calculations, product performance analysis, regional analysis, and customer retention analysis.

## Analysis Methodology

1. Connected Python to the MySQL `ecommerce` database.
2. Loaded the required tables into Pandas DataFrames.
3. Filtered delivered orders for completed sales analysis.
4. Used NumPy vectorized operations to calculate discounts and net sales.
5. Used Pandas aggregation methods such as `groupby()`, `sum()`, and `mean()` to calculate KPIs.
6. Used `nlargest()` to identify top-performing products and states.
7. Used `rolling()` to calculate the 7-day moving average.
8. Used `cumsum()` to calculate cumulative yearly revenue.
9. Used `pivot_table()` and NumPy division to calculate customer cohort retention.
10. Exported analysis results as CSV files and generated visualizations using Matplotlib and Seaborn.


## Key Business Insights

### Overall Sales Performance

| KPI | Result |
|---|---:|
| Gross Merchandise Value (GMV) | ₹1,49,54,447.00 |
| Net Revenue | ₹1,40,98,784.35 |
| Total Delivered Orders | 1,529 |
| Average Order Value (AOV) | ₹9,220.92 |

### Top Performing Products

- Cookware Set generated the highest net revenue.
- Smartwatch ranked second.
- Coffee Maker ranked third.

### Top Performing States

- Andhra Pradesh ranked first in net sales.
- Maharashtra ranked second.
- Delhi ranked third.

### Customer Retention

- Analyzed 300 unique purchasing customers.
- Generated monthly customer cohort retention counts and percentages.
- Identified repeat purchasing patterns across different cohorts.


## Installation and Execution

### Prerequisites

- Python 3.13
- MySQL Server
- Visual Studio Code

### Install Required Libraries

Run the following command in the terminal:

```bash
pip install pandas numpy matplotlib seaborn mysql-connector-python
```

### Database Configuration

1. Start your MySQL Server.
2. Create the `ecommerce` database.
3. Create and populate the required database tables.
4. Configure the MySQL connection details in the Python scripts.
5. Use a secure method to enter your MySQL password.

### Run the Project

First, test the database connection:

```bash
python test_connection.py
```

Run the KPI and sales analysis:

```bash
python tasks/kpi_analysis.py
```

Generate the visualizations:

```bash
python tasks/visualizations.py
```

### Output

- KPI summaries and analysis results are saved as CSV files in the `output` folder.
- Generated charts are saved as PNG images in `output/charts`.