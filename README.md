# sync-gandi-dns

Once completed this Python script will allow the IP address records for a domain registered with 
[Gandi](https://www.gandi.net) to be kept up to date with the dynamic values assigned by your ISP.

To keep it simple it will only update a single domain but can include updates to resource records for both IPV4 (`A`) 
and IPV6 (`AAAA`).

# Gandi API

This uses the Gandi LiveDNS API documented [here](https://api.gandi.net/docs/livedns/). As of this update the API is 
marked as (beta) but I've not experieced any issues with it.

# Running

```
$ syncgandidns --help
Usage: syncgandidns [OPTIONS] DOMAIN

  Sync a local dynamic IP address with a domain on Gandi DNS.

  DOMAIN: The domain to update the DNS for.

  APIKEY: Your Gandi API key.

Options:
  --version                       Show the version and exit.
  -ipv4 IPV4_ADDRESS              The IPV4 address to update the domain DNS
                                  with.
  -ipv6 IPV6_ADDRESS              The IPV6 address to update the domain DNS
                                  with.
  -l, --log-level [DEBUG|VERBOSE|INFO|WARNING]
                                  Show additional logging information.
                                  [default: INFO]
  --help                          Show this message and exit.
```
