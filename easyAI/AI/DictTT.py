#contributed by mrfesol (Tomasz Wesolowski)
from easyAI.AI.HashTT import HashTT

class DictTT:
    """
    A DictTT implements custom dictionary,
    which can be used with transposition tables.
    """
    def __init__(self, num_buckets=1024, own_hash = None):
        """
        Initializes a dictionary with the given number of buckets.
        """
        self.dict = []
        for i in range(num_buckets):
            self.dict.append((None, None))
        self.keys = dict()
        self.hash = hash
        if own_hash != None:
            own_hash.modulo = len(self.dict)
            self.hash = own_hash.get_hash
        self.num_collisions = 0
        self.num_calls = 0
    
    def hash_key(self, key):
        """
        Given a key this will create a number and then convert it to
        an index for the dict.
        """
        self.num_calls += 1
        return self.hash(key) % len(self.dict)
    
    def get_slot(self, key, default=None):
        """
        Returns the index, key, and value of a slot found in the dict.
        Returns -1, key, and default (None if not set) when not found.
        """
        slot = self.hash_key(key)
        
        if key == self.dict[slot][0]:
            return slot, self.dict[slot][0], self.dict[slot][1]
    
        return -1, key, default
    
    def get(self, key, default=None):
        """
        Gets the value for the given key, or the default.
        """        
        i, k, v = self.get_slot(key, default=default)
        return v
    
    def set(self, key, value):
        """
        Sets the key to the value, replacing any existing value.
        """
        slot = self.hash_key(key)
        
        if self.dict[slot] != (None, None):
            self.num_collisions += 1 #collision occured
                
        self.dict[slot] = (key, value)
     
        if self.keys.__contains__(key):
            self.keys[key] = self.keys[key] + 1
        else:
            self.keys[key] = 1
    
    def delete(self, key):
        """
        Deletes the given key from the dictionary.
        """
        
        slot = self.hash_key(key)
        self.dict[slot] = (None, None)
            
        if self.keys.__contains__(key):
            self.keys[key] = self.keys[key] - 1
            if self.keys[key] <= 0:
                del self.keys[key]
                
    def collisions(self):
        return self.num_collisions
                    
    def __getitem__(self, key):
        return self.get(key)
    
    def __missing__(self, key):
        return None
    
    def __setitem__(self, key, value):
        self.set(key, value)
        
    def __delitem__(self, key):
        self.delete(key)
        
    def __iter__(self):
        return iter(self.keys)
        
    def __contains__(self, key):
        return self.keys.__contains__(key)
        