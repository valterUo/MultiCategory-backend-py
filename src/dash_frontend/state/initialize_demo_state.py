from dash_frontend.state.state import State
## Pre-defined databases
from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase

possible_states = {
        "ecommerce": {'label': 'E-commerce dataset', 'value': 'ecommerce', 'available': True, 'db': ECommerceMultiModelDatabase().get_multi_model_db()},
        "patent": {'label': 'Patent dataset', 'value': 'patent', 'available': True, 'db': PatentMultiModelDatabase().get_multi_model_db()},
        "market_place": {'label': 'Online market place', 'value': 'market_place', 'available': False, 'db': None},
        "unibench_small": {'label': 'Unibench small dataset', 'value': 'unibench_small', 'available': False,'db': None},
        "university": {'label': 'University dataset', 'value': 'university', 'available': False, 'db': None},
        "person": {'label': 'Person dataset', 'value': 'person', 'available': False, 'db': None},
        "film": {'label': 'Film dataset', 'value': 'film', 'available': False, 'db': None}
    }

## Initially the E-commerce database is selected.
state = State("ecommerce", possible_states)