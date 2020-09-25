class ConvergedCollectionConnection:

    def __init__(self, domain_collection, domain_id, target_collection, target_id):
        self.domain_collection = domain_collection
        self.target_collection = target_collection
        self.domain_id = domain_id
        self.target_id = target_id

    def get_domain_collection(self):
        return self.domain_collection

    def get_target_collection(self):
        return self.target_collection

    def get_domain_id(self):
        return self.domain_id

    def get_target_id(self):
        return self.target_id