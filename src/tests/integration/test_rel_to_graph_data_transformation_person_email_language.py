import unittest

from tests.integration.common_graph_queries import count_edges, count_nodes, general_setup


class TestRelToGraphDataTransformationPersonEmailLanguage(unittest.TestCase):

    def setUp(self):
        general_setup("person_email_language")

    def test_data_transformation_person_has_tag_edges(self):
        count = count_edges("p_personid_plang_personid")
        self.assertEqual(count, 3771)

    def test_data_transformation_person_has_tag_nodes(self):
        count = count_nodes()
        self.assertEqual(count, 9161)
