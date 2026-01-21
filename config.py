import dns.resolver
from rich.console import Console

console = Console()
resolver = dns.resolver.Resolver()

record_types = ["A", "AAAA", "MX", "TXT", "CNAME", "SOA"]
common_subdomains = ["www", "mail", "ftp", "api", "dev", "test", "ns1", "ns2"]
srv_services = ["_sip._tcp","_sip._udp","_ldap._tcp","_xmpp-server._tcp","_xmpp-client._tcp"]
known_tlds = ["com","net","org","fr","edu","gouv.fr","co.uk"]

domain_regex = (
    rf"(?:[a-z0-9_]"
    rf"(?:[a-z0-9-_]{{0,61}}"
    rf"[a-z0-9_])?\.)"
    r"+[a-z0-9][a-z0-9-_]{0,61}"
    rf"[a-z]\.?"
)
ip_regex = (
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)
excluded_domains = {
    "microsoft.com",
    "akamai.net",
    "cloudflare. com",
    "fastly.net",
    "amazonaws.com",
    "azure.com",
    "googleusercontent.com",
    "gstatic.com",
    "office. com",
    "outlook.com",
}

visited_domains = set()
visited_ips = set()
ip_range = 1