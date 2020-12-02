import unittest
from tables import *
from multi_model_join.multi_model_join import MultiModelJoin
from multicategory.initialize_multicategory import multicategory

class TestECommerceMultiModelJoin(unittest.TestCase):

    def setUp(self):
        self.db = multicategory.get_multi_model_db("E-commerce multi-model database")

    def test_site_join_location(self):
        site = self.db.get_objects()["site"]
        location = self.db.get_objects()["location"]
        site_to_location_morphism = self.db.get_morphisms()["site_to_location_morphism"]

        join1 = MultiModelJoin(site, site_to_location_morphism, location)

    def test_customer_join_location(self):
        customer_graph = self.db.get_objects()["customer"]
        location = self.db.get_objects()["location"]
        customer_to_location_morphism = self.db.get_morphisms()["customer_to_location_morphism"]

        join2 = MultiModelJoin(customer_graph, customer_to_location_morphism, location, True)

    def test_customer_join_interest(self):
        customer_graph = self.db.get_objects()["customer"]
        interest_graph = self.db.get_objects()["interest"]
        customer_interest_morphism = self.db.get_morphisms()["customer_interest_morphism"]

        join3 = MultiModelJoin(customer_graph, customer_interest_morphism, interest_graph, True, True)

    def test_location_join_customer(self):
        location = self.db.get_objects()["location"]
        customer_graph = self.db.get_objects()["customer"]
        location_to_customer_morphism = self.db.get_morphisms()["location_to_customer_morphism"]

        description = dict()
        description["customer_id"] = StringCol(64, dflt='NULL')
        description["name"] = StringCol(64, dflt='NULL')
        description["creditLimit"] = StringCol(64, dflt='NULL')
        description["customer_locationId"] = StringCol(64, dflt='NULL')

        join4 = MultiModelJoin(location, location_to_customer_morphism, customer_graph, second_description = description)

    def test_join_over_composition(self):
        orders = self.db.get_objects()["orders"]
        customer_graph = self.db.get_objects()["customer"]
        composition_order_to_customer = self.db.get_morphisms()["composition_order_to_customer"]

        join5 = MultiModelJoin(orders, composition_order_to_customer, customer_graph, tree_attributes=["Orders"])