from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os;
import shutil;

class CustomFTPHandler(FTPHandler):
    def ftp_Store(self, file_path):
        filename = os.path.basename(file_path)
        #print("Filename: " + filename)

        backup_file_path = os.path.join(FTP_DIRECTORY, filename)
        #print("Backup File Path: " + backup_file_path)

        shutil.copy2(file_path, backup_file_path)
        
        self.respond("250 File updated successfully.")


FTP_PORT = 21
FTP_USER = "edwin"
FTP_PASSWORD = "admin"
FTP_DIRECTORY = "C:/xampp/htdocs/P8/backup/"
FTP_HOST_ADDRESS = "0.0.0.0"

FTP_MAX_CONNECTIONS = 10
FTP_MAX_CONNECTIONS_PER_IP = 5



def main():
    FTP_USER = str(input('Username: '))
    FTP_PASSWORD = str(input('Password: '))

    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')
    handler = FTPHandler
    handler.authorizer = authorizer

    handler.banner = "[Start of File Synchronisation]"
    address = (FTP_HOST_ADDRESS, FTP_PORT)

    server = FTPServer(address, handler)
    server.max_cons = FTP_MAX_CONNECTIONS
    server.max_cons_per_ip = FTP_MAX_CONNECTIONS_PER_IP

    server.serve_forever()

if __name__ == '__main__':
    main()