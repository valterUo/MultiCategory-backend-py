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

    def get_d3js_graph(self):
        graph = dict()
        graph["nodes"] = list(map(lambda x : x.get_d3js_element(), list(self.objects.values())))
        print(graph["nodes"])
        graph["links"] = []
        for morphism in self.morphisms.values():
            link = {'name': morphism.get_name()}
            source_name = morphism.get_source_object_name()
            target_name = morphism.get_target_object_name()
            for i in range(len(graph["nodes"])):
                if graph["nodes"][i]['name'] == source_name:
                    link['source'] = i
                if graph["nodes"][i]['name'] == target_name:
                    link['target'] = i
            graph["links"].append(link)
        return graph
                