#contributed by mrfesol (Tomasz Wesolowski)

class HashTT:
    """ 
        Base Class for various types of hashes
    """    
    
    def __init__(self):
        self.modulo = 1024 #default value
        
    def before(self, key):
        """
        Returns initial value of hash.
        It's also the place where you can initialize some auxiliary variables
        """
        return 0
    
    def after(self, key, hash):
        """
        Returns final value of hash
        """
        return hash
        
    def get_hash(self, key, depth = 0):
        """
        Recursively computes a hash
        """
        ret_hash = self.before(key)
        if type(key) is int:
            return self.hash_int(key)
        if type(key) is str and len(key) <= 1:
            return self.hash_char(key)
        for v in list(key):
            ret_hash = self.join(ret_hash, self.get_hash(v, depth+1)) % self.modulo
        if depth == 0:
            ret_hash = self.after(key, ret_hash)
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