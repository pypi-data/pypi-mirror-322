import nslookup
from dns import resolver
import dns.reversename
from .. import Random
import dns

#print("load " + '/'.join(__file__.split('/')[-2:]))

class Nslookup():
    def __init__(self, server:list[str]=["8.8.8.8", "1.1.1.1", "8.8.4.4"], tcp:bool=False) -> None:
        if type(server) == str:
            server = [server]

        self.server = server
        self.tcp = tcp
    
    def A(self, domain:str) -> list[str]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "A")
            return [str(rdata.address) for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def AAAA(self, domain:str) -> list[str]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "AAAA")
            return [str(rdata.address) for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def PTR(self, ip:str) -> list[str]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            reversed_ip = dns.reversename.from_address(ip)
            answer = rl.resolve(reversed_ip, "PTR")
            return [str(rdata.target) for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def MX(self, domain:str) -> list[dict]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "MX")
            return [{
                "preference": rdata.preference,
                "exchange": str(rdata.exchange)
            } for rdata in answer]
        except dns.resolver.NoAnswer:
            return []
    
    def CNAME(self, domain:str) -> list[str]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "CNAME")
            return [str(rdata.target) for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def TXT(self, domain:str) -> list[str]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "TXT")
            return [str(rdata.strings[0]) for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def NS(self, domain:str) -> list[str]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "NS")
            return [str(rdata.target) for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def SOA(self, domain:str) -> dict:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "SOA")
            soa_data = answer[0].to_text().split()
            return {
                "mname": soa_data[0],
                "rname": soa_data[1],
                "serial": int(soa_data[2]),
                "refresh": int(soa_data[3]),
                "retry": int(soa_data[4]),
                "expire": int(soa_data[5]),
                "minimum": int(soa_data[6])
            }
        except dns.resolver.NoAnswer:
            return {}

    def SRV(self, domain:str) -> list[dict]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "SRV")
            return [{
                "priority": rdata.priority,
                "weight": rdata.weight,
                "port": rdata.port,
                "target": str(rdata.target)
            } for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def CAA(self, domain:str) -> list[dict]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "CAA")
            return [{
                "flags": rdata.flags,
                "tag": rdata.tag,
                "value": rdata.value
            } for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def DS(self, domain:str) -> list[dict]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "DS")
            return [{
                "key_tag": rdata.key_tag,
                "algorithm": rdata.algorithm,
                "digest_type": rdata.digest_type,
                "digest": rdata.digest
            } for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def DNSKEY(self, domain:str) -> list[dict]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "DNSKEY")
            return [{
                "flags": rdata.flags,
                "protocol": rdata.protocol,
                "algorithm": rdata.algorithm,
                "key": rdata.key
            } for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def RRSIG(self, domain:str) -> list[dict]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "RRSIG")
            return [{
                "type_covered": rdata.type_covered,
                "algorithm": rdata.algorithm,
                "labels": rdata.labels,
                "original_ttl": rdata.original_ttl,
                "expiration": rdata.expiration,
                "inception": rdata.inception,
                "key_tag": rdata.key_tag,
                "signer_name": str(rdata.signer_name),
                "signature": rdata.signature
            } for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def NAPTR(self, domain:str) -> list[dict]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "NAPTR")
            return [{
                "order": rdata.order,
                "preference": rdata.preference,
                "flags": rdata.flags,
                "service": rdata.service,
                "regexp": rdata.regexp,
                "replacement": str(rdata.replacement)
            } for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def TLSA(self, domain:str) -> list[dict]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "TLSA")
            return [{
                "usage": rdata.usage,
                "selector": rdata.selector,
                "matching_type": rdata.matching_type,
                "certificate": rdata.certificate
            } for rdata in answer]
        except dns.resolver.NoAnswer:
            return []

    def SPF(self, domain:str) -> list[str]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        try:
            answer = rl.resolve(domain, "SPF")
            return [str(rdata.strings[0]) for rdata in answer]
        except dns.resolver.NoAnswer:
            return []
    
    def All(self, domain:str) -> dict:
        result = {}
        result["A"] = self.A(domain)
        result["AAAA"] = self.AAAA(domain)
        result["MX"] = self.MX(domain)
        result["CNAME"] = self.CNAME(domain)
        result["TXT"] = self.TXT(domain)
        result["NS"] = self.NS(domain)
        result["SOA"] = self.SOA(domain)
        result["SRV"] = self.SRV(domain)
        result["CAA"] = self.CAA(domain)
        result["DS"] = self.DS(domain)
        result["DNSKEY"] = self.DNSKEY(domain)
        result["RRSIG"] = self.RRSIG(domain)
        result["NAPTR"] = self.NAPTR(domain)
        result["TLSA"] = self.TLSA(domain)
        result["SPF"] = self.SPF(domain)

        return result

if __name__ == "__main__":
    ns = Nslookup()
    print("MX:", ns.MX('naarn.at'))