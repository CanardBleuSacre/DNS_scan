from dns_tools.dns_parsing_spe import parse_spf, parse_dmarc, is_spf, is_dmarc

# Test 1: parse_spf
print("=== Test parse_spf ===")
spf_txt = "v=spf1 include:_spf.google.com ip4:192.168.1.1 a:mail.example.com mx:smtp.example.com ~all"
domains, ips = parse_spf(spf_txt)
print(f"Domaines trouvés: {domains}")
print(f"IPs trouvées: {ips}")

# Test 2: parse_dmarc
print("\n=== Test parse_dmarc ===")
dmarc_txt = "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com; ruf=mailto:forensic@example.org"
domains = parse_dmarc(dmarc_txt)
print(f"Domaines trouvés: {domains}")

# Test 3: is_spf
print("\n=== Test is_spf ===")
print(f"Est SPF: {is_spf(spf_txt)}")
print(f"N'est pas SPF: {is_spf('quelque chose')}")

# Test 4: is_dmarc
print("\n=== Test is_dmarc ===")
print(f"Est DMARC: {is_dmarc(dmarc_txt)}")
print(f"N'est pas DMARC: {is_dmarc('autre chose')}")