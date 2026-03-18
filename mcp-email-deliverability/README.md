# Email Deliverability Checker

> SPF/DKIM/DMARC validation, spam score, domain reputation checking

**Price:** $29 | **MCP Protocol** | **Python 3.11+**

## Tools

### check_spf
Check SPF (Sender Policy Framework) record for a domain. Parses the SPF TXT record, extracts all mechanisms (ip4, ip6, include, a, mx, redirect, all), evaluates the policy strength (strict/moderate/permissive/dangerous), and identifies configuration issues.

### check_dkim
Check DKIM (DomainKeys Identified Mail) record for a domain. Looks up the DKIM TXT record at `{selector}._domainkey.{domain}`, parses key fields (v, k, p, t), determines key type and RSA bit length, and validates the configuration. Supports custom selector input with default fallback.

### check_dmarc
Check DMARC (Domain-based Message Authentication, Reporting & Conformance) record for a domain. Parses all DMARC tags (v, p, sp, rua, ruf, adkim, aspf, pct, fo, rf, ri), analyzes enforcement level, reporting configuration, alignment mode, and provides actionable recommendations.

### spam_score
Calculate a 0-100 email deliverability score for a domain. Runs all checks (SPF, DKIM with 15 common selectors, DMARC, MX records, reverse DNS) and returns a weighted score with letter grade (A-F), detailed breakdown, and prioritized recommendations.

**Scoring deductions:**
- No SPF: -20 | Permissive SPF: -10
- No DMARC: -20 | p=none DMARC: -10
- No MX records: -15
- No DKIM found: -15
- Missing reverse DNS: -10

### domain_reputation
Check domain email reputation. Analyzes MX records and identifies mail providers (Google Workspace, Microsoft 365, Proofpoint, etc.), checks the primary MX IP against 4 DNS blacklists (Spamhaus, SpamCop, Barracuda, SORBS), retrieves SOA and nameserver information, and provides an overall reputation assessment.

### validate_email
Validate an email address. Checks RFC 5322 format compliance, verifies the domain has MX records, detects 50+ disposable/temporary email domains (mailinator, guerrillamail, tempmail, etc.), and identifies role-based addresses (admin@, info@, support@, etc.). Returns validation result with risk level (low/medium/high).

## Installation

```bash
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-email-deliverability": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "<path-to-mcp-email-deliverability>"
    }
  }
}
```

## Dependencies

- `mcp>=1.0.0` - MCP protocol SDK
- `dnspython>=2.6.0` - Async DNS resolution
- `httpx>=0.27.0` - HTTP client
- `pydantic>=2.0.0` - Data validation

## License

Proprietary - All rights reserved.
