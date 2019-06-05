import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<number>')
def isPrime(number):
    for i in range(2,number):
        if number % i == 0:
            return '{} is not a prime number.\n'.format(number)
    cache.lpush(primes, number)
    return '{} is a prime number.\n'.format(number)

@app.route('/primesStored')
def stored_primes():
    
