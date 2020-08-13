class ClientApplicableSectionDataHolder:
    """
    def __init__(self, user_group_data_applied_list, request_data_applied_list, response_data_applied_list, policy_data_applied_list ):
        self.user_group_data_applied_list = user_group_data_applied_list
        self.request_data_applied_list = request_data_applied_list
        self.response_data_applied_list = response_data_applied_list
        self.policy_data_applied_list = policy_data_applied_list
    """

    def __init__(self):
        self.user_group_data_applied_list = []
        self.request_data_applied_list = []
        self.response_data_applied_list = []
        self.policy_data_applied_list = []

    def __repr__(self):
        return f"""
[user_group_data_applied_list]: [{self.user_group_data_applied_list}],
[request_data_applied_list]: [{self.request_data_applied_list}],
[response_data_applied_list]: [{self.response_data_applied_list}],
[policy_data_applied_list]: [{self.policy_data_applied_list}]
"""