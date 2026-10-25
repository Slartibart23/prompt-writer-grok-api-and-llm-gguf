# Changelog

## 1.2.0 — 2026-10-25

- **"Idea ▸" is now "Generation ▸"** (e.g. "Generation ▸ FLUX"). Saved workflows show the new name on loading, and values you saved under an old "Idea ▸" name carry over to the new one. The default preset is "Generation ▸ Krea 2".
- **Presets for API models:** 28 new presets ("Generation ▸" and "Caption ▸") for 14 API targets, written from the makers' own prompt guides:
  - images: Seedream 5.0, Seedream 4.5 / 4.0, Seedream Edit, GPT Image, Nano Banana, Grok Imagine Image, Flux 3;
  - video: Seedance 2.5, Seedance 2.0, Seedance 1.5 / 1.0 Pro, Seedance Reference, Kling 3.0, Veo 3.1, Grok Imagine Video.

  Each has its own model guide, an example result, a recommended length and German notes. The FLUX preset now also names FLUX.2 [pro] / [max] / [flex].
- **Fourth image input:** `image_4`, so every person has its own image input (`person_4` = `image_4` with `image_n_is_person_n`). It sits at the end of the node, so saved workflows keep their connections and values.
- **Preset filters:** "Filter: type" (All, Image, Edit, Video, Captions & tools, My presets) and "Filter: task" (All, Generation, Caption) above the preset list. Display only: the selected preset is kept, nothing re-runs, and the choice is kept per node in the workflow.
- `image_n_is_person_n` is now **off** for new nodes. Saved workflows keep their setting.
- The nodes always start in **English**; German applies until the page is reloaded and is no longer remembered in the browser.
- Tooltips, the persons' voice note and the README cover the new models.

## 1.1.0 — 2026-10-24

- Selected persons (`person_1` … `person_4`) get a dark red field background, selected style blocks (`style_1`, `style_2`) a dark blue one, on both writer nodes. "(none)" keeps the normal look. This is display only: it is not saved in the workflow and never re-runs a node.

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
