import unittest
from dns_tools import crawl_tld, reverse_dns, brute_sub, ip_voisines, parse_txt, scan_srv


class TestDns(unittest.TestCase):

    def test_crawl_tld(self):
        result = crawl_tld("www.example.com")
        self.assertIn("example.com", result)

    def test_reverse_dns_fail(self):
        result = reverse_dns("0.0.0.0")
        self.assertEqual(result, [])

    def test_brute_sub_fail(self):
        result = brute_sub("domaine.inexistant.xyz")
        self.assertEqual(len(result), 0)

    def test_ip_voisines(self):
        result = ip_voisines("8.8.8.8")
        self.assertIsInstance(result, set)

    def test_parse_txt(self):
        domains, ips = parse_txt("example.com")
        self.assertIsInstance(domains, set)
        self.assertIsInstance(ips, set)

    def test_scan_srv(self):
        result = scan_srv("example.com")
        self.assertIsInstance(result, set)


if __name__ == "__main__":
    unittest.main()