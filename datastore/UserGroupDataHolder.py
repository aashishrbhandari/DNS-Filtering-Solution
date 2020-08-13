class UserGroupDataHolder:
    """
    def __init__(self, ):
        self.status = None
        self.user_group_name = None
        self.user_group_description = None
        self.users_ip_list = None
    """

    def __init__(self, status, user_group_name, user_group_description, users_ip_list, users_mac_list):
        self.status = status
        self.user_group_name = user_group_name
        self.user_group_description = user_group_description
        self.users_ip_list = users_ip_list
        self.users_mac_list = users_mac_list

    def __repr__(self):
        return f"""
[User Group Status]: [{self.status}]
[User Group Name]: [{self.user_group_name}]
[User Group Description]: [{self.user_group_description}]
[Users IP List]: [{self.users_ip_list}]
[Users MAC List]: [{self.users_mac_list}]
"""