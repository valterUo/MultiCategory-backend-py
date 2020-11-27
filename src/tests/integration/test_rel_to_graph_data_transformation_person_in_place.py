import unittest

from tests.integration.common_graph_queries import count_edges, count_nodes, general_setup


class TestRelToGraphDataTransformationPersonInPlace(unittest.TestCase):

    def setUp(self):
        general_setup("person_in_place")

    def test_data_transformation_person_has_tag_edges(self):
        count = count_edges("pl_placeid_p_placeid")
        self.assertEqual(count, 3922)

    def test_data_transformation_person_has_tag_nodes(self):
        count = count_nodes()
        self.assertEqual(count, 3160)
