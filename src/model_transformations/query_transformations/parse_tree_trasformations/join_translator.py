class JoinTranslator:

    def __init__(self, data_transformation_functor = "default"):
        self.functor = data_transformation_functor
        self.joins = []

    def add_join(self, join):
        self.joins.append(join)
        if self.analyze_joins():
            return True
        else:
            return False

    def analyze_joins(self, joins):
        self.joins += joins
