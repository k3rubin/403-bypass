# TODO: Use OOP for these functions - i.e. put them in a class which can be inherited
def url_fuzzer_output(full_url, status_code):
    if (status_code != '404'):
        print(full_url + ' : ' + str(status_code))

def http_method_fuzzer_output(full_url, status_code, method):
    if (status_code != '404'):
        print(full_url +  ' : ' + 'Using '+ method + ': ' + str(status_code))