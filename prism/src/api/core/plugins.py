# ./src/api/core/plugins.py - v1.0.0
from __future__ import annotations

import importlib
import os
import pkgutil
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from .config import AppSettings


@dataclass
class PluginSpec:
    name: str
    version: str
    capabilities: List[str]
    labels: List[str]
    module: Any


class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, PluginSpec] = {}

    def register(self, spec: PluginSpec) -> None:
        self._plugins[spec.name] = spec

    def get(self, name: str) -> Optional[PluginSpec]:
        return self._plugins.get(name)

    def all(self) -> List[PluginSpec]:
        return list(self._plugins.values())


def load_plugins(settings: AppSettings) -> PluginRegistry:
    registry = PluginRegistry()

    base_dir = settings.plugins_dir
    pkg_path = base_dir.replace("/", ".")
    if pkg_path.endswith(".py"):
        pkg_path = pkg_path[:-3]

    # Accept both package (dir) and flat path relative to project root
    search_dir = base_dir if os.path.isabs(base_dir) else os.path.join(os.getcwd(), base_dir)
    if not os.path.isdir(search_dir):
        return registry

    # Discover *.py under plugins directory (excluding dunder files)
    for _, modname, ispkg in pkgutil.iter_modules([search_dir]):
        if ispkg:
            continue
        if modname.startswith("__"):
            continue
        module_qual = f"{pkg_path}.{modname}" if pkg_path else modname
        try:
            module = importlib.import_module(module_qual)
        except Exception:
            continue
        if not hasattr(module, "register"):
            continue
        try:
            info = module.register()
            spec = PluginSpec(
                name=info.get("name", modname),
                version=info.get("version", "v0.0.0"),
                capabilities=info.get("capabilities", []),
                labels=info.get("labels", []),
                module=module,
            )
            registry.register(spec)
        except Exception:
            continue

    return registry


async def classify_item(item: Dict[str, Any], *, registry: PluginRegistry, llm, notion, config: AppSettings) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    for spec in registry.all():
        if "classify" not in spec.capabilities:
            continue
        classify_fn = getattr(spec.module, "classify", None)
        if not callable(classify_fn):
            continue
        try:
            out = await _maybe_await(classify_fn(item, llm=llm, notion=notion, config=config))
            if not isinstance(out, dict):
                continue
            out = {
                "type": out.get("type", "Note"),
                "score": float(out.get("score", 0.0)),
                "tags": list(out.get("tags", [])),
                "reason": out.get("reason", ""),
                "plugin": spec.name,
            }
            results.append(out)
        except Exception:
            continue

    if not results:
        return {"type": "Note", "score": 0.0, "tags": [], "reason": "no plugin matched"}

    # Choose highest score; tie-breaker: Task > Knowledge > Note
    order = {"Task": 3, "Knowledge": 2, "Note": 1}
    results.sort(key=lambda r: (r.get("score", 0.0), order.get(r.get("type"), 0)), reverse=True)
    return results[0]


async def _maybe_await(value):
    if hasattr(value, "__await__"):
        return await value
    return value


__all__ = ["PluginRegistry", "load_plugins", "classify_item"]

# EOF ./src/api/core/plugins.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成