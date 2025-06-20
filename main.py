from fastapi import FastAPI
from faker import Faker
import random
import uuid

app = FastAPI()
fake = Faker()

@app.get("/")
def root():
    return {"message": "Dummy ecom API is live! "}

@app.get("/users")
def get_users(count: int=5):
    return [generate_user() for _ in range(count)]

@app.get("/products")
def get_products(count: int=5):
    return[generate_product() for _ in range(count)]

@app.get("/orders")
def get_orders(count: int=5):
    return[generate_order() for _ in range(count)]



def generate_user():
    return{
        "user_id": str(uuid.uuid4()),
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "registered_at": fake.iso8601()
    }

def generate_product():
    return {
        "product_id": str(uuid.uuid4()),
        "name": fake.word().capitalize(),
        "price": round(random.uniform(10, 500), 2),
        "category": fake.word(),
        "stock": random.randint(0, 100)
    }

def generate_order():
    product = generate_product()
    quantity = random.randint(1, 5)
    return {
        "order_id": str(uuid.uuid4()),
        "user": generate_user(),
        "product": generate_product(),
        "quantity": random.randint(1, 5),
        "total_price": round(product["price"] * quantity, 2),
        "ordered_at": fake.iso8601()
    }