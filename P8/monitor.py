from pathlib import Path
import time
import getpass
import os
import socket

SERVER_NAME = "127.0.0.1"
SERVER_PORT = 21
SERVER_ENCODING = "latin-1"
MAX_BUFFER_SIZE = 8192

IS_CONSTANT = True
WAIT_TIME = 10

def get_transfer_host_and_port(resp):
    import re as regular_expr
    conn_expr = regular_expr.compile(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', regular_expr.ASCII)
    m = conn_expr.search(resp)
    number_set = m.groups()
    host = '.'.join(number_set[:4])
    #print(host)
    port = (int(number_set[4]) << 8) + int(number_set[5])
    #print(port)
    return host, port


def send(socket, message, line_end=True, log_events=False):
    if log_events:
        print("[Sending Message] {}".format(message))
    suffix = "\r\n" if line_end else ""
    socket.sendall(bytearray((message + suffix).encode()))
    recv = socket.recv(1024)
    if log_events:
        print("[Received Response] {}".format(recv))
    return recv


def monitor(directory_path, username, password, callback=print):
    file_dict = {}

    while True:
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):  # Check if it's a file
                    if file_path not in file_dict:
                        file_dict[file_path] = os.path.getmtime(file_path)
                    else:
                        current_timestamp = os.path.getmtime(file_path)
                        if current_timestamp > file_dict[file_path]:
                            file_dict[file_path] = current_timestamp
                            callback(directory_path, file_path, username, password)

        time.sleep(1)



def update_file(directory_path, file_path, username, password):
    CLIENT_SOCKET = socket.create_connection((SERVER_NAME, SERVER_PORT))
    header = CLIENT_SOCKET.recv(1024)
    send(CLIENT_SOCKET, "USER {}".format(username))
    send(CLIENT_SOCKET, "PASS {}".format(password))

    resp = header.decode()
    if resp.startswith("530"):
        raise ValueError("Invalid username or password")

    send(CLIENT_SOCKET, "TYPE I")

    transfer_resp = send(CLIENT_SOCKET, "PASV")
    transfer_host, transfer_port = get_transfer_host_and_port(str(transfer_resp))
    transfer_socket = socket.create_connection((transfer_host, transfer_port))

    file_name = os.path.basename(file_path)
    send(CLIENT_SOCKET, "STOR {}".format(file_name))

    with transfer_socket:
        conn = transfer_socket.makefile('wb')
        fp = open(file_path, 'rb')
        buf = fp.read(MAX_BUFFER_SIZE)
        conn.write(buf)
        fp.close()

    send(CLIENT_SOCKET, "UPDATE {}".format(file_name))

    send(CLIENT_SOCKET, "QUIT")


# MAIN PROGRAM
# Prompt for FTP server credentials
USER = str(input("Server User: "))
PASS = str(getpass.getpass("Server Password: "))

# Check FTP server connection and credentials
try:
    tester = socket.create_connection((SERVER_NAME, SERVER_PORT))
    tester.recv(1024)
    send(tester, "USER {}".format(USER))
    res = str(send(tester, "PASS {}".format(PASS)))
    valid = "530" not in res
    if not valid:
        raise Exception
except Exception as e:
    exit("[Connection Unsuccessful: Server: {} Port: {} | @{}]".format(SERVER_NAME, SERVER_PORT, USER))
print("[Connection Successful: Server: {} Port: {} | @{}]".format(SERVER_NAME, SERVER_PORT, USER))

DIRECTORY_PATH = str(input("Choose the directory to track: "))
try:
    # Check if the directory exists
    if not os.path.isdir(DIRECTORY_PATH):
        raise Exception
except Exception as e:
    exit("[The directory <{}> does not exist]".format(DIRECTORY_PATH))

monitor(DIRECTORY_PATH, USER, PASS, update_file)