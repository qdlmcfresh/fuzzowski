from fuzzowski.monitors.imonitor import IMonitor
from fuzzowski.connections import ITargetConnection

http_request = b"GET / HTTP/1.1\r\n\r\n"

class httpMonitor(IMonitor):
    

    @staticmethod
    def name() -> str:
        return "httpMon"

    @staticmethod
    def help():
        return "Sends a HTTP request to the target and check the response"

    def test(self):
        conn = self.get_connection_copy()
        result = self.send_http_request(conn)
        return result


    def send_http_request(self, conn: ITargetConnection):
        result = False
        try:
            conn.open()
            conn.send(http_request)
            response = conn.recv_all(10000)
            if len(response) > 0:
                result = True
        except Exception as e:
            self.logger.log_error(f"Exception while receiving: {type(e).__name__}. {str(e)}")
        finally:
            conn.close()
        return result

