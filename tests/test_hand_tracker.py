from io import BytesIO

import pytest

import hand_tracker


def test_load_model_asset_uses_existing_file(tmp_path, monkeypatch):
    model_path = tmp_path / "model.task"
    model_path.write_bytes(b"existing-model")

    def unexpected_download(*args, **kwargs):
        raise AssertionError("An existing model should not be downloaded again")

    monkeypatch.setattr(hand_tracker, "urlopen", unexpected_download)

    assert hand_tracker._load_model_asset(model_path) == b"existing-model"


def test_load_model_asset_downloads_missing_file(tmp_path, monkeypatch):
    model_path = tmp_path / "cache" / "model.task"
    model_bytes = b"downloaded-model"
    monkeypatch.setattr(
        hand_tracker,
        "urlopen",
        lambda url, timeout: BytesIO(model_bytes),
    )

    assert hand_tracker._load_model_asset(model_path) == model_bytes
    assert model_path.read_bytes() == model_bytes
    assert list(model_path.parent.iterdir()) == [model_path]


def test_load_model_asset_reports_download_failure(tmp_path, monkeypatch):
    model_path = tmp_path / "cache" / "model.task"

    def fail_download(url, timeout):
        raise OSError("offline")

    monkeypatch.setattr(hand_tracker, "urlopen", fail_download)

    with pytest.raises(RuntimeError, match="Check your network connection"):
        hand_tracker._load_model_asset(model_path)

    assert not model_path.exists()