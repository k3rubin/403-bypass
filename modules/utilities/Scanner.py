class Scanner:
    def __init__(self, url, status_code):
        self.url = url
        self.status_code = status_code

    def output(self, message=" : "):
        if (self.status_code != '404'):
            print(self.url +  message + self.status_code)