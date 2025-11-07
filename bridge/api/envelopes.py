"""Helpers for deterministic HTTP response envelopes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, MutableMapping


@dataclass(slots=True)
class Envelope:
    """Simple serialisable envelope structure."""

    ok: bool
    data: Any
    errors: list[MutableMapping[str, Any]]

    def to_json(self) -> Dict[str, Any]:
        return {"ok": self.ok, "data": self.data, "errors": self.errors}


def _error_payload(code: str, message: str, *, details: Mapping[str, Any] | None = None) -> MutableMapping[str, Any]:
    payload: MutableMapping[str, Any] = {"code": code, "message": message}
    if details:
        payload["details"] = dict(details)
    return payload


def envelope_ok(data: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    """Wrap a payload in the canonical success envelope."""

    payload = Envelope(ok=True, data=dict(data or {}), errors=[])
    return payload.to_json()


def envelope_error(code: str, message: str, *, details: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    """Wrap an error description in the canonical failure envelope."""

    payload = Envelope(ok=False, data=None, errors=[_error_payload(code, message, details=details)])
    return payload.to_json()


__all__ = ["Envelope", "envelope_error", "envelope_ok"]
