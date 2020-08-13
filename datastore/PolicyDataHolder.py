class PolicyDataHolder:
    """
    def __init__(self):
        self.status = None
        self.policy_name = None
        self.policy_description = None
        self.user_group_list = None
        self.request_list = None
        self.web_category_list = None
        self.response_list = None
        self.policy_action = None

    """
    
    def __init__(self, status, policy_name, policy_description, user_group_list, request_list, request_list_to_web_category_list_connector, web_category_list,
                 response_list, policy_action):
        self.status = status
        self.policy_name = policy_name
        self.policy_description = policy_description
        self.user_group_list = user_group_list
        self.request_list = request_list
        self.request_list_to_web_category_list_connector = request_list_to_web_category_list_connector;
        self.web_category_list = web_category_list
        self.response_list = response_list
        self.policy_action = policy_action


    def __repr__(self):
        return f"""
[Policy Status]: [{self.status}]
[Policy Name]: [{self.policy_name}]
[Policy Description]: [{self.policy_description}]
[Policy User Group List]: [{self.user_group_list}]
[Policy Request List]: [{self.request_list}]
[Policy Request List To Web Category List Connector]: [{self.request_list_to_web_category_list_connector}]
[Policy Web Category List]: [{self.web_category_list}]
[Policy Response List]: [{self.response_list}]
[Policy Action]: [{self.policy_action}]
"""
