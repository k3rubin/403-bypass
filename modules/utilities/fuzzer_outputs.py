# TODO: Use OOP for these functions - i.e. put them in a class which can be inherited
# Change return to print if output does not work
def url_fuzzer_output(full_url, status_code):
    if (status_code != '404'):
        return full_url + ' : ' + str(status_code)

def http_method_fuzzer_output(full_url, status_code, method):
    if (status_code != '404'):
        return full_url +  ' : ' + 'Using '+ method + ': ' + str(status_code)

def header_fuzzer_output(full_url, status_code, payload_key, payload_value):
    if (status_code != '404'):
        return full_url + ' :  (' + payload_key + ': ' + payload_value + ') : ' + str(status_code)
    