from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]

class ProductUpdate(BaseModel):
    code: str
    name: str
    price: float
    stock: int

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):

    current = None
    for p in products:
        if p["id"] == product_id:
            current = p
            break

    if current is None:
        raise HTTPException(404, "Product not found")

    for p in products:
        if p["id"] != product_id and p["code"] == product.code:
            raise HTTPException(400, "Product code already exists")

    if product.name.strip() == "":
        raise HTTPException(400, "Product name cannot be empty")

    if product.price <= 0:
        raise HTTPException(400, "Price must be greater than 0")

    if product.stock < 0:
        raise HTTPException(400, "Stock must be greater than or equal to 0")

    current["code"] = product.code
    current["name"] = product.name
    current["price"] = product.price
    current["stock"] = product.stock

    return {
        "message": "Update product successfully",
        "data": current
    }