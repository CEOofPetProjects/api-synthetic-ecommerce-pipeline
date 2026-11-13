import random
from faker import Faker
import pandas as pd
import requests

fake = Faker()
url = "https://dummyjson.com/products" 
headers = {"User-Agent": "Mozilla/5.0"}
cities = ["Carbon City", "Maple Valley", "Sunny Bay"]
city_weights = [50, 30, 20]

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(
        data["products"],
        columns=[
            "id",
            "title",
            "category",
            "price",
            "discountPercentage",
            "rating",
            "brand",
            "sku",
        ],
    )

    df = df[df["category"].isin(["beauty", "fragrances"])]
    df = df.drop(columns=["id", "category"])
    df.insert(0, "product_id", range(1, len(df) + 1))
    df = df.reset_index(drop=True)

    products_list = df.to_dict("records")
    sales_data = []

    for order_id in range(1, 3001):
        product = random.choice(products_list)
        quantity = random.randint(1, 5)
        selected_city = random.choices(cities, weights=city_weights, k=1)[0]

        sales_data.append({
            "order_id": order_id,
            "order_date": fake.date_between(start_date="-1y", end_date="today"),
            "product_id": product["product_id"],
            "sku": product["sku"],
            "quantity": quantity,
            "unit_price": product["price"],
            "discountPercentage": product["discountPercentage"],
            "total_price": round(product["price"] * (1 - product["discountPercentage"] / 100) * quantity, 2,),
            "customer_name": fake.name(),
            "city": selected_city,
        })

    sales_df = pd.DataFrame(sales_data)

    df.to_csv("1_2_products.csv", index=False, sep=";", encoding="utf-8-sig")
    sales_df.to_csv("1_2_sales.csv", index=False, sep=";", encoding="utf-8-sig")

except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve data: {e}")