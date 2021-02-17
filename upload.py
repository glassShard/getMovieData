from ftplib import FTP


class Upload:
    def __init__(self):
        self.URL = 'ftpx.forpsi.com'
        self.PASSWORD = 'xxx'
        self.USERNAME = 'xxx'

    def upload_file(self, provider):
        ftp = FTP(self.URL)
        ftp.login(self.USERNAME, self.PASSWORD)
        ftp.cwd('www/filmkereso')
        file = open(f'{provider}-movies.json', 'rb')
        ftp.storbinary(f'STOR {provider}-movies.json', file)
        file.close()
        ftp.quit()
