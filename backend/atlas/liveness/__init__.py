"""Liveness layer (PoLE) — Tier 3 simulation ('Partial (sim)').

On real hardware the raw PPG/accelerometer stream arrives from the R10 over BLE
and is gated inside the Secure Enclave. Here we model the Bayesian gate,
synthetic presence streams, and the ratchet-paced attestation + removal
states so the algorithm — not the biology — is tested.
"""

from .bayes import LivenessGate, PoLEState
from .synthetic import live_stream, spoof_stream, SensorSample
from .attestation import (
    AttestationSubsystem,
    LivenessAttestation,
    RemovalState,
)

__all__ = [
    "LivenessGate",
    "PoLEState",
    "live_stream",
    "spoof_stream",
    "SensorSample",
    "AttestationSubsystem",
    "LivenessAttestation",
    "RemovalState",
]
