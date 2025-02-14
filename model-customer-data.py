import pandas as pd

classification_distribution = {
    "A": {"percentage": 0.10, "sales_share": 0.75, "project_size_range": (500000, 2000000), "price_range": (6, 10)},
    "B": {"percentage": 0.30, "sales_share": 0.20, "project_size_range": (100000, 500000), "price_range": (7, 12)},
    "C": {"percentage": 0.60, "sales_share": 0.05, "project_size_range": (10000, 100000), "price_range": (8, 15)}
}

def generate_customer_jobs(customer_ids):
    customer_data = []

    num_customers = len(customer_ids)
    
    num_A = int(num_customers * classification_distribution["A"]["percentage"])
    num_B = int(num_customers * classification_distribution["B"]["percentage"])
    num_C = num_customers - (num_A + num_B)

    classified_customers = (
        ["A"] * num_A + ["B"] * num_B + ["C"] * num_C
    )
    random.shuffle(classified_customers)

    total_sales = 1_000_000_000  

    sales_A = total_sales * classification_distribution["A"]["sales_share"]
    sales_B = total_sales * classification_distribution["B"]["sales_share"]
    sales_C = total_sales * classification_distribution["C"]["sales_share"]

    sales_A_values = list(np.random.exponential(sales_A / num_A, num_A))
    sales_B_values = list(np.random.exponential(sales_B / num_B, num_B))
    sales_C_values = list(np.random.exponential(sales_C / num_C, num_C))

    sales_volumes = sales_A_values + sales_B_values + sales_C_values
    random.shuffle(sales_volumes)

    for idx, customer_id in enumerate(customer_ids):
        classification = classified_customers[idx]

        # Assign jobs based on classification
        if classification == "A":
            num_jobs = random.randint(5, 10)
        elif classification == "B":
            num_jobs = random.randint(2, 5)
        else:  # "C"
            num_jobs = random.randint(1, 3)

        total_sales_value = 0
        jobs = []

        for job_num in range(1, num_jobs + 1):
            project_size = random.randint(*classification_distribution[classification]["project_size_range"])
            price_per_sqft = round(random.uniform(*classification_distribution[classification]["price_range"]), 2)
            total_value = project_size * price_per_sqft

            # Store each job as a separate row
            jobs.append({
                "Customer ID": customer_id,
                "Classification": classification,
                "Job": f"Customer{customer_id}-Job{job_num}",
                "Project-Size (sf)": project_size,
                "Price per Sq Ft": price_per_sqft,
                "Total Value ($)": total_value
            })

            total_sales_value += total_value  # Accumulate total value of all jobs

        # Ensure sales volume is at least the total job value
        adjusted_sales_volume = max(int(sales_volumes[idx]), int(total_sales_value * random.uniform(1.1, 2.5)))

        # Add sales volume to all jobs for consistency
        for job in jobs:
            job["Sales Volume ($)"] = adjusted_sales_volume

        customer_data.extend(jobs)

    return customer_data

# Generate the dataset
customer_jobs = generate_customer_jobs(customer_ids)

# Convert to DataFrame
df = pd.DataFrame(customer_jobs)


import pandas as pd

#pandas disp
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", 50)  # Increase max displayed rows
pd.set_option("display.width", 1000)  # Prevent wrapping of long rows
pd.set_option("display.float_format", "{:.2f}".format)  # Format floats nicely
print(df.head(10))
# Save to CSV and JSON
df.to_csv("customer_jobs_data.csv", index=False)
df.to_json("customer_jobs_data.json", index=False)
print("Data saved to customer_jobs_data.csv")

