import os
dirname = os.path.dirname(__file__)
unibench_sf10 = None

def init():

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


    global unibench_sf10

    unibench_sf10 = None