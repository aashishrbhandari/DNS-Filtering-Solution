import re


class ResponseDataHolder:

    """
        def __init__(self):
            self.status = None
            self.res_name = None
            self.res_description = None
            self.res_cname = None
            self.res_ip_list = None
    """

    def __init__(self, status, res_name, res_description, res_cname_list, res_ip_list):
        self.status = status
        self.res_name = res_name
        self.res_description = res_description
        self.res_cname_list = self.set_res_cname_list(res_cname_list)
        self.res_ip_list = res_ip_list

    def set_res_cname_list(self, res_cname_list):
        # Each Request Holder will have req_domain_name that will have multiple regex
        # and for better management we are using "," (comma) as the separator
        # which will be replaced by "|" (PIPE) to match for all regex pattern
        res_cname_regex = None;
        try:
            res_cname_list_changed = res_cname_list.replace(",", "|")
            print(f"Res_Cname_List Provided: [{res_cname_list}], Converted(Using Delimiter:[[,]->[|]]): [{res_cname_list_changed}]")
            res_cname_regex = re.compile(res_cname_list_changed) # many things can be added here
        except re.error as excep:
            print(f"Problem in Regex: [{excep}]")
            res_cname_regex = r"wrong-domain-problem-check"
        finally:
            return res_cname_regex

    def __repr__(self):
        return f"""
[Response Status]: [{self.status}]
[Response Name]: [{self.res_name}]
[Response Description]: [{self.res_description}]
[Response CNAME List]: [{self.res_cname_list}]
[Response IP List]: [{self.res_ip_list}]
"""


