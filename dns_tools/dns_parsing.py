import re
from config import resolver, domain_regex, ip_regex, known_tlds
from dns_tools.dns_parsing_spe import parse_spf, parse_dmarc, is_spf, is_dmarc

def parse_txt(domain):
    '''
    Analyse les enregistrements TXT d'un domaine pour extraire les
    noms de domaine et les adresses IP qu'ils contiennent.
    '''
    d, i = set(), set()
    try:
        for r in resolver.resolve(domain,"TXT"):
            txt = " ".join(s.decode() for s in r.strings)
            if is_spf(txt):
                spf_domains, spf_ips = parse_spf(txt)
                d |= spf_domains
                i |= spf_ips
            elif is_dmarc(txt):
                d |= parse_dmarc(txt)
            else:
                d |= set(re.findall(domain_regex, txt))
                i |= set(re.findall(ip_regex, txt))
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