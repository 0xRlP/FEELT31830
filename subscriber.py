import redis
import time

#configurando o cli do redis
redis_cli = redis.Redis(host="localhost", port=16379, decode_responses=True, encoding="utf-8")

subscriber = redis_cli.pubsub()
subscriber.psubscribe('channel-1')


#broadcast de dados no sistema
def set_all_caches(cmd,key,value):
    
    if cmd == 'create':
        print('create: '+ key+value)
        redis_cli.set(key,value)
    if cmd == 'update':
        print('update: '+ key+value)
        redis_cli.set(key,value)
    if cmd == 'delete':
        print('delete: '+ key)
        redis_cli.delete(key)

while True:
    messages = subscriber.get_message()
    
    if messages:
        print("Listen in channel-1")
        if messages["data"] != 1:
            cmd,key,value = messages["data"].split(" | ")
            set_all_caches(cmd, key,value)
    

    time.sleep(1)