import sys
import dns.resolver
import dns.reversename
from rich.console import Console
from rich.tree import Tree
import re

console = Console()
resolver = dns.resolver.Resolver()

record_types = ["A", "AAAA", "MX", "TXT", "CNAME"]
common_subdomains = ["www", "mail", "ftp", "api", "dev", "test", "ns1", "ns2"]
srv_services = ["_sip._tcp","_sip._udp","_ldap._tcp","_xmpp-server._tcp","_xmpp-client._tcp"]

domain_regex = (
    rf"(?:[a-z0-9_]"
    rf"(?:[a-z0-9-_]{{0,61}}"
    rf"[a-z0-9_])?\.)"
    r"+[a-z0-9][a-z0-9-_]{0,61}"
    rf"[a-z]\.?"
)

visited_domains = set()

def parse_args():
    if len(sys.argv) < 2:
        return [input("Entrez un nom de domaine : ").strip()]
    return sys.argv[1:]


def scan_srv(domain):
    f = set()
    for s in srv_services():
        try:
            for r in resolver.resolve(f"{s}.{domain}","SRV"):
                f.add(str(r.target).rstrip("."))
        except: pass
    return f 

def reverse_dns(ip):
    try: return [str(a).rstrip(".") for a in resolver.resolve(dns.reversename.from_address(ip),"PTR")]
    except: return []

def extract_domains(domain, rtype, text):
    new_domains = set()

    if rtype == "MX":
        parts = text.split()
        if len(parts) == 2:
            new_domains.add(parts[1].rstrip("."))

    elif rtype == "TXT":
        found = re.findall(domain_regex, text, flags=re.IGNORECASE)
        for d in found:
            new_domains.add(d.rstrip("."))

    base_parts = domain.split(".")
    if len(base_parts) >= 2:
        base_domain = ".".join(base_parts[-2:])
        for sub in common_subdomains:
            new_domains.add(f"{sub}.{base_domain}")

    return new_domains


def resolve_domain(domain):
    tree = Tree(f"[bold green]{domain}[/bold green]")

    for rtype in record_types:
        branch = tree.add(f"[cyan]{rtype}[/cyan]")
        try:
            answers = resolver.resolve(domain, rtype)

            for rdata in answers:
                text = rdata.to_text()
                branch.add(text)

                new_domains = extract_domains(domain, rtype, text)

                for nd in new_domains:
                    if nd not in visited_domains and nd != domain:
                        domains.append(nd)

        except dns.resolver.NoAnswer:
            branch.add("[red]aucune donnée[/red]")
        except dns.resolver.NXDOMAIN:
            branch.add("[red]domaine inexistant[/red]")
        except Exception as e:
            branch.add(f"[red]erreur : {e}[/red]")

    return tree

def main():
    global domains
    domains = parse_args()

    while domains:
        domain = domains.pop(0)
        if domain in visited_domains:
            continue

        visited_domains.add(domain)
        tree = resolve_domain(domain)
        console.print(tree)


if __name__ == "__main__":
    main()