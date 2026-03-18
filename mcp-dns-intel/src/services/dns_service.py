"""DNS record queries, subdomain enumeration, and reverse DNS services."""
import asyncio
import ipaddress
import dns.asyncresolver
import dns.reversename
import dns.name
import dns.rdatatype

ALL_RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "CAA", "SRV", "PTR"]

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "admin", "blog", "dev", "staging", "api", "app", "test",
    "ns1", "ns2", "mx", "smtp", "pop", "imap", "webmail", "cpanel", "panel", "dashboard",
    "portal", "vpn", "remote", "git", "gitlab", "github", "bitbucket", "jenkins", "ci", "cd",
    "deploy", "monitor", "grafana", "prometheus", "kibana", "elastic", "redis", "db", "database",
    "mysql", "postgres", "mongo", "cache", "cdn", "static", "assets", "media", "images", "img",
    "files", "docs", "wiki", "help", "support", "status", "health", "beta", "alpha", "demo",
    "sandbox", "preview", "qa", "uat", "prod", "production", "store", "shop", "pay", "payment",
    "billing", "invoice", "auth", "sso", "login", "oauth", "ldap", "radius", "proxy", "gateway",
    "lb", "loadbalancer", "k8s", "kube", "docker", "registry", "vault", "consul", "terraform",
    "ansible", "puppet", "chef", "nagios", "zabbix", "splunk", "log", "logs", "backup", "archive",
    "old", "new", "v1", "v2", "m", "mobile", "internal", "intranet", "extranet",
]


def _parse_record(rdtype_str: str, rdata, ttl: int) -> dict:
    """Parse a DNS record into a structured dict with record-specific fields."""
    base = {"type": rdtype_str, "ttl": ttl, "value": rdata.to_text()}

    if rdtype_str == "MX":
        base["priority"] = rdata.preference
        base["exchange"] = str(rdata.exchange)
    elif rdtype_str == "SOA":
        base["mname"] = str(rdata.mname)
        base["rname"] = str(rdata.rname)
        base["serial"] = rdata.serial
        base["refresh"] = rdata.refresh
        base["retry"] = rdata.retry
        base["expire"] = rdata.expire
        base["minimum"] = rdata.minimum
    elif rdtype_str == "CAA":
        base["flags"] = rdata.flags
        base["tag"] = rdata.tag
        base["ca_value"] = rdata.value
    elif rdtype_str == "SRV":
        base["priority"] = rdata.priority
        base["weight"] = rdata.weight
        base["port"] = rdata.port
        base["target"] = str(rdata.target)
    elif rdtype_str == "TXT":
        # Join multi-string TXT records
        base["value"] = " ".join(s.decode("utf-8", errors="replace") if isinstance(s, bytes) else s for s in rdata.strings)
    elif rdtype_str == "CNAME":
        base["target"] = str(rdata.target)
    elif rdtype_str == "NS":
        base["nameserver"] = str(rdata.target)
    elif rdtype_str in ("A", "AAAA"):
        base["address"] = rdata.address
    elif rdtype_str == "PTR":
        base["ptrdname"] = str(rdata.target)

    return base


async def _query_type(resolver, domain: str, rdtype: str) -> list[dict]:
    """Query a single record type, returning parsed records or empty list on failure."""
    try:
        answers = await resolver.resolve(domain, rdtype)
        ttl = answers.rrset.ttl
        return [_parse_record(rdtype, rdata, ttl) for rdata in answers]
    except (dns.asyncresolver.NXDOMAIN, dns.asyncresolver.NoAnswer,
            dns.asyncresolver.NoNameservers, dns.asyncresolver.LifetimeTimeout,
            dns.name.EmptyLabel, Exception):
        return []


async def dns_records(domain: str, record_type: str = "ALL") -> dict:
    """Query DNS records for a domain."""
    record_type = record_type.upper().strip()
    resolver = dns.asyncresolver.Resolver()
    resolver.lifetime = 10.0

    if record_type == "ALL":
        types_to_query = ALL_RECORD_TYPES
    elif record_type in ALL_RECORD_TYPES:
        types_to_query = [record_type]
    else:
        return {"success": False, "error": f"Unsupported record type: {record_type}. Supported: {', '.join(ALL_RECORD_TYPES)} or ALL"}

    tasks = [_query_type(resolver, domain, rt) for rt in types_to_query]
    results_lists = await asyncio.gather(*tasks)

    records = {}
    total = 0
    for rt, recs in zip(types_to_query, results_lists):
        if recs:
            records[rt] = recs
            total += len(recs)

    if total == 0:
        # Check if domain even exists
        try:
            await resolver.resolve(domain, "A")
        except dns.asyncresolver.NXDOMAIN:
            return {"success": False, "error": f"Domain '{domain}' does not exist (NXDOMAIN)"}
        except Exception:
            pass

    return {
        "success": True,
        "data": {
            "domain": domain,
            "query_type": record_type,
            "total_records": total,
            "records": records,
        },
    }


async def _resolve_subdomain(resolver, fqdn: str) -> dict | None:
    """Try to resolve a subdomain, return result or None."""
    try:
        answers = await resolver.resolve(fqdn, "A")
        ips = [rdata.address for rdata in answers]
        return {"subdomain": fqdn, "ips": ips}
    except Exception:
        return None


async def subdomain_enum(domain: str, wordlist: str = "common") -> dict:
    """Enumerate subdomains via async DNS brute-force."""
    subs = COMMON_SUBDOMAINS

    resolver = dns.asyncresolver.Resolver()
    resolver.lifetime = 5.0

    # Use a semaphore to limit concurrent lookups
    sem = asyncio.Semaphore(50)

    async def limited_resolve(fqdn):
        async with sem:
            return await _resolve_subdomain(resolver, fqdn)

    fqdns = [f"{sub}.{domain}" for sub in subs]
    tasks = [limited_resolve(fqdn) for fqdn in fqdns]
    results = await asyncio.gather(*tasks)

    found = [r for r in results if r is not None]
    found.sort(key=lambda r: r["subdomain"])

    return {
        "success": True,
        "data": {
            "domain": domain,
            "wordlist": wordlist,
            "total_checked": len(subs),
            "total_found": len(found),
            "subdomains": found,
        },
    }


async def reverse_dns(ip: str) -> dict:
    """Reverse DNS lookup with forward-confirmation check."""
    # Validate IP
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return {"success": False, "error": f"Invalid IP address: {ip}"}

    resolver = dns.asyncresolver.Resolver()
    resolver.lifetime = 10.0

    # PTR lookup
    try:
        rev_name = dns.reversename.from_address(ip)
        answers = await resolver.resolve(rev_name, "PTR")
        hostname = str(answers[0].target).rstrip(".")
    except dns.asyncresolver.NXDOMAIN:
        return {
            "success": True,
            "data": {
                "ip": ip,
                "hostname": None,
                "forward_confirmed": False,
                "additional_forward_ips": [],
                "note": "No PTR record found for this IP",
            },
        }
    except Exception as exc:
        return {"success": False, "error": f"PTR lookup failed: {exc}"}

    # Forward verification
    forward_confirmed = False
    additional_forward_ips = []
    rdtype = "AAAA" if addr.version == 6 else "A"
    try:
        fwd_answers = await resolver.resolve(hostname, rdtype)
        fwd_ips = [rdata.address for rdata in fwd_answers]
        forward_confirmed = ip in fwd_ips
        additional_forward_ips = [fip for fip in fwd_ips if fip != ip]
    except Exception:
        pass

    return {
        "success": True,
        "data": {
            "ip": ip,
            "hostname": hostname,
            "forward_confirmed": forward_confirmed,
            "additional_forward_ips": additional_forward_ips,
        },
    }
