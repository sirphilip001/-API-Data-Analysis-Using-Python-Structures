"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        customers = response.json()

        if not isinstance(customers, list):
            print("Could not fetch customers: expected a list in the API response.")
            return []

        return customers

    except requests.exceptions.RequestException as error:
        print(f"Could not fetch customers: {error}")
        return []
    except ValueError as error:
        print(f"Could not parse the API response as JSON: {error}")
        return []


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key, value in record.items():
        print("  " * indent + f"{key}: {type(value).__name__}")

        if isinstance(value, dict):
            explore(value, indent + 1)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    explore(item, indent + 1)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = []

    for customer in customers:
        email = customer["email"]

        rows.append({
            "customer_id": customer["id"],
            "name": customer["name"],
            "username": customer["username"],
            "email": email,
            "email_domain": email.rsplit(".", 1)[-1].lower(),
            "phone": customer["phone"],
            "city": customer["address"]["city"],
            "zipcode": customer["address"]["zipcode"],
            "latitude": float(customer["address"]["geo"]["lat"]),
            "longitude": float(customer["address"]["geo"]["lng"]),
            "company": customer["company"]["name"],
            "website": customer["website"],
        })

    return rows


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {customer["address"]["city"] for customer in customers}


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}

    for customer in customers:
        city = customer["address"]["city"]

        if city not in counts:
            counts[city] = 0

        counts[city] += 1

    return dict(sorted(counts.items(), key=lambda pair: (-pair[1], pair[0])))


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    domains = [
        customer["email"].rsplit(".", 1)[-1].lower()
        for customer in customers
    ]

    counts = {domain: domains.count(domain) for domain in set(domains)}

    return dict(sorted(counts.items(), key=lambda pair: (-pair[1], pair[0])))


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(rows)


def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    plt.bar(counts.keys(), counts.values())
    plt.title("Customers by Email Ending")
    plt.xlabel("Email ending")
    plt.ylabel("Number of customers")
    plt.savefig(path)
    plt.close()


if __name__ == "__main__":
    # TODO: run each step and print a short findings summary
    customers = get_customers()
    print(f"Customers fetched: {len(customers)}")
    if customers:
        counts = city_counts(customers)
        print(f"City counts: {counts}")

        explore(customers[0])
        rows = extract_attributes(customers)
        df = to_dataframe(rows)
        print(f"DataFrame shape: {df.shape}")
        print("DataFrame dtypes:")
        print(df.dtypes)

        pandas_city_counts = df["city"].value_counts().to_dict()
        print(f"Pandas city counts: {pandas_city_counts}")
        print(f"Pandas agrees with Python counts: {pandas_city_counts == counts}")
        print(rows[0]) 
        cities = unique_cities(customers)
        print(f"Unique cities: {len(cities)}")
        print(f"Customers: {len(customers)}")
        domain_counts = email_domain_counts(customers)
        print(f"Email domains: {domain_counts}") 

        output_dir = Path(__file__).resolve().parent / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_dir / "customers.csv", index=False)

        city_counts_df = pd.DataFrame(
            [
                {"city": city, "customer_count": count}
                for city, count in counts.items()
            ]
        )
        city_counts_df.to_csv(output_dir / "city_counts.csv", index=False)

        print("CSV files saved in the output folder.")


        chart_path = output_dir / "customer_distribution.png"
        plot_distribution(domain_counts, chart_path)
        print(f"Chart saved to: {chart_path}")


