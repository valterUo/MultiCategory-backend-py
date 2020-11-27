def tested_functors():
    functors = dict()

    functors["person_has_tag"] = {'domain': {'objects': ['person', 'tag', 'person_tag'], 'morphisms': [{'source': 'person_tag', 'morphism': ('pt_tagid', 't_tagid'), 'target': 'tag'}, {'source': 'person_tag', 'morphism': ('pt_personid', 'p_personid'), 'target': 'person'}]}, 'functor': {
        'person': 'nodes', 'tag': 'nodes', 'person_tag': 'edges', ('pt_tagid', 't_tagid'): 'source', ('pt_personid', 'p_personid'): 'target'}, 'target': {'objects': ['nodes', 'edges'], 'morphisms': [{'source': 'edges', 'morphism': 'source', 'target': 'nodes'}, {'source': 'edges', 'morphism': 'target', 'target': 'nodes'}]}}

    functors["person_knows_person"] = {'domain': {'objects': ['person', 'knows'], 'morphisms': [{'source': 'knows', 'morphism': ('k_person2id', 'p_personid'), 'target': 'person'}, {'source': 'knows', 'morphism': ('k_person1id', 'p_personid'), 'target': 'person'}]}, 'functor': {
        'person': 'nodes', 'knows': 'edges', ('k_person2id', 'p_personid'): 'source', ('k_person1id', 'p_personid'): 'target'}, 'target': {'objects': ['nodes', 'edges'], 'morphisms': [{'source': 'edges', 'morphism': 'source', 'target': 'nodes'}, {'source': 'edges', 'morphism': 'target', 'target': 'nodes'}]}}

    functors["person_in_place"] = {'domain': {'objects': ['person', 'place', ('p_placeid', 'pl_placeid')], 'morphisms': [{'source': ('p_placeid', 'pl_placeid'), 'morphism': 'p_placeid', 'target': 'place'}, {'source': ('p_placeid', 'pl_placeid'), 'morphism': 'pl_placeid', 'target': 'person'}]}, 'functor': {
        'person': 'nodes', 'place': 'nodes', ('p_placeid', 'pl_placeid'): 'edges', 'p_placeid': 'source', 'pl_placeid': 'target'}, 'target': {'objects': ['nodes', 'edges'], 'morphisms': [{'source': 'edges', 'morphism': 'source', 'target': 'nodes'}, {'source': 'edges', 'morphism': 'target', 'target': 'nodes'}]}}

    functors["tag_has_subtag"] = {'domain': {'objects': ['tagclass', ('tc_subclassoftagclassid', 'tc_tagclassid')], 'morphisms': [{'source': ('tc_subclassoftagclassid', 'tc_tagclassid'), 'morphism': 'tc_subclassoftagclassid', 'target': 'tagclass'}, {'source': ('tc_subclassoftagclassid', 'tc_tagclassid'), 'morphism': 'tc_tagclassid', 'target': 'tagclass'}]}, 'functor': {
        'tagclass': 'nodes', ('tc_subclassoftagclassid', 'tc_tagclassid'): 'edges', 'tc_subclassoftagclassid': 'source', 'tc_tagclassid': 'target'}, 'target': {'objects': ['nodes', 'edges'], 'morphisms': [{'source': 'edges', 'morphism': 'source', 'target': 'nodes'}, {'source': 'edges', 'morphism': 'target', 'target': 'nodes'}]}}

    functors["person_email_language"] = {'domain': {'objects': ['person', 'person_language', 'person_email', ('plang_personid', 'p_personid')], 'morphisms': [{'source': ('plang_personid', 'p_personid'), 'morphism': 'plang_personid', 'target': 'person'}, {'source': ('plang_personid', 'p_personid'), 'morphism': 'p_personid', 'target': 'person_language'}]}, 'functor': {
        'person': 'nodes', 'person_language': 'nodes', 'person_email': 'nodes', ('plang_personid', 'p_personid'): 'edges', 'plang_personid': 'source', 'p_personid': 'target'}, 'target': {'objects': ['nodes', 'edges'], 'morphisms': [{'source': 'edges', 'morphism': 'source', 'target': 'nodes'}, {'source': 'edges', 'morphism': 'target', 'target': 'nodes'}]}}

    return functors
