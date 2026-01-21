from config import resolver, srv_services, common_subdomains

def scan_srv(domain):
    '''
    Recherche les enregistrements SRV pour un domaine donné
    en utilisant une liste de services SRV courants.
    '''
    f = set()
    for s in srv_services:
        try:
            for r in resolver.resolve(f"{s}.{domain}","SRV"):
                f.add(str(r.target).rstrip("."))
        except: pass
    return f 

def brute_sub(domain):
    '''
    Effectue une recherche de sous-domaines en utilisant une liste
    de sous-domaines courants.
    '''
    found = set()
    for s in common_subdomains:
        try:
            resolver.resolve(f"{s}.{domain}","A")
            found.add(f"{s}.{domain}")
        except: pass
    return found