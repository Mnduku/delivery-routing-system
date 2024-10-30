# Replica of a Hash table Data structure
# For use in the delivery service program
# Will hold all packages
class HashTable:
    
    #Initilization function
    def __init__(self, items=None, load_factor=0.75):
        if items is None: 
            self.size = 0 
            self.max = 10
        else:
            self.size = len(items)
            self.max = self.findmax(len(items), load_factor)

        self.load_factor = load_factor
        self.table = [[] for _ in range(self.max)]

        if items is not None:
            for key, value in items:
                self._insert(key, value)


    # Returns a hash value for a key. O(1)
    def hasher(self, key):
        return hash(key) % self.max
    
    # Calculates the capacity for the hashtable
    def findmax(self, itemcount, load_factor):
        mincap = itemcount / load_factor
        capacity = 1
        while capacity < mincap:
            capacity *= 2
        return capacity

    # Resizes the Hash table O(n) complexity 
    # Creates new table with *2 size and transfers all data
    def resize(self):
        new_max = self.max * 2
        new_hashtable = [[] for _ in range(new_max)]
        for bucket in self.table:
            for key, value in bucket:
                index = self.hasher(key)
                new_hashtable[index].append([key, value])
        self.table = new_hashtable
        self.max = new_max

    # The set method adds a key-value pair to the hashtable. If the key already exists in the hashtable,
    # it updates the value. The average time complexity of this method is O(1).
    # If size after insertion is greater then max, hashtable will be resized
    def _insert(self, key, value):
        index = self.hasher(key)
        bucket = self.table[index]
        for i, pair in enumerate(bucket):
            x = pair[0]
            if key == x:
                bucket[i] = [key, value]
                return
        bucket.append([key, value])
        self.size += 1
        if self.size > self.max * self.load_factor:
            self.resize()

    # Finds a value in the table using a key
    # O(1) complexity because
    def _get(self, key):
        index = self.hasher(key)
        bucket = self.table[index]
        for i, pair in enumerate(bucket):
            k, v = pair
            if key == k:
                return v
        return None

    # The delete method removes the key-value pair from the hashtable based on the provided key.
    # The average time complexity is O(1) since there is only one key per bucket
    def delete(self, key):
        hash_index = self.hasher(key)
        bucket = self.table[hash_index]
        for i, pair in enumerate(bucket):
            k = pair[0]
            if key == k:
                del bucket[i]
                self.size -= 1
                return True
        return False

    # Returns string representation of table
    # O(n) since concatenating all elements
    def show(self):
        result = ""
        for i, bucket in enumerate(self.table):
            for pair in bucket:
                v = pair[1]
                result += f"Bucket {i} contains a package with the ID: {v.pid} \n"
        return result
