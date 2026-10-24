"""Direct, certificate-pinned TLS. Only enabled on the owner's local runtime."""
import hashlib
import hmac
import http.client
import ipaddress
import json
import os
import re
import socket
import ssl
import uuid


class SyncError(Exception):
    pass


def request(host, fingerprint, token, command=None):
    if os.environ.get("SYSTEM_LAN_SYNC") != "1":
        raise SyncError("Start the local launcher to enable LAN sync.")
    ip = ipaddress.ip_address(host)
    if ip.version != 4 or not (ip in ipaddress.ip_network("10.0.0.0/8") or
            ip in ipaddress.ip_network("172.16.0.0/12") or ip in ipaddress.ip_network("192.168.0.0/16")):
        raise SyncError("Enter the phone's private Wi-Fi IPv4 address.")
    pin = fingerprint.replace(":", "").strip().lower()
    if not re.fullmatch("[0-9a-f]{64}", pin):
        raise SyncError("Copy the complete certificate fingerprint from your phone.")
    if not token or any(c in token for c in "\r\n"):
        raise SyncError("Enter the pairing token shown on the phone.")
    # The pinned self-signed certificate is the trust anchor. Verify it BEFORE
    # transmitting the token, request path or personal data.
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    with socket.create_connection((str(ip), 8766), timeout=5) as raw:
        with context.wrap_socket(raw, server_hostname=str(ip)) as conn:
            actual = hashlib.sha256(conn.getpeercert(binary_form=True)).hexdigest()
            if not hmac.compare_digest(actual, pin):
                raise SyncError("Phone certificate mismatch. No credentials were sent.")
            body = json.dumps(command).encode() if command else b""
            path = "/v1/command" if command else "/v1/state"
            method = "POST" if command else "GET"
            header = (f"{method} {path} HTTP/1.1\r\nHost: {ip}\r\n"
                      f"Authorization: Bearer {token}\r\nContent-Type: application/json\r\n"
                      f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n").encode()
            conn.sendall(header + body)
            response = http.client.HTTPResponse(conn)
            response.begin()
            data = response.read(20_000_001)
            if len(data) > 20_000_000:
                raise SyncError("Phone response too large.")
            if response.status == 409:
                raise SyncError("Phone changed. Refresh and review before submitting again.")
            if response.status != 200:
                raise SyncError(f"Phone rejected sync ({response.status}). Check pairing and prerequisites.")
            result = json.loads(data)
            if not isinstance(result.get("state"), dict) or not isinstance(result.get("revision"), str):
                raise SyncError("Invalid phone response.")
            return result


def command(revision, op, args):
    return {"requestId": str(uuid.uuid4()), "revision": revision, "op": op, "args": args}
