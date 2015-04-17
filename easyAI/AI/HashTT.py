#contributed by mrfesol (Tomasz Wesolowski)

class HashTT:
    """ 
        Base Class for various types of hashes
    """    
    
    def __init__(self):
        self.modulo = 1024 #default value
        self.initial_value = 0 #initial hash value
        
    def get_hash(self, key):
        """
        Recursively computes a hash
        """
        ret_hash = self.initial_value
        if type(key) is int:
            return self.hash_int(key)
        if type(key) is str and len(key) <= 1:
            return self.hash_char(key)
        for v in list(key):
            ret_hash = self.join(ret_hash, self.get_hash(v)) % self.modulo
        return ret_hash
    
    def hash_int(self, number):
        """
        Returns hash for a number
        """
        return number
    
    def hash_char(self, string):
        """
        Returns hash for an one-letter string
        """
        return ord(string) 
    
    def join(self, one, two):
        """
        Returns combined hash from two hashes
        one - existing (combined) hash so far
        two - hash of new element
        one = join(one, two)
        """
        return (one * two) % self.modulo
    
"""
Different types of hashes.
Try each to choose the one that cause the least collisions (you can check it by printing DictTT.num_collisions)
Also, you can easily create one of your own!
"""

class SimpleHashTT(HashTT):
    """
    Suprisingly - very effective for strings
    """
    def join(self, one, two):
        return 101 * one  +  two

class XorHashTT(HashTT):
    def join(self, one, two):
        return one ^ two
    
class AddHashTT(HashTT):
    def join(self, one, two):
        return one  +  two
    
class RotateHashTT(HashTT):
    def join(self, one, two):
        return (one << 4) ^ (one >> 28) ^ two
    
class BernsteinHashTT(HashTT):
    def join(self, one, two):
        return 33 * one + two
    
class ShiftAndAddHashTT(HashTT):
    def join(self, one, two):
        return one ^ (one << 5) + (one >> 2) + two
    
class FNVHashTT(HashTT):
    def __init__(self):
        self.initial_value = 2166136261
    def join(self, one, two):
        return (one * 16777619) ^ two