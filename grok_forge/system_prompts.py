"""Your saved system prompts for Prompt Writer · System Prompt Library.

Stored in ComfyUI/user/grok_prompt_forge/system_prompts.json - not in the
workflow and never in the node pack: label -> text. The built-in presets'
system prompts are never stored here and can't be overwritten: a label that is
the name of a built-in preset is refused."""

import json
import os
import threading

from .api import user_dir
from .builtin_presets import BUILTIN

MAX_LABEL = 80
MARK = "★ "  # how the library node marks your own prompts; never part of a label

_lock = threading.Lock()


def _path():
    return os.path.join(user_dir(), "system_prompts.json")


def _read():
    try:
        with open(_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"[Prompt Writer] system_prompts.json unreadable, ignoring it: {e}")
        return {}
    prompts = data.get("prompts") if isinstance(data, dict) else None
    if not isinstance(prompts, dict):
        return {}
    return {str(k): str(v) for k, v in prompts.items() if isinstance(v, str)}


def _write(prompts):
    path = _path()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"version": 1, "prompts": prompts}, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def load():
    """label -> text, sorted by label."""
    with _lock:
        prompts = _read()
    return dict(sorted(prompts.items(), key=lambda kv: kv[0].lower()))


def labels():
    return list(load())


def get(label):
    return load().get(label)


def clean_label(label):
    label = (label or "").strip()
    while label.startswith(MARK.strip()):
        label = label[len(MARK.strip()):].strip()
    return label


def save(label, text):
    label = clean_label(label)
    if not label:
        raise ValueError("Label is empty.")
    if label in BUILTIN:
        raise ValueError(f'"{label}" is a built-in preset - built-ins stay unchanged. '
                         "Choose a name of your own.")
    if len(label) > MAX_LABEL:
        raise ValueError(f"Label is longer than {MAX_LABEL} characters.")
    if not (text or "").strip():
        raise ValueError("The system prompt is empty.")
    with _lock:
        prompts = _read()
        prompts[label] = text.strip()
        _write(prompts)
    return label


def delete(label):
    label = clean_label(label)
    with _lock:
        prompts = _read()
        if label not in prompts:
            return False
        del prompts[label]
        _write(prompts)
    return True
