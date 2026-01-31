from urllib.parse import urlparse, urlunparse

def validate_url(url):
    if not url or len(url.strip()) >= 255:
        return None

    if not (url.startswith('http://') or url.startswith('https://')):
        return None

    try:
        parsed_url = urlparse(url.strip())
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc

        if not netloc:
            return None

        if netloc.startswith('www.'):
            netloc = netloc[4:]

        normalized = urlunparse((
            scheme,
            netloc.lower(),
            parsed_url.path.rstrip('/') if parsed_url.path != '/' else '/',
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment
        ))
        return normalized
    except (Exception):
        return None

