import re
from .dns_checks import check_mx


# RFC 5322 simplified email regex
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)

DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "guerrillamail.com",
    "tempmail.com",
    "throwaway.email",
    "yopmail.com",
    "sharklasers.com",
    "guerrillamailblock.com",
    "grr.la",
    "dispostable.com",
    "trashmail.com",
    "trashmail.me",
    "trashmail.net",
    "mailnesia.com",
    "maildrop.cc",
    "discard.email",
    "mailcatch.com",
    "tempail.com",
    "fakeinbox.com",
    "mailnull.com",
    "spamgourmet.com",
    "jetable.org",
    "trash-mail.com",
    "mytemp.email",
    "temp-mail.org",
    "10minutemail.com",
    "20minutemail.com",
    "guerrillamail.info",
    "guerrillamail.net",
    "guerrillamail.de",
    "emailondeck.com",
    "33mail.com",
    "getnada.com",
    "mohmal.com",
    "tempinbox.com",
    "burnermail.io",
    "inboxbear.com",
    "mintemail.com",
    "spamfree24.org",
    "mailforspam.com",
    "safetymail.info",
    "filzmail.com",
    "mailexpire.com",
    "temporarymail.com",
    "harakirimail.com",
    "crazymailing.com",
    "mailnator.com",
    "tmail.ws",
    "tmpmail.net",
    "tmpmail.org",
    "binkmail.com",
    "spaml.com",
    "uglymailbox.com",
}

ROLE_BASED_PREFIXES = {
    "admin",
    "info",
    "support",
    "sales",
    "contact",
    "help",
    "abuse",
    "postmaster",
    "webmaster",
    "hostmaster",
    "noreply",
    "no-reply",
    "mailer-daemon",
    "office",
    "billing",
    "marketing",
    "security",
    "team",
    "hr",
    "jobs",
    "careers",
    "press",
    "media",
    "feedback",
    "subscribe",
    "unsubscribe",
}


async def validate_email(email: str) -> dict:
    checks = {}

    # Format validation
    format_valid = bool(EMAIL_REGEX.match(email))
    checks["format"] = {
        "valid": format_valid,
        "detail": "Valid email format" if format_valid else "Invalid email format per RFC 5322",
    }

    if not format_valid:
        return {
            "email": email,
            "valid": False,
            "checks": checks,
            "summary": "Invalid email format",
        }

    # Extract parts
    local_part, domain = email.rsplit("@", 1)
    domain_lower = domain.lower()

    # Domain MX check
    mx_records = await check_mx(domain)
    has_mx = mx_records is not None and len(mx_records) > 0
    checks["mx_records"] = {
        "valid": has_mx,
        "domain": domain,
        "mx_count": len(mx_records) if mx_records else 0,
        "detail": f"{len(mx_records)} MX record(s) found" if has_mx else "No MX records — domain cannot receive email",
    }

    # Disposable domain check
    is_disposable = domain_lower in DISPOSABLE_DOMAINS
    checks["disposable"] = {
        "is_disposable": is_disposable,
        "detail": "Disposable/temporary email domain detected" if is_disposable else "Not a known disposable domain",
    }

    # Role-based address check
    local_lower = local_part.lower()
    is_role_based = local_lower in ROLE_BASED_PREFIXES
    checks["role_based"] = {
        "is_role_based": is_role_based,
        "detail": f"'{local_lower}' is a role-based address (not a personal mailbox)" if is_role_based else "Personal address (not role-based)",
    }

    # Overall validity
    issues = []
    if not has_mx:
        issues.append("Domain has no MX records")
    if is_disposable:
        issues.append("Disposable email domain")
    if is_role_based:
        issues.append("Role-based address — may not reach a specific person")

    valid = format_valid and has_mx and not is_disposable
    risk_level = "low"
    if not valid:
        risk_level = "high"
    elif is_role_based:
        risk_level = "medium"

    return {
        "email": email,
        "valid": valid,
        "risk_level": risk_level,
        "local_part": local_part,
        "domain": domain,
        "checks": checks,
        "issues": issues,
        "summary": "Valid email address" if valid and not issues else "; ".join(issues) if issues else "Valid with warnings",
    }
