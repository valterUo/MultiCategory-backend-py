import unittest

from tests.integration.common_graph_queries import count_edges, count_nodes, general_setup


class TestRelToGraphDataTransformationPersonHasTag(unittest.TestCase):

    def setUp(self):
        general_setup("person_has_tag")

    def test_data_transformation_person_has_tag_edges(self):
        count = count_edges("pt_tagid_pt_personid")
        self.assertEqual(count, 39170)

    def test_data_transformation_person_has_tag_nodes(self):
        count = count_nodes()
        self.assertEqual(count, 17780)
