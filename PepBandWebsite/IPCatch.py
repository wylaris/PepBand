from ipware.ip import get_ip
# import logging

def IPCatcher(request):
    ip = get_ip(request)
    if ip is not None:
        print("We have an IP address for user")
        print(ip)
        # logger=logging.getLogger("log_recording.txt")

    else:
        print("we don't have an IP address for user")
