# Atlas PoC — Backend / Protocol Core (Milestone 1)

This is the Mac-side server/verifier node and the kit-independent protocol core.
It is the full substance of **Milestone 1** (security + cryptographic identity, no liveness) plus the
simulation-tier liveness math.

Everything here **runs and is fully tested off-device**. The iOS / Secure-Enclave
/ BLE / camera / JavaCard surfaces are written separately as Swift source and
verified on the Mac + physical kit — they cannot be exercised in this
environment.

## What's implemented

| Area | Module |
|------|--------|
| AES-256-GCM, HKDF<SHA-256>, SHA-3 hashes | `atlas/crypto/primitives.py` |
| Hybrid KEM — X-Wing-style **ML-KEM-768 + X25519** | `atlas/crypto/kem.py` |
| Hybrid signatures **ML-DSA-65 + Ed25519**; **SPHINCS+** root | `atlas/crypto/sign.py` |
| Shamir **2-of-3** over GF(256) | `atlas/crypto/shamir.py` |
| Public beacon — drand client + offline drand-shaped stand-in | `atlas/beacon/drand.py`, `local_beacon.py` |
| Private beacon — presence-fired Server-QRNG (Living Key) | `atlas/beacon/qrng.py` |
| Session key (coupled + decoupled) + forward-secret ratchet | `atlas/keys/derivation.py` |
| Context separators + scoped capability tokens | `atlas/keys/derivation.py`, `tokens.py` |
| Identity tree TSK→System-ID→children, 1:1 verification | `atlas/keys/identity.py` |
| Threshold recovery — stratified: Enclave (device-present) vs portable shares (total-loss) | `atlas/keys/recovery.py`, `enclave.py` |
| Bayesian liveness gate + PoLE state (no `ring_SE_sig` at Tier 3) | `atlas/liveness/bayes.py` |
| Synthetic live/spoof presence streams | `atlas/liveness/synthetic.py` |
| Ratchet-paced signed attestation + removal states | `atlas/liveness/attestation.py` |
| Device node (composes session key locally) | `atlas/session/device.py` |
| Recognition + evolving tunnel — **hybrid ML-KEM-768 + X25519** (post-quantum) | `atlas/session/recognition.py` |
| Vault encrypted at rest + PQC key-wrap | `atlas/session/vault.py` |
| Two send modes (normal / verified-human-only) | `atlas/session/tunnel.py` |
| Content provenance: **accountable attribution** (resolvable under cause) + ledger anchor; PAD advisory | `atlas/provenance/` |
| Payment arm-per-use (protocol logic; **not air-gapped in sim**) | `atlas/payment/` |

## Frozen decisions (PoC defaults)

Set once in `atlas/params.py`:

1. **Inter-arrival timing is committed** into the next QRNG firing (not merely
   observed) — otherwise forward secrecy is decorative.
2. **Tunnel is symmetric** (jointly rooted): recognition is a key-agreement with
   canonical ordering; neither device leads.
3. **Server returns timed randomness only**; each device composes its session
   key locally (structural — the server never holds a finished session key).
4. Recognition window **ε = 2.0 s**.
5. Epoch length floor/cap = **3 s / 30 s** (the replay window).

## Run it

```bash
cd backend
pip install -r requirements.txt          # pure-Python / prebuilt wheels; no GitHub, no C toolchain
python -m pytest -q                      # 59 tests
python -m demos.demo_milestone1_text     # Milestone-1 exit test, end to end
python -m demos.demo_milestone5_photo    # Milestone-5 capstone (provenanced photo)
```

### Milestone-1 exit test

`demos/demo_milestone1_text.py` runs both wallets in one process and shows:

* **Mode 1** encrypted text A→B over the recognition-seeded tunnel;
* **forward secrecy** — a 2nd message on a ratcheted key that a captured earlier
  key cannot read;
* **Mode 2** verified-human-only viewing — the live, on-network recipient opens
  it while offline / bot / expired-epoch / stolen-device holders are all denied.

## Notes

* **drand:** the public beacon uses a deterministic, drand-shaped offline stand-in (`LocalBeacon`).
  Swap in `DrandHTTPBeacon` on the Mac for the real League-of-Entropy chain; both
  satisfy the same `Beacon` interface. The HTTP client is unit-tested against a
  stub transport.
* **PQC**: the core uses pure-Python ML-KEM-768 / ML-DSA-65 and a prebuilt SPHINCS+
  wheel. On the Mac, `liboqs`/`python-oqs` (and CryptoKit on iOS) are drop-in
  behind the same module interfaces. Verify CryptoKit's PQC surface against your
  target iOS SDK before relying on it.
* Everything is **hybrid (classical + PQC)**.
