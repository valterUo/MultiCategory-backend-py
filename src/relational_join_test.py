import unittest
from functools import reduce
from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.Morphism import Morphism
from src.multi_model_join.help_functions import add_to_dict
from src.multi_model_join.relational_join import *


class TestRelationalJoin(unittest.TestCase):

    locationsTable = CollectionObject("locations", "relational", "location", lambda table: table, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\locationsTable.csv",
                                                                                                   "fileformat": "csv", "schema": ["id", "address", "city", "zipCode", "country"], "keyAttribute": "id", "separator": ";"})

    sitesTable = CollectionObject("sites", "relational", "site", lambda table: table, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\sites.csv",
                                                                                       "fileformat": "csv", "schema": ["id", "locationId", "name", "year", "description"], "keyAttribute": "id", "separator": ";"})

    siteLocated = Morphism("siteLocated", sitesTable,
                           lambda site: locationsTable.getCollection().get(site.get("locationId")), locationsTable, True)

    sitesInLocation = Morphism("sitesInLocation", locationsTable, lambda location: reduce(lambda xs, x: add_to_dict(
        xs, x, sitesTable.getCollection()[x]) if sitesTable.getCollection()[x].get("locationId") == location.get("id") else xs, sitesTable.getCollection(), dict()), sitesTable)

    orderToCustomerKeyValuePairs = CollectionObject(
        "orderToCustomerKeyValuePairs", "JSON", "pairs", lambda json: json, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\src\\keyValuePairs.json"})

    ordersXML = CollectionObject(
        "orders", "XML", "order", lambda document: document.getroot(), {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\orders.xml"})

    customersTable = CollectionObject(
        "customersTable", "relational", "customer")


    def test_relational_join_xml_twig1(self):
        def findFromOrders(customer):
            result = []
            for elem in ordersXML.getCollection().getroot():
                if orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text) == int(customer.get("id")):
                    result.append(elem)
            return result

        customerOrdered = Morphism(
            "customerOrdered", customersTable, lambda customer: findFromOrders(customer), ordersXML)

        result = [{'name': 'Mary', 'locationId': '14', 'Order_no': '3qqqeq9'},
                  {'name': 'Nora', 'locationId': '12', 'Order_no': 'null'},
                  {'name': 'John', 'locationId': '10', 'Order_no': '34e5e79'},
                  {'name': 'John', 'locationId': '10', 'Order_no': '4dwtfuu'},
                  {'name': 'Mill', 'locationId': '11', 'Order_no': '4839fh'},
                  {'name': 'Alice', 'locationId': '12', 'Order_no': '77idy65'},
                  {'name': 'William', 'locationId': '13', 'Order_no': '0cbdf508'},
                  {'name': 'Erica', 'locationId': '16', 'Order_no': 'ery63rg'},
                  {'name': 'William', 'locationId': '15', 'Order_no': 'null'},
                  {'name': 'Bob', 'locationId': '10', 'Order_no': 'reuihf54'},
                  {'name': 'Isabella', 'locationId': '14', 'Order_no': 'null'},
                  {'name': 'Olivia', 'locationId': '13', 'Order_no': 'null'},
                  {'name': 'Adrian', 'locationId': '13', 'Order_no': 'null'},
                  {'name': 'David', 'locationId': '11', 'Order_no': 'null'},
                  {'name': 'Charles', 'locationId': '10', 'Order_no': 'null'},
                  {'name': 'Benjamin', 'locationId': '16', 'Order_no': 'null'},
                  {'name': 'Lucas', 'locationId': '14', 'Order_no': 'null'},
                  {'name': 'Ava', 'locationId': '10', 'Order_no': 'null'},
                  {'name': 'Aaron', 'locationId': '14', 'Order_no': 'null'},
                  {'name': 'Alexander', 'locationId': '10', 'Order_no': 'null'},
                  {'name': 'Hannah', 'locationId': '16', 'Order_no': 'null'},
                  {'name': 'Max', 'locationId': '13', 'Order_no': 'null'},
                  {'name': 'Lucas', 'locationId': '15', 'Order_no': 'null'},
                  {'name': 'Lucy', 'locationId': '10', 'Order_no': 'null'},
                  {'name': 'Julia', 'locationId': '14', 'Order_no': 'null'},
                  {'name': 'David', 'locationId': '11', 'Order_no': 'null'},
                  {'name': 'Charlotte', 'locationId': '14', 'Order_no': 'null'}]

        join_result = join_relational_xml(customersTable, customerOrdered, ordersXML, [
                                          "name", "locationId", "Order_no"])

        self.assertListEqual(result, join_result.getCollection())

    def test_relational_join_relational_functional(self):

        joined_tables = join_relational_relational_over_functional_morphism(
            sitesTable, siteLocated, locationsTable)

    def test_relational_join_relational_nonfunctional(self):

        joined_tables = join_relational_relational_over_nonfunctional_morphism(
            locationsTable, sitesInLocation, sitesTable)
