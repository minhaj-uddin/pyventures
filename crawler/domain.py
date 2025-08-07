from urllib.parse import urlparse


def get_domain_name(url: str) -> str:
    try:
        parts = get_sub_domain_name(url).split('.')
        return '.'.join(parts[-2:]) if len(parts) >= 2 else ''
    except Exception:
        return ''


def get_sub_domain_name(url: str) -> str:
    try:
        return urlparse(url).netloc
    except Exception:
        return ''
