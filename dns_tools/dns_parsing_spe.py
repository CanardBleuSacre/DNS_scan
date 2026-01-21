import re


def parse_spf(txt_record):
    '''
    Analyse un enregistrement TXT SPF pour extraire les
    noms de domaine et les adresses IP qu'il contient.
    '''
    domains = set()
    ips = set()
    if not txt_record.startswith("v=spf1"):
        return domains, ips
    
    includes = re.findall(r'include:([a-zA-Z0-9._-]+)', txt_record)
    domains.update(includes) 
    a_records = re.findall(r'a:([a-zA-Z0-9._-]+)', txt_record)
    domains.update(a_records)    
    mx_records = re.findall(r'mx:([a-zA-Z0-9._-]+)', txt_record)
    domains.update(mx_records)    
    ipv4 = re.findall(r'ip4:([0-9./]+)', txt_record)
    ips.update(ipv4)
    ipv6 = re.findall(r'ip6:([0-9a-f:/]+)', txt_record)
    ips.update(ipv6)
    
    return domains, ips


def parse_dmarc(txt_record):
    '''
    Analyse un enregistrement TXT DMARC pour extraire les
    noms de domaine qu'il contient.
    '''
    domains = set()
    
    if not txt_record.startswith("v=DMARC1"):
        return domains
    emails = re.findall(r'ru[af]=mailto:.*?@([a-zA-Z0-9._-]+)', txt_record)
    domains.update(emails)
    
    return domains

def is_spf(txt_record):
    '''
    Vérifie si un enregistrement TXT est de type SPF.
    '''
    return txt_record.startswith("v=spf1")

def is_dmarc(txt_record):
    '''
    Vérifie si un enregistrement TXT est de type DMARC.
    '''
    return txt_record.startswith("v=DMARC1")