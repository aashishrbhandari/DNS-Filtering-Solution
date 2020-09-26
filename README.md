# dns_filter_version1

### A Simple Dns Blocker

This is a basic implementation of a simple DNS Proxy (because it accepts a DNS Query from the Client and then Checks for Policy -> Cache (If Not) -> Queries Root DNS Server -> Returns Respons eback to Client as well as Caches) and it can be further expanded

I worked on it for few days :) This might not be one of a kind project as their are many DNS based Filtering Projects
Few Listed:

### AdGuard Home (It can be installed in any OS)

#### https://adguard.com/en/adguard-home/overview.html
#### https://adguard.com/en/blog/in-depth-review-adguard-home.html

### 

https://github.com/diladele/dnssafety


Well My Broader Approach for this Custom DNS Server Filtering was to ease the way of DNS Filtering by using 
##### Categories: Custom & Predefined Web Category Stored in SQLite or May be a File
##### Regex: Almost Present in any DNS Filtering or Web Solution But to extend it and use a Grouping Factor

It can be used to block dns query, you can add up all
- ads domains
- adult domains
- phishing domains
- any domain that you feel should be blocked
