# Shodan Bulk Query

This script is ~~stolen~~ inspired by:
https://github.com/emresaglam/shodan-bulk-ip-query

Its purpose is to facilitate the search for entities responsible for devices associated with IP addresses. To use it, a Shodan account with a "Membership" status is necessary (which can sometimes be snagged for $5), allowing the use of the API. The key can be found at https://account.shodan.io.

**NOTE** - the query limit for the "Membership" plan is 100 IP addresses per month, although it's unclear what counts toward credit usage. As of now, I have tested the script on several hundred addresses in one day and it has not charged me for it:
https://help.shodan.io/the-basics/credit-types-explained

Credit status can be monitored here:
https://developer.shodan.io/dashboard

# Requirements
* `pip3 install -r requirements`
* Paste your API key into the file `shodan_api_key.txt`.
* Prepare a list of IP addresses in the file `iplist.txt`, each address on a new line.

# Usage
Run `python3 shodanQuery.py` which reads the IP list from `iplist.txt`, then begins to retrieve information for each address sequentially and displays the information in the terminal:
```
[INFO] - fetching host 195.117.120.97, progress: 42.3%
```
In case of an error, a message appears about the cause, e.g., no IP in the Shodan database, connection error, or too many rapid requests (in this case, rerun the script with `-d` and specify the pause duration in seconds, default is 1).

By default, the script outputs two files to the output folder:
* `shodan_results_TIMESTAMP.json` - contains a full dump of information about the IP addresses
* `shodan_results_TIMESTAMP.xlsx` - contains basic information helpful in establishing entities behind addresses. If Shodan lacks data about specific IP, the corresponding cells show `-`. If an IP address is not in the database at all, then all cells take the value `NoData`. Additionally, for xlsx, abuse addresses are fetched from WHOIS. Unfortunately, the script does not currently use RIPE, so this functionality is somewhat lacking...

Furthermore, if errors occur while retrieving information for certain IPs, a list of them is saved in:
`shodan_results_TIMESTAMP.txt`
