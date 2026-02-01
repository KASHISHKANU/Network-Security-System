import sys
from networksecurity.logging.logger import logger

class NetworkSecurityException(Exception):
    """Base exception class for Network Security System."""
    def __init__(self,error_message,error_detail:sys):
        self.error_message = error_message
        self.error_detail = error_detail
        _,  _, exc_tb = self.error_detail.exc_info()
        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        print("Exception occurred python script name : [{0}] at line number: [{1}] with message: [{2}]".format(
            self.file_name, self.line_number, str(self.error_message)
        ))

       