import unittest
from functools import reduce
import json
from instance_category.objects.collection_object import CollectionObject
from multi_model_join.relational_join import join_relational_relational_over_functional_morphism, join_relational_relational_over_nonfunctional_morphism, join_relational_xml
from instance_category.morphisms.morphism import Morphism
from multi_model_join.help_functions import add_to_dict
import initialize_demo_datasets.initialize_ecommerce as commerce

commerce.init()
objects = commerce.e_commerce_instance.get_objects()
morphisms = commerce.e_commerce_instance.get_morphisms()

class TestRelationalJoin(unittest.TestCase):

    def test_relational_join_relational_functional(self):
        with open('relational_test_result.json', 'r') as openfile: 
            result_file = json.load(openfile)
        result = result_file[1].get("result")
        joined_tables = join_relational_relational_over_functional_morphism(
            objects["sites_table"], morphisms["site_located"], objects["locations_table"])
        self.assertEqual(result, str(joined_tables.getCollection()))


    def test_relational_join_relational_nonfunctional(self):
        with open('relational_test_result.json', 'r') as openfile: 
            result_file = json.load(openfile)
        result = result_file[2].get("result")
        joined_tables = join_relational_relational_over_nonfunctional_morphism(
            objects["locations_table"], morphisms["sites_in_location"], objects["sites_table"])
        self.assertEqual(result, str(joined_tables.getCollection()))


    def test_relational_join_xml_twig1(self):
        join_result = join_relational_xml(objects["customers_table"], morphisms["customer_ordered"], objects["orders_xml"], [
                                          "name", "locationId", "Order_no"])
        with open('relational_test_result.json', 'r') as openfile: 
            result_file = json.load(openfile)
        result = result_file[0].get("result")
        self.assertEqual(result, str(join_result.getCollection()))


    def test_relational_join_xml_twig2_attribute_not_existing(self):
        join_result = join_relational_xml(objects["customers_table"], morphisms["customer_ordered"], objects["orders_xml"], [
                                          "name", "locationid", "Order_no"])
        with open('relational_test_result.json', 'r') as openfile: 
            result_file = json.load(openfile)
        result = result_file[3].get("result")
        self.assertEqual(result, str(join_result.getCollection()))


    def test_relational_join_xml_twig3_multiple_attributes_from_xml_doc(self):
        join_result = join_relational_xml(objects["customers_table"], morphisms["customer_ordered"], objects["orders_xml"], [
                                          "name", "locationId", "Order_no", "Product_Name"])
        with open('relational_test_result.json', 'r') as openfile: 
            result_file = json.load(openfile)
        result = result_file[4].get("result")
        self.assertEqual(result, str(join_result.getCollection()))

if __name__ == '__main__':
    unittest.main()
