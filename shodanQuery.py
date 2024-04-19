import json
import shodan
import argparse
import time
import whois
from datetime import datetime
from rich import print
import pandas as pd

with open('shodan_api_key.txt', 'r') as api_file:
    SHODAN_API_KEY = api_file.read().strip()
api = shodan.Shodan(SHODAN_API_KEY)

parser = argparse.ArgumentParser(description='Get a list of IPs and return shodan info.')
parser.add_argument('--filename', '-f', default='iplist.txt')
parser.add_argument('--delay', '-d', default=1, type=int)
parser.add_argument('--verbose', '-v', default=True)
parser.add_argument('--output', '-o', default=None)
parser.add_argument('--ip', '-i', default='', type=str)

argsc = parser.parse_args()

if argsc.ip != '':
    ips = [argsc.ip]
else:
    with open(argsc.filename, 'r') as f:
        ips = [line.strip() for line in f]

ipInfo = {}
bad_ips = []
counter = 0
err_count = 0
total_ips = len(ips)
for ip in ips:
    counter += 1
    progress = (counter / total_ips) * 100
    if argsc.verbose:
        print(f'[INFO] - fetching host {ip}, progress: {progress:.1f}%')
    try:
        time.sleep(argsc.delay)
        hostinfo = api.host(ip)
        ipInfo[ip] = hostinfo
    except shodan.APIError as e:
        err_msg = f'[ERROR] - fetching host {ip}: {e}'
        bad_ips.append(err_msg)
        ipInfo[ip] = '{}'.format(e) 
        err_count += 1
        if argsc.verbose:
            print(err_msg)
result_len = len(ipInfo)
success_ip = result_len - err_count
script_time = datetime.now().strftime("%Y%m%d%H%M%S")
ofname=f'shodan_results_{script_time}'
if argsc.output != None:
    ofname = argsc.output
#save .json of the results
with open(f'./output/{ofname}.json', 'w') as of:
    of.write(json.dumps(ipInfo))
print(f'\nSuccesfully processed {success_ip} out of {total_ips} IP addresses, {err_count} returned no data')
print(f'output written to \"output/{ofname}.json\"')

#convert to xlsx with IP, Organization, ISP, County code, Domains and Hostnames columns
print("\nParsing common fields into XLSX file...")

#define list for conversion into excel data
ip_data_list = []

print(f'[INFO] - fetching abuse emails, please wait... ')
counter = 0
for ip_address, ip_data in ipInfo.items():
    counter += 1
    progress = (counter / total_ips) * 100
    print(f'[INFO] - progress: {progress:.1f}%', end='\r')
    try:
        whois_data = whois.whois(ip_address)
        abuse_mail = whois_data.get('emails', 'Unknown') or 'Unknown'
    except Exception as e:
        print(f"An error occurred fetching abuse email for {ip_address}: {e}")
        abuse_mail = 'Unavailable'
    # Check if ip_data is a proper dictionary before attempting to use 'get'
    if isinstance(ip_data, dict):
        organization = ip_data.get('org', '-') or '-'
        isp = ip_data.get('isp', '-') or '-'
        country_code = ip_data.get('country_code', '-') or '-'
        domains = ip_data.get('domains', '-') or '-'
        hostnames = ip_data.get('hostnames', '-') or '-'
    else:
        organization = 'NoData'
        isp = 'NoData'
        country_code = 'NoData'
        domains = 'NoData'
        hostnames = 'NoData'
    ip_data_list.append({'IP': ip_address, 'Abuse': abuse_mail, 'Organization': organization, 'ISP': isp, 'Country Code': country_code, 'Domains': domains, 'Hostnames': hostnames})

print()
# Convert the list to a DataFrame
ip_data_df = pd.DataFrame(ip_data_list)
# Save the DataFrame to an Excel file
ip_data_df.to_excel(f'./output/{ofname}.xlsx', index=False)
print(f'Done, results saved to \"output/{ofname}.xlsx\"')
if bad_ips:
    with open(f'./output/{ofname}.txt', 'w') as f:
        for message in bad_ips:
            f.write(f"{message}\n")
    print(f'\nIPs with errors saved to \"output/{ofname}.txt\"')
