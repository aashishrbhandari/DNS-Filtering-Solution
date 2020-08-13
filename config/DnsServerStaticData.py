class DnsServerStaticData:

    DEFAULT_DNS_AUTH_SERVER = ('8.8.8.8.', 53)
    DNS_CONFIG_FILE_FULL_PATH = "F:\\WebTesting\\python\\dns_filter_version1\\dns_server_config.xml"
    DNS_CONFIG_FULL_PATH = "F:\\WebTesting\\python\\dns_filter_version1"
    DNS_SERVER_LOG_FILE = "dns_server.log"
    DNS_SERVER_LOG_FILE_FULL_PATH = "F:\\WebTesting\\python\\dns_filter_version1\\dns_server.log"

    DNS_SERVER_LOG_DEBUG_STATUS = False

    DNS_QUERY_TYPE = {
        1: 'A',
        2: 'NS',
        5: 'CNAME',
        6: 'SOA',
        12: 'PTR',
        15: 'MX',
        16: 'TXT',
        28: 'AAAA',
        33: 'SRV',
        255: 'ANY'
    }


    DNS_SERVER_CACHE_STATUS = {
        "cached": "FETCHED FROM CACHE",
        "not-cached": "FETCHED FROM AUTHORITATIVE SERVER"
    }

    # Database

    ## Access DB
    ACCESS_DB_FILE_FULL_PATH = "F:\\WebTesting\\python\\dns_filter_version1\\access_table.db" # Very Important to use \\a for \a encoding problem
    ACCESS_DB_TABLE_NAME = "access_table"

    SQL_CREATE_ACCESS_TABLE = f'''CREATE TABLE IF NOT EXISTS {ACCESS_DB_TABLE_NAME}(
    client_ip_address TEXT,
    client_mac_address TEXT,
    auth_server_ip_address TEXT,
    requested_domain TEXT,
    requested_domain_extracted TEXT,
    requested_query_type TEXT,
    policy_status TEXT,
    unique_key TEXT,
    web_category_list TEXT,
    response_ip_list TEXT,
    response_cname_list TEXT,
    response_ptr_list TEXT,
    cache_status TEXT,
    web_category_cache_status TEXT,
    client_applicable_data_holder TEXT,
    dns_start_time TEXT,
    dns_end_time TEXT,
    dns_process_time TEXT
    );
    '''

    SQL_INSERT_INTO_ACCESS_TABLE = f'''INSERT INTO {ACCESS_DB_TABLE_NAME} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''

    ## Category DB
    CATEGORY_DB_FILE_FULL_PATH = "F:\\WebTesting\\python\\dns_filter_version1\\category_table.db"
    CATEGORY_DB_TABLE_NAME = "category_table"

    CATEGORY_DB_CREATE_SQL_QUERY = f'''CREATE TABLE IF NOT EXISTS {CATEGORY_DB_TABLE_NAME} (
        website_name text NOT NULL CHECK (website_name <> ''),
        web_category_name text NOT NULL CHECK (web_category_name <> ''),
        unique (website_name, web_category_name)
    );
    ''';

    CATEGORY_DB_INSERT_SQL_QUERY = f'''INSERT INTO {CATEGORY_DB_TABLE_NAME} VALUES (?,?);'''

    CATEGORY_DB_SELECT_GET_WEB_CATEGORY_NAME_SQL_QUERY = f'''SELECT web_category_name FROM {CATEGORY_DB_TABLE_NAME};'''