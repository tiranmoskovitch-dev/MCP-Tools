"""SSL certificate inspection service."""
import asyncio
import ssl
import socket
from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, dsa, ed25519, ed448


def _get_cert_pem(domain: str, port: int) -> bytes:
    """Synchronous SSL certificate fetch. Returns PEM-encoded cert bytes."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # We want to inspect even invalid certs

    conn = ctx.wrap_socket(
        socket.create_connection((domain, port), timeout=10),
        server_hostname=domain,
    )
    try:
        der_cert = conn.getpeercert(binary_form=True)
        if der_cert is None:
            raise ConnectionError("No certificate returned by server")
        return der_cert
    finally:
        conn.close()


def _get_chain_info(domain: str, port: int) -> list[dict]:
    """Fetch full certificate chain info."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    chain = []
    try:
        conn = ctx.wrap_socket(
            socket.create_connection((domain, port), timeout=10),
            server_hostname=domain,
        )
        try:
            peer_certs = conn.get_verified_chain()
            if peer_certs is None:
                peer_certs = conn.get_unverified_chain()
            if peer_certs:
                for i, cert_bytes in enumerate(peer_certs):
                    try:
                        c = x509.load_der_x509_certificate(cert_bytes.public_bytes(serialization_encoding=None) if hasattr(cert_bytes, 'public_bytes') else cert_bytes)
                        chain.append({
                            "position": i,
                            "subject": _extract_name_attrs(c.subject),
                            "issuer": _extract_name_attrs(c.issuer),
                        })
                    except Exception:
                        chain.append({"position": i, "subject": "parse_error"})
        except (AttributeError, Exception):
            pass
        finally:
            conn.close()
    except Exception:
        pass
    return chain


def _extract_name_attrs(name: x509.Name) -> dict:
    """Extract common name attributes from an x509 Name."""
    mapping = {
        x509.oid.NameOID.COMMON_NAME: "CN",
        x509.oid.NameOID.ORGANIZATION_NAME: "O",
        x509.oid.NameOID.LOCALITY_NAME: "L",
        x509.oid.NameOID.STATE_OR_PROVINCE_NAME: "ST",
        x509.oid.NameOID.COUNTRY_NAME: "C",
        x509.oid.NameOID.ORGANIZATIONAL_UNIT_NAME: "OU",
    }
    result = {}
    for oid, key in mapping.items():
        try:
            vals = name.get_attributes_for_oid(oid)
            if vals:
                result[key] = vals[0].value
        except Exception:
            continue
    return result


def _get_public_key_info(cert: x509.Certificate) -> dict:
    """Extract public key type and bit size."""
    pub = cert.public_key()
    if isinstance(pub, rsa.RSAPublicKey):
        return {"type": "RSA", "bits": pub.key_size}
    elif isinstance(pub, ec.EllipticCurvePublicKey):
        return {"type": "EC", "bits": pub.key_size, "curve": pub.curve.name}
    elif isinstance(pub, dsa.DSAPublicKey):
        return {"type": "DSA", "bits": pub.key_size}
    elif isinstance(pub, ed25519.Ed25519PublicKey):
        return {"type": "Ed25519", "bits": 256}
    elif isinstance(pub, ed448.Ed448PublicKey):
        return {"type": "Ed448", "bits": 448}
    else:
        return {"type": type(pub).__name__, "bits": None}


def _inspect_cert(domain: str, port: int) -> dict:
    """Synchronous certificate inspection."""
    der_bytes = _get_cert_pem(domain, port)
    cert = x509.load_der_x509_certificate(der_bytes)

    now = datetime.now(timezone.utc)

    # Subject and Issuer
    subject = _extract_name_attrs(cert.subject)
    issuer = _extract_name_attrs(cert.issuer)

    # Validity
    not_before = cert.not_valid_before_utc if hasattr(cert, 'not_valid_before_utc') else cert.not_valid_before.replace(tzinfo=timezone.utc)
    not_after = cert.not_valid_after_utc if hasattr(cert, 'not_valid_after_utc') else cert.not_valid_after.replace(tzinfo=timezone.utc)
    days_until_expiry = (not_after - now).days
    is_expired = now > not_after

    # Signature algorithm
    sig_algo = cert.signature_algorithm_oid._name if hasattr(cert.signature_algorithm_oid, '_name') else str(cert.signature_algorithm_oid.dotted_string)
    try:
        sig_algo = cert.signature_hash_algorithm.name if cert.signature_hash_algorithm else sig_algo
    except Exception:
        pass

    # Public key
    pk_info = _get_public_key_info(cert)

    # SANs
    san_domains = []
    try:
        san_ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        san_domains = san_ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        pass
    except Exception:
        pass

    # Wildcard check
    is_wildcard = any(d.startswith("*.") for d in san_domains)
    if not is_wildcard and subject.get("CN", "").startswith("*."):
        is_wildcard = True

    # Serial
    serial_hex = format(cert.serial_number, "X")

    # Chain info (best-effort)
    chain = _get_chain_info(domain, port)

    return {
        "domain": domain,
        "port": port,
        "subject": subject,
        "issuer": issuer,
        "serial_number": serial_hex,
        "not_before": not_before.isoformat(),
        "not_after": not_after.isoformat(),
        "days_until_expiry": days_until_expiry,
        "signature_algorithm": sig_algo,
        "public_key_type": pk_info["type"],
        "public_key_bits": pk_info.get("bits"),
        "san_domains": san_domains,
        "is_expired": is_expired,
        "is_wildcard": is_wildcard,
        "certificate_chain": chain if chain else None,
    }


async def ssl_cert_info(domain: str, port: int = 443) -> dict:
    """Inspect SSL certificate for a domain."""
    try:
        result = await asyncio.to_thread(_inspect_cert, domain, port)
        return {"success": True, "data": result}
    except socket.gaierror:
        return {"success": False, "error": f"Could not resolve domain: {domain}"}
    except socket.timeout:
        return {"success": False, "error": f"Connection to {domain}:{port} timed out"}
    except ConnectionRefusedError:
        return {"success": False, "error": f"Connection refused: {domain}:{port}"}
    except ssl.SSLError as exc:
        return {"success": False, "error": f"SSL error: {exc}"}
    except Exception as exc:
        return {"success": False, "error": f"Certificate inspection failed: {exc}", "error_type": type(exc).__name__}
