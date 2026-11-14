# Changelog

## 1.5.1 — 2026-11-14

- **Stronger styles:** with a style block selected, the prompt now opens and closes with the medium and technique, and every element - persons, clothes, objects, background - is described in the language of the style, not only named once. This overrides the order of the model guides, so paintings and drawings no longer drift into photos.
- **Sharper style templates** with the styles' own technical terms (impasto, chiaroscuro, craquelure, hatching, eraser marks ...), especially Oil painting, Rembrandt, Pencil sketch, Van Gogh, Line drawing and GTA VI.
- **New style templates:** *Manga* (black-and-white ink, screentones, speed lines - unlike *Anime*, the colour look of animation) and *Hentai* (explicit adult anime look with clearly adult characters).
- "📥 Add templates" updates style blocks that still hold an earlier template text unchanged.

## 1.5.0 — 2026-11-14

- **New node Prompt Writer · System Prompt:** your own system prompt with a label, connected to the new `system` input of the writer nodes. Mode `append` adds it to the preset's system prompt, mode `replace` uses it instead. With `save` on it is kept in `ComfyUI/user/grok_prompt_forge/system_prompts.json` (not in the workflow), off it is temporary. Buttons to load (with the text on hover), save now and delete.
- **`light` on the writer nodes:** `daylight` (default) asks for clear, white, natural daylight without drama; `night` for deep darkness with one faint light source; `free` sets nothing. Your text always wins; the medium is never changed by it. The example results of all presets now use natural daylight.
- **Adult content:** explicit by default and precise - who does what to whom with which body part, contact points, positions, state of undress and body fluids by name. All persons in such content are adults. The new switch **`safe`** (default off) only implies sexual content instead, e.g. for the API models with content filters.
- **New persons are filled in from their label:** "Peter" suggests the name and trigger "P3ter" (first a, e, i or o becomes a digit), gender male and a description that starts with the name. Your own changes are kept; renaming also renames the name in the description.
- **Style templates:** "📥 Add templates" now also adds fifteen style blocks - Natural daylight, Cartoon, Oil painting, Line drawing, Watercolour, Pencil sketch, Anime, Comic book, 3D render, Vintage film photo, Van Gogh, Rembrandt, Simpsons, Pixar and GTA VI. They use positive words only: what the picture is and how it was made (painted, drawn, computer-generated ...), never what it is not.
- **Positive wording:** the system prompt tells the writer to describe styles and light only positively and never to name a left-out quality, not even negated ("not a photograph", "no realism") - image models are pulled towards every word in a prompt. A style block that brings its own light (e.g. Rembrandt) wins over `light`.
- Template persons: the trigger is now the name (K3nji …); Sean's name is S3an, following the first-letter rule.
- New inputs and widgets sit at the end of the writer nodes, so saved workflows keep their values and connections.

## 1.4.0 — 2026-11-10

- **Label and name are separate:** a person entry has a **label** for the list and the selection boxes (e.g. "Peter with glasses", "Peter with beard") and a **name in the prompt** (e.g. "P3ter"). Several entries may share a name and differ in their description. Entries without a name keep working as before: their label is the name.
- **Gender** (male / female / unknown) as a new field; it goes into the prompt so pronouns and gendered details fit, and groups get "all members are male / female".
- **On hover:** the tooltip of `person_1` … `person_4` shows the selected person's name, gender, trigger and description; so does an entry in the persons dialog's list.
- **Templates:** labels are now the real names (Kenji, Kwame, Amara …), the names in the prompt stay K3nji, Kw4me, 4mara …; every template has its gender. "📥 Add templates" adds them under the new labels; template entries added with 1.3.0 (labelled K3nji etc.) stay in your library until you delete them.

## 1.3.0 — 2026-11-02

- **New node Prompt Writer · Persons:** chooses up to four persons from your library outside the writer nodes. Its `persons` output goes to the new `persons` input of Prompt Writer · Grok API and LLM GGUF; one Persons node can feed several writers. While the input is connected, the writer's own `person_1` … `person_4` are greyed out, locked and ignored. The slot numbers come from the Persons node, also for `image_n_is_person_n`. The new input sits at the end of the writer nodes, so saved workflows keep their values and connections.
- **Template persons:** "📥 Add templates" in the persons dialog adds ten fictional persons (eight men, two women) and two groups, **Group_of_men** (six) and **Group_of_women** (four). The descriptions cover only the outer appearance, in detailed English sentences without measurements, and every name is also its trigger (e.g. K3nji, 4mara). Names already in your library are never changed.
- **Groups:** a person entry whose description starts with "A group of" stands for several named persons in one slot. The prompt introduces every member by name and assigns actions to members; the group's own name is only a label.

## 1.2.1 — 2026-10-31

- **Prompts in full sentences:** every preset that writes prose (all image and video targets except the tag models and the edit instructions, plus "Describe image" and "LoRA training caption") now asks for complete sentences that each end with a period, each with one clear statement about a subject's look, pose, action, the background, the light and so on. Long descriptions are split into several sentences instead of comma-chained fragments.
- **Krea 2:** 120–250 words in full sentences (was 60–200); a short closing sentence may name the medium or look.
- The example results of the presets follow the new rule.

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
- Tooltips, the persons' voice note and the README cover the new models. The screenshots show 1.2.0, plus a new one of the filtered preset list.

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
