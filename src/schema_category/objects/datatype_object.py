class DatatypeObject:

    def __init__(self, name, typeVar, incoming_morphisms = [], outgoing_morphisms = []):
        self.name = name
        self.typeVar = typeVar
        self.incoming_morphisms = incoming_morphisms
        self.outgoing_morphisms = outgoing_morphisms

    def __eq__(self, other):
        return self.name == other.name
    
    def __str__(self):
        return self.name

    def add_incoming_morphism(self, morphism):
        self.incoming_morphisms.append(morphism)

    def add_outgoing_morphism(self, morphism):
        self.outgoing_morphisms.append(morphism)