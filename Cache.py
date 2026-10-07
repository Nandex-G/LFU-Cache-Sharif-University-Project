class LFUCache:
    def __init__ (self, capacity):
        if not 1 <= capacity <= 10000:
            raise ValueError("Capacity must be between 1 and 10,000")
        
        self.cache = {}
        self.capacity = capacity
        self.operations = 0
        self.frequencies = {}
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
            "last": self.operations
        }

        if 1 not in self.frequencies:
            self.frequencies[1] = []

        self.frequencies[1].append(key)
        self.smallest = 1

    def __remove_cache(self):
        smallest_keys = self.frequencies[self.smallest].copy()

        del self.cache[smallest_keys[0]]   
        self.frequencies[self.smallest].remove(smallest_keys[0])
        
        if len(smallest_keys) == 1:
            del self.frequencies[self.smallest]

    def __increase_frequency(self, key):
        old_frequency = self.cache[key]["frequency"]
        new_frequency = self.cache[key]["frequency"] + 1

        self.frequencies[old_frequency].remove(key)

        if len(self.frequencies[old_frequency]) == 0:
            del self.frequencies[old_frequency] 

        if new_frequency not in self.frequencies:
            self.frequencies[new_frequency] = []

        if len(self.frequencies[new_frequency]) >= 1:
            if self.cache[self.frequencies[new_frequency][0]]["last"] > self.cache[key]["last"]:
                self.frequencies[new_frequency].insert(0, key)
            else:
                self.frequencies[new_frequency].append(key)
        else:
            self.frequencies[new_frequency].append(key)

        self.cache[key]["frequency"] = new_frequency

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
