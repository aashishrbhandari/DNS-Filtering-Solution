import sqlite3

from config.DnsServerStaticData import DnsServerStaticData


class TempCategoryDatabaseHandler:
    def __init__(self):
        print(f"[Process: Starting Sqlite3 DB Connection Table: [{DnsServerStaticData.CATEGORY_DB_TABLE_NAME}]]")
        self.category_db_connection = sqlite3.connect(DnsServerStaticData.CATEGORY_DB_FILE_FULL_PATH,
                                                     check_same_thread=False,
                                                     timeout=60.0)  # Done Because Sqlite is not good for Multi-threaded application [VVIP]
        db_cursor = self.category_db_connection.cursor()
        db_cursor.execute(DnsServerStaticData.CATEGORY_DB_CREATE_SQL_QUERY);

    def get_category_db_connection(self):
        return self.category_db_connection;

    def get_results(self, sql_query):
        return self.category_db_connection.execute(sql_query)


results = TempCategoryDatabaseHandler().get_results(DnsServerStaticData.CATEGORY_DB_SELECT_GET_WEB_CATEGORY_NAME_SQL_QUERY);

print("Results Set")
for one_data in results:
    print(one_data)