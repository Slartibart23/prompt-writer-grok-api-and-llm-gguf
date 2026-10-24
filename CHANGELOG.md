# Changelog

## 1.0.0 — 2026-10-24

First release of **Prompt Writer – Grok API & LLM GGUF**. It replaces **comfyui-grok-prompt-forge** (last version 3.3.0) under a name that says what it does.

**Nodes**, all in the node menu under *Prompt Writer*:

- **Prompt Writer · Grok API** (formerly Grok Prompt Forge): writes and rewrites prompts and captions images through the xAI Grok API. The default model is `grok-4.20-0309-reasoning`.
- **Prompt Writer · LLM GGUF** (formerly Local Prompt Forge): the same with a local, uncensored Qwen3.8-27B (huihui abliterated or HauhauCS Aggressive). Model and vision projector are downloaded on the first run.
- **Prompt Writer · Show Prompt:** shows a text with its word, tag, sentence and character count.
- **Prompt Writer · System Prompt Loader** and **Prompt Writer · Text File Loader.**

**Included from comfyui-grok-prompt-forge:**

- 30 task presets: "Idea ▸" and "Caption ▸" for Krea 2, Qwen-Image 2.1, Qwen-Image-Edit 2.1, Z-Image, FLUX, Illustrious, Pony, SDXL, Wan 2.2 / 2.7 / 3.0 and MiniMax H3 FL2VA / REF2VA, plus LoRA training caption, describe image, recast and custom.
- Each preset has a model guide with an example result, the standard negative prompt and sampling settings.
- Your own presets.
- Up to four persons and two style blocks from a local library, with export and import.
- A prompt archive with recast.
- An optional word range.
- A rule that makes the user's input binding.
- Three reference image inputs.
- A language switch for English and German.

**Changes against comfyui-grok-prompt-forge 3.3.0:**

- New names for the pack, the nodes and the menu category. The internal node IDs are unchanged, so saved workflows load as they are. Remove the old pack first: both register the same nodes.
- The legacy nodes *Grok Text Refine* and *Grok Vision Caption* were removed. Use Prompt Writer · Grok API with a "Caption ▸ …" preset or "Caption ▸ Describe image" instead.
- Presets, persons, style blocks and the archive are still read from `ComfyUI/user/grok_prompt_forge/`, so your data carries over.
