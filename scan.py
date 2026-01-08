import sys
import dns.resolver
from rich.console import Console
from rich.table import Table

console = Console()
record_types = ["A", "AAAA", "MX", "TXT"]

if len(sys.argv) < 2:
    domain = input("Entrez un nom de domaine : ").strip()
    domains = [domain]
else:
    domains = sys.argv[1:]
#ajouter un ou plusieurs domains pendant la boucle, faire une recherche en anneau

while domains:
    domain = domains.pop(0)
    console.rule(f"Résultats DNS pour [bold green]{domain}[/bold green]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan", width=6)
    table.add_column("Résultat")

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for rdata in answers:
                table.add_row(rtype, rdata.to_text())
        except dns.resolver.NoAnswer:
            table.add_row(rtype, "aucune donnée trouvée", style="red")
        except dns.resolver.NXDOMAIN:
            table.add_row(rtype, "le domaine n'existe pas", style="red")
        except Exception as e:
            table.add_row(rtype, f"erreur — {e}", style="red")

    console.print(table)


#exemple d'utilisation : python adressipsearch.py mdk.fr google.com wikipedia.fr