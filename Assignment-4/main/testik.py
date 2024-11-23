import redis

r = redis.Redis(host='localhost', port=6379, db=0)

try:
    r.ping()
    print("Connected to Redis!")
except redis.ConnectionError as e:
    print("Redis connection error:", e)
