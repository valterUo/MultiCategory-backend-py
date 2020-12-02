import unittest
from tables import *
from multi_model_join.multi_model_join import MultiModelJoin
from multicategory.initialize_multicategory import multicategory


class TestPatentMultiModelJoin(unittest.TestCase):

    def setUp(self):
        self.db = multicategory.get_multi_model_db(
            "Patent multi-model database")

    def test_site_join_location(self):
        patent = self.db.get_objects()["patent"]
        category = self.db.get_objects()["category"]
        morphism = self.db.get_morphisms()["patent_to_category_morphism"]
        join1 = MultiModelJoin(patent, morphism, category)

    def test_customer_join_location(self):
        citation_graph = self.db.get_objects()["citation"]
        patent = self.db.get_objects()["patent"]
        morphism = self.db.get_morphisms()["citation_to_patent_morphism"]
        join2 = MultiModelJoin(citation_graph, morphism, patent, True)
