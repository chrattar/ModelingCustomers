import random

def generate_customer_data(customer_ids):
    customer_data = {}  #DICT

    for customer_ID in customer_ids:
        customer_data[customer_ID] = {
            "sales_volume": random.randint(150000, 20000000),
            "project_size_sqft": random.randint(10000, 2000000),
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6)
        }

    return customer_data 
customer_data = generate_customer_data(customer_ids)


for customer, details in list(customer_data.items())[:5]:
    print(f"Customer {customer}: {details}")
