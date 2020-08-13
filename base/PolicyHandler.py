from config.ConfigParser import process_policy
from handlers.LoggingHandler import logger

"""Implementation Left"""
class PolicyHandler:

    # sets Policy Status to ALLOW or BLOCK
    @classmethod
    def process_policy_check_for_dns_request(cls, client_data_holder):
        ## No Implementation there ALLOW for all
        status = process_policy(client_data_holder=client_data_holder)
        print("Status: ", status)
        if status["status"] == "BLOCK":
            client_data_holder.policy_status = "BLOCK:" + status.get("type");
        else:
            client_data_holder.policy_status = "ALLOW:" + status.get("type");

        client_data_holder.unique_key = client_data_holder.requested_domain + "_" + client_data_holder.requested_query_type + "_" + client_data_holder.policy_status.split(":")[0];

        logger.debug(f"[Process: Policy Checking(Request) & Unique Key Rewrite], Unique Key: [{client_data_holder.unique_key}] [Not Implemented] ");
        #print(f"[Process: Policy Checking(Request) & Unique Key Rewrite], Unique Key: [{client_data_holder.unique_key}] [Not Implemented] ");
        return client_data_holder


    @classmethod
    def process_policy_check_for_dns_response(cls, client_data_holder):
        ## No Implementation there ALLOW for all
        client_data_holder.policy_status = "ALLOW";
        client_data_holder.unique_key = client_data_holder.requested_domain + "_" + client_data_holder.requested_query_type + "_" + client_data_holder.policy_status;
        logger.debug(
            f"[Process: Policy Checking(Response) & Unique Key Rewrite], Unique Key: [{client_data_holder.unique_key}]  [Not Implemented]");
        return client_data_holder
