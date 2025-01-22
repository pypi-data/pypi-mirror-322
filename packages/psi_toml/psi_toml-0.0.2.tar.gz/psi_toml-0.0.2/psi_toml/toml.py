"""A module to replace tomli and tomli_w for simple cases."""
import re
# from icecream import ic

from ._version import __version__

version = __version__

valid_keys_re = [
    r'^[A-Za-z0-9_-]{1,}$',
    r'^".{1,}"$',
    r"^'.{1,}'$",
]

valid_table_re = [
    r'^\[\w{1,}\]$',
    r'^\["\w{1,}"]$',
    r"^\['\w{1,}']$",
]

valid_equals_re = [
    r'^\w{1,}=\w{1,}$',
    r'^\w{1,}\s{0,}=\s{0,}\w{0,}\s{0,}"\w{0,}\s{0,}=\w{0,}"',
    r"^\w{1,}\s{0,}=\s{0,}\w{0,}\s{0,}'\w{0,}\s{0,}=\w{0,}'",
]

quoted_hash_re = [
    r"\w{0,}'\w{0,}#\w{0,}'\w{0,}",
    r'\w{0,}"\w{0,}#\w{0,}"\w{0,}',
]

valid_number_re = r'^-{0,1}[0-9]{0,}\.{0,1}[0-9]{0,}$'

multi_line_re = r'^\"{3}.{0,}\"{3}$'


class TOMLDecodeError(Exception):
    """Exception raised for custom error in the application."""

    def __init__(self, message: str = '') -> None:
        super().__init__(message)

    def __str__(self):
        return f'TOMLDecodeError: {self.message}'


def load(file_handle) -> list:
    """Read and parse a text file and return a dict."""
    try:
        text = file_handle.read()
        return parse(text.split('\n'))
    except Exception as err:
        raise Exception(err.args[0])


def dump(dict: dict, file_handle) -> None:
    """Write dict in TOML format."""
    try:
        text = _dict_to_list(dict)
        file_handle.write(text)
    except Exception as err:
        raise Exception(err.args[0])


def parse(data: list) -> dict:
    result = {}
    for line, text in enumerate(data):
        try:
            (key, item) = _parse(line, text)
            if key:
                if key in result:
                    raise TOMLDecodeError(
                        f'Multiple key defined: line {line+1}')
                result[key] = item
        except TOMLDecodeError as err:
            raise TOMLDecodeError(err.args[0])
    return result


def _parse(line: int, text: str) -> tuple:
    (key, item) = ('', '')
    if not text:
        return (key, item)

    # Comments
    if text[0] == '#':
        return (key, item)
    if '#' in text:
        for test in quoted_hash_re:
            if re.search(test, text):
                break
        else:  # after or no break
            text = text[:text.index('#')]

    # Tables
    if '[' in text or ']' in text or '=' not in text:
        _validate_tables(line, text)

    # Standard items
    if '=' in text:
        if text.count('=') > 1:
            _validate_equals(line, text)
        index = text.index('=')
        key = _get_key(line, text[:index])
        item = _get_item(line, text[index+1:].strip())
    return (key, item)


def _get_key(line: int, key: str) -> str:
    key = key.strip()
    for test in valid_keys_re:
        if re.search(test, key):
            break
    else:  # after or no break
        raise TOMLDecodeError(f'Invalid key definition: line {line+1}')
    key = key.replace('"', '')
    key = key.replace("'", '')
    return key


def _get_item(line: int, item: str) -> str:
    if not item:
        raise TOMLDecodeError(f'Invalid value definition: line {line+1}')

    item = item.strip()
    if re.search(multi_line_re, item):
        item = item.replace('"""', '')
    if (item[0] == '"' and item[-1] == '"'
            or item[0] == "'" and item[-1] == "'"):
        item = item[1:-1]
        return item
    if re.search(valid_number_re, item):
        if '.' in item:
            return float(item)
        return int(item)
    if item == 'true':
        return True
    if item == 'false':
        return False
    return item


def _validate_equals(line: int, text: str) -> None:
    for test in valid_equals_re:
        if re.search(test, text):
            break
    else:  # after or no break
        raise TOMLDecodeError(f'Invalid equals definition: line {line+1}')


def _validate_tables(line: int, text: str) -> None:
    for test in valid_table_re:
        if re.search(test, text):
            break
    else:  # after or no break
        raise TOMLDecodeError(f'Invalid table definition: line {line+1}')


def _dict_to_list(dict) -> str:
    toml = []
    for key, item in dict.items():
        if isinstance(item, str):
            item = f'"{item}"'
        elif item is True:
            item = 'true'
        elif item is False:
            item = 'false'
        toml.append(f'{key} = {item}')
    return '\n'.join(toml)
