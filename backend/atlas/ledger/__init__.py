"""Individual ledgers + global anchoring.

Per-user / per-space append-only ledgers (Merkle accumulators) whose COMMITMENTS — never
content — anchor to a decentralized global ledger, bound to a drand round (the decentralized
timekeeper). A per-conversation policy chooses accountable-anchored vs deniable.
"""
