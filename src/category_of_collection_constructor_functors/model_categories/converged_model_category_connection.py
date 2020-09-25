class ConvergedModelCategoryConnection:

    def __init__(self, domain_model_category, domain_id, target_model_category, target_id):
        self.domain_model_category = domain_model_category
        self.target_model_category = target_model_category
        self.domain_id = domain_id
        self.target_id = target_id

    def get_domain_model_category(self):
        return self.domain_model_category

    def get_target_model_category(self):
        return self.target_model_category

    def get_domain_id(self):
        return self.domain_id

    def get_target_id(self):
        return self.target_id