from fuzzowski.fuzzers.ifuzzer import IFuzzer
from fuzzowski.mutants.spike import *
from fuzzowski import *
from fuzzowski import Session

class HTTP(IFuzzer):
    """
    HTTP Fuzzing Module
    @Author: https://github.com/qdlmcfresh
    Based on https://github.com/jtpereyda/boofuzz-http
    """

    name = 'http'

    @staticmethod
    def get_requests() -> List[callable]:
        return [HTTP.requests]

    @staticmethod
    def define_nodes(*args, **kwargs) -> None:
        s_initialize(name="Request")
        with s_block("Request_Line"):
            s_group("Method", ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE'])
            s_delim(" ", name='space_1')
            s_string("/index.html", name='Request_URI')
            s_delim(" ", name='space_2')
            s_string('HTTP/1.1', name='HTTP_Version')
            s_static("\r\n", name="Request_Line_CRLF")
        s_static("\r\n", "Request_CRLF")
    
    @staticmethod
    def requests(session: Session) -> None:
        session.connect(s_get("Request"))
