import os
import sys
import socket
import getpass

def get_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    if ip[:2] != "10":
        return "172.17.0.1"
    else:
        if ip.split(".")[2] == "0":
            return "10.10.0.1"
        elif ip.split(".")[2] == "1":
            return "10.10.1.1"


def cmd():
    args = sys.argv
    username = getpass.getuser()
    if len(args) == 1:
        status = os.system("curl http://"+get_ip()+":8080?username="+username)
    elif args[-1] == "gpu":
        gpu()
    elif args[-1] == "top":
        status = os.system("curl http://"+get_ip()+":8080/top?username="+username)
    elif args[-1] == "topall":
        status = os.system("curl http://"+get_ip()+":8080/top_all?username="+username)
    elif args[-1] == "query":
        status = os.system("curl http://"+get_ip()+":8080/query?username="+username)
    elif args[-1] == "notify":
        notify()
    elif args[-1] == "restart":
        restart()
    else:
        print("Usage: ids [(Null)|top|topall|notify|query|gpu]")

def restart():
    username = getpass.getuser()
    print("Do you really want to restart your current docker container? Please make sure you have saved your work (y/n): ", end="")
    ans = input()
    if ans == "y":
        print("This operation is irreversible. Are you sure to restart your current docker container? (y/n): ", end="")
        ans = input()
        if ans == "y":
            status = os.system("curl http://"+get_ip()+":8080/restart?username="+username)
            print("Your current docker container is restarting. Please wait for a while.")

def gpu():
    notify()

def notify():
    username = getpass.getuser()
    print("Do you really want to notify other users to free up GPU resources? (y/n): ", end="")
    ans = input()
    if ans == "y":
        status = os.system("curl http://"+get_ip()+":8080/gpu_notify?username="+username)


def top():
    username = getpass.getuser()
    status = os.system("curl http://"+get_ip()+":8080/top?username="+username)


def topall():
    username = getpass.getuser()
    status = os.system("curl http://"+get_ip()+":8080/top_all?username="+username)


def query():
    username = getpass.getuser()
    status = os.system("curl http://"+get_ip()+":8080/query?username="+username)

if __name__ == "__main__":
    cmd()