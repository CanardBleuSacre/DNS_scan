import re
from config import resolver, domain_regex, ip_regex, known_tlds

def parse_txt(domain):
    '''
    Analyse les enregistrements TXT d'un domaine pour extraire les
    noms de domaine et les adresses IP qu'ils contiennent.
    '''
    d, i = set(), set()
    try:
        for r in resolver.resolve(domain,"TXT"):
            t = " ".join(s.decode() for s in r.strings)
            d |= set(re.findall(domain_regex,t))
            i |= set(re.findall(ip_regex,t))
    except: pass
    return d,i

def crawl_tld(domain):
    '''
    identifie les domaines parents en supprimant les sous-domaines
    jusqu'à atteindre un TLD connu.
    '''
    parts, parents = domain.split("."), []
    for i in range(1,len(parts)):
        cand = ".".join(parts[i:])
        if cand in known_tlds: break
        parents.append(cand)
    return parents