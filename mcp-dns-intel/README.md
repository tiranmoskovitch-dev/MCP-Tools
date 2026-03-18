# DNS & Domain Intelligence MCP Server

> WHOIS lookup, DNS records, subdomain enumeration, SSL certificate analysis, reverse DNS, domain age.

**MCP Protocol** | **Python 3.11+** | **Async**

## Tools

| Tool | Description |
|------|-------------|
| **whois_lookup** | Full WHOIS data: registrar, dates, name servers, status, registrant, DNSSEC |
| **dns_records** | Query A, AAAA, MX, NS, TXT, CNAME, SOA, CAA, SRV, PTR with parsed fields |
| **subdomain_enum** | Async brute-force subdomain discovery (100 common subdomain wordlist) |
| **ssl_cert_info** | SSL/TLS certificate inspection: subject, issuer, SANs, expiry, chain |
| **reverse_dns** | PTR lookup with forward-confirmed reverse DNS verification |
| **domain_age** | Domain age calculation with human-readable output and new-domain detection |

## Installation

```bash
cd mcp-dns-intel
pip install -e .
```

## Usage with Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-dns-intel": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/mcp-dns-intel"
    }
  }
}
```

## Tool Details

### whois_lookup
```json
{ "domain": "example.com" }
```
Returns registrar, creation/expiration/updated dates, name servers, status codes, registrant org/country, DNSSEC.

### dns_records
```json
{ "domain": "example.com", "record_type": "ALL" }
```
Supported types: `A`, `AAAA`, `MX`, `NS`, `TXT`, `CNAME`, `SOA`, `CAA`, `SRV`, `PTR`, or `ALL`.
Returns TTL, values, and parsed fields (MX priority, SOA serial/refresh/retry/expire, SRV weight/port, CAA flags/tag).

### subdomain_enum
```json
{ "domain": "example.com", "wordlist": "common" }
```
Async DNS brute-force with 100 common subdomains. 50 concurrent lookups. Returns found subdomains with A record IPs.

### ssl_cert_info
```json
{ "domain": "example.com", "port": 443 }
```
Returns subject (CN/O/L/ST/C), issuer, serial, validity dates, days until expiry, signature algorithm, public key type/bits, SANs, wildcard status, certificate chain info.

### reverse_dns
```json
{ "ip": "8.8.8.8" }
```
PTR lookup with forward-confirmation: resolves the PTR hostname back and checks if it maps to the original IP.

### domain_age
```json
{ "domain": "example.com" }
```
Returns creation date, age in days, human-readable age ("3 years, 2 months, 15 days"), expiration info, and new-domain flag (< 30 days).

## Architecture

```
src/
  server.py              # MCP server: list_tools + call_tool dispatch
  services/
    whois_service.py     # whois_lookup, domain_age
    dns_service.py       # dns_records, subdomain_enum, reverse_dns
    ssl_service.py       # ssl_cert_info
```

## License

Proprietary - All rights reserved.
