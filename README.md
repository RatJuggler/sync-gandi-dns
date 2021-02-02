# sync-gandi-dns

![Test & QA](https://github.com/RatJuggler/sync-gandi-dns/workflows/Test%20&%20QA/badge.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/RatJuggler/sync-gandi-dns)

This is a simple Python package which allows the IP address records for a domain registered with [Gandi](https://www.gandi.net)
to be kept up to date with the dynamic public values assigned by your ISP.

To keep it simple it will only update a single domain but can include updates to resource records for both IPV4 (`A`) and IPV6 
(`AAAA`).

## How it works

It uses the Gandi LiveDNS API documented [here](https://api.gandi.net/docs/livedns/) to query the current settings and make 
changes. The API is marked as (beta), but I've not experienced any issues with it.

To access the API you need to obtain a key via the Security tab under "User Settings", 
"Manage the user account and security settings".

For development one of the tests requires access to a key, and an accessible domain to show a working API call. These need to be
set as the environment variables GANDI_API_KEY and GANDI_TEST_DOMAIN. No tests attempt to make any changes.

Of course, it also needs to find out what the latest IP address is before deciding if an update is required. To do this it uses
the [ipify API](https://www.ipify.org/) which provides simple endpoints for finding your public [IPV4](https://api.ipify.org)
and [IPV6](https://api6.ipify.org) address.

## Installing

Checkout the source code from here:
```
$ git clone https://github.com/RatJuggler/sync-gandi-dns.git
$ cd sync-gandi-dns
```
Then install/update as a Python package:
```
$ sudo pip3 install -U .
```

## Running

```
$ syncgandidns --help
Usage: syncgandidns [OPTIONS] DOMAIN

  Sync a dynamic IP address (V4 & V6) with a Gandi DNS domain entry.

  The external IP address is determined automatically.

  DOMAIN: The domain to update the DNS for.

  APIKEY: Your Gandi API key.

Options:
  --version                       Show the version and exit.
  -no-ipv6, --no-ipv6-update      Don't update the IPV6 address, will override
                                  '-ipv6'.
  -ipv4, --ipv4-address IPV4_ADDRESS
                                  Override the IPV4 address to update the
                                  domain DNS with.
  -ipv6, --ipv6-address IPV6_ADDRESS
                                  Override the IPV6 address to update the
                                  domain DNS with.
  -l, --log-level [DEBUG|VERBOSE|INFO|WARNING]
                                  Show additional logging information.
                                  [default: INFO]
  --help                          Show this message and exit.
```

I've currently got it running as an hourly `cron` job.
