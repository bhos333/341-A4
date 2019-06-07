import time

import redis
from math import sqrt
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

@app.route('/isPrime/<number>/')
def isPrime(number):
    try:
        if int(number) > 1:
            for i in range(2,int(sqrt(int(number)))):
                if int(number) % i == 0 or i == int(number):
                    return '{} is not a prime number.\n'.format(number)
            cache.lrem('primes', 0, number)
            cache.lpush('primes', number)
            return '{} is a prime number.\n'.format(number)
        else:
            return'please enter a number more than 1\n'
    except ValueError:
        return'Please enter a number as digits.\n'
@app.route('/primesStored/')
def stored_primes():
    prime_string = ' \n'
    primes_list = cache.lrange('primes', 0, -1)
    for n in primes_list:
        prime_string = '{} {}\n'.format(prime_string, n)
    return(prime_string)