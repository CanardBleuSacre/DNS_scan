import sys
import dns.resolver
from rich.console import Console
from rich.tree import Tree
import re

console = Console()
record_types = ["A", "AAAA", "MX", "TXT", "CNAME"]
common_subdomains = ["www", "mail", "ftp", "api", "dev", "test", "ns1", "ns2"]

domain_regex = (
    rf"(?:[a-z0-9_]"
    rf"(?:[a-z0-9-_]{{0,61}}"
    rf"[a-z0-9_])?\.)"
    r"+[a-z0-9][a-z0-9-_]{0,61}"
    rf"[a-z]\.?"
)

visited_domains = set()

if len(sys.argv) < 2:
    domain = input("Entrez un nom de domaine : ").strip()
    domains = [domain]
else:
    domains = sys.argv[1:]

while domains:
    domain = domains.pop(0)
    if domain in visited_domains:
        continue
    visited_domains.add(domain)

    tree = Tree(f"[bold green]{domain}[/bold green]")

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            
            for rdata in answers:
                text = rdata.to_text()
                branch = tree.add(f"[cyan]{rtype}[/cyan]")
                
                new_domains = set()

                if rtype == "MX":
                    parts = text.split()
                    if len(parts) == 2:
                        new_domains.add(parts[1].rstrip("."))

                elif rtype == "TXT":
                    found = re.findall(domain_regex, text, flags=re.IGNORECASE)
                    for d in found:
                        new_domains.add(d.rstrip("."))
                
                base_parts = domain.split('.')
                if len(base_parts) >= 2:
                    base_domain = ".".join(base_parts[-2:])  # ex: example.com
                    for sub in common_subdomains:
                        new_domains.add(f"{sub}.{base_domain}")
                
                for nd in new_domains:
                    if nd not in visited_domains and nd != domain:
                        domains.append(nd)
        
        except dns.resolver.NoAnswer:
            branch.add("[red]aucune donnée[/red]")
        except dns.resolver.NXDOMAIN:
            branch.add("[red]domaine inexistant[/red]")
        except Exception as e:
            branch.add(f"[red]erreur : {e}[/red]")

    console.print(tree)