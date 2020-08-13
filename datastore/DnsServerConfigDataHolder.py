class DnsServerConfigDataHolder:

    def __init__(self):
        self.setup_config_data_holder = None
        self.blocked_data_holder = None
        self.allowed_data_holder = None

    def __repr__(self):
        return f"""
[self.setup_config_data_holder]: [{self.setup_config_data_holder}]
[self.blocked_data_holder]: [{self.blocked_data_holder}]
[self.allowed_data_holder]: [{self.allowed_data_holder}]
"""


    """ Getter & Setter left to implement """
