class LFUCache:
    def __init__(self, capacity):
        if not 1 <= capacity <= 10000:
            raise ValueError("Capacity must be between 1 and 10,000")

        self.cache = {}
        self.frequencies = {}

        self.capacity = capacity
        
        self.operations = 0
        self.smallest = 0

    def get(self, key):
        self.__operation_check()

        if key not in self.cache:
            return -1

        self.cache[key]["last"] = self.operations
        self.__increase_frequency(key)

        return self.cache[key]["value"]

    def put(self, key, value):
        self.__operation_check()

        if key in self.cache:
            self.cache[key]["value"] = value
            return

        if len(self.cache) >= self.capacity:
            self.__remove_cache()

        self.cache[key] = {
            "value": value,

            "frequency": 1,
            "last": self.operations,

            "previous": None,
            "following": None
        }

        if 1 not in self.frequencies:
            self.frequencies[1] = {
                "first": None,
                "end": None,
                "whole": 0
            }

        self.__add_cache(key, 1)
        self.smallest = 1

    # -----------==========-----------------

    def __add_cache(self, key, frequency):
        frequency_cache = self.frequencies[frequency]

        first_key = frequency_cache["first"]

        self.cache[key]["previous"] = None
        self.cache[key]["following"] = first_key

        if first_key is not None:
            self.cache[first_key]["previous"] = key
        else:
            frequency_cache["end"] = key

        frequency_cache["first"] = key
        frequency_cache["whole"] += 1

    def __remove_cache_key(self, key, frequency):
        frequency_cache = self.frequencies[frequency]

        previous_key = self.cache[key]["previous"]
        following_key = self.cache[key]["following"]

        if previous_key is not None:
            self.cache[previous_key]["following"] = following_key
        else:
            frequency_cache["first"] = following_key

        if following_key is not None:
            self.cache[following_key]["previous"] = previous_key
        else:
            frequency_cache["end"] = previous_key

        self.cache[key]["previous"] = None
        self.cache[key]["following"] = None

        frequency_cache["whole"] -= 1

    def __remove_cache(self):
        frequency_cache = self.frequencies[self.smallest]
        key = frequency_cache["end"]

        self.__remove_cache_key(key, self.smallest)

        del self.cache[key]

        if frequency_cache["whole"] == 0:
            del self.frequencies[self.smallest]

    def __increase_frequency(self, key):
        old_frequency = self.cache[key]["frequency"]
        new_frequency = old_frequency + 1

        self.__remove_cache_key(key, old_frequency)

        if self.frequencies[old_frequency]["whole"] == 0:
            del self.frequencies[old_frequency]

        if new_frequency not in self.frequencies:
            self.frequencies[new_frequency] = {
                "first": None,
                "end": None,
                "whole": 0
            }

        self.cache[key]["frequency"] = new_frequency

        self.__add_cache(key, new_frequency)

        if old_frequency == self.smallest:
            if old_frequency not in self.frequencies:
                self.smallest = new_frequency

    def __operation_check(self):
        self.operations += 1

        if self.operations > 200000:
            raise ValueError("Too many operations")



cache = LFUCache(2)

cache.put(1, 1)

cache.put(2,2)

print(cache.get(1))

cache.put(3,3)

print(cache.get(2))

print(cache.get(3))

cache.put(4,4)

print(cache.get(1))

print(cache.get(3))

print(cache.get(4))
