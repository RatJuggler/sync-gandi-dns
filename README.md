# sync-gandi-dns

Once completed this Python script will allow the IP address records for a domain registered with 
[Gandi](https://www.gandi.net) to be kept up to date with the dynamic values assigned by your ISP.

To keep it simple it will only update a single domain but can include updates to resource records for both IPV4 (`A`) 
and IPV6 (`AAAA`).

# Gandi API Key

This script uses the Gandi LiveDNS API documented [here](https://api.gandi.net/docs/livedns/) to query the current
settings and make changes. As of this update the API is marked as (beta) but I've not experienced any issues with it.

To access the API you need to obtain a key via the Security tab under "User Settings", 
"Manage the user account and security settings".

For development one of the tests requires access to a key and an accessible domain to show a working API call. These
need to be set as the environment variables GANDI_API_KEY and GANDI_TEST_DOMAIN. No tests attempt to make any changes.

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
