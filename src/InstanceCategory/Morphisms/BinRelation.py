class BinaryRelation:


    def __init__(self, A, B):
        self.relation = set()
        for a in A:
            for b in B:
                self.relation.add((a,b))
    

    def compose(self, relation):
        compositionRelation = set()
        for (a,b) in self.relation:
            for (c,d) in relation.relation:
                if b == c:
                    compositionRelation.add((a,d))
                    break
        return compositionRelation
