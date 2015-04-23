#contributed by mrfesol (Tomasz Wesolowski)
"""
Different types of hashes.
Try each to choose the one that cause the least collisions (you can check it by printing DictTT.num_collisions)
Also, you can easily create one of your own!

You can read more about these hash function on:
http://www.eternallyconfuzzled.com/tuts/algorithms/jsw_tut_hashing.aspx
"""
from .HashTT import HashTT

class SimpleHashTT(HashTT):
    """
    Surprisingly - very effective for strings
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
    def before(self, key):
        return 2166136261
    def join(self, one, two):
        return (one * 16777619) ^ two
        
class OneAtATimeTT(HashTT):
    def join(self, one, two):
        one += two
        one += (one << 10)
        return one ^ (one >> 6)
    
    def after(self, key, hash):
        hash += (hash << 3)
        hash ^= (hash >> 11)
        hash += (hash << 15)
        return hash
    
class JSWHashTT(HashTT):
    def before(self, key):
        return 16777551
    def join(self, one, two):
        return (one << 1 | one >> 31) ^ two
    
class ELFHashTT(HashTT):
    def before(self, key):
        self.g = 0
        return 0
    def join(self, one, two):
        one = (one << 4) + two;
        self.g = one & 0xf0000000L;

        if self.g != 0:
            one ^= self.g >> 24

        one &= ~self.g;
        return (one << 1 | one >> 31) ^ two
    
class JenkinsHashTT(HashTT):
    """
    The most advanced hash function on the list.
    Way too many things going on to put something smart in short comment.
    """
    def mix(self, a, b, c):
        """
        Auxiliary function.
        """
        a -= b; a -= c; a ^= (c >> 13)
        b -= c; b -= a; b ^= (a << 8)
        c -= a; c -= b; c ^= (b >> 13)
        a -= b; a -= c; a ^= (c >> 12)
        b -= c; b -= a; b ^= (a << 16)
        c -= a; c -= b; c ^= (b >> 5)
        a -= b; a -= c; a ^= (c >> 3)
        b -= c; b -= a; b ^= (a << 10)
        c -= a; c -= b; c ^= (b >> 15)
        return a, b, c
    
    def before(self, key):
        self.a = self.b = 0x9e3779b9
        self.c = 0
    
    def get_hash(self, key, depth = 0):
        """
        Overridden.
        Just to create list of single elements to hash
        """
        if depth == 0:
            self.before(key)
        if type(key) is int:
            return [key]
        if type(key) is str and len(key) <= 1:
            return [key]
        tab = []
        for v in list(key):
            tab = tab + self.get_hash(v, depth+1)
        return self.compute_hash(tab)
    
    def compute_hash(self, tab):
        """
        Computes real hash
        """
        length = len(tab)
        cur = 0
        while length >= 12:
            self.a += (abs(tab[cur+0]) + (tab[cur+1] << 8) + (tab[cur+2] << 16) + (tab[cur+3] << 24))
            self.b += (tab[cur+4] + (tab[cur+5] << 8) + (tab[cur+6] << 16) + (tab[cur+7] << 24))
            self.c += (tab[cur+8] + (tab[cur+9] << 8) + (tab[cur+10] << 16) + (tab[cur+11] << 24))
    
            self.a, self.b, self.c = self.mix(self.a, self.b, self.c)
    
            cur += 12;
            length -= 12;
        
        self.c += len(tab);

        if(length == 11): self.c += (tab[cur+10] << 24);
        if(length == 10): self.c += (tab[9] << 16);
        if(length == 9): self.c += (tab[8] << 8);
        if(length == 8): self.b += (tab[7] << 24);
        if(length == 7): self.b += (tab[6] << 16);
        if(length == 6): self.b += (tab[5] << 8);
        if(length == 5): self.b += tab[4];
        if(length == 4): self.a += (tab[3] << 24);
        if(length == 3): self.a += (tab[2] << 16);
        if(length == 2): self.a += (tab[1] << 8);
        if(length == 1): self.a += tab[0];

        self.a, self.b, self.c = self.mix(self.a, self.b, self.c)

        return self.c