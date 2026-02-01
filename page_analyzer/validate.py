from urllib.parse import urlparse


def validate_url(url):
    if not url or len(url) > 255:
        return None
    parsed = urlparse(url)

    if not (parsed.scheme and parsed.netloc):
        return None
    if parsed.scheme.lower() not in ('http', 'https'):
        return 422
    return f"{parsed.scheme}://{parsed.netloc.lower()}"
