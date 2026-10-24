# Direct phone ↔ laptop sync

The phone owns the authoritative SQLite database. A local Streamlit runtime
polls it every 10 seconds while the page is active. The hosted Streamlit site
cannot reach your private Wi-Fi network and does not accept pairing credentials.

## Setup

1. Install the updated Android build, retaining the original signing identity.
   Export a backup first. Open the new **SYSTEM Sync** launcher.
2. Join the same Wi-Fi as your laptop. Tap **Show pairing details**, then
   **Enable Wi-Fi sync**. A foreground notification provides a Stop control.
3. On the laptop, install requirements and run:

       python run_laptop.py

4. In the sidebar, copy the phone IP, SHA-256 certificate fingerprint and token
   directly from the phone. Click Connect. Do not paste credentials into chat
   or a hosted site.

The phone IP may change; reconnect using its new address. Networks with client
isolation (including some campus Wi-Fi) may prevent direct communication; use
a trusted private Wi-Fi network in that case. Do not forward port 8766.

## Behavior and limits

Live snapshots include the phone state. The laptop can record study completion
with evidence, notes and assistance used. The phone validates it through the
same Career rules as native completion and updates matching planned tasks.
The API also permits study planning, skill assessments and project commands;
the laptop UI currently exposes study completion only. It does not overwrite
whole backups or edit financial/focus settings.

Commands compare the displayed state revision inside a SQLite transaction.
Concurrent edits return a conflict, requiring refresh and review. A unique
request ID and receipt are committed atomically with each accepted command.
Retry last unconfirmed update reuses the original ID; 500 recent receipts are
retained. Older requests still cannot overwrite a later state revision.
Offline views remain readable but cannot commit; no background offline queue
or automatic conflict merge is included.

TLS 1.2 encrypts transfers; the client verifies the exact phone certificate
before sending credentials. Tokens are generated on-device, held in local
Streamlit session memory and excluded from Android backups. Stop/revoke
invalidates the token. The endpoint binds only to a private Wi-Fi IPv4 address,
uses bounded requests and timeouts, and rejects browser-origin requests.

The service runs while Android permits its foreground service. No Android app
can guarantee 24/7 availability through force-stop, reboot, Doze, battery
management or lost Wi-Fi. Re-enable sync after reboot or a network change.
No wake lock or battery-optimization exemption is forced on the user.

## Validation

Python tests cover local-only gating, address restrictions, no token transmission
on pin mismatch, GET/POST handling and conflict reporting using mocked TLS.
Streamlit AppTest covers every page. Native compile/lint/tests run in GitHub CI.
Physical OnePlus screen-off behavior, Android Keystore TLS and real Wi-Fi
transfer require device acceptance testing; mocked tests do not establish those.
