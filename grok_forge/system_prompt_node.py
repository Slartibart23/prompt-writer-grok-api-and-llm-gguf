"""Prompt Writer · System Prompt Library: the system prompt for the writer nodes,
chosen from the whole library - the built-in presets' system prompts, your own
presets and your saved system prompts (system_prompts.json, not in the
workflow). The browser part (web/grok_prompt_forge.js) lists them with filters,
puts the chosen one into label and text and has a large editor, "Save as..." and
"Delete"; this node only delivers label, text and mode.

The class ID and its first four widgets are the ones of the 1.5.0 node
"Prompt Writer · System Prompt", so saved workflows load unchanged."""

from . import system_prompts
from .builtin_presets import BUILTIN

LOG = "[Prompt Writer · System Prompt Library]"
MODES = ["replace", "append"]


class PromptWriterSystemPrompt:
    CATEGORY = "Prompt Writer"
    RETURN_TYPES = ("PW_SYSTEM",)
    RETURN_NAMES = ("system",)
    OUTPUT_TOOLTIPS = ("Connect to the 'system' input of Prompt Writer · Grok API or LLM GGUF. "
                       "In mode 'replace' the writer's own system_prompt field is locked.",)
    FUNCTION = "build"
    DESCRIPTION = ("The system prompt library: choose a system prompt from the built-in presets, "
                   "your own presets or your saved system prompts, edit it in a large editor and "
                   "save it under a name of your own. Preset, negative prompt and sampling stay "
                   "on the writer node.")

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "label": ("STRING", {"default": "", "tooltip":
                "Name of this system prompt. Choosing one from the library fills it in; "
                "'💾 Save as...' asks for a name of your own (built-in presets are never "
                "overwritten)."}),
            "text": ("STRING", {"multiline": True, "default": "", "tooltip":
                "The system prompt (mode replace) or the extra instructions (mode append). "
                "'📝 Open editor...' edits it in a large window with a word and character "
                "count. Empty = this node does nothing."}),
            "mode": (MODES, {"default": "replace", "tooltip":
                "replace (default): used instead of the writer's system_prompt field, which is "
                "locked while this node is connected.\n"
                "append: added to the writer's system prompt as extra binding instructions "
                "(e.g. your own rules on top of a model guide)."}),
            "save": ("BOOLEAN", {"default": False, "tooltip":
                "On: the text is saved under the label in your library "
                "(ComfyUI/user/grok_prompt_forge/system_prompts.json) every time it runs.\n"
                "Off (default): nothing is saved on a run - '💾 Save as...' saves on demand "
                "under a name you choose. Built-in presets are never overwritten."}),
        }}

    def build(self, label, text, mode, save):
        label = system_prompts.clean_label(label)
        if save and label and (text or "").strip():
            if label in BUILTIN:
                print(f'{LOG} "{label}" is a built-in preset - not saved; built-ins stay unchanged.')
            else:
                try:
                    system_prompts.save(label, text)
                except (OSError, ValueError) as e:
                    print(f"{LOG} not saved: {e}")
        return ({"label": label, "text": text or "", "mode": mode if mode in MODES else "replace"},)
