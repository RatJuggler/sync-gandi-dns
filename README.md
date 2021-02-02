# sync-gandi-dns

![Test & QA](https://github.com/RatJuggler/sync-gandi-dns/workflows/Test%20&%20QA/badge.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/RatJuggler/sync-gandi-dns)

This is a simple Python package which allows the IP address records for domains registered with [Gandi](https://www.gandi.net)
to be kept up to date with the dynamic public values assigned to you by your ISP.

To keep it simple it can only update a single domain at a time but can update resource records for both IPV4 (`A`) and IPV6 
(`AAAA`).

## How it works

It uses the Gandi LiveDNS API documented [here](https://api.gandi.net/docs/livedns/) to query the current settings and make 
changes. The API is marked as (beta), but I've not experienced any issues with it.

To access the API you need to obtain a key via the Security tab under "User Settings", "Manage the user account and security 
settings".

It also needs to find out what the latest IP address is before deciding if an update is required. To do this it uses the [ipify API](https://www.ipify.org/) 
which provides simple endpoints for finding your public [IPV4](https://api.ipify.org) and [IPV6](https://api6.ipify.org) address.

## Installing

Checkout the source code from here:

    $ git clone https://github.com/RatJuggler/sync-gandi-dns.git
    $ cd sync-gandi-dns

Then install/update as a Python package:

    $ sudo pip3 install -U .

## Running

The domain to update, and the API key can be supplied as options or environment variables.
```
$ syncgandidns --help
Usage: syncgandidns [OPTIONS] DOMAIN

  Sync a dynamic IP address (V4 & V6) with a Gandi DNS domain entry.

  The external IP address is determined automatically by default.

Options:
  --version                       Show the version and exit.
  -d, --domain TEXT               The domain to update the DNS for. Taken from
                                  environment variable GANDI_DOMAIN if not
                                  supplied.  [required]
  -a, --apikey TEXT               Your Gandi API key. Taken from environment
                                  variable GANDI_APIKEY if not supplied.
                                  [required]
  -ipv4, --ipv4-address IPV4_ADDRESS
                                  Override the IPV4 address to update the
                                  domain DNS with.
  -no-ipv4, --no-ipv4-update      Don't update the IPV4 address, will override
                                  '-ipv4'.
  -ipv6, --ipv6-address IPV6_ADDRESS
                                  Override the IPV6 address to update the
                                  domain DNS with.
  -no-ipv6, --no-ipv6-update      Don't update the IPV6 address, will override
                                  '-ipv6'.
  -l, --log-level [DEBUG|VERBOSE|INFO|WARNING]
                                  Show additional logging information.
                                  [default: INFO]
  -t, --test                      Test the Gandi API key and exit.  [default:
                                  False]
  --help                          Show this message and exit.
```
## Docker

Alternatively docker build and compose files are available which create a standalone image to run the sync on an hourly schedule.

Edit the *docker/crontab.txt* file for your domain and preferred timings. If you have multiple domains just repeat the entries for
each domain.

Create the image with: `docker build -f docker/Dockerfile -t sync-gandi-dns:local .`

We need to be careful that the Gandi API key is not included in the image in case it is pushed to a public repository (and it's 
also just best practice). There are a number of ways to inject the key into the image but probably the easiest is to create an 
`env.list` file from the supplied template, set the key in it and then run the image with the `--env-file` option. You could also
set the domain here if you have a single domain.

    docker run sync-gandi-dns:local -d --env-file ./docker/env.list

Or just use the compose file to do everything:

    docker-compose up -d

## Development

For development one of the tests requires access to a key, and an accessible domain to show a working API call. These need to be
set as the environment variables GANDI_TEST_APIKEY and GANDI_TEST_DOMAINS. No tests attempt to make any changes.
