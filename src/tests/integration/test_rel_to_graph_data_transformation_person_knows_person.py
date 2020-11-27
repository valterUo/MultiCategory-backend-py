import unittest

from tests.integration.common_graph_queries import general_setup, count_nodes, count_edges


class TestRelToGraphDataTransformationPersonKnowsPerson(unittest.TestCase):

    def setUp(self):
        general_setup("person_knows_person")

    def test_data_transformation_person_has_tag_edges(self):
        count = count_edges("k_person2id_k_person1id")
        self.assertEqual(count, 35354)

    def test_data_transformation_person_has_tag_nodes(self):
        count = count_nodes()
        self.assertEqual(count, 1700)
