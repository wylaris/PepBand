from ipware.ip import get_ip
import logging

logger=logging.getLogger('user_data')

def IPCatcher(request):
    ip = get_ip(request)
    if ip is not None:
        logging.info('User data is being collected for' + ip)

    else:
        pass
        print("we don't have an IP address for user")
