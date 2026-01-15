import sys
import dns.resolver
from rich.console import Console
from rich.table import Table
import re

console = Console()
record_types = ["A", "AAAA", "MX", "TXT"]

DOMAIN_REGEX = (
    rf"(?:[a-z0-9_]"
    rf"(?:[a-z0-9-_]{{0,61}}"
    rf"[a-z0-9_])?\.)"
    r"+[a-z0-9][a-z0-9-_]{0,61}"
    rf"[a-z]\.?"
)

if len(sys.argv) < 2:
    domain = input("Entrez un nom de domaine : ").strip()
    domains = [domain]
else:
    domains = sys.argv[1:]
visited = set()

while domains:
    domain = domains.pop(0)
    if domain in visited:
        continue
    visited.add(domain)

    console.rule(f"Résultats DNS pour [bold green]{domain}[/bold green]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan", width=6)
    table.add_column("Résultat")

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            
            for rdata in answers:
                text = rdata.to_text()
                table.add_row(rtype, rdata.to_text())
                
                new_domains = set()

                if rtype == "MX":
                    parts = text.split()
                    if len(parts) == 2:
                        new_domains.add(parts[1].rstrip("."))

                elif rtype == "TXT":
                    found = re.findall(DOMAIN_REGEX, text, flags=re.IGNORECASE)
                    for d in found:
                        new_domains.add(d.rstrip("."))
                
                for nd in new_domains:
                    if nd not in visited and nd != domain:
                        domains.append(nd)
        
        except dns.resolver.NoAnswer:
            table.add_row(rtype, "aucune donnée trouvée", style="red")
        except dns.resolver.NXDOMAIN:
            table.add_row(rtype, "le domaine n'existe pas", style="red")
        except Exception as e:
            table.add_row(rtype, f"erreur — {e}", style="red")

    console.print(table)