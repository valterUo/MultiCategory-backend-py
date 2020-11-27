import unittest

from tests.integration.common_graph_queries import count_edges, count_nodes, general_setup


class TestRelToGraphDataTransformationTagHasSubtag(unittest.TestCase):

    def setUp(self):
        general_setup("tag_has_subtag")

    def test_data_transformation_person_has_tag_edges(self):
        count = count_edges("tc_tagclassid_tc_subclassoftagclassid")
        self.assertEqual(count, 70)

    def test_data_transformation_person_has_tag_nodes(self):
        count = count_nodes()
        self.assertEqual(count, 71)
