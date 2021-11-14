### A Simple Python Based Custom Dns FilterCancel changes
A Simple Python Based DNS Blocker (~Filtering) Service.  Give it a Shot.

I worked on it for few days :) .
This might not be one of a kind project as their are many DNS based Filtering Projects

### Few Info [My ViewPoints & Some Research Work]

#### Implementation

- This is a basic implementation of a simple DNS Proxy
- Customizable (and it can be further expanded)
- Quick Flow

(1) It accepts a DNS Query from the Client and then Checks for Policy 

(2) Checks Cache (If Not) 
            
(3) Queries Root DNS Server

(4) Returns Response back to Client as well as Caches



#### DNS Security Solution:
> My Personal Fav List

| Dns Security Solution | Doc Links |
| --------------------- | --------- |
| AdGuard Home (DNS) | https://adguard.com/en/adguard-home/overview.html, https://github.com/AdguardTeam/AdguardHome, https://adguard.com/en/blog/in-depth-review-adguard-home.html |
| DilaDele DnsSafety | https://github.com/diladele/dnssafety |
| Pi-Hole | https://github.com/pi-hole/pi-hole/#one-step-automated-install |

> Well My Broader Approach for this Custom DNS Server Filtering was to ease the way of DNS Filtering by using 
> - [x] Categories: Custom & Predefined Web Category Stored in SQLite or May be a File
> - [x] Regex: Almost Present in any DNS Filtering or Web Solution But to extend it and use a Grouping Factor
