import redis
import hashlib
import json

class CacheService:
    def __init__(self, host="localhost", port=6379, db=0, expire_seconds=300):
        self.client = redis.Redis(host=host, port=port, db=db)
        self.expire_seconds = expire_seconds

    def get_cache_key(self, prompt, model):
        raw = f"{model}:{prompt}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, prompt, model):
        key = self.get_cache_key(prompt, model)
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, prompt, model, response):
        key = self.get_cache_key(prompt, model)
        self.client.setex(key, self.expire_seconds, json.dumps(response))
