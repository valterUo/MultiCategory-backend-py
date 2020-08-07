import os
from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism
from instance_category.instance_category import InstanceCategory
dirname = os.path.dirname(__file__)
unibench_sf10 = None

def init():

    objects, morphisms = dict(), dict()

    customer_data_path = os.path.join(
        dirname, "..\\data\\Unibench\\SF10\\Customer\\person_0_0.csv")
    feedback_data_path = os.path.join(
        dirname, "..\\data\\Unibench\\SF10\\Feedback\\feedback.csv")
    order_data_path = os.path.join(
        dirname, "..\\data\\Unibench\\SF10\\Order\\order.json")
    product_data_path = os.path.join(
        dirname, "..\\data\\Unibench\\SF10\\Product\\Product.csv")
    post_data_path = os.path.join(
        dirname, "..\\data\\Unibench\\SF10\\SocialNetwork\\post_0_0.csv")
    vendor_data_path = os.path.join(
        dirname, "..\\data\\Unibench\\SF10\\Vendor\\vendor.csv")
    person_knows_person_data_path = os.path.join(
        dirname, "..\\data\\Unibench\\SF10\\SocialNetwork\\person_knows_person_0_0.csv")
    post_hasCreator_person_data_path = os.path.join(
        dirname, "..\\data\\Unibench\\SF10\\SocialNetwork\\post_hasCreator_person_0_0.csv")
    post_hasTag_tag_data_path = os.path.join(
        dirname, "..\\data\\Unibench\\SF10\\SocialNetwork\\post_hasTag_tag_0_0.csv")


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

    product_table = CollectionObject("product_table", "relational", "product", lambda x: x,
                                    {"filePath": product_data_path, "fileformat": "csv",
                                    "schema": ["asin", "title", "price", "imgUrl", "productId", "brand"],
                                    "keyAttribute": "asin", "separator": ","})

    post_table = CollectionObject("post_table", "relational", "post", lambda x: x,
                                {"filePath": post_data_path, "fileformat": "csv",
                                "schema": ["id", "imageFile", "creationDate", "locationIP", "browserUsed", "language", "content", "length"],
                                "keyAttribute": "id", "separator": "|"})

    vendor_table = CollectionObject("vendor_table", "relational", "vendor", lambda x: x,
                                    {"filePath": vendor_data_path, "fileformat": "csv",
                                    "schema": ["id", "name", "country", "cdf", "industry"],
                                    "keyAttribute": "id", "separator": ","})

    person_knows_person_graph = CollectionObject("person_knows_person_graph", "property graph", "customer", lambda graph: list(graph.nodes), {
        "vertex": [
            {"filePath": person_knows_person_data_path, "fileformat": "csv", "schema": ["from", "to", "creationDate"], "keyAttribute": "creationDate", "separator": "|"}],
        "edge": [
            {"filePath": person_knows_person_data_path, "fileformat": "csv", "schema": ["from", "to", "creationDate"], "keyAttribute": "creationDate", "fromKeyAttribute": "from", "toKeyAttribute": "to", "separator": "|"}]
    })

    post_hasCreator_person_graph = CollectionObject("post_hasCreator_person_graph", "property graph", "post + person", lambda graph: list(graph.nodes), {
        "vertex": [
            {"filePath": post_hasCreator_person_data_path, "fileformat": "csv", "schema": ["PostId", "PersonId"], "keyAttribute": ["PostId", "PersonId"], "separator": "|"}],
        "edge": [
            {"filePath": post_hasCreator_person_data_path, "fileformat": "csv", "schema": ["PostId", "PersonId"], "keyAttribute": ["PostId", "PersonId"], "fromKeyAttribute": "PostId", "toKeyAttribute": "PersonId", "separator": "|"}]
    })

    post_hasTag_tag_graph = CollectionObject("post_hasTag_tag_graph", "property graph", "post + tag", lambda graph: list(graph.nodes), {
        "vertex": [
            {"filePath": post_hasTag_tag_data_path, "fileformat": "csv", "schema": ["PostId", "TagId"], "keyAttribute": ["PostId", "TagId"], "separator": "|"}],
        "edge": [
            {"filePath": post_hasTag_tag_data_path, "fileformat": "csv", "schema": ["PostId", "TagId"], "keyAttribute": ["PostId", "TagId"], "fromKeyAttribute": "PostId", "toKeyAttribute": "TagId", "separator": "|"}]
    })

    objects["customer_table"] = customer_table
    objects["orders_json"] = orders_json
    objects["feedback_table"] = feedback_table
    objects["product_table"] = product_table
    objects["post_table"] = post_table
    objects["vendor_table"] = vendor_table
    objects["person_knows_person_graph"] = person_knows_person_graph
    objects["post_hasCreator_person_graph"] = post_hasCreator_person_graph
    objects["post_hasTag_tag_graph"] = post_hasTag_tag_graph

    # Formulating ArangoDB query into demo system's syntax:

    fixed_id = "2199023286963"

    # LET customer = (FOR doc IN Customer FILTER doc._key == @key RETURN doc )
    single_customer_table = CollectionObject("single_customer_table", "relational", "customer")
    single_customer_for_fixed_id = Morphism("single_customer", customer_table, lambda customer: customer_table.get_collection().get(fixed_id, "Key not in the dictonary!"), single_customer_table, True, True)

    # # LET orders = (FOR order in Order FILTER order.PersonId==@key RETURN order )
    orders_by_customer_with_fixed_id = CollectionObject("orders_by_customer_with_fixed_id", "JSON", "order")
    orders_with_fixed_id = Morphism("orders_of_fixed_customer", orders_json, lambda order: list(filter(lambda o : True if str(o["PersonId"]) == fixed_id else False, orders_json.get_collection())), orders_by_customer_with_fixed_id, True, True)

    # # LET feedback = (For feedback in Feedback FILTER TO_STRING(feedback.PersonId)==@key RETURN feedback )
    feedbacks_by_customer_with_fixed_id = CollectionObject("feedbacks_by_customer_with_fixed_id", "relational", "feedback")
    feedbacks_with_fixed_id = Morphism("feedbacks_of_fixed_customer", feedback_table, lambda feedback: list(filter(lambda f : True if str(f["personId"]) == fixed_id else False, feedback_table.get_collection().values())), feedbacks_by_customer_with_fixed_id, True, True)

    # LET posts = (FOR post IN Outbound @id PersonHasPost RETURN post)

    # LET plist = Flatten(For order in orders return order.Orderline[*])

    # LET list1 = (For item in plist collect category=item.brand with count into cnt sort cnt DESC return { category, cnt })

    # LET list2 = (For post in posts For Tag in Outbound post PostHasTag Collect id= Tag._key WITH COUNT INTO cnt SORT cnt DESC Return { id, cnt })

    # Return {customer, orders, feedback, posts, list1, list2}
    # The above return clause means that we obtain the above objects from the instance category

    #print(feedbacks_by_customer_with_fixed_id.get_collection())

    global unibench_sf10

    unibench_sf10 = InstanceCategory("Unibench_sf10", objects, morphisms)