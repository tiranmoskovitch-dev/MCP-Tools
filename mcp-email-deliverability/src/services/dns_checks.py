import base64
import dns.asyncresolver
import dns.exception
import dns.rdatatype


async def _resolve(qname: str, rdtype: str, timeout: float = 5.0):
    resolver = dns.asyncresolver.Resolver()
    resolver.lifetime = timeout
    try:
        return await resolver.resolve(qname, rdtype)
    except dns.asyncresolver.NXDOMAIN:
        return None
    except dns.asyncresolver.NoAnswer:
        return None
    except dns.asyncresolver.NoNameservers:
        return None
    except dns.exception.Timeout:
        return None
    except Exception:
        return None


def _parse_spf_mechanisms(record: str) -> list[dict]:
    mechanisms = []
    parts = record.split()
    for part in parts:
        if part.lower().startswith("v=spf1"):
            continue
        qualifier = "+"
        if part[0] in "+-~?":
            qualifier = part[0]
            part = part[1:]

        if ":" in part:
            mechanism_type, value = part.split(":", 1)
        elif "=" in part:
            mechanism_type, value = part.split("=", 1)
        elif "/" in part and not part.startswith("ip"):
            mechanism_type = part.split("/")[0]
            value = part
        else:
            mechanism_type = part
            value = None

        mechanisms.append({
            "qualifier": qualifier,
            "type": mechanism_type.lower(),
            "value": value,
        })
    return mechanisms


def _rate_spf_policy(mechanisms: list[dict]) -> dict:
    all_mechanism = None
    for m in mechanisms:
        if m["type"] == "all":
            all_mechanism = m
            break

    if all_mechanism is None:
        return {"rating": "moderate", "detail": "No 'all' mechanism found — implicit deny"}

    q = all_mechanism["qualifier"]
    ratings = {
        "-": {"rating": "strict", "detail": "-all: Hard fail — unauthorized senders are rejected"},
        "~": {"rating": "moderate", "detail": "~all: Soft fail — unauthorized senders are marked but not rejected"},
        "?": {"rating": "permissive", "detail": "?all: Neutral — no policy on unauthorized senders"},
        "+": {"rating": "dangerous", "detail": "+all: Pass all — anyone can send as this domain"},
    }
    return ratings.get(q, {"rating": "unknown", "detail": f"Unknown qualifier: {q}"})


async def check_spf(domain: str) -> dict:
    answers = await _resolve(domain, "TXT")
    if answers is None:
        return {
            "domain": domain,
            "found": False,
            "record": None,
            "mechanisms": [],
            "policy": {"rating": "none", "detail": "No SPF record found"},
            "issues": ["No SPF record found — any server can send email as this domain"],
        }

    spf_record = None
    for rdata in answers:
        txt = rdata.to_text().strip('"')
        if txt.lower().startswith("v=spf1"):
            spf_record = txt
            break

    if spf_record is None:
        return {
            "domain": domain,
            "found": False,
            "record": None,
            "mechanisms": [],
            "policy": {"rating": "none", "detail": "No SPF record found in TXT records"},
            "issues": ["No SPF record found — any server can send email as this domain"],
        }

    mechanisms = _parse_spf_mechanisms(spf_record)
    policy = _rate_spf_policy(mechanisms)
    issues = []

    if policy["rating"] == "dangerous":
        issues.append("+all mechanism allows anyone to send as this domain")
    if policy["rating"] == "permissive":
        issues.append("?all provides no protection — consider ~all or -all")

    include_count = sum(1 for m in mechanisms if m["type"] == "include")
    if include_count > 10:
        issues.append(f"Too many include mechanisms ({include_count}) — SPF has a 10 DNS lookup limit")

    if len(spf_record) > 255:
        issues.append("SPF record exceeds 255 characters — may cause issues with some resolvers")

    return {
        "domain": domain,
        "found": True,
        "record": spf_record,
        "mechanisms": mechanisms,
        "policy": policy,
        "issues": issues,
    }


def _rsa_key_bit_length(b64_key: str) -> int | None:
    try:
        der = base64.b64decode(b64_key)
        if len(der) < 10:
            return None
        # SubjectPublicKeyInfo wraps the RSA key
        # The modulus is the large integer — estimate bits from DER length
        # A proper parse: after the SEQUENCE and BIT STRING headers, read the modulus
        # Shortcut: RSA public key DER size maps roughly to key size
        # 162 bytes ~ 1024-bit, 294 bytes ~ 2048-bit, 550 bytes ~ 4096-bit
        bit_estimate = (len(der) - 38) * 8  # rough approximation
        # Round to nearest standard size
        for standard in [512, 1024, 2048, 4096]:
            if abs(bit_estimate - standard) < 256:
                return standard
        return bit_estimate
    except Exception:
        return None


async def check_dkim(domain: str, selector: str = "default") -> dict:
    qname = f"{selector}._domainkey.{domain}"
    answers = await _resolve(qname, "TXT")

    if answers is None:
        return {
            "domain": domain,
            "selector": selector,
            "found": False,
            "record": None,
            "fields": {},
            "key_info": None,
            "issues": [f"No DKIM record found at {qname}"],
        }

    raw_parts = []
    for rdata in answers:
        raw_parts.append(rdata.to_text().strip('"'))

    record_text = "".join(raw_parts)
    # Some records are split across multiple strings within one TXT record
    record_text = record_text.replace('" "', "")

    fields = {}
    for part in record_text.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            fields[key.strip()] = value.strip()

    key_info = {}
    key_type = fields.get("k", "rsa")
    key_info["type"] = key_type
    key_info["flags"] = fields.get("t", None)

    public_key = fields.get("p", "")
    if not public_key:
        key_info["status"] = "revoked"
        key_info["detail"] = "Empty public key — this DKIM key has been revoked"
    elif key_type == "rsa":
        bit_len = _rsa_key_bit_length(public_key)
        key_info["bit_length"] = bit_len
        if bit_len and bit_len < 1024:
            key_info["status"] = "weak"
            key_info["detail"] = f"RSA key is only {bit_len} bits — minimum 1024 recommended, 2048 preferred"
        elif bit_len and bit_len >= 2048:
            key_info["status"] = "strong"
            key_info["detail"] = f"RSA key is {bit_len} bits"
        elif bit_len:
            key_info["status"] = "acceptable"
            key_info["detail"] = f"RSA key is {bit_len} bits — 2048+ recommended"
        else:
            key_info["status"] = "unknown"
            key_info["detail"] = "Could not determine key length"
    else:
        key_info["status"] = "present"
        key_info["detail"] = f"Key type: {key_type}"

    issues = []
    if key_info.get("status") == "revoked":
        issues.append("DKIM key has been revoked (empty p= tag)")
    if key_info.get("status") == "weak":
        issues.append(f"DKIM key is too short ({key_info.get('bit_length')} bits)")
    if fields.get("t") and "y" in fields["t"]:
        issues.append("DKIM is in testing mode (t=y) — messages may not be verified by all receivers")

    return {
        "domain": domain,
        "selector": selector,
        "found": True,
        "record": record_text,
        "fields": fields,
        "key_info": key_info,
        "issues": issues,
    }


def _parse_dmarc_tags(record: str) -> dict:
    tags = {}
    for part in record.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            tags[key.strip().lower()] = value.strip()
    return tags


async def check_dmarc(domain: str) -> dict:
    qname = f"_dmarc.{domain}"
    answers = await _resolve(qname, "TXT")

    if answers is None:
        return {
            "domain": domain,
            "found": False,
            "record": None,
            "tags": {},
            "policy_analysis": {
                "enforcement": "none",
                "detail": "No DMARC record found",
            },
            "reporting": {"rua": None, "ruf": None, "configured": False},
            "alignment": {"dkim": "relaxed", "spf": "relaxed"},
            "recommendations": [
                "Add a DMARC record to protect against email spoofing",
                "Start with p=none to monitor, then move to p=quarantine or p=reject",
            ],
        }

    dmarc_record = None
    for rdata in answers:
        txt = rdata.to_text().strip('"').replace('" "', "")
        if txt.lower().startswith("v=dmarc1"):
            dmarc_record = txt
            break

    if dmarc_record is None:
        return {
            "domain": domain,
            "found": False,
            "record": None,
            "tags": {},
            "policy_analysis": {
                "enforcement": "none",
                "detail": "No DMARC record found in TXT records at _dmarc subdomain",
            },
            "reporting": {"rua": None, "ruf": None, "configured": False},
            "alignment": {"dkim": "relaxed", "spf": "relaxed"},
            "recommendations": ["Add a DMARC record starting with v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com"],
        }

    tags = _parse_dmarc_tags(dmarc_record)

    policy = tags.get("p", "none")
    enforcement_map = {
        "reject": {"enforcement": "strict", "detail": "p=reject — unauthorized emails are rejected"},
        "quarantine": {"enforcement": "moderate", "detail": "p=quarantine — unauthorized emails are sent to spam"},
        "none": {"enforcement": "monitoring", "detail": "p=none — no enforcement, monitoring only"},
    }
    policy_analysis = enforcement_map.get(policy, {"enforcement": "unknown", "detail": f"Unknown policy: {policy}"})

    pct = tags.get("pct", "100")
    if pct != "100":
        policy_analysis["pct"] = int(pct) if pct.isdigit() else pct
        policy_analysis["detail"] += f" (applied to {pct}% of messages)"

    sp = tags.get("sp")
    if sp:
        policy_analysis["subdomain_policy"] = sp

    rua = tags.get("rua")
    ruf = tags.get("ruf")
    reporting = {
        "rua": rua,
        "ruf": ruf,
        "configured": bool(rua or ruf),
    }

    adkim = tags.get("adkim", "r")
    aspf = tags.get("aspf", "r")
    alignment = {
        "dkim": "strict" if adkim == "s" else "relaxed",
        "spf": "strict" if aspf == "s" else "relaxed",
    }

    recommendations = []
    if policy == "none":
        recommendations.append("Move from p=none to p=quarantine or p=reject for enforcement")
    if not rua:
        recommendations.append("Add rua= tag to receive aggregate DMARC reports")
    if not ruf:
        recommendations.append("Consider adding ruf= tag for forensic failure reports")
    if pct != "100" and policy in ("quarantine", "reject"):
        recommendations.append(f"Increase pct from {pct} to 100 for full coverage once confident")
    if adkim != "s":
        recommendations.append("Consider strict DKIM alignment (adkim=s) for tighter security")

    return {
        "domain": domain,
        "found": True,
        "record": dmarc_record,
        "tags": tags,
        "policy_analysis": policy_analysis,
        "reporting": reporting,
        "alignment": alignment,
        "recommendations": recommendations,
    }


async def check_mx(domain: str) -> list[dict] | None:
    answers = await _resolve(domain, "MX")
    if answers is None:
        return None
    records = []
    for rdata in answers:
        records.append({
            "priority": rdata.preference,
            "host": str(rdata.exchange).rstrip("."),
        })
    records.sort(key=lambda r: r["priority"])
    return records


COMMON_DKIM_SELECTORS = [
    "default",
    "google",
    "selector1",  # Microsoft
    "selector2",  # Microsoft
    "s1",
    "s2",
    "k1",
    "dkim",
    "mail",
    "smtp",
    "mandrill",
    "everlytickey1",
    "cm",
    "mxvault",
    "protonmail",
]


async def try_common_dkim_selectors(domain: str) -> list[dict]:
    found = []
    for selector in COMMON_DKIM_SELECTORS:
        result = await check_dkim(domain, selector)
        if result["found"]:
            found.append(result)
    return found
