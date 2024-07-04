#!/usr/bin/env python3
""" modules filters log messages """
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
