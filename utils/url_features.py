from urllib.parse import urlparse
import re
import ipaddress


def extract_url_features(url):
    """
    Extract URL-based features for phishing detection.
    Returns a list of 18 numeric features.
    """

    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    domain = parsed.netloc
    path = parsed.path
    query = parsed.query

    # Remove port
    domain = domain.split(":")[0]

    # 1. URL length
    url_length = len(url)

    # 2. Domain length
    domain_length = len(domain)

    # 3. Path length
    path_length = len(path)

    # 4. Number of dots
    dot_count = url.count(".")

    # 5. Number of hyphens
    hyphen_count = url.count("-")

    # 6. Number of special characters
    special_chars = len(re.findall(r"[^a-zA-Z0-9]", url))

    # 7. Number of digits
    digit_count = sum(c.isdigit() for c in url)

    # 8. Number of subdomains
    subdomain_count = max(domain.count(".") - 1, 0)

    # 9. HTTPS
    is_https = 1 if parsed.scheme == "https" else 0

    # 10. IP address
    try:
        ipaddress.ip_address(domain)
        has_ip = 1
    except ValueError:
        has_ip = 0

    # 11. @ symbol
    has_at = 1 if "@" in url else 0

    # 12. Double slash
    has_double_slash = 1 if "//" in parsed.path else 0

    # 13. Suspicious keywords
    suspicious_words = [
        "login",
        "signin",
        "verify",
        "verification",
        "account",
        "secure",
        "security",
        "update",
        "password",
        "bank",
        "paypal",
        "confirm",
        "authenticate",
        "wallet",
        "credential"
    ]

    lower_url = url.lower()

    suspicious_keyword_count = sum(
        1 for word in suspicious_words if word in lower_url
    )

    # 14. URL contains query
    has_query = 1 if query else 0

    # 15. URL contains fragment
    has_fragment = 1 if parsed.fragment else 0

    # 16. Number of path segments
    path_segments = len([x for x in path.split("/") if x])

    # 17. Number of query parameters
    query_parameters = len(query.split("&")) if query else 0

    # 18. Long domain indicator
    long_domain = 1 if domain_length > 30 else 0

    features = [
        url_length,
        domain_length,
        path_length,
        dot_count,
        hyphen_count,
        special_chars,
        digit_count,
        subdomain_count,
        is_https,
        has_ip,
        has_at,
        has_double_slash,
        suspicious_keyword_count,
        has_query,
        has_fragment,
        path_segments,
        query_parameters,
        long_domain
    ]

    return features