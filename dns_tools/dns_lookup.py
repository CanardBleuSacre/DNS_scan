import dns.reversename
from ipaddress import ip_address
from config import resolver, ip_range

def reverse_dns(ip):
    '''
    Effectue une recherche DNS inversée pour une adresse IP donnée.
    '''
    try: 
        return [str(a).rstrip(".") for a in resolver.resolve(dns.reversename.from_address(ip),"PTR")]
    except: return []

def ip_voisines(ip):
    '''
    Trouve les adresses IP voisines dans une plage définie autour de l'IP
    donnée et effectue une recherche DNS inversée sur chacune d'elles.
    '''
    res, base = set(), int(ip_address(ip))
    for o in range(-ip_range,ip_range+1):
        if o==0: continue
        try: 
            res |= set(reverse_dns(str(ip_address(base+o))))
        except: pass
    return res