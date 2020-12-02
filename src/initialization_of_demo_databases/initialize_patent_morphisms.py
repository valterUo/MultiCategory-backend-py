from category_of_collection_constructor_functors.collection_constructor_morphism import CollectionConstructorMorphism
from category_of_collection_constructor_functors.collections.collection_relationship import CollectionRelationship
from category_of_collection_constructor_functors.model_categories.model_relationship import ModelRelationship
from constructing_multi_model_db.collection_constructor.create_collection_constructor_morphism import create_collection_constructor_morphisms
from supportive_functions.row_manipulations import row_to_dictionary


def initialize_patent_morphisms(objects):
    patent_morphisms_config = []

    # Each node in the citation graph is functionally in a relationship with a unique row in the patent table: PATENTID  in graph nodes --> PATENT in patent table

    def fun(graph_elem, patent):
        result = []
        condition = "PATENT == b'" + str(graph_elem[0]) + "'"
        if len(graph_elem) == 3:
            return result
        else:
            #print(patent_collection.get_collection().get_table().will_query_use_indexing(condition))
            for patent_row in patent.get_collection().get_table().where(condition):
                result.append(row_to_dictionary(patent_row))
            return result

    patent_morphisms_config.append({'name': 'citation_patent_model_relationship',
                                    'source': 'citation',
                                    'target': 'patent',
                                    'modelRelationship': [{"PATENTID": "PATENT"}],
                                    'lambda': lambda graph_elem: fun(graph_elem, objects["patent"]),
                                    })

    patent_morphisms_config.append({'name': 'inventor_to_patent_morphism',
                                    'source': 'inventor',
                                    'target': 'patent',
                                    'modelRelationship': [{"PATENT": "PATENT"}],
                                    'lambda': lambda inventor_row: [x for x in objects["patent"].get_collection().get_rows() if x['PATENT'] == inventor_row["PATENT"]]
                                    })

    patent_morphisms_config.append({'name': 'patent_to_assignee_morphism',
                                    'source': 'patent',
                                    'target': 'assignee',
                                    'modelRelationship': [{"ASSIGNEE": "ASSIGNEE"}],
                                    'lambda': lambda patent_row: [x for x in objects["assingee"].get_collection().get_rows() if x['ASSIGNEE'] == patent_row["ASSIGNEE"]]
                                    })

    patent_morphisms_config.append({'name': 'patent_to_class_morphism',
                                    'source': 'patent',
                                    'target': 'class',
                                    'modelRelationship': [{"NCLASS": "CLASS"}],
                                    'lambda': lambda patent_row: [x for x in objects["class"].get_collection().get_rows() if x['CLASS'] == patent_row["NCLASS"]]
                                    })

    patent_morphisms_config.append({'name': 'patent_to_category_morphism',
                                    'source': 'patent',
                                    'target': 'category',
                                    'modelRelationship': [{"CAT": "CAT"}],
                                    'lambda': lambda patent_row: [x for x in objects["category"].get_collection().get_rows() if x['CAT'] == patent_row["CAT"]]
                                    })

    patent_morphisms_config.append({'name': 'patent_to_subcategory_morphism',
                                    'source': 'patent',
                                    'target': 'category',
                                    'modelRelationship': [{"SUBCAT": "CAT"}],
                                    'lambda': lambda patent_row: [x for x in objects["category"].get_collection().get_rows() if x['CAT'] == patent_row["SUBCAT"]]
                                    })

    morphisms = create_collection_constructor_morphisms(
        patent_morphisms_config, objects)
    return morphisms
