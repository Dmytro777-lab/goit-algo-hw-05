class HashTable:
    def __init__(self, size):
        self.buckets = [[] for _ in range(size)]

    def hash_function(self, key):
        return hash(key)

    def insert(self, key, value):
        index = self.hash_function(key) % len(self.buckets)
        self.buckets[index].append((key, value))

    def delete(self, key):
        index = self.hash_function(key) % len(self.buckets)
        bucket = self.buckets[index]

        if not bucket:
            print("The key is not found")
            return None

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return v

        print("The key is not found")
        return None



ht = HashTable(10)
ht.insert("apple", 5)
ht.insert("banana", 3)

print(ht.delete("apple"))
print(ht.delete("orange"))