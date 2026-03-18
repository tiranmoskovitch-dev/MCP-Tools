from .dns_checks import check_spf, check_dmarc, check_mx, try_common_dkim_selectors, _resolve


async def _check_reverse_dns(mx_records: list[dict] | None) -> dict:
    if not mx_records:
        return {"checked": False, "detail": "No MX records to check"}

    results = []
    for mx in mx_records[:3]:
        host = mx["host"]
        a_answers = await _resolve(host, "A")
        if a_answers is None:
            results.append({"host": host, "ip": None, "reverse": None, "match": False})
            continue

        ip = str(list(a_answers)[0])
        reversed_ip = ".".join(reversed(ip.split(".")))
        ptr_name = f"{reversed_ip}.in-addr.arpa"
        ptr_answers = await _resolve(ptr_name, "PTR")

        if ptr_answers is None:
            results.append({"host": host, "ip": ip, "reverse": None, "match": False})
        else:
            ptr_host = str(list(ptr_answers)[0]).rstrip(".")
            match = ptr_host.lower() == host.lower() or ptr_host.lower().endswith(f".{host.lower()}")
            results.append({"host": host, "ip": ip, "reverse": ptr_host, "match": match})

    has_reverse = any(r["match"] or r["reverse"] for r in results)
    return {"checked": True, "has_reverse_dns": has_reverse, "details": results}


async def calculate_spam_score(domain: str) -> dict:
    score = 100
    breakdown = []
    recommendations = []

    # SPF check
    spf_result = await check_spf(domain)
    if not spf_result["found"]:
        score -= 20
        breakdown.append({"check": "SPF", "deduction": -20, "reason": "No SPF record found"})
        recommendations.append("Add an SPF record to specify authorized mail servers")
    elif spf_result["policy"]["rating"] in ("permissive", "dangerous"):
        score -= 10
        breakdown.append({"check": "SPF Policy", "deduction": -10, "reason": f"SPF policy is {spf_result['policy']['rating']}"})
        recommendations.append("Tighten SPF policy to ~all or -all")

    # DMARC check
    dmarc_result = await check_dmarc(domain)
    if not dmarc_result["found"]:
        score -= 20
        breakdown.append({"check": "DMARC", "deduction": -20, "reason": "No DMARC record found"})
        recommendations.append("Add a DMARC record to protect against spoofing")
    elif dmarc_result["tags"].get("p", "none") == "none":
        score -= 10
        breakdown.append({"check": "DMARC Policy", "deduction": -10, "reason": "DMARC policy is p=none (monitoring only)"})
        recommendations.append("Upgrade DMARC policy from p=none to p=quarantine or p=reject")

    # MX check
    mx_records = await check_mx(domain)
    if mx_records is None:
        score -= 15
        breakdown.append({"check": "MX Records", "deduction": -15, "reason": "No MX records found"})
        recommendations.append("Configure MX records for the domain")

    # DKIM check
    dkim_results = await try_common_dkim_selectors(domain)
    if not dkim_results:
        score -= 15
        breakdown.append({"check": "DKIM", "deduction": -15, "reason": "No DKIM records found with common selectors"})
        recommendations.append("Configure DKIM signing for outbound email")
    else:
        selectors_found = [r["selector"] for r in dkim_results]
        breakdown.append({"check": "DKIM", "deduction": 0, "reason": f"DKIM found for selectors: {', '.join(selectors_found)}"})

    # Reverse DNS check
    rdns_result = await _check_reverse_dns(mx_records)
    if rdns_result["checked"] and not rdns_result.get("has_reverse_dns", False):
        score -= 10
        breakdown.append({"check": "Reverse DNS", "deduction": -10, "reason": "MX servers lack reverse DNS"})
        recommendations.append("Configure reverse DNS (PTR records) for mail server IPs")
    elif rdns_result["checked"]:
        breakdown.append({"check": "Reverse DNS", "deduction": 0, "reason": "Reverse DNS configured"})

    score = max(0, score)

    if score >= 80:
        grade = "A" if score >= 90 else "B"
        summary = "Good deliverability configuration"
    elif score >= 60:
        grade = "C"
        summary = "Moderate deliverability — some improvements recommended"
    elif score >= 40:
        grade = "D"
        summary = "Poor deliverability — significant issues found"
    else:
        grade = "F"
        summary = "Critical deliverability issues — emails likely to be rejected or spam-filtered"

    return {
        "domain": domain,
        "score": score,
        "grade": grade,
        "summary": summary,
        "breakdown": breakdown,
        "recommendations": recommendations,
        "checks": {
            "spf": spf_result,
            "dmarc": dmarc_result,
            "mx": mx_records,
            "dkim_selectors_found": [r["selector"] for r in dkim_results],
            "reverse_dns": rdns_result,
        },
    }
