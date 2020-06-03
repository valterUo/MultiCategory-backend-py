import unittest
import networkx as nx
from multi_model_join.graph_join.graph_join import join_graph_graph, join_graph_relational
from instance_category.objects.collection_object import CollectionObject
import initialize_demo_datasets.initialize_ecommerce as commerce

commerce.init()
objects = commerce.e_commerce_instance.get_objects()
morphisms = commerce.e_commerce_instance.get_morphisms()

customer1 = frozenset(
    {('id', '14'), ('locationId', '15'), ('creditLimit', '2900'), ('name', 'Lucas')})
customer2 = frozenset(
    {('locationId', '11'), ('name', 'David'), ('id', '23'), ('creditLimit', '1245')})
customer3 = frozenset(
    {('id', '7'), ('creditLimit', '9999'), ('locationId', '10'), ('name', 'Bob')})
customer4 = frozenset(
    {('name', 'Hannah'), ('creditLimit', '7458'), ('id', '16'), ('locationId', '16')})

interest1 = frozenset(
    {('locationId', '13'), ('topic', 'pottery'), ('id', 'I3')})
interest2 = frozenset(
    {('locationId', '15'), ('topic', 'volunteering'), ('id', 'I5')})
interest3 = frozenset(
    {('locationId', '16'), ('id', 'I6'), ('topic', 'dancing')})


class TestGraphJoin(unittest.TestCase):

    def test_graph_join_graph_pattern1(self):
        gluing_graph = nx.DiGraph()
        gluing_graph.add_edge(0, 1)

        customerGraph1 = nx.DiGraph()
        customerGraph1.add_nodes_from([customer1])

        customerGraph2 = nx.DiGraph()
        customerGraph2.add_nodes_from([customer4])

        instanceObject1 = CollectionObject(
            "customers1", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph1)
        instanceObject2 = CollectionObject(
            "customers2", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph2)

        def morphism_induced_by_function(customer1, customer2): return True if dict(
            customer1).get("creditLimit") > dict(customer2).get("creditLimit") else False

        join_graph = join_graph_graph(
            instanceObject1, morphism_induced_by_function, instanceObject2, gluing_graph)

        resultGraph = nx.DiGraph()
        resultGraph.add_edges_from([(customer4, customer1)])

        for edge in resultGraph.edges:
            if edge not in join_graph.get_collection().edges:
                self.assertFalse(False)
        else:
            for edge in join_graph.get_collection().edges:
                if edge not in resultGraph.edges:
                    self.assertFalse(False)
            else:
                self.assertTrue(True)


    def test_graph_join_empty_relation(self):
        gluing_graph = nx.DiGraph()
        gluing_graph.add_edge(0, 1)

        customerGraph1 = nx.DiGraph()
        customerGraph1.add_nodes_from([customer1])

        customerGraph2 = nx.DiGraph()
        customerGraph2.add_nodes_from([customer4])

        instanceObject1 = CollectionObject(
            "customers1", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph1)
        instanceObject2 = CollectionObject(
            "customers2", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph2)

        def morphism_induced_by_function(customer1, customer2): return True if dict(
            customer1).get("creditLimit") == dict(customer2).get("creditLimit") else False

        join_graph = join_graph_graph(
            instanceObject1, morphism_induced_by_function, instanceObject2, gluing_graph)

        resultGraph = nx.DiGraph()
        resultGraph.add_nodes_from([customer1])

        for edge in resultGraph.edges:
            if edge not in join_graph.get_collection().edges:
                self.assertFalse(False)
        else:
            for edge in join_graph.get_collection().edges:
                if edge not in resultGraph.edges:
                    self.assertFalse(False)
            else:
                self.assertTrue(True)


    def test_graph_join_graph_with_single_node_pattern_simple(self):
        gluing_graph = nx.DiGraph()
        gluing_graph.add_node(0)

        customerGraph1 = nx.DiGraph()
        customerGraph1.add_nodes_from([customer1])

        customerGraph2 = nx.DiGraph()
        customerGraph2.add_nodes_from([customer4])

        instanceObject1 = CollectionObject(
            "customers1", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph1)
        instanceObject2 = CollectionObject(
            "customers2", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph2)

        def morphism_induced_by_function(customer1, customer2): return True if dict(
            customer1).get("creditLimit") < dict(customer2).get("creditLimit") else False

        join_graph = join_graph_graph(
            instanceObject1, morphism_induced_by_function, instanceObject2, gluing_graph)

        resultGraph = nx.DiGraph()
        resultGraph.add_nodes_from([frozenset({customer1, customer4})])

        for edge in resultGraph.edges:
            if edge not in join_graph.get_collection().edges:
                self.assert_(False, edge)
        else:
            for edge in join_graph.get_collection().edges:
                if edge not in resultGraph.edges:
                    self.assert_(False, edge)
            else:
                self.assertTrue(True)


    def test_graph_join_graph_with_single_node_pattern_advanced(self):
        gluing_graph = nx.DiGraph()
        gluing_graph.add_node(0)

        customerGraph1 = nx.DiGraph()
        customerGraph1.add_edges_from(
            [(customer1, customer2), (customer2, customer3), (customer3, customer4), (customer4, customer1)])

        customerGraph2 = nx.DiGraph()
        customerGraph2.add_edges_from(
            [(customer1, interest1), (customer2, interest2), (customer1, interest3), (customer2, interest3)])

        instanceObject1 = CollectionObject(
            "customers1", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph1)
        instanceObject2 = CollectionObject(
            "customers2", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph2)

        def morphism_induced_by_function(
            customer, customer_or_interest): return True if customer == customer_or_interest else False

        join_graph = join_graph_graph(
            instanceObject1, morphism_induced_by_function, instanceObject2, gluing_graph)

        self.assertEqual(join_graph.get_collection().edges(), nx.compose(customerGraph1, customerGraph2).edges())


    def test_graph_join_relational_with_functional_morphism(self):

        join_graph = join_graph_relational(objects["customersGraph"], morphisms["located"], objects["locations_table"])


    # def test_graph_join_xml(self):
    #     self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
