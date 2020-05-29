class SchemaCategory:

    def __init__(self, name, objects, morphisms):
        self.name = name
        self.objects = objects
        self.morphisms = morphisms
    
    def __str__(self):
        allmorphisms = ""
        for morphism in self.morphisms.values():
            allmorphisms += str(morphism) + "\n"
        return allmorphisms

    def add_morphism(self, morphism):
            self.objects.add(morphism.sourceObject)
            self.objects.add(morphism.targetObject)
            self.morphisms.add(morphism)

    def add_object(self, obj):
        self.objects.add(obj)

    def contains_object(self, obj):
        return self.objects.contains(obj)

    def get_name(self):
        return self.name
                