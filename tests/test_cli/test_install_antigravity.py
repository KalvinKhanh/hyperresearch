"""Tests for `hyperresearch install --harness antigravity|claude|both`."""

from __future__ import annotations

import json
from typing import Any

import pytest
from typer.testing import CliRunner

from hyperresearch.cli import app

runner = CliRunner()


def test_install_harness_antigravity(tmp_vault: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_vault.root)
    result = runner.invoke(
        app, ["install", str(tmp_vault.root), "--harness", "antigravity", "--json"]
    )
    assert result.exit_code == 0

    # Antigravity artifacts
    router = tmp_vault.root / ".agents" / "skills" / "hyperresearch" / "SKILL.md"
    assert router.exists()
    assert "Hyperresearch V8" in router.read_text(encoding="utf-8")

    step1 = tmp_vault.root / ".agents" / "skills" / "hyperresearch-1-decompose" / "SKILL.md"
    assert step1.exists()

    step14 = tmp_vault.root / ".agents" / "skills" / "hyperresearch-14-patcher" / "SKILL.md"
    assert step14.exists()

    hooks = tmp_vault.root / ".agents" / "hooks.json"
    assert hooks.exists()
    hooks_data = json.loads(hooks.read_text(encoding="utf-8"))
    assert "hyperresearch-vault-checker" in hooks_data

    agents_doc = tmp_vault.root / "AGENTS.md"
    assert agents_doc.exists()
    assert "Research Base (hyperresearch)" in agents_doc.read_text(encoding="utf-8")

    gemini_doc = tmp_vault.root / "GEMINI.md"
    assert gemini_doc.exists()

    # Claude folder should NOT be created when exclusively targeting antigravity
    assert not (tmp_vault.root / ".claude").exists()


def test_install_harness_claude(tmp_vault: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_vault.root)
    result = runner.invoke(
        app, ["install", str(tmp_vault.root), "--harness", "claude", "--json"]
    )
    assert result.exit_code == 0

    # Claude artifacts
    router = tmp_vault.root / ".claude" / "skills" / "hyperresearch" / "SKILL.md"
    assert router.exists()

    claude_doc = tmp_vault.root / "CLAUDE.md"
    assert claude_doc.exists()

    # Antigravity folder should NOT be created when exclusively targeting claude
    assert not (tmp_vault.root / ".agents").exists()


def test_install_steps_only_antigravity(tmp_vault: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_vault.root)
    result = runner.invoke(
        app, ["install", str(tmp_vault.root), "--steps-only", "--harness", "antigravity", "--json"]
    )
    assert result.exit_code == 0

    step2 = tmp_vault.root / ".agents" / "skills" / "hyperresearch-2-width-sweep" / "SKILL.md"
    assert step2.exists()


def test_install_default_installs_both(tmp_vault: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_vault.root)
    result = runner.invoke(app, ["install", str(tmp_vault.root), "--json"])
    assert result.exit_code == 0

    # Both harnesses present
    assert (tmp_vault.root / ".agents" / "skills" / "hyperresearch" / "SKILL.md").exists()
    assert (tmp_vault.root / ".claude" / "skills" / "hyperresearch" / "SKILL.md").exists()
    assert (tmp_vault.root / "AGENTS.md").exists()
    assert (tmp_vault.root / "CLAUDE.md").exists()
