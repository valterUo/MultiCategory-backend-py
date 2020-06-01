import unittest
import initialize_demo_datasets.initialize_ecommerce as commerce
from instance_functor.instance_functor import InstanceFunctor
import os
from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism

dirname = os.path.dirname(__file__)
orders_xml_path = os.path.join(
    dirname, "..\\data\\eCommerce\\orders.xml")
commerce.init()
objects = commerce.e_commerce_instance.get_objects()
morphisms = commerce.e_commerce_instance.get_morphisms()
functor = InstanceFunctor(commerce.e_commerce_instance)


class TestInstanceFunctor(unittest.TestCase):

    def test_instance_functor_maps_object_right(self):
        orders_xml = CollectionObject(
            "orders_xml", "XML", "order", lambda document: document.getroot(), {"filePath": orders_xml_path})
        mapped_element = functor.instance_map(orders_xml)
        self.assertEqual(mapped_element.get_name(), "orders_xml")

    def test_instance_functor_maps_morphism_right(self):
        customers = Morphism("customers", objects["customers_graph"],
                             lambda customer: dict(customer), objects["customers_table"], True)
        self.assertEqual(functor.instance_map(
            customers).get_name(), "customers")

    def test_instance_functor_maps_key1_right(self):
        schema_object = functor.instance_map("customers_graph")
        self.assertEqual(schema_object.get_name(), "customers_graph")

    def test_instance_functor_maps_key2_right(self):
        schema_morphism = functor.instance_map("knows")
        self.assertEqual(schema_morphism.get_name(), "knows")


if __name__ == '__main__':
    unittest.main()
