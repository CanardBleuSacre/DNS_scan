from config import resolver, srv_services, common_subdomains

def scan_srv(domain):
    f = set()
    for s in srv_services:
        try:
            for r in resolver.resolve(f"{s}.{domain}","SRV"):
                f.add(str(r.target).rstrip("."))
        except: pass
    return f 

def brute_sub(domain):
    found = set()
    for s in common_subdomains:
        try:
            resolver.resolve(f"{s}.{domain}","A")
            found.add(f"{s}.{domain}")
        except: pass
    return found