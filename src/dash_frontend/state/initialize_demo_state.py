from dash_frontend.state.state import State
from tables import *
import json
import os
dirname = os.path.dirname(__file__)
## Pre-defined databases
from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase

possible_states = {
    "ecommerce": {'label': 'E-commerce dataset', 'value': 'ecommerce', 'available': True, 'db': ECommerceMultiModelDatabase().get_multi_model_db()},
    "patent": {'label': 'Patent dataset', 'value': 'patent', 'available': True, 'db': PatentMultiModelDatabase().get_multi_model_db()},
    "market_place": {'label': 'Online market place', 'value': 'market_place', 'available': False, 'db': None},
    "unibench_small": {'label': 'Unibench small dataset', 'value': 'unibench_small', 'available': False, 'db': None},
    "university": {'label': 'University dataset', 'value': 'university', 'available': False, 'db': None},
    "person": {'label': 'Person dataset', 'value': 'person', 'available': False, 'db': None},
    "film": {'label': 'Film dataset', 'value': 'film', 'available': False, 'db': None}
}

examples_path = os.path.join(dirname, "filtering_examples.json")
with open(examples_path) as f:
    examples = json.load(f)
    for key in possible_states:
        possible_states[key]["filtering_examples"] = examples[key]

## Initially the E-commerce database is selected.
state = State("ecommerce", possible_states)

## Parameters for multi-model join
parameter_state_dict = {"parameters": {"left": False, "right": False, "second_description": None,
                                       "tree_attributes": None, "domain": None, "target": None, "morphism": None}}

parameter_state = State("parameters", parameter_state_dict)

## State to store automatic examples for second table description
description = dict()
description["customer_id"] = StringCol(64, dflt='NULL')
description["name"] = StringCol(64, dflt='NULL')
description["creditLimit"] = StringCol(64, dflt='NULL')
description["customer_locationId"] = StringCol(64, dflt='NULL')

automatic_example_settings_dict = {
    "ecommerce": {"location": {"customer": description}}
}

automatic_example_settings = State("ecommerce", automatic_example_settings_dict)

## State to store multi-model results
multi_model_join_results = State("initial", {"initial": {}})
multi_model_query_results = State("initial", {"initial": {}})