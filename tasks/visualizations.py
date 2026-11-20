
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the top 10 products data
top_products = pd.read_csv("output/top_10_products.csv")

# Sort products by revenue for a horizontal bar chart
top_products = top_products.sort_values(
    by="net_sales",
    ascending=True
)

# Create the chart
plt.figure(figsize=(10, 6))

plt.barh(
    top_products["product_name"],
    top_products["net_sales"]
)

# Add chart title and labels
plt.title("Top 10 Products by Net Revenue")
plt.xlabel("Net Revenue (₹)")
plt.ylabel("Product")

# Adjust layout
plt.tight_layout()

# Save the chart
plt.savefig(
    "output/charts/top_10_products.png",
    dpi=300
)


# Display the chart
plt.show()



# Read the top 5 states data
top_states = pd.read_csv("output/top_5_states.csv")

# Sort states by revenue
top_states = top_states.sort_values(
    by="net_sales",
    ascending=True
)

# Create the chart
plt.figure(figsize=(10, 6))

plt.barh(
    top_states["state"],
    top_states["net_sales"]
)

# Add title and labels
plt.title("Top 5 States by Net Revenue")
plt.xlabel("Net Revenue (₹)")
plt.ylabel("State")

# Adjust layout
plt.tight_layout()

# Save the chart
plt.savefig(
    "output/charts/top_5_states.png",
    dpi=300
)

# Display the chart
plt.show()



# Read daily revenue trends
daily_revenue = pd.read_csv("output/daily_revenue_trends.csv")

# Convert order_date into datetime format
daily_revenue["order_date"] = pd.to_datetime(
    daily_revenue["order_date"]
)

# Create the line chart
plt.figure(figsize=(12, 6))

plt.plot(
    daily_revenue["order_date"],
    daily_revenue["total_revenue"],
    label="Daily Revenue"
)

plt.plot(
    daily_revenue["order_date"],
    daily_revenue["7_day_moving_average"],
    label="7-Day Moving Average"
)

# Add title and labels
plt.title("Daily Revenue Trend")
plt.xlabel("Order Date")
plt.ylabel("Revenue (₹)")

plt.legend()
plt.xticks(rotation=45)

# Adjust layout
plt.tight_layout()

# Save the chart
plt.savefig(
    "output/charts/daily_revenue_trend.png",
    dpi=300
)

# Display the chart
plt.show()


# Read customer cohort retention percentages
retention_matrix = pd.read_csv(
    "output/cohort_retention_percentages.csv",
    index_col=0
)

# Convert cohort month index into readable strings
retention_matrix.index = retention_matrix.index.astype(str)


# Create cohort retention heatmap
plt.figure(figsize=(16, 8))

sns.heatmap(
    retention_matrix,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    vmin=0,
    vmax=100
)

# Add title and labels
plt.title("Customer Cohort Retention Analysis")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Customer Cohort")

# Adjust layout
plt.tight_layout()

# Save the heatmap
plt.savefig(
    "output/charts/cohort_retention_heatmap.png",
    dpi=300
)

# Display the heatmap
plt.show()
