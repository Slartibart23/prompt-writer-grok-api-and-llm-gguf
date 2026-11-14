"""Prompt Writer · System Prompt: your own system prompt for the writer nodes,
with a label. It either replaces the preset's system prompt or is appended to
it, and it is either saved in your library (system_prompts.json, not in the
workflow) or used only for this run."""

from . import system_prompts

LOG = "[Prompt Writer · System Prompt]"
MODES = ["append", "replace"]


class PromptWriterSystemPrompt:
    CATEGORY = "Prompt Writer"
    RETURN_TYPES = ("PW_SYSTEM",)
    RETURN_NAMES = ("system",)
    OUTPUT_TOOLTIPS = ("Connect to the 'system' input of Prompt Writer · Grok API or LLM GGUF.",)
    FUNCTION = "build"
    DESCRIPTION = ("Your own system prompt with a label: appended to the preset's system prompt "
                   "or used instead of it, saved in your library or only for this run.")

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "label": ("STRING", {"default": "", "tooltip":
                "Name of this system prompt in your library. '📂 Load...' picks a saved one; "
                "a new label creates a new entry when it is saved."}),
            "text": ("STRING", {"multiline": True, "default": "", "tooltip":
                "The system prompt or the extra instructions. Empty = this node does nothing."}),
            "mode": (MODES, {"default": "append", "tooltip":
                "append: added to the preset's system prompt as extra binding instructions "
                "(e.g. your own rules on top of a model guide).\n"
                "replace: used instead of the preset's system prompt."}),
            "save": ("BOOLEAN", {"default": False, "tooltip":
                "On: the text is saved under the label in your library "
                "(ComfyUI/user/grok_prompt_forge/system_prompts.json) every time it runs, so you "
                "can load it again in any workflow.\n"
                "Off: temporary - used only for this run, the library stays as it is. "
                "'💾 Save now' saves it at once without a run."}),
        }}

    def build(self, label, text, mode, save):
        label = (label or "").strip()
        if save and label and (text or "").strip():
            try:
                system_prompts.save(label, text)
            except (OSError, ValueError) as e:
                print(f"{LOG} not saved: {e}")
        return ({"label": label, "text": text or "", "mode": mode if mode in MODES else "append"},)
