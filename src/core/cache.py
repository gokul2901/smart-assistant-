# src/core/cache.py

import time



cache_store = {}



def set_cache(
    key,
    value,
    expire=300
):

    cache_store[key] = {

        "value": value,

        "expire":
        time.time()+expire

    }



def get_cache(key):

    data = cache_store.get(
        key
    )


    if not data:

        return None


    if time.time() > data["expire"]:

        del cache_store[key]

        return None


    return data["value"]



def clear_cache():

    cache_store.clear()