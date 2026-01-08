import sys
import dns.resolver
#ajouter rich

record_types = ["A", "AAAA", "MX", "TXT"]

if len(sys.argv) < 2:
    domain = input("Entrez un nom de domaine : ").strip()
    domains = [domain]
else:
    domains = sys.argv[1:]

for domain in domains: #ajouter un while pour chaque domaine, enlever un domain a chaque boucle, ajouter un ou plusieur domains pendant la boucle, faire une recherche en anneau
    print("\n" + "="*50)
    print(f"|       |{' Résultats DNS pour ' + domain :^48}|")
    print("="*50)

    for rtype in record_types:
        print(f"| {rtype:<5} | ", end="")
        try:
            answers = dns.resolver.resolve(domain, rtype)
            print("Résultat(s) :")
            for rdata in answers:
                print(f"|       |  {rdata.to_text()}")
        except dns.resolver.NoAnswer:
            print("aucune donnée trouvée")
        except dns.resolver.NXDOMAIN:
            print("le domaine n'existe pas")
        except Exception as e:
            print(f"erreur — {e}")

    print("="*50)


#exemple d'utilisation : python adressipsearch.py mdk.fr google.com wikipedia.fr