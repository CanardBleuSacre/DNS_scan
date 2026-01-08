import sys
import dns.resolver

record_types = ["A", "AAAA", "MX", "TXT"]

if len(sys.argv) < 2:
    domain = input("Entrez un nom de domaine : ").strip()
    domains = [domain]
else:
    domains = sys.argv[1:]

for domain in domains:
    print(f"{' Résultats DNS pour ' + domain}|")

    for rtype in record_types:
        print(f"{rtype:<5}")
        try:
            answers = dns.resolver.resolve(domain, rtype)
            print("Résultat(s) :")
            for rdata in answers:
                print(f"{rdata.to_text()}")
        except dns.resolver.NoAnswer:
            print("aucune donnée trouvée")
        except dns.resolver.NXDOMAIN:
            print("le domaine n'existe pas")
        except Exception as e:
            print(f"erreur — {e}")