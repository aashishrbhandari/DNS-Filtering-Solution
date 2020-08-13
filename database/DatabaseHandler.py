import sqlite3

from handlers.LoggingHandler import logger, timed
from config.DnsServerStaticData import DnsServerStaticData


class AccessDatabaseHandler:

    def __init__(self):
        logger.debug(f"[Process: Starting Sqlite3 DB Connection Table: [{DnsServerStaticData.ACCESS_DB_TABLE_NAME}]]")
        self.sqlite3_db_connection = sqlite3.connect(DnsServerStaticData.ACCESS_DB_FILE_FULL_PATH,
                                                     check_same_thread=False,
                                                     timeout=60.0) # Done Because Sqlite is not good for Multi-threaded application [VVIP]
        db_cursor = self.sqlite3_db_connection.cursor()
        db_cursor.execute(DnsServerStaticData.SQL_CREATE_ACCESS_TABLE);

    def get_connection(self):
        return self.sqlite3_db_connection;

    @timed
    def insert_to_access_db(self, client_data_holder):
        client_data_holder_tuple = (client_data_holder.client_ip_address,
         client_data_holder.client_mac_address,
         client_data_holder.auth_server_ip_address,
         client_data_holder.requested_domain,
         client_data_holder.requested_query_type,
         client_data_holder.policy_status,
         client_data_holder.unique_key,
         client_data_holder.web_category_list,
         client_data_holder.response_ip_list,
         client_data_holder.response_cname_list,
         client_data_holder.response_ptr_list,
         client_data_holder.cache_status,
         client_data_holder.web_category_cache_status,
         client_data_holder.client_applicable_data_holder,
         client_data_holder.dns_start_time,
         client_data_holder.dns_end_time,
         client_data_holder.dns_process_time
         )
        db_cursor = self.sqlite3_db_connection.cursor()
        result = db_cursor.execute(DnsServerStaticData.SQL_INSERT_INTO_ACCESS_TABLE, client_data_holder_tuple) # Changed uses new cursor for each INSERT
        logger.debug(f"[Process: Insert Operation Done on {DnsServerStaticData.ACCESS_DB_TABLE_NAME}], Result: [{result}]")


    @classmethod
    def insert_to_access_db(cls, db_connection, client_data_holder):
        client_data_holder_tuple = (client_data_holder.client_ip_address,
                                    client_data_holder.client_mac_address,
                                    client_data_holder.auth_server_ip_address,
                                    client_data_holder.requested_domain,
                                    client_data_holder.requested_domain_extracted,
                                    client_data_holder.requested_query_type,
                                    client_data_holder.policy_status,
                                    client_data_holder.unique_key,
                                    client_data_holder.web_category_list,
                                    client_data_holder.response_ip_list,
                                    client_data_holder.response_cname_list,
                                    client_data_holder.response_ptr_list,
                                    client_data_holder.cache_status,
                                    client_data_holder.web_category_cache_status,
                                    client_data_holder.client_applicable_data_holder,
                                    client_data_holder.dns_start_time,
                                    client_data_holder.dns_end_time,
                                    client_data_holder.dns_process_time
                                    )
        result = db_connection.execute(DnsServerStaticData.SQL_INSERT_INTO_ACCESS_TABLE,
                                   client_data_holder_tuple)  # Changed uses new cursor for each INSERT
        logger.debug(f"[Process: Insert Operation Done on {DnsServerStaticData.ACCESS_DB_TABLE_NAME}], Result: [{result}]")

    @timed
    def commit_changes(self):
        self.sqlite3_db_connection.commit();
        logger.debug(f"[Process: Commit Operation Done on {DnsServerStaticData.ACCESS_DB_TABLE_NAME}]")

    def close_db_connection(self):
        self.sqlite3_db_connection.close();
        logger.debug(f"[Process: Connection Close Operation Done on {DnsServerStaticData.ACCESS_DB_TABLE_NAME}]")


class CategoryDatabaseHandler:
    def __init__(self):
        logger.debug(f"[Process: Starting Sqlite3 DB Connection Table: [{DnsServerStaticData.CATEGORY_DB_TABLE_NAME}]]")
        self.category_db_connection = sqlite3.connect(DnsServerStaticData.CATEGORY_DB_FILE_FULL_PATH,
                                                     check_same_thread=False,
                                                     timeout=60.0)  # Done Because Sqlite is not good for Multi-threaded application [VVIP]
        db_cursor = self.category_db_connection.cursor()
        db_cursor.execute(DnsServerStaticData.CATEGORY_DB_CREATE_SQL_QUERY);

    def get_category_db_connection(self):
        return self.category_db_connection;

    def get_results(self, sql_query):
        return self.category_db_connection.execute(sql_query)

    def insert_into_category_db(self, dataset):
        return self.category_db_connection.execute(DnsServerStaticData.CATEGORY_DB_INSERT_SQL_QUERY, dataset)