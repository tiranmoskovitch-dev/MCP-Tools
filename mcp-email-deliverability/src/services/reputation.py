import asyncio
from .dns_checks import check_mx, _resolve


EMAIL_PROVIDERS = {
    "google.com": "Google Workspace",
    "googlemail.com": "Google Workspace",
    "gmail-smtp-in.l.google.com": "Google Workspace",
    "outlook.com": "Microsoft 365",
    "protection.outlook.com": "Microsoft 365",
    "pphosted.com": "Proofpoint",
    "mimecast.com": "Mimecast",
    "emailsrvr.com": "Rackspace",
    "secureserver.net": "GoDaddy",
    "zoho.com": "Zoho Mail",
    "yahoodns.net": "Yahoo Mail",
    "messagelabs.com": "Broadcom (Symantec)",
    "reflexion.net": "Sophos",
    "barracudanetworks.com": "Barracuda",
    "fireeyecloud.com": "Trellix (FireEye)",
    "protonmail.ch": "Proton Mail",
    "mx.cloudflare.net": "Cloudflare Email",
}

DNSBL_SERVERS = [
    "zen.spamhaus.org",
    "bl.spamcop.net",
    "b.barracudacentral.org",
    "dnsbl.sorbs.net",
]


def _identify_provider(mx_host: str) -> str | None:
    mx_lower = mx_host.lower()
    for domain_part, provider in EMAIL_PROVIDERS.items():
        if domain_part in mx_lower:
            return provider
    return None


async def _check_blacklist(ip: str, dnsbl: str) -> dict:
    reversed_ip = ".".join(reversed(ip.split(".")))
    query = f"{reversed_ip}.{dnsbl}"
    result = await _resolve(query, "A")
    return {
        "dnsbl": dnsbl,
        "listed": result is not None,
    }


async def _check_all_blacklists(ip: str) -> list[dict]:
    tasks = [_check_blacklist(ip, dnsbl) for dnsbl in DNSBL_SERVERS]
    return await asyncio.gather(*tasks)


async def _get_soa(domain: str) -> dict | None:
    result = await _resolve(domain, "SOA")
    if result is None:
        return None
    soa = list(result)[0]
    return {
        "primary_ns": str(soa.mname).rstrip("."),
        "admin_email": str(soa.rname).rstrip("."),
        "serial": soa.serial,
        "refresh": soa.refresh,
        "retry": soa.retry,
        "expire": soa.expire,
        "minimum_ttl": soa.minimum,
    }


async def _get_nameservers(domain: str) -> list[str] | None:
    result = await _resolve(domain, "NS")
    if result is None:
        return None
    return [str(ns).rstrip(".") for ns in result]


async def check_domain_reputation(domain: str) -> dict:
    # Gather DNS data in parallel
    mx_records, soa_info, nameservers = await asyncio.gather(
        check_mx(domain),
        _get_soa(domain),
        _get_nameservers(domain),
    )

    # Identify mail provider
    mx_analysis = []
    if mx_records:
        for mx in mx_records:
            provider = _identify_provider(mx["host"])
            mx_analysis.append({
                "host": mx["host"],
                "priority": mx["priority"],
                "provider": provider or "Custom / Unknown",
            })

    # Get MX server IPs and check blacklists
    blacklist_results = []
    if mx_records:
        primary_mx = mx_records[0]["host"]
        a_result = await _resolve(primary_mx, "A")
        if a_result:
            primary_ip = str(list(a_result)[0])
            bl_checks = await _check_all_blacklists(primary_ip)
            blacklist_results = {
                "ip_checked": primary_ip,
                "mx_host": primary_mx,
                "results": bl_checks,
                "listed_count": sum(1 for r in bl_checks if r["listed"]),
                "clean": all(not r["listed"] for r in bl_checks),
            }
        else:
            blacklist_results = {
                "ip_checked": None,
                "mx_host": primary_mx,
                "results": [],
                "error": "Could not resolve MX server IP",
            }
    else:
        blacklist_results = {
            "ip_checked": None,
            "mx_host": None,
            "results": [],
            "error": "No MX records found",
        }

    # Build reputation summary
    issues = []
    positive = []

    if not mx_records:
        issues.append("No MX records — domain cannot receive email")
    else:
        positive.append(f"{len(mx_records)} MX record(s) configured")

    if soa_info:
        positive.append(f"SOA record present (serial: {soa_info['serial']})")
    else:
        issues.append("No SOA record found — domain may not be properly configured")

    if nameservers:
        positive.append(f"Nameservers: {', '.join(nameservers[:4])}")
    else:
        issues.append("Could not determine nameservers")

    if isinstance(blacklist_results, dict):
        if blacklist_results.get("clean"):
            positive.append("Primary MX IP is clean on all checked blacklists")
        elif blacklist_results.get("listed_count", 0) > 0:
            issues.append(f"Primary MX IP is listed on {blacklist_results['listed_count']} blacklist(s)")

    # Overall assessment
    if not issues:
        assessment = "good"
        detail = "Domain has a clean reputation with properly configured email infrastructure"
    elif len(issues) <= 1:
        assessment = "fair"
        detail = "Domain has minor reputation concerns"
    else:
        assessment = "poor"
        detail = "Domain has significant reputation issues"

    return {
        "domain": domain,
        "assessment": assessment,
        "detail": detail,
        "mx_analysis": mx_analysis,
        "soa": soa_info,
        "nameservers": nameservers,
        "blacklists": blacklist_results,
        "positive_signals": positive,
        "issues": issues,
    }
