from abstract_category.functor.functor_error import FunctorError


class Functor:

    def __init__(self, name, domain_category, fun, target_category):
        self.name = name
        self.functor = fun
        try:
            for obj in domain_category["objects"]:
                if self.functor(obj) not in target_category["objects"]:
                    ## This property will be chekced again in the later loop but just in case we want more detailed error
                    raise FunctorError(
                        "Functor does not map every object in the domain category to the target category")
            for mor in domain_category["morphisms"]:
                image = {"source": self.functor(mor["source"]), "target": self.functor(mor["target"])}
                if image not in target_category["morphisms"]:
                    raise FunctorError(
                        "Functor does not map every morphism in the domain category to the correct morphism in the target category")
        except:
            raise FunctorError("Domain category, target category or functor definition are invalid.")

    def get_name(self):
        return self.name

    def get_functor(self):
        return {"domain_category": self.domain_category, "functor": self.functor, "target_category": self.target_category}
