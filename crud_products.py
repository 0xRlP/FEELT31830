import socket
import database as db
import redis
import json

session = db.Session()
redis_cli = redis.Redis(host="localhost", port=16379, decode_responses=True, encoding="utf-8")



def validate_restaurant(cid):
    restaurant = session.query(db.Restaurant).filter(db.Restaurant.id == cid)
    for data in restaurant:
            return True
    return False


def key_exists(key):
    cache = redis_cli.get(f"product-{id}")
    if cache:
        return cache
    
    products = session.query(db.Product).filter(db.Product.id == key)
    response =[]
    for data in products:
        response.append(data)
    return response

def name_exists(name):
    products = session.query(db.Product).filter(db.Product.name == name)
    response =[]
    for data in products:
        response.append(data)
    return response

def create_product(key, data):
    id,price,name = data
    if not key_exists(id) and not name_exists(name):
        value = {"restaurant_id": key, "price": price, "name": name}
        redis_cli.publish('channel-1', f'create | product-{id} | '+json.dumps(value))
        print("Publish data created in channel-1")

        product = db.Product(key, id, price, name)
        session.add(product)
        session.commit()
        return f'"name": {product.name}, "price": {product.price}'
    return f'Error: Product already exists!'

def read_product(data):
    id = data[0]
    cache = redis_cli.get(f"product-{id}")
    if cache:
        print("Data searched in cache")
        return cache

    print("Data searched in database")
    products = session.query(db.Product).filter(db.Product.id == id)
    response = []
    for data in products:
        return f'id: {data.id},  preco: {data.price},  departamento: {data.departament}'
    return f'Error: product with id: {id} does not exists'

def update_product(data):
    id,price,name = data

    if key_exists(id) and not name_exists(name):
        value = {"price": price, "name": name}
        redis_cli.publish('channel-1', f'update | product-{key} | '+json.dumps(value))
        print("Publish data updated in channel-1")

        session.query(db.Product).filter(db.Product.id == id).update({
            'price': price,
            'name': name
            })
        session.commit()
        return f'Product {id} updated!'
    return f'Error: Product with id: {id} does not exists or name alredy in use'

def delete_product(data):
    id = data[0]
    if key_exists(id):
        redis_cli.publish('channel-1', f'delete | product-{key} | '+json.dumps(value))
        print("Publish data deleted in channel-1")
        
        session.query(db.Product).filter(db.Product.id == id).delete()
        session.commit()
        return f'Product {id} deleted!'
    return f'Error: Product with id: {id} does not exists'