### A Simple Python Based Custom Dns Filter

#### Few Info [My ViewPoints & Some Research Work]

This is a basic implementation of a simple DNS Proxy
(because it accepts a DNS Query from the Client and then Checks for Policy 

-> Cache (If Not) 

-> Queries Root DNS Server 

-> Returns Response back to Client as well as Caches)
and it can be further expanded

I worked on it for few days :) This might not be one of a kind project as their are many DNS based Filtering Projects
Few Listed:

| Dns Security Solution | Doc Links |
| --------------------- | --------- |
| AdGuard Home (DNS) | https://adguard.com/en/adguard-home/overview.html |
| AdGuard Docs | https://adguard.com/en/blog/in-depth-review-adguard-home.html |
| DilaDele DnsSafety | https://github.com/diladele/dnssafety |
| Pi-Hole | https://github.com/pi-hole/pi-hole/#one-step-automated-install |

> Well My Broader Approach for this Custom DNS Server Filtering was to ease the way of DNS Filtering by using 
> - [x] Categories: Custom & Predefined Web Category Stored in SQLite or May be a File
> - [x] Regex: Almost Present in any DNS Filtering or Web Solution But to extend it and use a Grouping Factor
