import socket
import database as db
import redis
import json

session = db.Session()
redis_cli = redis.Redis(host="localhost", port=16379, decode_responses=True, encoding="utf-8")

def create_user(key,role):
    user = session.query(db.User).filter(db.User.id == key)
    for data in user:
        return
    admin = db.User(key, role)
    session.add(admin)
    session.commit()

def validate_user_admin(key):
    user = session.query(db.User).filter(db.User.id == key)
    for data in user:
        if data.role == 'admin':
            return True
    return False

def key_exists(key):
    cache = redis_cli.get(f"restaurant-{id}")
    if cache:
        return cache
    # se nao existe no cache, verifico no banco    
    restaurants = session.query(db.Restaurant).filter(db.Restaurant.id == key)
    response =[]
    for data in restaurants:
        response.append(data)
    return response

def name_exists(name):
    restaurants = session.query(db.Restaurant).filter(db.Restaurant.name == name)
    response =[]
    for data in restaurants:
        response.append(data)
    return response

def create_restaurant(key, data):
    name, segment, uf = data
    
    if not name_exists(name) and not key_exists(key):
    ## verificar se o nome ja existe no banco
        value = {"name": name, "segment": segment, "uf": uf}
        redis_cli.publish('channel-1', f'create | restaurant-{key} | '+json.dumps(value))
        print("Publish data created in channel-1")

        restaurant = db.Restaurant(key, name, segment, uf)
        session.add(restaurant)
        session.commit()
        return f'"name": {restaurant.name}, "segment": {restaurant.segment}, "uf": {restaurant.uf}'
    return f'Error: Restaurant already exists!'

def read_restaurant(id):
    cache = redis_cli.get(f'restaurant-{id}')
    if cache:
        print("Data searched in cache")
        return cache

    print("Data searched in database")
    restaurants = session.query(db.Restaurant).filter(db.Restaurant.id == id)
    response = []
    for data in restaurants:
        return f'"name": {data.name}, "segment": {data.segment}, "uf": {data.uf}'
    return f'Error: Restaurant with id: {id}, not exists'

def update_restaurant(key, data):
    name, segment, uf = data

    if not name_exists(name) and key_exists(key):
        value = {"name": name, "segment": segment, "uf": uf}
        redis_cli.publish('channel-1', f'update| restaurant-{key} | '+json.dumps(value))
        print("Publish data updated in channel-1")

        session.query(db.Restaurant).filter(db.Restaurant.id == key).update({
            'name': name,
            'segment': segment,
            'uf': uf
            })
        session.commit()
        return f'"name": {name}, "segment": {segment}, "uf": {uf}'
    return f'Error: Restaurant with id: {id}, not exists'

def delete_restaurant(id):
    if key_exists(id):
        redis_cli.publish('channel-1', f'delete | restaurant-{key} | -')
        print("Publish data deleted in channel-1")
        
        session.query(db.Restaurant).filter(db.Restaurant.id == id).delete()
        session.commit()
        return f'Restaurant deleted!'
    return f'Error: Restaurant with id: {id}, not exists'