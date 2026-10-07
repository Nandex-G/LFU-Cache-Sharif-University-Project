class LFUCache:
    def __init__(self, capacity):
        if not 1 <= capacity <= 10000:
            raise ValueError("Capacity must be between 1 and 10,000")

        self.capacity = capacity
        self.operations = 0
        self.smallest = 1

        self.frequencies = {}
        self.cache = {}

    def get(self, key):
        self.__check_operations()

        if key not in self.cache:
            return -1

        self.__increase_frequency(key)

        return self.cache[key]["value"]

    def put(self, key, value):
        self.__check_operations()

        if key in self.cache:
            self.cache[key]["value"] = value
            return

        if len(self.cache) >= self.capacity:
            self.__remove_extra_cache()

        self.cache[key] = {
            "value": value,
            "frequency": 1,

            "previous": None,
            "next": None 
        }

        self.__add_frequency(key, 1)

        self.smallest = 1


    # ----------------------------------------------------


    def __remove_extra_cache(self):
        smallest_frequency_list = self.frequencies[self.smallest]
            
        last_frequency_key = smallest_frequency_list["last"]

        self.__remove_selected_frequency(last_frequency_key, self.smallest)
        
        del self.cache[last_frequency_key]

    def __remove_selected_frequency(self, key, frequency):
        selected_frequency_list = self.frequencies[frequency]
        previous_key = self.cache[key]["previous"]
        next_key = self.cache[key]["next"]

        if next_key == None:
            selected_frequency_list["last"] = previous_key

        else:
            self.cache[next_key]["previous"] = previous_key


        if previous_key == None:
            selected_frequency_list["first"] = next_key

        else:
            self.cache[previous_key]["next"] = next_key

        self.cache[key]["previous"] = None
        self.cache[key]["next"] = None
        
        selected_frequency_list["size"] -= 1

        if selected_frequency_list["size"] == 0:
            del self.frequencies[frequency]

    def __add_frequency(self, key, frequency):
        if frequency not in self.frequencies:
            self.frequencies[frequency] = {
                "first": None,
                "last": None, 
                "size": 0
            }

        selected_frequency_list = self.frequencies[frequency]
        old_first_frequency = selected_frequency_list["first"]

        if old_first_frequency != None:
            self.cache[old_first_frequency]["previous"] = key

        selected_frequency_list["first"] = key

        if selected_frequency_list["last"] == None:
            selected_frequency_list["last"] = selected_frequency_list["first"]
        
        self.cache[key]["next"] = old_first_frequency
        self.cache[key]["previous"] = None

        selected_frequency_list["size"] += 1

    def __increase_frequency(self, key):
        selected_key_frequency = self.cache[key]["frequency"]

        self.__remove_selected_frequency(key, selected_key_frequency)

        self.__add_frequency(key, selected_key_frequency + 1)

        new_key_frequency = self.cache[key]["frequency"] + 1

        if selected_key_frequency == self.smallest:
            if selected_key_frequency not in self.frequencies:
                self.smallest = new_key_frequency

        self.cache[key]["frequency"] = new_key_frequency

    def __check_operations(self):
        self.operations += 1

        if self.operations >= 200001:
            raise ValueError("Too many operations: you've reached the operation limit (200,000)")



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