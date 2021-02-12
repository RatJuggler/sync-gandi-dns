# sync-gandi-dns

![Test & QA](https://github.com/RatJuggler/sync-gandi-dns/workflows/Test%20&%20QA/badge.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/RatJuggler/sync-gandi-dns)

This is a simple Python package which allows the IP address records for domains registered with [Gandi](https://www.gandi.net)
to be kept up to date with the dynamic public values assigned to you by your ISP.

It can be used to update the resource record for either IPV4 (`A`) or IPV6 (`AAAA`) or both, for a single or multiple domains.

## How it works

It uses the [Gandi LiveDNS API](https://api.gandi.net/docs/livedns/) to query the current settings and make changes. The API is 
marked as (beta), but I've not experienced any issues with it. To access the API you need to obtain a key via the Security tab 
under "User Settings", "Manage the user account and security settings".

It also needs to find out what the latest IP address is before deciding if an update is required. To do this it uses the *[ipify API](https://www.ipify.org/)* 
which provides simple endpoints for finding your public [IPV4](https://api.ipify.org) and [IPV6](https://api6.ipify.org) address.

## Installing

Checkout the source code from here:

    $ git clone https://github.com/RatJuggler/sync-gandi-dns.git
    $ cd sync-gandi-dns

Then install/update as a Python package:

    $ sudo pip3 install -U .

## Running
```
$ syncgandidns --help
Usage: syncgandidns [OPTIONS]

  Sync a dynamic IP address (V4 & V6) with a Gandi DNS domain entry.

  The external IP address is determined automatically by default.

  Domains can be set using the GANDI_DOMAINS environment variable. For
  multiple domains separate with a ';'.

  The Gandi API key can be set using the GANDI_APIKEY environment variable.

Options:
  --version                       Show the version and exit.
  -d, --domain DOMAIN             A domain to update the DNS for. Repeat the
                                  option to update multiple domains.
                                  [required]
  -a, --apikey TEXT               Your Gandi API key.  [required]
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
There are a number of ways of configuring the domain(s) to update, and the API key. You can set them directly with options on the
command line or provide them pre-set in environment variables, but probably the easiest way to do this is to create a 
`sync-gandi-dns.env` file from the supplied template, then edit the file and set them there. 

    $ cp sync-gandi-dns.env.template sync-gandi-dns.env

The edited file should then look something like this (not real data):

    GANDI_APIKEY="12345abcde67890fghij12kl"
    GANDI_DOMAINS="mydomain.com;otherdomain.co.uk;anyothers.io"

It will always start by looking for this file in the current directory and then search upwards. Test that your configuration is 
working by using:

    $ syncgandidns --test

## Docker

**Note:** IPV6 connectivity is not enabled by default for docker containers, so the *ipify* IPV6 lookup will always fail, and the 
IPV6 address cannot then be kept up to date. I am currently [researching](https://medium.com/@skleeschulte/how-to-enable-ipv6-for-docker-containers-on-ubuntu-18-04-c68394a219a2) 
how best to proceed with configuring this.

Docker build and compose files are available which create a standalone image to run the sync on an hourly schedule.

Edit the *docker/crontab.txt* file to set your preferred timings.

Create the image with:

    $ docker build -f docker/Dockerfile -t sync-gandi-dns:local .

Environment variables should be used to set the domains to update, and the Gandi API key. It is important that the API key is not 
included in the image in case it is pushed to a public repository (and it's also just best practice). There are a number of ways 
to do this but probably the easiest is to create a `sync-gandi-dns.env` file as described above and then run the image with the 
`--env-file` option.

    $ docker run sync-gandi-dns:local -d --env-file sync-gandi-dns.env

Or just use the compose file to do everything:

    $ docker-compose up -d

Environment variables can also be used to configure image tagging (see the file).

## Development

For development one of the tests requires access to a key, and an accessible domain to show a working API call. These need to be
set as the environment variables GANDI_TEST_APIKEY and GANDI_TEST_DOMAINS. No tests attempt to make any changes.
