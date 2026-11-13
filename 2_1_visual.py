import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sales_df = pd.read_csv("sales.csv", sep=";")
products_df = pd.read_csv("products.csv", sep=";")
product_subset = products_df[["product_id", "title", "rating", "brand"]]
df = sales_df.merge(product_subset, on="product_id", how="left")

df["order_date"] = pd.to_datetime(df["order_date"])
df["year_month"] = df["order_date"].dt.to_period("M")

sns.set_theme(style="whitegrid")
gradient_colors = ["#ff595e", "#ffca3a"]
custom_palette_10 = sns.blend_palette(gradient_colors, n_colors=10)

city_palette = {
    "Carbon City": "#1982c4",
    "Sunny Bay": "#ffca3a",
    "Maple Valley": "#ff595e",
}

# Plot 1: MONTHLY REVENUE BREAKDOWN BY CITY
df["month_str"] = df["year_month"].astype(str)
monthly_city_rev = (
    df.groupby(["month_str", "city"])["total_price"].sum().reset_index()
)

fig, ax = plt.subplots(figsize=(14, 6), dpi=300)
sns.barplot(
    data=monthly_city_rev,
    x="month_str",
    y="total_price",
    hue="city",
    palette=city_palette,
    ax=ax,
)

ax.set_title(
    "MONTHLY REVENUE BREAKDOWN BY CITY", fontsize=14, fontweight="bold", pad=15
)
ax.set_xlabel("Month", fontsize=11, labelpad=8)
ax.set_ylabel("Total Revenue (USD)", fontsize=11, labelpad=8)
ax.tick_params(axis="x", rotation=45)
ax.legend(title="City", frameon=True)
ax.grid(True, axis="y", linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig("2_2_monthly_revenue_by_city.png", dpi=300)
plt.close()

# Plot 2: TOP 10 BEST-SELLING PRODUCTS (UNITS SOLD)
top_products = (
    df.groupby("title")["quantity"].sum().nlargest(10).reset_index()
)

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
sns.barplot(
    data=top_products,
    x="quantity",
    y="title",
    palette=custom_palette_10,
    hue="title",
    legend=False,
    ax=ax,
)

ax.set_title(
    "TOP 10 BEST-SELLING PRODUCTS (UNITS SOLD)",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
ax.set_xlabel("Total Units Sold", fontsize=11, labelpad=8)
ax.set_ylabel("Product Title", fontsize=11, labelpad=8)
ax.grid(True, axis="x", linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig("2_2_top_10_products.png", dpi=300)
plt.close()

# Plot 3: TOTAL REVENUE BY BRAND
brand_rev = (
    df.groupby("brand")["total_price"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

n_brands = len(brand_rev)
brand_palette = sns.blend_palette(gradient_colors, n_colors=n_brands)

fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
sns.barplot(
    data=brand_rev,
    x="total_price",
    y="brand",
    palette=brand_palette,
    hue="brand",
    legend=False,
    ax=ax,
)

ax.set_title(
    "TOTAL REVENUE BY BRAND", fontsize=14, fontweight="bold", pad=15
)
ax.set_xlabel("Total Revenue (USD)", fontsize=11, labelpad=8)
ax.set_ylabel("Brand", fontsize=11, labelpad=8)
ax.grid(True, axis="x", linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig("2_2_total_rev_by_brand.png", dpi=300)
plt.close()