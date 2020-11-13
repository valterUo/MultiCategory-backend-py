from abstract_category.functor.functor_error import FunctorError


class Functor:

    def __init__(self, name, dom, fun, tar):
        self.name = name
        self.functor = fun
        self.domain = dom
        self.target = tar
        print(dom, fun, tar)
        if len(self.domain) == 0:
            raise FunctorError("Domain category is empty.")
        if len(self.target) == 0:
            raise FunctorError("Target category is empty.")
        if len(self.functor) == 0:
            raise FunctorError("The mapping is not properly defined.")
        try:
            for obj in dom["objects"]:
                if self.functor[obj] not in tar["objects"]:
                    raise FunctorError(
                        "Functor does not map every object in the domain category to the target category")
            for mor in dom["morphisms"]:
                image = {"source": self.functor[mor["source"]],
                         "morphism": self.functor[mor["morphism"]], "target": self.functor[mor["target"]]}
                if image not in tar["morphisms"]:
                    raise FunctorError(
                        "Functor does not map every morphism in the domain category to the correct morphism in the target category")
        except:
            raise FunctorError(
                "Domain category, target category or functor definition are invalid.")

    def get_name(self):
        return self.name

    def get_morphisms_of_domain_category(self):
        return self.domain["morphisms"]

    def get_functor(self):
        return {"domain_category": self.domain, "functor": self.functor, "target_category": self.target_category}

## In the case that the functor is about transformation from relational instance to graph instance

    def get_tables_to_nodes(self):
        return self.preimage("nodes")

    def get_tables_to_edges(self):
        return self.preimage("edges")

    def get_edge_source(self):
        return self.preimage("source")

    def get_edge_target(self):
        return self.preimage("target")

    def preimage(self, element):
        result = []
        for key in self.functor.keys():
            if self.functor[key] == element:
                result.append(key)
        return result
