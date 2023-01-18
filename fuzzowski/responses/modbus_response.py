from .response import Response
from typing import Mapping
import pprint
import struct

class ModbusResponse(Response):
    ERROR_CODES = {
        1: 'Illegal function',
        2: 'Illegal data address',
        3: 'Illegal data value',
        4: 'Slave device failure',
        5: 'Acknowledge',
        6: 'Slave device busy',
        7: 'Negative acknowledge',
        8: 'Memory parity error',
        10: 'Gateway path unavailable',
        11: 'Gateway target device failed to respond',
    }       


    def __init__(self, name, required_vars, optional_vars):
        super().__init__(name, required_vars, optional_vars)

    def _extract_variables(self, data):
        trans_id, proto_id, length, unit_id, function_code = struct.unpack('>HHHBB', data[:8])
        response_vars = {
            'trans_id': trans_id,
            'proto_id': proto_id,
            'length': length,
            'unit_id': unit_id,
            'function_code': function_code
        }
        # Check if error bit is set
        if function_code & 0x80 == 0x80:
            response_vars['error_code'] = data[8]
            return response_vars
        else:
            response_vars['data'] = data[8:]
        return response_vars
    
    def _parse_request(self, data: bytes, vars_set=Mapping[str, bytes]) -> str:
        """
        Parse the request, and returns a comprehensive response. When this function is called, the variables have been
        already extracted in self.vars
        This method should be overriden to return more comprehensive responses
        Args:
        data: The response bytes
        vars_set: The set variables (is the same as

        Returns: A string with the parsed variables
        """
        if vars_set.get('error_code') is not None:
            return f'Error code: {vars_set.get("error_code")}' + " - " + self.ERROR_CODES.get(vars_set.get('error_code'), "Unknown error code")
        else:
            return '\n' + pprint.pformat(vars_set) + '\n'
        