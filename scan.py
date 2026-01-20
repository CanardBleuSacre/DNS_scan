import sys
import dns.resolver
import dns.reversename
from ipaddress import ip_address
from rich.console import Console
from rich.tree import Tree
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
import re

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

visited_domains = set()
visited_ips = set()
ip_range = 1

def parse_txt(domain):
    d, i = set(), set()
    try:
        for r in resolver.resolve(domain,"TXT"):
            t = " ".join(s.decode() for s in r.strings)
            d |= set(re.findall(domain_regex,t))
            i |= set(re.findall(ip_regex,t))
    except: pass
    return d,i

def crawl_tld(domain):
    parts, parents = domain.split("."), []
    for i in range(1,len(parts)):
        cand = ".".join(parts[i:])
        if cand in known_tlds: break
        parents.append(cand)
    return parents

def scan_srv(domain):
    f = set()
    for s in srv_services:
        try:
            for r in resolver.resolve(f"{s}.{domain}","SRV"):
                f.add(str(r.target).rstrip("."))
        except: pass
    return f 

def reverse_dns(ip):
    try: 
        return [str(a).rstrip(".") for a in resolver.resolve(dns.reversename.from_address(ip),"PTR")]
    except: return []

def ip_voisines(ip):
    res, base = set(), int(ip_address(ip))
    for o in range(-ip_range,ip_range+1):
        if o==0: continue
        try: 
            res |= set(reverse_dns(str(ip_address(base+o))))
        except: pass
    return res

def brute_sub(domain):
    found = set()
    for s in common_subdomains:
        try:
            resolver.resolve(f"{s}.{domain}","A")
            found.add(f"{s}.{domain}")
        except: pass
    return found

def explore(domain, tree, depth, max_depth, progress=None, task=None):
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

    for p in crawl_tld(domain):
        explore(p, tree.add(f"[blue]parent → {p}[/blue]"), depth+1,max_depth, progress, task)
    
    for s in scan_srv(domain):
        explore(s, tree.add(f"[purple]SRV → {s}[/purple]"), depth+1,max_depth, progress, task)
    
    for sb in brute_sub(domain):
        explore(sb, tree.add(f"[white]sub → {sb}[/white]"), depth+1,max_depth, progress, task)

def main():
    if len(sys.argv) < 2:
        print("Usage: python scan.py [domain] [depth]")
        exit(1)

    start_domain = sys.argv[1].rstrip(".")
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    root = Tree(f"[bold red]{start_domain}[/bold red]")
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.completed}[/bold] domaines explorés"),
        TimeElapsedColumn()
    ) as progress:
        task = progress.add_task("Initialisation...", total=None)
        explore(start_domain, root, depth=0, max_depth=max_depth, progress=progress, task=task)
    console.print(root)

if __name__ == "__main__":
    main()