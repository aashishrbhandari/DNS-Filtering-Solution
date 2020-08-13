import re as PyRegex


def set_regex_pattern(regex_pattern):
    # Each Request Holder will have req_domain_name that will have multiple regex
    # and for better management we are using "," (comma) as the separator
    # which will be replaced by "|" (PIPE) to match for all regex pattern
    _regex_pattern = None;
    try:
        regex_pattern_changed = regex_pattern.replace(",", "|")
        print(f"Req_Domain_Name_List Provided: [{regex_pattern}], Converted(Using Delimiter:[[,]->[|]]): [{regex_pattern_changed}]")
        _regex_pattern = PyRegex.compile(regex_pattern_changed) # many things can be added here
    except PyRegex.error as excep:
        regex_pattern_changed = regex_pattern_changed.replace("*", ".*")
        _regex_pattern = PyRegex.compile(regex_pattern_changed);
        print(f"Problem in Regex: [{excep}], Therefore Regex To:[{_regex_pattern}]")
    finally:
        return _regex_pattern


class AllowedDataHolder:
    def __init__(self, allow_policy_name,
                 allow_policy_description,
                 allow_policy_regex_pattern,
                 allow_policy_webcategory_list):
        self.allow_policy_name = allow_policy_name
        self.allow_policy_description = allow_policy_description
        self.allow_policy_regex_pattern = set_regex_pattern(allow_policy_regex_pattern)
        self.allow_policy_webcategory_list = allow_policy_webcategory_list

    def __repr__(self):
        return f"""
[allow_policy_name]: [{self.allow_policy_name}]
[allow_policy_description]: [{self.allow_policy_description}]
[allow_policy_regex_pattern]: [{self.allow_policy_regex_pattern}]
[allow_policy_webcategory_list]: [{self.allow_policy_webcategory_list}]
"""