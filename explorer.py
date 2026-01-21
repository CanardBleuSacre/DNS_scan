from config import (resolver, record_types, visited_domains, visited_ips, excluded_domains)
from dns_tools.__init__ import (parse_txt, crawl_tld, scan_srv, reverse_dns, ip_voisines, brute_sub)

def doit_explore(domain):
    '''
    Vérifie si un domaine doit être exploré en fonction de la liste des exclusions.
    '''
    for excluded in excluded_domains:
        if domain.endswith(excluded) or domain == excluded:
            return False
    return True

def explore(domain, tree, depth, max_depth, progress=None, task=None):
    '''
    Explore récursivement les enregistrements DNS d'un domaine donné
    jusqu'à une profondeur maximale spécifiée, en construisant un arbre
    de résultats avec Rich.
    '''
    if depth>max_depth or domain in visited_domains: return
    visited_domains.add(domain)
    
    if progress and task is not None:
        progress.update(task, advance=1, description=f"[cyan]Exploration : {domain}[/cyan]")

    for rtype in record_types:
        branch = tree.add(f"[cyan]{rtype}[/cyan]")
        
        try:
            for r in resolver.resolve(domain,rtype):
                val = r.to_text()
                branch.add(val)

                new_domains = set()
                new_ips = set()
                if rtype in ("A","AAAA"):
                    new_ips.add(val)
                if rtype=="MX":
                    new_domains.add(val.split()[-1].rstrip("."))
                if rtype=="CNAME":
                    new_domains.add(val.rstrip("."))
                if rtype=="SOA":
                    new_domains.add(val.split()[0].rstrip("."))
                if rtype=="TXT":
                    d,i=parse_txt(domain)
                    new_domains|=d
                    new_ips|=i

                for d in new_domains:
                    explore(d, tree.add(f"[green]{d}[/green]"), depth+1, max_depth, progress, task)
                
                for ip in new_ips:
                    if ip not in visited_ips:
                        visited_ips.add(ip)
                        ip_branch = tree.add(f"[yellow]{ip}[/yellow]")

                        for rd in reverse_dns(ip):
                            explore(rd, ip_branch.add(f"[magenta]{rd}[/magenta]"), depth+1,max_depth, progress, task)
                        
                        for nb in ip_voisines(ip):
                            explore(nb, ip_branch.add(f"[magenta]{nb}[/magenta]"), depth+1,max_depth, progress, task)

        except:
            branch.add("[red]aucune donnée[/red]")
    
    try:
        dmarc_domain = f"_dmarc.{domain}"
        for r in resolver.resolve(dmarc_domain, "TXT"):
            txt = " ".join(s.decode() for s in r.strings)
            from dns_tools.dns_parsing_spe import parse_dmarc
            new_domains |= parse_dmarc(txt)
    except:
        pass

    for p in crawl_tld(domain):
        explore(p, tree.add(f"[blue]parent → {p}[/blue]"), depth+1,max_depth, progress, task)
    
    for s in scan_srv(domain):
        explore(s, tree.add(f"[purple]SRV → {s}[/purple]"), depth+1,max_depth, progress, task)
    
    for sb in brute_sub(domain):
        explore(sb, tree.add(f"[white]sub → {sb}[/white]"), depth+1,max_depth, progress, task)