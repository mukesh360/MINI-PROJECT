import tempfile
from pathlib import Path

from ingestion.fingerprint import (
    compute_file_fingerprint,
    is_file_registered,
    register_file,
)


def test_compute_file_fingerprint_consistent():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"hello world")
        path = f.name

    fp1 = compute_file_fingerprint(path)
    fp2 = compute_file_fingerprint(path)

    assert fp1 == fp2


def test_file_registry_roundtrip(tmp_path, monkeypatch):
    # Use temp registry instead of real one
    fake_registry = tmp_path / "registry.json"

    monkeypatch.setattr(
        "ingestion.fingerprint.REGISTRY_PATH",
        str(fake_registry),
    )

    fingerprint = "abc123"
    metadata = {"name": "test.pdf"}

    assert not is_file_registered(fingerprint)

    register_file(fingerprint, metadata)

    assert is_file_registered(fingerprint)
