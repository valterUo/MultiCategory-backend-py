from logging import error
from abstract_category.functor.functor_error import FunctorError


class Functor:

    """
    The following class definition lacks the checks that the identity morphisms and
    the compositions are mapped correctly. In the current application the lack of these chekcs do not matter.
    In practice we do not need a functor between empty categories.

    In order to create a valid morphism from relational to graph, we are required to add some additional requirements to the 
    functor:
        1. the functor needs to be a full functor. This means that the function Hom(X, Y) -> Hom(FX, FY) is a surjective function between
        the Hom-sets.
        2. We require that valid transformation from relational instance to graph instance F : C -> D is such functor that if an object c belongs 
        to C and f : Fc -> d is a morphism in D, then there exists such object c' in C that Fc' = d.
      """

    def __init__(self, name, functor_info):
        self.name = name
        self.functor = functor_info["functor"]
        self.domain = functor_info["domain"]
        self.target = functor_info["target"]

        # The first requirement
        if len(self.domain) == 0:
            raise FunctorError("Domain category is empty.")
        if len(self.target) == 0:
            raise FunctorError("Target category is empty.")
        if len(self.functor) == 0:
            raise FunctorError("The mapping is not properly defined.")

        for obj in self.domain["objects"]:
            if self.functor[obj] not in self.target["objects"]:
                raise FunctorError(
                    "Functor does not map every object in the domain category to the target category")

        for mor in self.domain["morphisms"]:
            try:
                image = {"source": self.functor[mor["source"]],
                        "morphism": self.functor[mor["morphism"]], "target": self.functor[mor["target"]]}
            except KeyError:
                raise FunctorError("The image of the functor is not defined")
            if image not in self.target["morphisms"]:
                raise FunctorError(
                    "Functor does not map every morphism in the domain category to the correct morphism in the target category")

        # The second requirement
        try:
            for dom_obj in self.domain["objects"]:
                for tar_mor in self.target["morphisms"]:
                    if tar_mor["source"] == self.functor[dom_obj]:
                        if len(self.preimage(tar_mor["target"])) == 0:
                            raise FunctorError(
                                "The functor does not satisfy the second requirement.")
        except:
            raise FunctorError(
                "The functor does not satisfy the second requirement.")

    def get_name(self):
        return self.name

    def get_morphisms_of_domain_category(self):
        return self.domain["morphisms"]

    def get_functor(self):
        return {"domain_category": self.domain, "functor": self.functor, "target_category": self.target_category}

    ## In the case that the functor is a transformation from relational instance to graph instance

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
