from tables import *

## State to store automatic examples for second table description
description = dict()
description["customer_id"] = StringCol(64, dflt='NULL')
description["name"] = StringCol(64, dflt='NULL')
description["creditLimit"] = StringCol(64, dflt='NULL')
description["customer_locationId"] = StringCol(64, dflt='NULL')

automatic_example_settings_dict = {
    "ecommerce": {"location": {"customer": description}}
}