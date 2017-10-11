from ipware.ip import get_ip
import logging

logger=logging.getLogger('user_data')

def IPCatcher(request):
    ip = get_ip(request)
    if ip is not None:
        print("We have an IP address for user")
        print(ip)
        logging.info('User data is being collected')

    else:
        print("we don't have an IP address for user")
