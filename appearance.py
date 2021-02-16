class Appearance:
    def __init__(self,doc,freq):
        self.doc = doc;
        self.freq = freq;
        self.score = 0; #idfscore