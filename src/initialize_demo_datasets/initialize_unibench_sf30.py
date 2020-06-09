from instance_category.objects.collection_object import CollectionObject
import os
dirname = os.path.dirname(__file__)

customer_data_path = os.path.join(
    dirname, "..\\data\\Unibench\\SF30\\Customer\\person_0_0.csv")
feedback_data_path = os.path.join(
    dirname, "..\\data\\Unibench\\SF30\\Feedback\\feedback.csv")
order_data_path = os.path.join(
    dirname, "..\\data\\Unibench\\SF30\\Order\\order.json")
product_data_path = os.path.join(
    dirname, "..\\data\\Unibench\\SF30\\Product\\Product.csv")

customer_table = CollectionObject("customer_table", "relational", "customer", lambda x: x,
                                  {"filePath": customer_data_path, "fileformat": "csv",
                                   "schema": ["id", "firstName", "lastName", "gender", "birthday", "creationDate", "locationIP", "browserUsed"],
                                   "keyAttribute": "id", "separator": "|"})

orders_json = CollectionObject("orders", "JSON", "order", lambda json: json, {
                               "filePath": order_data_path})

feedback_table = CollectionObject("feedback_table", "relational", "feedback", lambda x: x,
                                  {"filePath": feedback_data_path, "fileformat": "csv",
                                   "schema": ["asin", "personId", "feedback"],
                                   "keyAttribute": ["asin", "personId"], "separator": "|"})