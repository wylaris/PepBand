from ipware.ip import get_ip
import logging

logger=logging.getLogger('user_data')

def IPCatcher(request):
    ip = get_ip(request)
    if ip is not None:
        print("We have an IP address for user")
        print(ip)
        logging.basicConfig(filename='log_recording.txt',
                            level=logging.DEBUG,format='%(asctime)s %(message)s',
                                                              datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info('User data is being collected')

    else:
        print("we don't have an IP address for user")
