# Whop Product Listings — MCP Tools Week 1
> Ready to publish. Price: $29 each.

---

## 1. Email Deliverability Checker MCP

**Tagline:** Audit any domain's email setup in seconds — SPF, DKIM, DMARC, spam score, blacklist checks.

**Description:**
Stop guessing why emails land in spam. This MCP server gives Claude (or any MCP client) 6 professional-grade email deliverability tools:

- **check_spf** — Parse SPF records, evaluate policy strength (strict/moderate/permissive), flag misconfigurations
- **check_dkim** — Validate DKIM keys across 15 common selectors, check RSA bit length
- **check_dmarc** — Full DMARC tag analysis with enforcement level and alignment checks
- **spam_score** — 0-100 deliverability score with letter grade (A-F), weighted deductions, prioritized fixes
- **domain_reputation** — MX provider detection (Google/M365/Proofpoint), 4-blacklist check (Spamhaus/SpamCop/Barracuda/SORBS)
- **validate_email** — Full email address validation

One `pip install`, one line in your Claude config. Works with Claude Code, Cursor, Windsurf, or any MCP client.

**What you get:** Source code, pip-installable package, README with setup instructions, lifetime updates.

---

## 2. DNS & Domain Intelligence MCP

**Tagline:** WHOIS, DNS records, subdomain discovery, SSL certs, domain age — all from your AI assistant.

**Description:**
Turn Claude into a domain intelligence analyst. 6 async tools for instant domain recon:

- **whois_lookup** — Full WHOIS: registrar, dates, name servers, status, registrant, DNSSEC
- **dns_records** — Query A, AAAA, MX, NS, TXT, CNAME, SOA, CAA, SRV, PTR with parsed fields
- **subdomain_enum** — Async brute-force discovery with 100-word common subdomain list
- **ssl_cert_info** — Certificate inspection: subject, issuer, SANs, expiry, chain validation
- **reverse_dns** — PTR lookup with forward-confirmed reverse DNS verification
- **domain_age** — Age calculation with human-readable output and new-domain flagging

Built async for speed. Perfect for security audits, due diligence, competitive research, or domain purchasing decisions.

---

## 3. QR Code Factory MCP

**Tagline:** Generate and decode QR codes, vCards, WiFi configs, styled QRs — right from Claude.

**Description:**
6 QR code tools your AI assistant can use directly:

- **generate_qr** — Text/URL to QR code (PNG or SVG), configurable size/border/error correction
- **decode_qr** — Decode QR codes from images (supports multiple codes per image)
- **generate_vcard_qr** — Contact cards: name, email, phone, org, title, URL, address
- **generate_wifi_qr** — WiFi auto-connect QRs (WPA/WEP/open, hidden SSID support)
- **styled_qr** — Custom colors + embedded logo with auto error correction
- **bulk_generate** — Batch generate from a list with auto-naming

Use cases: event badges, WiFi cards for offices/AirBnBs, business cards, inventory labels, marketing materials. Let Claude generate them all.

---

## 4. PDF Toolkit MCP

**Tagline:** Merge, split, extract, OCR, watermark, and convert PDFs — 7 tools for Claude.

**Description:**
Production-grade PDF manipulation via MCP. Built on pypdf, pdfplumber, and reportlab:

- **merge_pdfs** — Combine multiple PDFs into one
- **split_pdf** — Split by pages, ranges, or every-N chunks
- **extract_text** — Plain or structured text with layout info
- **fill_form** — List fields or fill PDF forms programmatically
- **add_watermark** — Text overlay (center/diagonal/header/footer) on every page
- **pdf_ocr** — OCR fallback for scanned documents (with Tesseract)
- **pdf_to_images** — Convert pages to PNG/JPEG

Perfect for document processing pipelines, invoice handling, report generation, contract management. Let your AI handle the PDF grunt work.

---

## 5. Image Tools MCP

**Tagline:** Resize, convert, compress, watermark, strip metadata, read EXIF — 7 image processing tools.

**Description:**
Professional image processing via MCP, powered by Pillow:

- **resize_image** — Aspect-ratio-aware resizing with lanczos/bilinear/bicubic resampling
- **convert_format** — PNG/JPEG/WebP/TIFF/BMP/GIF/ICO with auto RGBA-to-RGB handling
- **compress_image** — Smart format-aware compression with optional downscaling
- **add_watermark** — Text or image watermarks (center/corners/tile) with opacity control
- **strip_metadata** — Remove all EXIF/IPTC/XMP metadata, optional ICC preservation
- **read_exif** — Structured EXIF: camera, exposure, GPS coordinates, orientation
- **batch_process** — Pipeline chains (resize + convert + compress + watermark) across directories

Use cases: thumbnail generation, social media prep, GDPR metadata stripping, photo processing pipelines, e-commerce image optimization.

---

## Bundle: Developer Essentials (all 5) — $99

Get all 5 Week 1 MCP tools at 32% off. 32 total tools for email, DNS, QR codes, PDFs, and images. One purchase, lifetime updates, works with any MCP client.
