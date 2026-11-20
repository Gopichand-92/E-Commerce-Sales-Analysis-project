
import mysql.connector
import pandas as pd
import numpy as np
import os
from getpass import getpass


# ============================================================
# 1. CONNECT TO MYSQL DATABASE
# ============================================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=getpass("Enter MySQL password: "),
    database="ecommerce"
)

print("\nSuccessfully connected to MySQL database!")


try:

    # ========================================================
    # 2. LOAD DATA FROM MYSQL TABLES
    # ========================================================

    orders_df = pd.read_sql(
        "SELECT * FROM orders", connection
    )

    order_items_df = pd.read_sql(
        "SELECT * FROM order_items", connection
    )

    products_df = pd.read_sql(
        "SELECT * FROM products", connection
    )

    customers_df = pd.read_sql(
        "SELECT * FROM customers", connection
    )


    # ========================================================
    # 3. DISPLAY INITIAL DATA
    # ========================================================

    print("\nOrders Data:")
    print(orders_df.head())

    print("\nOrder Items Data:")
    print(order_items_df.head())

    print("\nProducts Data:")
    print(products_df.head())

    print("\nCustomers Data:")
    print(customers_df.head())


    # ========================================================
    # 4. FILTER ONLY DELIVERED ORDERS
    # ========================================================

    delivered_orders = orders_df.loc[
        orders_df["order_status"] == "Delivered"
    ].copy()

    print("\nDelivered Orders:")
    print(delivered_orders.head())

    print("\nTotal Delivered Orders:", len(delivered_orders))


    # ========================================================
    # 5. FILTER ITEMS BELONGING TO DELIVERED ORDERS
    # ========================================================

    delivered_order_ids = delivered_orders["order_id"]

    delivered_items = order_items_df.loc[
        order_items_df["order_id"].isin(delivered_order_ids)
    ].copy()

    print("\nDelivered Order Items:")
    print(delivered_items.head())

    print("\nTotal Delivered Order Items:", len(delivered_items))


    # ========================================================
    # 6. CALCULATE GROSS AMOUNT BEFORE DISCOUNT
    # ========================================================

    delivered_items["gross_amount"] = (
        delivered_items["quantity"] *
        delivered_items["unit_price"]
    )

    print("\nGross Amount Calculation:")
    print(
        delivered_items[
            ["order_id", "product_id", "quantity",
             "unit_price", "gross_amount"]
        ].head()
    )


    # ========================================================
    # 7. CALCULATE GROSS MERCHANDISE VALUE (GMV)
    # ========================================================

    gmv = delivered_items["gross_amount"].sum()

    print("\nTotal GMV:", round(gmv, 2))


    # ========================================================
    # 8. CALCULATE DISCOUNT AMOUNT USING NUMPY
    # ========================================================

    delivered_items["discount_amount"] = np.round(
        delivered_items["gross_amount"] *
        delivered_items["discount_pct"] / 100,
        2
    )

    print("\nDiscount Calculation:")
    print(
        delivered_items[
            ["gross_amount", "discount_pct", "discount_amount"]
        ].head()
    )


    # ========================================================
    # 9. CALCULATE NET SALES AFTER DISCOUNT
    # ========================================================

    delivered_items["net_sales"] = np.round(
        delivered_items["gross_amount"] -
        delivered_items["discount_amount"],
        2
    )

    print("\nNet Sales Calculation:")
    print(
        delivered_items[
            ["gross_amount", "discount_amount", "net_sales"]
        ].head()
    )


    # ========================================================
    # 10. CALCULATE REVENUE FOR EACH ORDER
    # ========================================================

    order_revenue = delivered_items.groupby(
        "order_id"
    )["net_sales"].sum().reset_index()

    order_revenue = order_revenue.merge(
        delivered_orders[
            ["order_id", "order_date", "shipping_fee"]
        ],
        on="order_id",
        how="inner"
    )

    # Add shipping fee once per order
    order_revenue["total_revenue"] = (
        order_revenue["net_sales"] +
        order_revenue["shipping_fee"]
    )

    print("\nOrder-wise Revenue:")
    print(order_revenue.head())


    # ========================================================
    # 11. CALCULATE TOTAL NET ITEM REVENUE
    # ========================================================

    net_item_revenue = delivered_items["net_sales"].sum()

    print(
        "\nTotal Net Item Revenue:",
        round(net_item_revenue, 2)
    )


    # ========================================================
    # 12. CALCULATE TOTAL SHIPPING FEES
    # ========================================================

    total_shipping = delivered_orders["shipping_fee"].sum()

    print(
        "\nTotal Shipping Fees:",
        round(total_shipping, 2)
    )


    # ========================================================
    # 13. CALCULATE TOTAL NET REVENUE
    # ========================================================

    net_revenue = net_item_revenue + total_shipping

    print("\nTotal Net Revenue:", round(net_revenue, 2))


    # ========================================================
    # 14. CALCULATE AVERAGE ORDER VALUE (AOV)
    # ========================================================

    aov = order_revenue["total_revenue"].mean()

    print("\nAverage Order Value:", round(aov, 2))


    # ========================================================
    # 15. CREATE AND SAVE KPI SUMMARY
    # ========================================================

    kpi_summary = pd.DataFrame({
        "Metric": [
            "Total Delivered Orders",
            "GMV",
            "Net Item Revenue",
            "Total Shipping Fees",
            "Net Revenue",
            "Average Order Value"
        ],

        "Value": [
            len(delivered_orders),
            round(gmv, 2),
            round(net_item_revenue, 2),
            round(total_shipping, 2),
            round(net_revenue, 2),
            round(aov, 2)
        ]
    })

    print("\nKPI Summary:")
    print(kpi_summary)

    os.makedirs("output", exist_ok=True)

    kpi_summary.to_csv(
        "output/kpi_summary.csv",
        index=False
    )

    print("\nKPI Summary CSV saved successfully!")


    # ========================================================
    # 16. MERGE DELIVERED ITEMS WITH PRODUCT DETAILS
    # ========================================================

    product_sales = delivered_items.merge(
        products_df,
        on="product_id",
        how="inner"
    )

    print("\nProduct Sales Data:")
    print(
        product_sales[
            ["product_id", "product_name", "net_sales"]
        ].head()
    )


    # ========================================================
    # 17. CALCULATE PRODUCT-WISE NET REVENUE
    # ========================================================

    product_revenue = product_sales.groupby(
        ["product_id", "product_name"]
    )["net_sales"].sum().reset_index()

    print("\nProduct-wise Net Revenue:")
    print(product_revenue.head(10))


    # ========================================================
    # 18. FIND TOP 10 PRODUCTS BY NET REVENUE
    # ========================================================

    top_10_products = product_revenue.nlargest(
        10, "net_sales"
    )

    print("\nTop 10 Products by Net Revenue:")
    print(top_10_products)

    top_10_products.to_csv(
        "output/top_10_products.csv",
        index=False
    )


    # ========================================================
    # 19. MERGE DELIVERED ORDERS WITH CUSTOMER DETAILS
    # ========================================================

    regional_orders = delivered_orders.merge(
        customers_df,
        on="customer_id",
        how="inner"
    )

    print("\nRegional Orders Data:")
    print(
        regional_orders[
            ["order_id", "customer_id", "city", "state"]
        ].head()
    )


    # ========================================================
    # 20. MERGE REGIONAL DATA WITH DELIVERED ITEMS
    # ========================================================

    regional_sales = delivered_items.merge(
        regional_orders[["order_id", "state"]],
        on="order_id",
        how="inner"
    )

    print("\nRegional Sales Data:")
    print(
        regional_sales[
            ["order_id", "state", "net_sales"]
        ].head()
    )


    # ========================================================
    # 21. CALCULATE STATE-WISE NET ITEM REVENUE
    # ========================================================

    state_revenue = regional_sales.groupby(
        "state"
    )["net_sales"].sum().reset_index()

    print("\nState-wise Net Item Revenue:")
    print(state_revenue)


    # ========================================================
    # 22. FIND TOP 5 STATES BY NET ITEM REVENUE
    # ========================================================

    top_5_states = state_revenue.nlargest(
        5, "net_sales"
    )

    print("\nTop 5 States by Net Item Revenue:")
    print(top_5_states)

    top_5_states.to_csv(
        "output/top_5_states.csv",
        index=False
    )


    # ========================================================
    # 23. CALCULATE DAILY REVENUE
    # ========================================================

    order_revenue["order_date"] = pd.to_datetime(
        order_revenue["order_date"]
    )

    daily_revenue = order_revenue.groupby(
        "order_date"
    )["total_revenue"].sum().reset_index()

    daily_revenue = daily_revenue.sort_values(
        "order_date"
    )

    print("\nDaily Revenue:")
    print(daily_revenue.head(10))


    # ========================================================
    # 24. CALCULATE 7-DAY MOVING AVERAGE
    # ========================================================

    # Add dates with no orders and assign them zero revenue
    daily_revenue = daily_revenue.set_index(
        "order_date"
    ).asfreq("D", fill_value=0)

    # Calculate the average revenue over the current
    # day and previous six days
    daily_revenue["7_day_moving_average"] = (
        daily_revenue["total_revenue"]
        .rolling(window=7)
        .mean()
    )

    daily_revenue = daily_revenue.reset_index()

    print("\n7-Day Moving Average:")
    print(daily_revenue.head(12))


    # ========================================================
    # 25. CALCULATE CUMULATIVE YEAR-TO-DATE REVENUE
    # ========================================================

    daily_revenue["cumulative_revenue"] = (
        daily_revenue.groupby(
            daily_revenue["order_date"].dt.year
        )["total_revenue"].cumsum()
    )

    print("\nCumulative Year-to-Date Revenue:")
    print(
        daily_revenue[
            ["order_date", "total_revenue",
             "cumulative_revenue"]
        ].head(12)
    )

    daily_revenue.to_csv(
        "output/daily_revenue_trends.csv",
        index=False
    )


    # ========================================================
    # 26. CHECK CUSTOMER PURCHASE HISTORY
    # ========================================================

    customer_orders = delivered_orders[
        ["customer_id", "order_id", "order_date"]
    ].copy()

    print("\nCustomer Purchase History:")
    print(customer_orders.head(10))

    print(
        "\nTotal Unique Purchasing Customers:",
        customer_orders["customer_id"].nunique()
    )

    print(
        "\nTotal Delivered Orders:",
        customer_orders["order_id"].nunique()
    )


    # ========================================================
    # 27. IDENTIFY EACH CUSTOMER'S FIRST PURCHASE MONTH
    # ========================================================

    customer_orders["order_date"] = pd.to_datetime(
        customer_orders["order_date"]
    )

    customer_orders["order_month"] = (
        customer_orders["order_date"].dt.to_period("M")
    )

    customer_cohort = customer_orders.groupby(
        "customer_id"
    )["order_month"].min().reset_index()

    customer_cohort.rename(
        columns={"order_month": "cohort_month"},
        inplace=True
    )

    print("\nCustomer Cohort Month:")
    print(customer_cohort.head(10))


    # ========================================================
    # 28. CALCULATE CUSTOMER PURCHASE MONTH INDEX
    # ========================================================

    customer_orders = customer_orders.merge(
        customer_cohort,
        on="customer_id",
        how="left"
    )

    customer_orders["month_index"] = (
        (customer_orders["order_month"].dt.year -
         customer_orders["cohort_month"].dt.year) * 12
        +
        (customer_orders["order_month"].dt.month -
         customer_orders["cohort_month"].dt.month)
    )

    print("\nCustomer Purchase Month Index:")
    print(customer_orders.head(15))


    # ========================================================
    # 29. CREATE COHORT RETENTION COUNT MATRIX
    # ========================================================

    cohort_data = customer_orders.pivot_table(
        index="cohort_month",
        columns="month_index",
        values="customer_id",
        aggfunc="nunique"
    )

    # Create all month-index columns from 0 to the
    # maximum observed month index
    max_month_index = int(
        customer_orders["month_index"].max()
    )

    cohort_data = cohort_data.reindex(
        columns=range(max_month_index + 1),
        fill_value=0
    )

    # Find the latest month present in the purchase data
    latest_order_month = customer_orders["order_month"].max()

    # Keep future, unobserved cohort months blank
    for cohort_month in cohort_data.index:

        observed_months = (
            (latest_order_month.year - cohort_month.year) * 12
            +
            (latest_order_month.month - cohort_month.month)
        )

        cohort_data.loc[
            cohort_month,
            cohort_data.columns > observed_months
        ] = np.nan

    print("\nCohort Retention Count Matrix:")
    print(cohort_data)

    cohort_data.to_csv(
        "output/cohort_retention_counts.csv"
    )


    # ========================================================
    # 30. CALCULATE COHORT RETENTION PERCENTAGES
    # ========================================================

    # Replace missing values temporarily with zero
    # so NumPy can perform the division
    cohort_counts = cohort_data.fillna(0)

    # Get the original number of customers in each cohort
    cohort_sizes = (
        cohort_counts.iloc[:, 0]
        .to_numpy()
        .reshape(-1, 1)
    )

    # Calculate retention percentages using NumPy
    retention_values = np.divide(
        cohort_counts.to_numpy(),
        cohort_sizes,
        out=np.zeros_like(
            cohort_counts.to_numpy(),
            dtype=float
        ),
        where=cohort_sizes != 0
    ) * 100

    # Convert the result back into a DataFrame
    retention_matrix = pd.DataFrame(
        np.round(retention_values, 2),
        index=cohort_counts.index,
        columns=cohort_counts.columns
    )

    # Keep future, unobserved months blank instead of
    # incorrectly reporting them as 0% retention
    for cohort_month in retention_matrix.index:

        observed_months = (
            (latest_order_month.year - cohort_month.year) * 12
            +
            (latest_order_month.month - cohort_month.month)
        )

        retention_matrix.loc[
            cohort_month,
            retention_matrix.columns > observed_months
        ] = np.nan

    print("\nCohort Retention Percentage Matrix:")
    print(retention_matrix)

    retention_matrix.to_csv(
        "output/cohort_retention_percentages.csv"
    )


    # ========================================================
    # 31. DISPLAY PROJECT OUTPUT FILES
    # ========================================================

    print("\nAll analysis tasks completed successfully!")

    print("\nCSV files saved in the output folder:")
    print("- kpi_summary.csv")
    print("- top_10_products.csv")
    print("- top_5_states.csv")
    print("- daily_revenue_trends.csv")
    print("- cohort_retention_counts.csv")
    print("- cohort_retention_percentages.csv")


finally:

    # ========================================================
    # 32. CLOSE MYSQL DATABASE CONNECTION
    # ========================================================

    if connection.is_connected():
        connection.close()

