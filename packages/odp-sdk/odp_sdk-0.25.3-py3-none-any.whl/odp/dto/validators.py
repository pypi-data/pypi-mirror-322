import re

RX_RESOURCE_NAME = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9\-_.]*")
RX_RESOURCE_KIND = re.compile(r"^(?:[a-zA-Z0-9][a-zA-Z0-9\-_\.]*)\/(?:[a-zA-Z0-9][a-zA-Z0-9\-_\.]*)$")
RX_RESOURCE_VERSION = re.compile(r"^v[0-9]+(?:(?:alpha|beta)[0-9]+)?$")


def validate_resource_version(val: str) -> str:
    if not RX_RESOURCE_VERSION.fullmatch(val):
        raise ValueError(f"Invalid resource version: {val}")
    return val


def validate_resource_kind(val: str) -> str:
    if not RX_RESOURCE_KIND.fullmatch(val):
        raise ValueError(f"Invalid resource kind: {val}")
    return val


def validate_resource_name(val: str) -> str:
    if not RX_RESOURCE_NAME.fullmatch(val):
        raise ValueError(f"Invalid resource component: {val}")
    return val
