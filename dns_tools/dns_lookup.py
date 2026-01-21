import dns.reversename
from ipaddress import ip_address, AddressValueError
from config import resolver, ip_voisines_range, ip_voisines_max_fails

def reverse_dns(ip):
    '''
    Effectue une recherche DNS inversée pour une adresse IP donnée.
    '''
    try: 
        return [str(a).rstrip(".") for a in resolver.resolve(dns.reversename.from_address(ip),"PTR")]
    except: return []

def ip_voisines(ip, aggressive=False):
    res = set()
    
    try: 
        base = int(ip_address(ip))
    except (AddressValueError, ValueError):
        return res
    
    ranges_to_use = ip_voisines_range if aggressive else ip_voisines_range[:2]
    
    for max_range in ranges_to_use:  
        consecutive_fails = 0
        found_in_range = False
        
        for offset in range(1, max_range + 1):
            found_in_iteration = False
            
            for direction in [offset, -offset]:
                try: 
                    neighbor_ip = str(ip_address(base + direction))
                    domains = reverse_dns(neighbor_ip)
                    
                    if domains:
                        res.update(domains)
                        found_in_iteration = True
                        found_in_range = True
                        consecutive_fails = 0
                    
                except (AddressValueError, OverflowError):
                    pass
            
            if not found_in_iteration:  
                consecutive_fails += 1
                
                if consecutive_fails >= ip_voisines_max_fails:
                    break
        
        if not found_in_range and not aggressive:
            break
    
    return res