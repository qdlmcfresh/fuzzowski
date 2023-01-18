from .irestarter import IRestarter
from fuzzowski import FuzzLogger
from fuzzowski.loggers import FuzzLoggerText
from time import sleep
import urllib3

# Use with --restarter fritzhome "<host>" "<user>" "<password>" "<ain>" --restart-delay <delay>
class TasmotaRestarter(IRestarter):
    POWEROFF_REQUEST = "cm?cmnd=Power%20Off"
    POWERON_REQUEST = "cm?cmnd=Power%20On"

    def __init__(self, tasmota_host, *args, **kwargs):
        self.logger = FuzzLogger([FuzzLoggerText()])
        self.logger.log_info(f"Initializing TasmotaRestarter with host: {tasmota_host}")
        self.tasmota_host = tasmota_host
        self.http = urllib3.PoolManager()

    @staticmethod
    def name() -> str:
        return 'tasmota'

    @staticmethod
    def help():
        return 'Restart the target by toggling a Tasmota smart plug'

    def restart(self, *args, **kwargs) -> str or None:
        self.logger.log_info("Restarting target")
        r = self.http.request('GET', f'{self.tasmota_host}/{self.POWEROFF_REQUEST}')
        sleep(2)
        r = self.http.request('GET', f'{self.tasmota_host}/{self.POWERON_REQUEST}')
        sleep(2)
        return "Restarted target"
