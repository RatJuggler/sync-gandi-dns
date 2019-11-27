# sync-gandi-dns

Simple Python script to keep the IP address records for a domain registered with [Gandi](https://www.gandi.net) up to
date with the dynamic values assigned by your ISP. 

To keep it simple it will only update a single domain but can include updates to resource records for both IPV4 (`A`) 
and IPV6 (`AAAA`).
