import re

class RequestDataHolder:

    """
    def __init__(self):
        self.status = None
        self.req_name = None
        self.req_description = None
        self.req_domain_name = None
    """

    def __init__(self, status, req_name, req_description, req_domain_name_list, req_querytype_list):
        self.status = status
        self.req_name = req_name
        self.req_description = req_description
        self.req_domain_name_list = self.set_req_domain_name_list(req_domain_name_list)
        self.req_querytype_list = req_querytype_list
        self._req_domain_name_list = req_domain_name_list

    def set_req_domain_name_list(self, req_domain_name_list):
        # Each Request Holder will have req_domain_name that will have multiple regex
        # and for better management we are using "," (comma) as the separator
        # which will be replaced by "|" (PIPE) to match for all regex pattern
        req_domain_name_regex = None;
        try:
            req_domain_name_list_changed = req_domain_name_list.replace(",", "|")
            print(f"Req_Domain_Name_List Provided: [{req_domain_name_list}], Converted(Using Delimiter:[[,]->[|]]): [{req_domain_name_list_changed}]")
            req_domain_name_regex = re.compile(req_domain_name_list_changed) # many things can be added here
        except re.error as excep:
            print(f"Problem in Regex: [{excep}]")
            req_domain_name_regex = r"wrong-domain-problem-check"
        finally:
            return req_domain_name_regex

    def __repr__(self):
        return f"""
[Request Status]: [{self.status}]
[Request Name]: [{self.req_name}]
[Request Description]: [{self.req_description}]
[Request Domain Name List]: [{self.req_domain_name_list}]
[Request Query Type List]: [{self.req_querytype_list}]
"""