import urllib.request

def get_tld_list():
    """Télécharge la liste TLD ou utilise fallback"""
    try:
        with urllib.request.urlopen("https://data.iana.org/TLD/tlds-alpha-by-domain.txt", timeout=3) as response:
            content = response.read().decode('utf-8')
            tlds = set(line.strip().lower() for line in content.splitlines()[1:])
            return tlds
    except: 
        return {"com", "net", "org", "fr", "edu", "gov", "co.uk", "gouv.fr"}

known_tlds = get_tld_list()