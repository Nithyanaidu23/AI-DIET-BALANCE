"""
Middleware to extract client metadata (IP, User-Agent, OS, Device, Browser) for audit logging.
"""
import re


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip or '127.0.0.1'


def parse_user_agent(ua_string: str) -> dict:
    """Parse User-Agent string to detect Browser, OS, and Device."""
    if not ua_string:
        return {'browser': 'Unknown Browser', 'os': 'Unknown OS', 'device': 'Desktop/Unknown'}

    ua_lower = ua_string.lower()

    # Browser detection
    if 'edg/' in ua_lower or 'edge/' in ua_lower:
        browser = 'Microsoft Edge'
    elif 'chrome/' in ua_lower and 'chromium/' not in ua_lower:
        browser = 'Google Chrome'
    elif 'firefox/' in ua_lower:
        browser = 'Mozilla Firefox'
    elif 'safari/' in ua_lower and 'chrome/' not in ua_lower:
        browser = 'Apple Safari'
    elif 'opera/' in ua_lower or 'opr/' in ua_lower:
        browser = 'Opera'
    else:
        browser = 'Other Browser'

    # OS detection
    if 'windows nt 10.0' in ua_lower:
        os_name = 'Windows 10/11'
    elif 'windows' in ua_lower:
        os_name = 'Windows'
    elif 'mac os x' in ua_lower:
        os_name = 'macOS'
    elif 'android' in ua_lower:
        os_name = 'Android'
    elif 'iphone' in ua_lower or 'ipad' in ua_lower:
        os_name = 'iOS'
    elif 'linux' in ua_lower:
        os_name = 'Linux'
    else:
        os_name = 'Unknown OS'

    # Device type detection
    if 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
        device = 'Mobile'
    elif 'ipad' in ua_lower or 'tablet' in ua_lower:
        device = 'Tablet'
    else:
        device = 'Desktop'

    return {'browser': browser, 'os': os_name, 'device': device}


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')
        parsed = parse_user_agent(ua)

        request.audit_meta = {
            'ip': ip,
            'user_agent': ua,
            'browser': parsed['browser'],
            'os': parsed['os'],
            'device': parsed['device'],
        }

        response = self.get_response(request)
        return response
