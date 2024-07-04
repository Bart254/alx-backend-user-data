#!/usr/bin/env python3
""" modules filters log messages """
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ obfuscates log message containing personal data

    Args:
        fields(List[str]): represents all fields to obfuscate
        redaction(str): represents by what the field will be obfuscated
        message: represents the log line
        separator: character separating each field in the log line

    Returns:
        str: obfuscated log message
    """
    pattern = '|'.join([f'({field}=[^{separator}]*)' for field in fields])
    return re.sub(pattern, lambda m: m.group(0).split('=')[0] +
                  f'={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ object initializion """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ formats record """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ returns logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


PII_FIELDS = ["name", "email", "phone", "ssn", "password"]
