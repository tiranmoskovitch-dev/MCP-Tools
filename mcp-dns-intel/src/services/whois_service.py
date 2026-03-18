"""WHOIS lookup and domain age services."""
import asyncio
from datetime import datetime, timezone


def _normalize_date(val):
    """Extract a single datetime from WHOIS date fields (may be list or single)."""
    if val is None:
        return None
    if isinstance(val, list):
        val = val[0] if val else None
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, str):
        for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
    return None


def _serialize_date(dt):
    if dt is None:
        return None
    if isinstance(dt, datetime):
        return dt.isoformat()
    return str(dt)


def _get_whois_data(domain: str) -> dict:
    """Synchronous WHOIS fetch via python-whois."""
    import whois

    w = whois.whois(domain)
    if w.domain_name is None:
        raise ValueError(f"Domain '{domain}' not found or WHOIS data unavailable")
    return {
        "domain": w.domain_name if isinstance(w.domain_name, str) else (w.domain_name[0] if w.domain_name else domain),
        "registrar": w.registrar,
        "creation_date": _serialize_date(_normalize_date(w.creation_date)),
        "expiration_date": _serialize_date(_normalize_date(w.expiration_date)),
        "updated_date": _serialize_date(_normalize_date(w.updated_date)),
        "name_servers": sorted(set(ns.lower() for ns in w.name_servers)) if w.name_servers else [],
        "status": w.status if isinstance(w.status, list) else ([w.status] if w.status else []),
        "registrant": {
            "org": w.org if hasattr(w, "org") else None,
            "country": w.country if hasattr(w, "country") else None,
            "state": w.state if hasattr(w, "state") else None,
            "city": w.city if hasattr(w, "city") else None,
        },
        "dnssec": w.dnssec if hasattr(w, "dnssec") else None,
        "emails": w.emails if hasattr(w, "emails") else None,
    }


async def whois_lookup(domain: str) -> dict:
    """Full WHOIS lookup for a domain."""
    try:
        result = await asyncio.to_thread(_get_whois_data, domain)
        return {"success": True, "data": result}
    except ValueError as exc:
        return {"success": False, "error": str(exc)}
    except Exception as exc:
        return {"success": False, "error": f"WHOIS lookup failed: {exc}", "error_type": type(exc).__name__}


async def domain_age(domain: str) -> dict:
    """Calculate domain age from WHOIS creation date."""
    try:
        raw = await asyncio.to_thread(_get_whois_data, domain)
    except ValueError as exc:
        return {"success": False, "error": str(exc)}
    except Exception as exc:
        return {"success": False, "error": f"WHOIS lookup failed: {exc}", "error_type": type(exc).__name__}

    creation_dt = _normalize_date(raw.get("creation_date") or raw.get("creation_date"))
    expiration_dt = _normalize_date(raw.get("expiration_date"))
    now = datetime.now(timezone.utc)

    # Parse back serialized ISO dates if needed
    if creation_dt is None and raw.get("creation_date"):
        try:
            creation_dt = datetime.fromisoformat(raw["creation_date"])
        except (ValueError, TypeError):
            pass

    if expiration_dt is None and raw.get("expiration_date"):
        try:
            expiration_dt = datetime.fromisoformat(raw["expiration_date"])
        except (ValueError, TypeError):
            pass

    if creation_dt is None:
        return {"success": False, "error": "Creation date not available in WHOIS data"}

    # Make timezone-aware if naive
    if creation_dt.tzinfo is None:
        creation_dt = creation_dt.replace(tzinfo=timezone.utc)

    age_delta = now - creation_dt
    age_days = age_delta.days

    # Human-readable age
    years = age_days // 365
    remaining = age_days % 365
    months = remaining // 30
    days = remaining % 30
    parts = []
    if years > 0:
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months > 0:
        parts.append(f"{months} month{'s' if months != 1 else ''}")
    parts.append(f"{days} day{'s' if days != 1 else ''}")
    age_human = ", ".join(parts)

    days_until_expiry = None
    if expiration_dt:
        if expiration_dt.tzinfo is None:
            expiration_dt = expiration_dt.replace(tzinfo=timezone.utc)
        days_until_expiry = (expiration_dt - now).days

    # SOA serial for additional dating context
    soa_serial = None
    try:
        import dns.asyncresolver
        answers = await dns.asyncresolver.resolve(domain, "SOA")
        for rdata in answers:
            soa_serial = rdata.serial
            break
    except Exception:
        pass

    return {
        "success": True,
        "data": {
            "domain": domain,
            "creation_date": _serialize_date(creation_dt),
            "age_days": age_days,
            "age_human": age_human,
            "expiration_date": _serialize_date(expiration_dt),
            "days_until_expiry": days_until_expiry,
            "registrar": raw.get("registrar"),
            "is_new_domain": age_days < 30,
            "soa_serial": soa_serial,
        },
    }
