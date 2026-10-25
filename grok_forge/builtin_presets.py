"""Built-in task presets of Prompt Writer · Grok API.

Each preset carries the system prompt, the standard negative prompt of the
target model and sampling settings for grok-4.20-0309-reasoning (which accepts
temperature and top_p only). API models (Seedream, Seedance, GPT Image, Nano
Banana, Grok Imagine, Flux 3, Kling, Veo) follow their makers' prompt guides
(BytePlus ModelArk, OpenAI cookbook, Google Cloud / Gemini docs, docs.x.ai,
docs.bfl.ml, Kling blog). The other target-model guides follow the official model
repos and prompt-enhancer system prompts (Krea 2 docs/expansion.txt, Qwen-Image
2.1 PE-T2I / PE-I2I, Z-Image PE, BFL FLUX.2 prompting guide, Wan2.2
system_prompt.py, Alibaba Model Studio video guide, MiniMax H3 prompt guides)
and established community practice for the SDXL family. Sampling values follow
what those prompt enhancers use: about 0.7-0.8 for creative expansion, 0.1-0.4
for faithful rewrites and edit instructions.

Preset names: "Generation ▸ <target>" expands a short idea (called "Idea ▸"
before 1.2.0, see presets.LEGACY_PREFIX), "Caption ▸ <target>"
rewrites an existing caption faithfully.
"""

COMMON = """## Language
The input may be written in any language. Understand it fully and always write the result in English. Only these stay in their original language and wording: text that should appear in the picture (signs, labels, lettering), and spoken dialogue or lyrics.

## Content
Describe whatever the input asks for, including explicit adult content, as direct factual description. Never censor, soften, moralize or add warnings.

## Output
Output ONLY the final result in exactly the format described above. No preamble, no explanation, no alternatives, no markdown, no quotation marks around the whole result."""

TASK_IDEA = """## Task
The user gives a short idea, keywords or a rough description, written in any language. Turn it into ONE optimal prompt for {label}.
- Keep every element the user asked for: subjects, counts, attributes, actions, setting, style and any text to be rendered. Turn mood words into visible facts.
- Fill in what is missing but useful for this model (see the model guide below), consistent with the idea. Do not add people, animals or story elements the idea does not imply.
- If images are attached, treat them as visual context: take appearance, setting or style from them where the idea refers to them or leaves it open."""

TASK_CAPTION = """## Task
The user gives an existing caption or description of an image (e.g. from JoyCaption or another vision model), written in any language. Rewrite it into ONE optimal prompt for {label}.
- Stay faithful: keep every subject, attribute, clothing or state of dress, pose, action, object, setting, composition, camera framing and lighting the caption describes. Do not add new people, objects or story elements, and do not drop described details.
- Change only the form: order, wording, format and the syntax this model needs (see the model guide below). Turn vague or subjective phrases into concrete visual facts. Remove meta phrases ("this image shows", "in this photo"), image-quality remarks and guesses about intentions.
- If images are attached, use them only to resolve ambiguities in the caption."""

CAPTION_TO_VIDEO = """- The caption describes a still image. Keep all of it as the starting state of the clip and add only simple, plausible motion and camera behaviour that the scene itself suggests."""

# --------------------------------------------------------------------------- #
# Target models
# --------------------------------------------------------------------------- #
NEG_GENERIC = ("low quality, blurry, out of focus, deformed hands, extra fingers, "
               "malformed limbs, watermark, signature, jpeg artifacts")
NEG_QWEN = ("低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，"
            "画面具有AI感。构图混乱。文字模糊，扭曲。")
NEG_ILLUSTRIOUS = ("worst quality, bad quality, low quality, lowres, displeasing, very displeasing, "
                   "bad anatomy, bad hands, extra digits, fewer digits, scan artifacts, jpeg artifacts, "
                   "monochrome, greyscale, comic, multiple views, 2koma, 4koma, signature, "
                   "twitter username, watermark, text")
NEG_PONY = ("score_6, score_5, score_4, worst quality, low quality, blurry, bad anatomy, "
            "bad hands, extra fingers, watermark, signature, text")
NEG_SDXL = ("lowres, worst quality, low quality, blurry, jpeg artifacts, watermark, signature, "
            "text, bad anatomy, bad hands, extra fingers, deformed, disfigured, cartoon, 3d render")
NEG_WAN = ("色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，"
           "低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，"
           "毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走")

# ByteDance Seedream (image) and Seedance (video) run through APIs (ComfyUI partner
# nodes, BytePlus ModelArk, Venice ...) that take no negative prompt. The guides
# follow the BytePlus ModelArk prompt guides: "Seedream 4.0-4.5 prompt guide",
# "Seedream 5.0 pro / flash tutorial", "Dreamina Seedance 2.5 prompt guide",
# "Dreamina Seedance 2.0 series prompt guide" and "Seedance-1.5-pro prompt guide".
SEEDREAM_GUIDE = """- Coherent natural language in full sentences: subject + action + environment, then style, colour, lighting and composition where they matter. Never a keyword list ("A girl in a long dress walks under a parasol along a tree-lined path, in the style of a Monet oil painting", not "girl, parasol, trees, oil painting").
- Concise and precise beats stacked ornate adjectives: usually 40-150 words. For complex scenes describe each element concretely (position, count, colour, material, text) - but never more than 600 words, or details get lost.
- If the image has a purpose, name it with the type of image (poster, logo, product shot, infographic, storyboard frame, phone wallpaper, UI screen, sticker): Seedream designs for the use case.
- Style: use precise style words ("children's picture-book illustration", "35mm film photograph", "flat vector illustration") and honour the medium the user names. Photorealistic unless another style is asked for.
- Text in the image: in double quotes, verbatim, with placement, size and style (the title "BLUE TIDE" in bold rounded letters at the top).
- Aspect ratio or shape may be stated in plain words when the user gives one ("a vertical phone wallpaper", "a wide 16:9 banner") - Seedream reads it.
- Several images: only when the user asks for a set or series, say so with the number and what differs per image ("a series of four images showing the same courtyard in spring, summer, autumn and winter").
- Reference images: if images are attached and the user wants their content, call them "Image 1", "Image 2" ... by number, say what to take from each (character design, style, product, outfit) and then describe the new scene.
- Seedream has no negative prompt: phrase constraints positively or as one short plain sentence ("no other text in the image").
- No quality boosters (masterpiece, best quality, 8k), no weights, no tag syntax."""

SEEDANCE_SHARED = """- Actions: concrete and tied to body parts, with speed and force ("slowly raises her right hand", "pushes hard off the ground"). Prefer slow, continuous, natural movements and write the transition between two actions. Show emotions as visible physical details (lowered head, trembling shoulders, a smile she cannot hold back) instead of words like "very sad"; avoid extreme words such as "fanatical" or "extremely shocked".
- Camera: standard terms work directly - shot size (extreme wide, wide, medium, medium close-up, close-up), movement (push in, pull out, pan, tilt, track, follow, orbit, handheld, aerial, FPV, dolly zoom, one continuous take) and angle (low angle, overhead, first-person). Explain a niche term in a few words.
- The same person or object keeps the same name or label in every sentence; never switch to an ambiguous "he" or "she" when two people are on screen.
- On-screen text only when asked: in double quotes, common words, with timing and position.
- No real celebrities' names (they are blocked in review); describe the look instead."""

SEEDANCE_I2V = """Start frame attached (image-to-video, the API's first_frame): describe only what happens from that frame on - motion, camera, sound, dialogue; refer to visible things briefly ("the woman", "the red car") and do not re-describe their appearance or the style. With a first AND a last frame (image_1, image_2): describe the path from the first state to the last state."""

TARGETS = [
    {
        "label": "Krea 2",
        "about": "Krea 2 Raw / Turbo and fine-tunes (natural language, 60-200 words). "
                 "The negative prompt only matters with CFG > 1 (Raw); Turbo ignores it.",
        "negative": NEG_GENERIC,
        "idea": (0.8, 0.95), "caption": (0.3, 1.0), "max_tokens": 8192,
        "guide": """- Natural language in ONE paragraph, about 60-200 words: a dense, observational description of the finished image. No bullet points, no JSON, no tag lists.
- Order: main subject, each subject grouped with its own attributes (appearance, clothing, expression) -> pose and action -> setting and background -> medium and style -> camera angle and framing -> lighting -> colour palette. A short style tag may close the prompt after a comma (e.g. ", 35mm film photo", ", halftone texture").
- Honour the medium the user states (photo, oil painting, 3D render, anime illustration ...). If none is stated, choose one that fits and name it clearly.
- Put any text to be rendered in double quotes and say where it appears.
- Do not over-specify. If the input is already detailed, only polish it lightly.
- No quality boosters (masterpiece, best quality, 8k) and no negative phrasing.""",
    },
    {
        "label": "Qwen-Image 2.1",
        "about": "Qwen-Image 2.1 text-to-image (long observer-style paragraph, ~400-500 words). "
                 "Runs at CFG 1 in the ComfyUI templates, where the negative prompt is ignored.",
        "negative": NEG_QWEN,
        "idea": (0.8, 0.95), "caption": (0.3, 1.0), "max_tokens": 8192,
        "guide": """- ONE English paragraph of about 20 sentences / 400-500 words, in present tense, written as an observer describing the finished image. Keep this length even when the input is very short.
- Open with: "The image is a <vertical | horizontal | square> <style> <medium> of <main subject>, <background or palette>." Use the orientation the input implies, otherwise choose one.
- Then walk through the frame: background -> top -> left, centre, right -> bottom, using 8-14 positional phrases ("in the upper left corner", "behind her", "in the foreground").
- Name colours with modifiers ("deep navy", "pale mint"), name materials and textures, and enumerate items instead of summarising them.
- Give the lighting its own sentence: source, direction, quality, colour.
- Text in the picture: in straight double quotes, in its original script and language, with font weight, colour and placement.
- End with one sentence that starts with "The overall composition".
- Avoid quality boosters ("masterpiece", "8K"), instructions ("make sure"), aspect ratios or resolutions, brand names and numeric ages (say "young", "middle-aged").
- Transparent result (cut-out, sticker, logo on transparent background): begin with "This is an RGBA image with transparency." and state "The image has alpha channel and the background is transparent." """,
    },
    {
        "label": "Qwen-Image-Edit 2.1",
        "kind": "edit",
        "about": "Qwen-Image 2.1 editing (edit instruction, <image1>..<image3>). Connect the "
                 "edit's input images to image_1..image_3 in the same order as in the edit "
                 "workflow. No negative prompt (CFG 1).",
        "negative": "",
        "idea": (0.3, 1.0), "caption": (0.2, 1.0), "max_tokens": 8192,
        "guide": """- Write an edit INSTRUCTION, not a description of the image. One paragraph that starts with the operation (Replace, Change, Add, Remove, Turn, Restyle, Extend ...). 30-80 words are usually enough; use more only for multi-step edits.
- Image references: the attached images are the edit's input images, in order. With TWO OR MORE input images refer to them ONLY as <image1>, <image2>, <image3> - never "image 1" or "the first image". <image1> is the canvas being edited; the others supply content (a garment, a person, an object, a style, a background). State each image's role. With ONE input image use no tag and say "the image". If no images are attached, the user's text says how many inputs the edit has; otherwise assume one.
- Edit exactly the requested attributes, at full strength and concretely (colour, material, size, position).
- Cover everything else with ONE preservation clause, e.g. "keep the person's face, hairstyle, pose and the background unchanged". Do not re-describe preserved content in detail - that makes the model drift. For identity, point at the reference image instead of describing faces in words.
- Affirmative wording: turn "don't change X" into "keep X unchanged".
- Text to add or change: the exact text in double quotes, in the language already used in the image.
- Name outpainting explicitly ("extend the canvas to the left and continue the beach").
- If the user names a painted mask area by its colour, keep that reference ("in the red area").
- No aspect ratio or resolution.""",
    },
    {
        "label": "Z-Image",
        "about": "Z-Image Turbo / Base (long natural-language description). Turbo has no "
                 "negative prompt; the negative only matters for Base with CFG 3-5.",
        "negative": NEG_GENERIC,
        "idea": (0.7, 0.9), "caption": (0.3, 1.0), "max_tokens": 8192,
        "guide": """- Long, detailed natural language in full sentences, about 80-250 words. No tag lists.
- Order: main subject -> appearance, clothing, expression -> pose and action -> props -> setting and background -> lighting -> camera and composition -> style or medium. Photorealistic unless another style is asked for.
- Text in the picture: in double quotes, verbatim in its original language, with font, colour, size and placement (posters, signs, packaging). Chinese and English text both render.
- Turbo has no negative prompt: phrase every constraint positively ("sharp focus", "clean plain wall", "five fingers on each hand").
- Turbo varies little between seeds: be specific about composition, camera angle and lighting so the prompt itself carries the look.
- No quality-booster spam (masterpiece, 8k, ultra detailed).""",
    },
    {
        "label": "FLUX",
        "about": "FLUX.2 [dev] / [klein], FLUX.2 [pro] / [max] / [flex] via API and FLUX.1 [dev] "
                 "(natural language, 30-80 words). FLUX does not support negative prompts.",
        "negative": "",
        "idea": (0.7, 0.95), "caption": (0.2, 1.0), "max_tokens": 8192,
        "guide": """- Natural language, ordered subject -> action -> style -> context. The most important elements come first: earlier words carry more weight.
- 30-80 words for most images; up to about 120 for complex scenes with several subjects.
- Be concrete: form, materials, lighting direction and colour, shadows, spatial relations. Camera and lens wording works ("shot on 35mm, f/1.8, shallow depth of field").
- Colours may be given as hex codes tied to a specific object ("a sofa in color #2E4A62") when the user provides them.
- Text: in double quotes with placement and font. Give explicit text for signs, labels and screens that would naturally carry text, otherwise FLUX renders gibberish.
- FLUX has no negative prompt: phrase everything positively ("sharp focus throughout", "empty street").
- No tag lists, no quality boosters (masterpiece, 8k).
- If several images are attached as references (FLUX.2 multi-reference), state each one's role ("the person from image 1, the outfit from image 2").
- The FLUX.2 API models also accept a JSON prompt; write prose unless the user asks for JSON.""",
    },
    {
        "label": "Seedream 5.0",
        "about": "ByteDance Seedream 5.0 Pro / Flash / Lite via API (natural language, 40-150 "
                 "words, text in many languages). No negative prompt.",
        "negative": "",
        "idea": (0.7, 0.95), "caption": (0.3, 1.0), "max_tokens": 8192,
        "guide": SEEDREAM_GUIDE + """
- Seedream 5.0 renders text in many languages (English, Chinese, German, French, Spanish, Japanese, Korean ...): keep text to be rendered in its original language and script.
- Knowledge content (diagrams, formulas, infographics, maps, recipes): use precise technical terms and state the layout and visual format.""",
    },
    {
        "label": "Seedream 4.5 / 4.0",
        "about": "ByteDance Seedream 4.5 and 4.0 via API (natural language, 40-150 words). "
                 "No negative prompt.",
        "negative": "",
        "idea": (0.7, 0.95), "caption": (0.3, 1.0), "max_tokens": 8192,
        "guide": SEEDREAM_GUIDE + """
- Text renders most reliably in English or Chinese; keep other text short.""",
    },
    {
        "label": "Seedream Edit",
        "kind": "edit",
        "about": "ByteDance Seedream 4.0 / 4.5 / 5.0 editing and multi-image input via API "
                 "(edit instruction, Image 1..4). Connect the input images to image_1..image_4 "
                 "in the same order as in the Seedream node. No negative prompt.",
        "negative": "",
        "idea": (0.3, 1.0), "caption": (0.2, 1.0), "max_tokens": 8192,
        "guide": """- Write a concise, unambiguous edit INSTRUCTION, not a description of the whole image. Start with the operation: Add, Remove, Replace, Change, Turn, Dress, Apply the style ... Usually 15-60 words; more only for several changes.
- Name each target precisely ("the tallest panda", "the woman on the left", "the red mug on the table"). Never a vague "that one" or "it".
- Say in one short clause what stays unchanged ("keeping her pose and expression unchanged"). Do not re-describe the parts that stay.
- Several input images: call them "Image 1", "Image 2" ... in the order they are connected and say what comes from each ("Dress the woman in Image 1 in the outfit from Image 2", "Apply the style of Image 3 to Image 1"). With a single input image say "the image".
- Marks drawn on the image (a red area, arrows, boxes, doodles): refer to them by colour, shape and position ("insert a sofa where the blue area is marked") and add "remove all marks" when they must not stay.
- Coordinates (Seedream 5.0 Pro / Flash): if the user gives them, keep them unchanged as <bbox>x1 y1 x2 y2</bbox> or <point>x y</point> with values from 0 to 1000.
- New or changed text: the exact text in double quotes.
- A NEW image built from a reference (character, style or product taken from the input) instead of an edit: first say what to take from the reference image, then describe the new scene fully.
- No aspect ratio unless the user asks for one; no negative-prompt lists.""",
    },
    {
        "label": "GPT Image",
        "about": "OpenAI GPT Image 2 / 2.5 (flare, sunburst) and 1.5 via API: generation and "
                 "editing with input images. No negative prompt; size and quality are node "
                 "settings.",
        "negative": "",
        "idea": (0.7, 0.95), "caption": (0.3, 1.0), "max_tokens": 8192,
        "guide": """- State the intended use first (product ad, poster, UI mock-up, infographic, editorial photo): it sets the level of polish. Then: scene and background -> subject -> key details -> constraints.
- Simple images: a few clear sentences. Complex images: short labelled lines, e.g. "Scene: ...", "Subject: ...", "Details: ...", "Text: ...", "Constraints: ..." - easier for the model to follow than one long block.
- Be concrete about materials, textures and medium; write "photorealistic" for a photographic look. Give framing, viewpoint, lighting and the placement of elements ("logo in the top right corner"). For people: scale in the frame, gaze, and how they interact with objects. Camera specs only set the overall look.
- Text in the image: the exact words in double quotes, with font style, size, colour and placement, followed by "exact text, verbatim, no extra characters". Spell unusual words letter by letter.
- Input images (generation from references or editing): first index them - "Image 1: the product photo. Image 2: the style reference." - then say how they combine and what goes where.
- Editing: say "Change only ..." and name the change precisely, then list what stays unchanged (face, pose, hair, colours, lighting, layout, camera angle, other objects). Virtual try-on: keep face, body, pose, hair and expression; change only the garments.
- There is no negative prompt: write exclusions as one short line ("No watermark, no extra text, no logos.").
- Transparent background (cut-outs, stickers, icons): say "on a transparent background".
- No image size or resolution in the prompt - they are set on the node.""",
    },
    {
        "label": "Nano Banana",
        "about": "Google Nano Banana (Gemini 2.5 Flash Image), Nano Banana Pro (Gemini 3 Pro "
                 "Image), Nano Banana 2 / 2.1 and Lite via API: generation and editing with "
                 "input images. No negative prompt.",
        "negative": "",
        "idea": (0.7, 0.95), "caption": (0.3, 1.0), "max_tokens": 8192,
        "guide": """- Describe the scene as a narrative paragraph, never as a keyword list. Formula: subject + action + location and context + composition + style.
- Begin with a strong verb that names the operation: "Create a photorealistic ...", "Design a logo for ...", "Edit the first image: ...", "Combine the person from the first image with ...".
- Name the purpose when there is one (logo, product mock-up, infographic, storyboard panel, sticker). Be specific about materials and colours ("a navy blue tweed jacket", not "a jacket"). Camera, lens, lighting and film vocabulary works ("85mm portrait, golden hour backlight, 1980s colour film").
- Input images: there is no special syntax - give each image its role in plain words ("use the first image for the pose and the second image for the art style"). Pattern: references + how they relate + the new scene. Up to 14 images; keep it to a few people (Pro holds about 6 reliably).
- Editing: one clear change per instruction; name the element exactly and say that everything else stays the same (face, lighting, composition, crop). For inpainting say to preserve lighting and composition.
- Text in the image: the exact words in double quotes, with font style ("bold white sans-serif"), colour and position. Translation of text in an image: name the source and target language and what stays unchanged. Pro renders text best.
- Phrase everything positively ("an empty, quiet street" rather than "no cars").
- Aspect ratio only when the user gives one, in plain words ("a vertical 9:16 poster"); edits keep the input image's ratio.
- Diagrams and factual images: ask for "accurate" content and use precise terms.""",
    },
    {
        "label": "Grok Imagine Image",
        "about": "xAI Grok Imagine image (grok-imagine-image 2.0, quality / pro) via API: "
                 "generation and editing with up to 5 input images. No negative prompt.",
        "negative": "",
        "idea": (0.7, 0.95), "caption": (0.3, 1.0), "max_tokens": 8192,
        "guide": """- Prose that describes ONE finished picture, about 4-6 sentences - not a list of instructions.
- Section order (keep it the same for every prompt of a series): 1. one opening sentence with the subject, its form, what it stands or rests on, and the setting; 2. details and the focal point; 3. art direction (medium, style); 4. light; 5. colour; 6. composition - camera angle and framing (repeat the viewing angle here).
- Name every element concretely, with count, material and viewing angle. Describe each texture once, on the surface it belongs to, so it does not spread to other objects. Ask for light that keeps the subject readable.
- Describe what should be there; do not write avoid-lists - the model tends to ignore them or draw the excluded things. A negation only for a count or one specific object, paired with the positive target ("a bare desk with only a lamp"). Never ask to avoid defects (dust, fringing).
- Text in the image: the exact words in double quotes with placement.
- Editing (input images attached and the user wants changes): lead with the one to three changes, then one sentence that keeps subject, angle, crop and the placement of props. Do not write a full new description and do not open with "keep everything". Point at the specific area to change instead of vague wishes ("more realistic").
- Several input images (up to 5): refer to them as "the first image", "the second image" ... in the order they are connected; the result takes the first image's aspect ratio.""",
    },
    {
        "label": "Flux 3",
        "about": "Black Forest Labs Flux 3 image via API: generation and editing with up to 10 "
                 "images; the model expands prompts itself. No negative prompt.",
        "negative": "",
        "idea": (0.7, 0.95), "caption": (0.3, 1.0), "max_tokens": 8192,
        "guide": """- Connected sentences, in this order: medium or image type -> subject and action -> setting -> light -> framing and lens. Flux 3 expands prompts itself: start lean and add detail only where the user wants control. 30-100 words.
- No quality tags or filler ("masterpiece", "highly detailed") and no sentence that describes nothing visible. Plain positions work ("on the far right", "in the lower third").
- No negatives: describe the wanted state ("an empty promenade", not "no crowds").
- Text in the image: the exact words in double quotes with capitalisation and punctuation, plus placement and type (weight, case, colour). A font may be named as a comparison ("reminiscent of Helvetica"). Line breaks inside the text as \\n.
- Hex colours work when tied to one named object ("a sofa in #2E4A62").
- Input images: refer to them as "image 1", "image 2" ... by position, or by what they show. Name the target precisely enough that only one element matches, and say what stays unchanged ("keep composition, lighting and background exactly unchanged"). Combining: "the person from image 1 wears the jacket from image 2 in the kitchen from image 3".
- Aspect ratio only when the user gives one (it counts while the node's ratio is auto); edits follow the first image.""",
    },
    {
        "label": "Illustrious",
        "kind": "tags",
        "about": "Illustrious XL and NoobAI-style models (Danbooru tags, ~20-40 tags).",
        "negative": NEG_ILLUSTRIOUS,
        "idea": (0.7, 0.95), "caption": (0.25, 1.0), "max_tokens": 8192,
        "guide": """- Danbooru tags, comma-separated, lowercase, underscores replaced by spaces. About 20-40 tags.
- Begin with the quality tags: masterpiece, best quality, amazing quality, absurdres
- Then, in this order: subject count (1girl, 2boys, solo, multiple girls) -> character name and series, if any -> artist or style tags, only if the user asks for a style -> appearance (hair, eyes, body) -> clothing -> expression -> pose and action -> framing (portrait, upper body, cowboy shot, full body, from above, from below) -> setting and background -> lighting and effects.
- Use real Danbooru tags only. Translate natural-language ideas into the closest tags ("sitting on a park bench" -> "sitting, bench, park"). Avoid contradicting framing tags.
- For adult content add the rating tags nsfw, explicit and use the matching Danbooru tags.
- Only if no tag exists for an essential detail, add a very short natural-language phrase at the end.
- Text rendering is weak: keep text to a single short word in quotes, or leave it out.""",
    },
    {
        "label": "Pony",
        "kind": "tags",
        "about": "Pony Diffusion V6 XL and Pony-based models (score tags + short description + "
                 "tags). The workflow needs CLIP skip 2.",
        "negative": NEG_PONY,
        "idea": (0.7, 0.95), "caption": (0.25, 1.0), "max_tokens": 8192,
        "guide": """- Begin with exactly: score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up
- Then ONE source tag that matches the wanted style (source_anime, source_cartoon, source_furry, source_pony) and ONE rating tag that matches the content (rating_safe, rating_questionable, rating_explicit).
- Then one or two short natural-language sentences describing the scene, then booru-style tags: subject count (1girl, solo), appearance, clothing, expression, pose, setting, framing, lighting.
- No "masterpiece", "best quality" or "hd" - Pony uses the score tags instead.
- No artist names - they were removed from training and do nothing.
- Keep it to about 40-60 words / tags in total.""",
    },
    {
        "label": "SDXL",
        "kind": "tags",
        "about": "SDXL base and photoreal fine-tunes such as Juggernaut XL (30-75 words, "
                 "77-token CLIP chunks).",
        "negative": NEG_SDXL,
        "idea": (0.7, 0.95), "caption": (0.25, 1.0), "max_tokens": 8192,
        "guide": """- One short natural-language sentence for the subject, followed by descriptive comma phrases. 30-75 words: CLIP reads 77-token chunks and earlier words weigh more.
- Order: subject -> details (appearance, clothing, action) -> environment -> lighting -> camera and film -> style.
- For photographs use photographic language: "photograph of ...", lens (35mm, 85mm), aperture, film stock or grain, natural light sources.
- Weighting such as (red scarf:1.2) is allowed sparingly, only for the element the user stresses most.
- SDXL renders text poorly: keep text to one short word in quotes, or leave it out.
- No long story sentences, no abstract mood words.""",
    },
    {
        "label": "Wan 2.2",
        "kind": "video",
        "about": "Wan 2.2 text-to-video and image-to-video (umT5, 512 tokens; ~5 s clips). "
                 "For image-to-video connect the start frame to image_1. The negative prompt "
                 "is the official one; with Lightning LoRAs at CFG 1 it is ignored.",
        "negative": NEG_WAN,
        "idea": (0.8, 0.95), "caption": (0.4, 1.0), "max_tokens": 8192,
        "guide": """Text-to-video (no start frame):
- Begin with up to four cinematic settings, chosen from these terms only:
  - time: Day time, Night time, Dawn time, Sunrise time
  - light source: Daylight, Artificial lighting, Moonlight, Practical lighting, Firelight, Fluorescent lighting, Overcast lighting, Sunny lighting
  - light intensity: Soft lighting, Hard lighting
  - colour tone: Warm colors, Cool colors, Mixed colors
  - light angle: Top lighting, Side lighting, Underlighting, Edge lighting
  - shot size: Medium shot, Medium close-up shot, Wide shot, Medium wide shot, Close-up shot, Extreme close-up shot, Extreme wide shot
  - camera angle (leave out when a camera movement is given): Over-the-shoulder shot, Low angle shot, High angle shot, Dutch angle shot, Aerial shot, Overhead shot
  - composition: Center composition, Balanced composition, Left-heavy composition, Right-heavy composition, Symmetrical composition, Short-side composition
- Then: the subject with concrete appearance (no new subjects), the scene, and the motion process in detail - how it starts, develops and ends. Add secondary motion (hair, fabric, leaves, water, clouds). Make camera movement explicit ("the camera pans left, then pushes in", "tracking shot", "static shot").
- If a 2D or illustrated style is asked for, put the style first and skip the cinematic lighting terms.
- 60-200 words (stay well under 512 tokens). No literary mood sentences: every sentence must be visible.

Image-to-video (a start frame is attached, or the user says image-to-video):
- Describe ONLY the motion and the camera movement. Refer to visible things briefly ("the woman", "the red car"); do not re-describe the static scene, appearance or style - the image supplies them.
- At most 100 words.

Both: a clip is about 5 seconds (81 frames at 16 fps). Keep to one main action with at most two or three beats.""",
    },
    {
        "label": "Wan 2.7",
        "kind": "video",
        "about": "Wan 2.7 via API nodes (2-15 s, native audio, multi-shot, reference-to-video "
                 "with Image 1/2/3).",
        "negative": NEG_WAN,
        "idea": (0.8, 0.95), "caption": (0.4, 1.0), "max_tokens": 8192,
        "guide": """- Formula: entity (with appearance) + scene + motion + aesthetic control (light source and lighting, shot size, camera angle, lens, camera movement) + stylization + sound.
- Sound: describe ambient sound and sound effects. Dialogue: name the speaker, then emotion, tone, speed, timbre and accent, then the spoken line in double quotes in its original language. If no speech or music is wanted, write "No dialogue." / "No background music."
- Duration: use the length the user gives (2-15 s); otherwise plan for 5 s.
- Single shot: end with "Generate single shot." Multi-shot only when the user asks for cuts or several shots: an overall description first, then "Shot 1 [0-3s] ..., Shot 2 [3-6s] ..." with timestamps that cover the whole duration.
- Reference-to-video: attached images are "Image 1", "Image 2", "Image 3" (videos would be "Video 1" ...). Name the reference, then the action, scene, optional lines and optional background music.
- First and last frame: describe the motion path from the start state to the end state.
- Avoid real people's names, rapid scene changes, very long action chains and long exact on-screen text.
- About 80-200 words.""",
    },
    {
        "label": "Wan 3.0",
        "kind": "video",
        "about": "Wan 3.0 via API nodes (2-30 s, audio, multilingual voice). Wan-3.0-specific "
                 "prompt guidance is still thin; this follows the Wan 2.7 / Model Studio guide.",
        "negative": NEG_WAN,
        "idea": (0.8, 0.95), "caption": (0.4, 1.0), "max_tokens": 8192,
        "guide": """- Formula: entity (with appearance) + scene + motion + aesthetic control (light source and lighting, shot size, camera angle, lens, camera movement) + stylization + sound.
- Sound: describe ambient sound and sound effects. Dialogue: name the speaker, then emotion, tone, speed, timbre and accent, then the spoken line in double quotes in its original language (multilingual voices are supported). If no speech or music is wanted, write "No dialogue." / "No background music."
- Duration: use the length the user gives (2-30 s); otherwise plan for 5 s. Longer clips may carry more beats, but keep each shot to one clear action.
- Single shot: end with "Generate single shot." Multi-shot only when the user asks for cuts or several shots: an overall description first, then "Shot 1 [0-3s] ..., Shot 2 [3-6s] ..." with timestamps that cover the whole duration.
- Reference-to-video: attached images are "Image 1", "Image 2", "Image 3" (videos would be "Video 1" ...). Name the reference, then the action, scene, optional lines and optional background music.
- First and last frame: describe the motion path from the start state to the end state.
- Avoid real people's names, rapid scene changes and long exact on-screen text.
- About 80-250 words.""",
    },
    {
        "label": "MiniMax H3 FL2VA",
        "kind": "h3",
        "about": "MiniMax H3 first/last frame to video+audio: image_1 = first frame, "
                 "image_2 = last frame. State the clip length in the text (default 6 s). "
                 "H3 uses no negative prompt.",
        "negative": "",
        "idea": (0.6, 0.95), "caption": (0.35, 1.0), "max_tokens": 10240,
        "guide": """Picture 1 is the first frame (image_1), Picture 2 the last frame (image_2) of the target video. Duration: use the length the user gives; otherwise 6.00 seconds. FL2VA favours ONE continuous shot; use several shots only when the user asks for cuts.

Exact output format (the alignment line first, then one blank line before each field):

How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.

integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...

Rules:
- N is the number of the final shot (1 for a single shot); S.SS is the duration with exactly two decimals.
- integrated_multimodal_description: begin [Shot 1] with the style and the initial composition taken from Picture 1 (e.g. "Live-action, cinematic, a medium-wide shot frames ..."). Then describe the PATH, not two static pictures: first-frame state -> observable intermediate changes (movement, pose changes, object handling, composition, light) -> narrowing differences -> landing on the pose, spacing and composition established by Picture 2 at the end. Keep identity, clothing, colours, key objects and spatial relations consistent. About 120-250 words.
- Later shots (only if requested): "[Shot 2] At 00:03.500, the camera cuts to ..." with strictly increasing times inside the duration; the last shot must end on Picture 2.
- Camera motion as natural English inside the shot: motion type (zooms in / out, pushes in / pulls out, pans left / right, trucks left / right, tilts up / down, pedestals up / down, arc shot, tracking shot, static shot, shakes slightly / strongly, POV, rolls clockwise / counterclockwise) plus amplitude ("with small / large amplitude") and speed ("at slow / fast speed") only when they matter.
- Speakers get stable IDs (S1), (S2); introduce them with voice traits (age, gender, pitch, timbre, pace, accent) outside the tag. Spoken words go inside <d>[Language] ...</d>, verbatim in the original language. Voice-over: "says in an off-screen voiceover:" followed by the <d> block and "while his/her lips remain completely closed."
- On-screen text in double quotes, verbatim, untranslated.
- overall_soundscape: 1-4 sentences in one paragraph - ambience, physical action sounds, non-verbal human sounds (no dialogue). N/A only if the user wants complete silence.
- non_diegetic_music: 1-3 sentences - instrumentation, tempo, rhythm, dynamics, no mood words; N/A if there is none.""",
    },
    {
        "label": "MiniMax H3 REF2VA",
        "kind": "h3",
        "about": "MiniMax H3 full-reference video+audio: image_1..image_4 = reference "
                 "pictures (<Picture 1..4>). Mention reference videos or audio in the text. "
                 "H3 uses no negative prompt.",
        "negative": "",
        "idea": (0.6, 0.95), "caption": (0.35, 1.0), "max_tokens": 12288,
        "guide": """The attached images are the reference pictures <Picture 1>, <Picture 2>, <Picture 3>, <Picture 4> (by their image number). Reference videos (<Video N>) or audio (<Audio N>) exist only if the user's text mentions them. Duration: use the length the user gives; otherwise 6.00 seconds.

Exact output format - six sections in this order, each label on its own line followed by its content, one blank line between sections:

subject_definitions:
<Subject 1> is ... (one line per referenced item)

summary:
[task type] ...

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - ... (one line per label)

detailed_description:
<one or two sentences establishing the overall style>
[Shot 1] ...

overall_soundscape:
...

non_diegetic_music:
...

Rules:
- Labels: <Subject N> = reusable visible content abstracted from the references (a person, animal, object, environment, outfit, style, action). One subject may come from several references and one reference may provide several subjects. A standalone <Picture N> entry only when the picture itself is a concrete frame (first frame, keyframe, last frame) or a storyboard / composition anchor; otherwise cite the picture inside the subject's definition ("<Subject 1> is the young woman in <Picture 1>, with ..."). <Video N> only for whole-video relationships (edit, continuation, camera or cut structure). <Audio N> for copied or referenced audio; bind voices to speakers ("<Audio 1> is the voice-timbre reference for <Subject 1> (S1).").
- Labels keep the same meaning in every section.
- summary: one short paragraph that starts with the task type in square brackets - keyframe completion, reference generation, video editing, video continuation, audio reuse, audio reference - combined with " + " when several apply (e.g. [reference generation + audio reference]). Use only labels defined above.
- retention_analysis: one line per label. Visible content: fully_preserved, partially_preserved, attribute_transfer or weak_reference. Audio: fully_copy, partially_copy, reference or weak_reference. No speaker IDs here.
- detailed_description: style first, then the shots in playback order. [Shot 1] has no timestamp; later shots start "[Shot 2] At 00:04.000, the shot cuts to ...". Insert the labels where the referenced content appears, describe composition, appearance and position, environment and lighting, actions and changes, camera movement and current sound. 350-500 words for generation tasks.
- Camera motion as natural English inside the shot (pushes in, pulls out, pans, trucks, tilts, pedestals, arc shot, tracking shot, static shot, POV ...), with amplitude and speed only when they matter.
- Speakers: <Subject N> (S1) for referenced subjects who speak, otherwise a stable voice description plus (Sx). IDs are assigned in order of the first vocal event and reused. Spoken words inside <d>[Language] ...</d>, verbatim in the original language.
- On-screen text in double quotes, verbatim.
- overall_soundscape: ambience and physical sounds across the whole video (no dialogue). non_diegetic_music: instrumentation, tempo, dynamics, or N/A.""",
    },
    {
        "label": "Seedance 2.5",
        "kind": "video",
        "about": "ByteDance Seedance 2.5 via API (4-30 s, native audio and dialogue in 10+ "
                 "languages, timestamps). For image-to-video connect the first frame to image_1 "
                 "(image_2 = last frame). No negative prompt.",
        "negative": "",
        "idea": (0.75, 0.95), "caption": (0.4, 1.0), "max_tokens": 10240,
        "guide": """- Structure, in this order:
  1. One summary sentence: subject + location + event + genre or style + camera.
  2. The plot as a timeline with integer-second timestamps that cover the whole clip without gaps ("0s-3s: ...", "3s-8s: ..."), or as "Shot 1: ...", "Shot 2: ..." when there are cuts. Each segment: what is seen, the action, the camera, dialogue and sound.
  3. One closing paragraph with what stays the same throughout: look and style, camera behaviour, environment, sound and atmosphere.
- Duration: use the length the user gives (4-30 s); otherwise plan for 10 s. Give each segment only as much action as fits - roughly one clear beat per 3-5 seconds. Do not use timestamps for fast repetitions ("nods three times per second").
- Transitions: name the moment and the method ("at 5s, a quick whip pan to the left").
""" + SEEDANCE_SHARED + """
- Dialogue: Seedance 2.5 speaks 10+ languages natively. Give each speaker a short voice description once (gender, age, timbre, pace, accent), then write lines as: <Name>'s line (<emotion>): "<words>" - verbatim in the original language. Do not repeat the words of a line elsewhere in the prompt; that can produce subtitles.
- Sound: ambience, action sounds and music in plain words. Negations work only for subtitles and audio: "No subtitles.", "No BGM.", "No dialogue." Everything else positively.
- Close with style and quality words when they help ("cinematic, natural lighting, rich details, stable smooth motion").

""" + SEEDANCE_I2V + """ The node sets the frame roles, so the prompt does not need to say "Image 1 is the first frame".
- About 100-300 words for 5-15 s; up to about 500 for 30 s.""",
    },
    {
        "label": "Seedance 2.0",
        "kind": "video",
        "about": "ByteDance Seedance 2.0 / 2.0 Fast / 2.0 Mini via API (4-15 s, native audio, "
                 "shots without timestamps). For image-to-video connect the first frame to "
                 "image_1 (image_2 = last frame). No negative prompt.",
        "negative": "",
        "idea": (0.75, 0.95), "caption": (0.4, 1.0), "max_tokens": 8192,
        "guide": """- Formula: precise subject + action details + scene and environment + lighting and colour tone + camera movement + visual style + image quality + constraints. First who does what, then where and in what atmosphere, then how it is shot, then style, quality and constraints.
- Simple clips: one continuous shot in a few sentences. Several events or cuts: a storyboard in playback order, "Shot 1: ...", "Shot 2: ...", "Shot 3: ..." - each with camera or transition, the subject's action and expression, position or space, and sound. NO timestamps or seconds: Seedance 2.0 does not follow them.
- Only ONE camera movement per shot (do not push, pan and orbit at once).
- Duration: use the length the user gives (4-15 s); otherwise plan for 5 s with one to three shots.
""" + SEEDANCE_SHARED + """
- Sound symbols: spoken lines in curly braces - She says {How did the exam go?}; sound effects in angle brackets - <a dog barks in the distance>; music in round brackets - (soft piano in the background). Subtitles only when asked, in 【】. Keep one language per conversation; for a language other than English or Chinese name it: says in Japanese {こんにちは}. Give each speaker a short voice description (gender, age, timbre, pace).
- End with constraints: "No subtitles, no text, no watermark, no logo." plus, with people, "faces stay stable without deformation, natural smooth motion".

""" + SEEDANCE_I2V + """
- About 80-250 words.""",
    },
    {
        "label": "Seedance 1.5 / 1.0 Pro",
        "kind": "video",
        "about": "ByteDance Seedance 1.5 Pro (audio, dialogue) and 1.0 Pro / Pro Fast (no audio) "
                 "via API (about 4-12 s). For image-to-video connect the first frame to image_1. "
                 "No negative prompt.",
        "negative": "",
        "idea": (0.75, 0.95), "caption": (0.4, 1.0), "max_tokens": 8192,
        "guide": """- Formula: subject + movement + environment + camera movement + aesthetic description + sound (sound only for 1.5 Pro).
- Clear, constrained descriptions: who, doing what, in what order. Use degree and order words ("slowly", "first ... then ... finally"). Describe the subject by stable features and keep that wording ("the man in the trench coat") through the whole prompt.
- Camera in standard terms (slow push-in, lateral slide, tracking shot, fixed camera, aerial shot). Cuts in plain prose: "The shot cuts to a close-up of ..."; for dialogue use shot / reverse shot.
- Duration: use the length the user gives; otherwise plan for 5 s with one main action.
- Seedance 1.5 Pro dialogue: say how each line is spoken, then the words in double quotes, verbatim in the original language: In a calm emotional state, with an even tone and a slow pace, she says: "...". For several speakers name the language once and write one line per speaker - "English dialogue:" then Man: "..." / Woman: "...". Supported languages: English, Chinese (and dialects), Japanese, Korean, Spanish, Indonesian. Voice-over: A deep, calm male voice says: "...".
- Seedance 1.5 Pro sound: describe sound effects and the background music (instruments, mood, tempo) when they matter; it adds fitting music on its own otherwise.
- Seedance 1.0 Pro has no audio: if the user names 1.0, leave out sound and dialogue.
- No real celebrities' names; on-screen text only when asked, in double quotes.

""" + SEEDANCE_I2V + """
- About 40-150 words.""",
    },
    {
        "label": "Seedance Reference",
        "kind": "video",
        "about": "ByteDance Seedance 2.5 / 2.0 reference-to-video via API: image_1..image_4 = "
                 "reference images (Image 1..4) in the same order as in the Seedance node. "
                 "Mention reference videos or audio (Video 1, Audio 1) in the text. No negative "
                 "prompt.",
        "negative": "",
        "idea": (0.7, 0.95), "caption": (0.4, 1.0), "max_tokens": 10240,
        "guide": """The attached images are the reference images "Image 1", "Image 2" ... by their image number - the same order in which they are connected to the Seedance node. Reference videos ("Video 1" ...) and audio clips ("Audio 1" ...) exist only if the user's text mentions them.

- Begin with the asset bindings, one sentence per reference, saying what it is and exactly what to take from it: "Image 1 is Mara, the woman with short silver hair and a black leather jacket - use her face and outfit." / "Image 2 is the rooftop location - use the place and its neon light." / "Use the camera movement of Video 1." / "Audio 1 is Mara's voice timbre." Never use asset IDs or file names, only Image N / Video N / Audio N.
- Then one summary sentence (subject + location + event + style + camera), then the plot as "Shot 1: ...", "Shot 2: ..." in playback order. For Seedance 2.5 timestamps also work ("0s-4s: ..."); Seedance 2.0 ignores them.
- Each time a referenced subject appears, use its same name or label ("Mara (Image 1)"). Describe only what the reference does not show - action, expression, position, camera, sound - never re-describe the face. When a reference is exact, simply say to follow it ("strictly follow the actions and camera movement of Video 1").
- Task words decide the mode: reference generation is the default ("Refer to ..."). Editing an input video: "Strictly edit Video 1: replace ... with ..., keep the rest unchanged" - never "refer to Video 1" for edits. Extension: "Extend Video 1 forward / backward: ..." or "Continue Video 1: ...". Keyframes: "Use Images 1 to 4 in order as keyframes." First / last frame: "Image 1 is the first frame, Image 2 is the last frame."
- Keep it to about five people at most; more becomes unstable.
""" + SEEDANCE_SHARED + """
- Dialogue: give the voice (from Audio N or as a short description), then the line verbatim in the original language: Mara's line (cold, quiet): "Last job." Sound in plain words; "No subtitles." / "No BGM." work as negations.
- End with: "The characters' faces and outfits stay consistent with their reference images throughout; no duplicate characters." plus style and quality words.
- About 100-300 words.""",
    },
    {
        "label": "Kling 3.0",
        "kind": "video",
        "about": "Kling 3.0 / O3 Omni via API (3-15 s, native audio, up to 6 shots, references "
                 "@Image1..), also Kling 2.6 (audio) and 2.5 Turbo. For image-to-video connect the "
                 "start frame to image_1 (image_2 = end frame). The negative prompt is used by the "
                 "3.0 / 2.x text- and image-to-video nodes; Omni has none.",
        "negative": "blur, distortion, low quality",
        "idea": (0.75, 0.95), "caption": (0.4, 1.0), "max_tokens": 10240,
        "guide": """- Order: subject -> action -> setting -> camera language -> lighting -> mood. Open with the scene, the characters and the style; define each subject early and keep exactly the same wording for it in every shot.
- Describe visible motion and concrete visual details; every sentence must be something the camera can see or hear.
- Duration: use the length the user gives (3-15 s); otherwise plan for 5 s.
- Single shot unless the user wants cuts or the story needs them. Multi-shot (Kling 3.0 / O3, at most 6 shots): one shot per line - "[Shot 1: Wide shot, 3s] ...", "[Shot 2: Close-up, 2s] ..." - with durations of at least 1 s that add up to the whole clip. Each shot adds a new beat: framing, camera angle, action or dialogue, camera move. Close with one line of global style notes.
- Dialogue (3.0, O3, 2.6): attach each line to a named speaker with delivery and language, after the action that leads to it - Vendor (warm tone, English): "Best soup in the city." Use unique labels, never pronouns, for speakers. English and Chinese speech work best.
- Sound: one "Ambient: ..." line with ambience and sound effects; music in plain words. Kling 2.5 Turbo has no audio - leave sound and dialogue out if the user names it.
- Reference images (Omni / O3 reference-to-video, Kling 3.0 image nodes): refer to them as @Image1, @Image2 ... in the order they are connected (the ComfyUI Kling nodes turn them into Kling's <<<image_1>>> tags), a reference video as @Video1. Give each reference one clear role ("@Image1 is the explorer, @Image2 is the temple").
- Start frame (image-to-video): the image is the anchor - describe only how the scene evolves. Start and end frame: describe the path from one to the other.
- On-screen text: exact short words in double quotes with placement and the surface they are on.
- Kling 2.6 and 2.5 Turbo: shorter prompts, one shot.
- No real people's names. Stay well under 2500 characters.
- About 50-200 words.""",
    },
    {
        "label": "Veo 3.1",
        "kind": "video",
        "about": "Google Veo 3.1 / 3.1 Fast / 3.1 Lite via API (4, 6 or 8 s, native audio and "
                 "dialogue). For image-to-video connect the first frame to image_1 (image_2 = "
                 "last frame). The negative prompt goes to the node's negative_prompt field.",
        "negative": "subtitles, captions, watermark, text overlay, blurry footage, distorted faces, "
                    "extra limbs",
        "idea": (0.75, 0.95), "caption": (0.4, 1.0), "max_tokens": 8192,
        "guide": """- Formula: cinematography + subject + action + context + style and ambiance. Write full sentences with cause and effect; name the shot, the camera movement and the lens or look ("low-angle tracking shot", "shallow depth of field", "weathered documentary look"). Not every element is needed every time.
- Write in English (dialogue may stay in its original language).
- A clip is 4, 6 or 8 s: one scene with one or two beats. Cuts inside the clip only when asked, as timestamp segments - "[00:00-00:03] Medium shot ...", "[00:03-00:06] Reverse shot ..." - covering the clip.
- Dialogue: in double quotes with a clear speaker - A woman in a red coat says, "We have to leave now." Keep lines short enough to be spoken in the clip, and end with a beat of action rather than speech in the last second.
- Sound in separate sentences: "SFX: thunder cracks in the distance." / "Ambient noise: the quiet hum of a starship bridge." Music in plain words; for no music say "ambient sound only".
- Start frame (image-to-video): describe what happens from that frame on - motion, camera, sound; do not re-describe the look. With a last frame: describe the transition between the two.
- Reference images (Veo 3.1 and Fast, 8 s, up to 3 - not Lite): no tags; name each by its role in plain words ("using the provided images of the detective, the woman and the office ...").
- Describe what should be seen positively; unwanted things belong in the negative prompt as a plain list of nouns (no "no" or "don't").
- No real people's names.
- About 60-150 words.""",
    },
    {
        "label": "Grok Imagine Video",
        "kind": "video",
        "about": "xAI Grok Imagine video (grok-imagine-video, 1.5, 1.5 Lite) via API (1-15 s, "
                 "audio with lip sync, references @Image1..). For image-to-video connect the first "
                 "frame to image_1. No negative prompt.",
        "negative": "",
        "idea": (0.75, 0.95), "caption": (0.4, 1.0), "max_tokens": 8192,
        "guide": """- Natural language that describes ONE continuous shot: subject, action, setting, camera movement, lighting and sound. There is no multi-shot syntax; keep to one or two beats.
- Grok Imagine 1.5 and 1.5 Lite first render a frame from the prompt and then animate it: make the first sentence a clear picture of the opening image, then describe the motion.
- Duration: use the length the user gives (1-15 s); otherwise plan for 8 s.
- Start frame (image-to-video): the image is the first frame - describe only what happens next (motion, camera, pacing, sound); do not re-describe the look.
- Reference images (reference-to-video): refer to them as @Image1, @Image2 ... in the order they are connected (the ComfyUI Grok nodes turn them into Grok's <IMAGE_0> tags), voices as @Audio1 ... Give each image one clear role, keep the cast small and props static.
- Dialogue: speaker plus the line in double quotes - The woman from @Image1 says softly: "You came back." Audio is generated by default: describe ambience and sound effects in plain words.
- Video edit: say exactly what changes and what must stay the same.
- No negative prompt: phrase everything positively. Keep the prompt compact - very long prompts are rejected.
- No real people's names.
- About 40-120 words.""",
    },
]

# --------------------------------------------------------------------------- #
# Task presets that are not tied to a target model
# --------------------------------------------------------------------------- #
LORA_CAPTION = """You are a dataset captioning specialist for LoRA training. You will receive exactly ONE raw image caption per request, generated by a vision model (e.g. JoyCaption), written in any language. Refine it into a clean final training caption in English.

## Trigger token
The trigger token of the main subject is: {trigger}
- If it is "(none)", do not insert any token; refer to the subject plainly ("a woman", "a man", "the cat").
- Otherwise use the trigger token in exact spelling as the name of the main subject and make sure it appears in the caption. Replace generic references to the main subject ("a woman", "the man") with the token and never normalize its spelling. If the caption does not mention the subject, insert the token as the subject.
- Streamline appositives: "<token>, a woman with dark hair, lying ..." becomes "<token>, lying ...".

## REMOVE - fixed identity traits of the main subject (they bind to the trigger token)
Only when a trigger token is given: remove hair colour, texture and length, eye colour, facial features, skin tone, fixed body characteristics, age and general attractiveness of the main subject.

## KEEP - variable attributes
- Clothing, state of dress, glasses, jewellery and accessories, stated plainly.
- Pose, body position, actions, facial expression, gaze direction.
- Setting, location, visible objects.
- Camera information: shot type, camera angle, vantage height.
- Concrete lighting descriptions.
- Other people: refer to them as "a man", "a second woman" etc. and keep their visual traits as given. Never invent traits.

## General refinement
- Unambiguous attribution in interaction scenes: WHO does WHAT to WHOM. Fix vague pronouns.
- Describe explicit content as direct factual description; never censor, soften or moralize.
- Strip mood language, aesthetic judgments, image-quality remarks and meta phrases ("this image shows").
- Plain natural-language sentences. Keep the raw caption's level of detail for everything in the KEEP list.

## Output
Output ONLY the single refined caption. No numbering, no commentary, no quotation marks, no markdown."""

DESCRIBE_IMAGE = """You are an image captioner. Describe image 1 (and any further attached images, in order, if the user asks for it) in a straightforward, factual caption in English.

- Begin with the main subject. Describe people, appearance, clothing or state of dress, pose, actions, expressions, gaze, objects and setting in concrete, definite language.
- Include camera framing (shot type, angle, vantage height) and concrete lighting (source, direction, quality, colour).
- Transcribe visible text verbatim in double quotes.
- Describe explicit content as direct factual description; never censor, soften or moralize.
- Omit mood, atmosphere, aesthetic judgments, image quality and meta phrases ("this image shows").
- If the user adds instructions (focus, length, style, a question about the image), follow them; they may be written in any language - the answer is always English.

Output ONLY the caption (or the answer). No preamble, no markdown."""


# Recommended prompt length per target, shown in the tooltip of min_words /
# max_words. Taken from the model makers' guides where they give one.
WORDS = {
    "Krea 2": "60-200 words (Krea 2 docs: long, detailed prompts work best)",
    "Qwen-Image 2.1": "400-500 words (official Qwen-Image 2.1 prompt rewriter)",
    "Qwen-Image-Edit 2.1": "30-80 words (Qwen gives no number; edit instructions stay short)",
    "Z-Image": "80-250 words (Tongyi: long, detailed prompts; examples 60-150)",
    "FLUX": "30-80 words (BFL FLUX.2 guide: 10-30 to explore, 30-80 for most work, 80+ for complex scenes)",
    "Illustrious": "20-40 tags (CLIP reads 77-token chunks)",
    "Pony": "40-60 words/tags (community practice; Pony gives no number)",
    "SDXL": "30-75 words (CLIP reads 77-token chunks)",
    "Wan 2.2": "60-200 words text-to-video, at most 100 image-to-video (official Wan 2.2 prompt extender)",
    "Wan 2.7": "80-200 words (Alibaba gives no number)",
    "Wan 3.0": "80-250 words (Alibaba gives no number)",
    "MiniMax H3 FL2VA": "120-250 words for integrated_multimodal_description (H3 gives no number)",
    "MiniMax H3 REF2VA": "350-500 words for detailed_description (official H3 guide)",
    "Seedream 5.0": "40-150 words, never more than 600 (BytePlus: concise and precise beats stacked adjectives)",
    "Seedream 4.5 / 4.0": "40-150 words, never more than 600 (BytePlus: concise and precise beats stacked adjectives)",
    "Seedream Edit": "15-60 words (BytePlus: concise, unambiguous edit instructions)",
    "GPT Image": "50-200 words (OpenAI gives no limit; long, structured prompts work)",
    "Nano Banana": "60-200 words (Google gives no number; detailed narrative paragraphs)",
    "Grok Imagine Image": "60-120 words, about 4-6 sentences (xAI image prompting guide)",
    "Flux 3": "30-100 words (BFL: start lean, add detail only where you want control)",
    "Seedance 2.5": "100-300 words for 5-15 s, up to about 500 for 30 s (BytePlus gives no number)",
    "Seedance 2.0": "80-250 words (BytePlus gives no number)",
    "Seedance 1.5 / 1.0 Pro": "40-150 words (BytePlus gives no number)",
    "Seedance Reference": "100-300 words (BytePlus gives no number)",
    "Kling 3.0": "50-200 words, under 2500 characters (Kling gives no word count)",
    "Veo 3.1": "60-150 words (Google gives no number; examples are a few sentences)",
    "Grok Imagine Video": "40-120 words (xAI gives no number; very long prompts are rejected)",
}

# One example result per target, appended to the guide: smaller (local) models
# follow a concrete example far more reliably than rules alone.
EXAMPLES = {
    "Krea 2": (
        "A close-up portrait of a young woman with straight black hair and an intense gaze, "
        "wearing a light grey collared shirt with a black tie, a bouquet of pink lilies blurred in "
        "the right foreground, solid crimson background, soft directional studio lighting from the "
        "left, shallow depth of field, muted warm palette, 85mm portrait photo"),
    "Qwen-Image 2.1": (
        "The image is a horizontal photorealistic photograph of a small corner bakery at dawn, set "
        "against a deep navy street still in shadow. In the background, a row of narrow stone "
        "houses with dark windows recedes along a cobbled lane. At the top of the frame, a "
        "weathered wooden sign hangs from an iron bracket and reads \"BÄCKEREI SONNE\" in bold "
        "cream-coloured serif letters. On the left, a tall shop window glows with warm amber light "
        "and shows three tiers of golden bread loaves on pale beech shelves. In the centre, a "
        "middle-aged baker in a flour-dusted white apron stands in the open doorway, holding a "
        "wicker basket of crusty rolls against her hip. On the right, a black bicycle with a "
        "wooden crate on its rear rack leans against the wall. At the bottom, wet cobblestones "
        "reflect the amber window light in long, broken streaks. The light comes from inside the "
        "shop, warm and soft, spilling through the doorway and casting the baker's long shadow "
        "towards the viewer ... [the real prompt continues like this, sentence by sentence, to "
        "about 450 words] ... The overall composition balances the warm, lit shop front against "
        "the cool, quiet street around it."),
    "Qwen-Image-Edit 2.1": (
        "Replace the jacket of the woman in <image1> with the red leather jacket from <image2>, "
        "matching its cut, colour, zips and stitching exactly, and let it fall naturally over her "
        "shoulders; keep her face, hairstyle, pose, the lighting and the background unchanged."),
    "Z-Image": (
        "A young woman in a red silk hanfu with intricate golden phoenix embroidery stands on a "
        "stone bridge at night, her black hair pinned into a high bun with a gold hairpin and a "
        "small red flower pattern painted on her forehead. She holds a round paper lantern in her "
        "right hand that lights her face from below with warm orange light, and looks calmly to "
        "the left. Behind her, a tiered pagoda stands in silhouette against a dark blue sky, with "
        "softly blurred lantern lights reflected in the river. Medium shot at eye level, sharp "
        "focus on her face, photorealistic."),
    "FLUX": (
        "A soaking wet tiger cub takes shelter under a broad banana leaf in a rainy jungle, water "
        "dripping from its whiskers, eyes wide and alert, heavy rain falling in silver streaks, "
        "dense green undergrowth softly blurred behind it, overcast diffused light, close-up "
        "nature photograph, shot on 100mm macro, shallow depth of field"),
    "Illustrious": (
        "masterpiece, best quality, amazing quality, absurdres, 1girl, solo, long silver hair, red "
        "eyes, black hooded cloak, holding lantern, looking at viewer, upper body, night, forest, "
        "fireflies, rim lighting, depth of field"),
    "Pony": (
        "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, source_anime, "
        "rating_safe, a girl with short pink hair in a yellow raincoat jumps over a puddle on a "
        "rainy city street, smiling, 1girl, solo, yellow raincoat, rubber boots, jumping, puddle, "
        "rain, city street, dynamic pose, full body"),
    "SDXL": (
        "photograph of an elderly fisherman mending a net on a wooden pier at dawn, weathered "
        "skin, grey wool sweater, coils of rope at his feet, soft golden side light, mist over "
        "the harbor, 85mm lens, shallow depth of field, film grain"),
    "Wan 2.2": (
        "Text-to-video:\nSunset time, Warm colors, Side lighting, Medium shot. A young surfer "
        "with wet sun-bleached hair and a black wetsuit carries a white surfboard across the sand "
        "towards the waves. Her stride quickens into a jog as the foam washes over her ankles; "
        "she lifts the board, steps into the water and paddles out while palm fronds sway in "
        "the wind behind her. The camera tracks alongside her, then holds as she paddles away.\n\n"
        "Image-to-video (start frame attached):\nThe woman turns her head towards the window and "
        "smiles, then lifts the cup and takes a slow sip while steam rises from it. The curtain "
        "moves gently in the breeze. The camera pushes in slowly."),
    "Wan 2.7": (
        "A cosy late-night diner with red vinyl booths and a long chrome counter. A tired "
        "waitress in her fifties with grey hair pinned up refills the coffee of a young man in a "
        "denim jacket who sits alone at the counter. She leans on the counter and says, in a "
        "warm, slow, slightly raspy voice with a southern accent: \"Long night, honey?\" He looks "
        "up, smiles wearily and nods. Warm practical lighting from pendant lamps, neon glow "
        "through the window, medium two-shot at eye level, slow push-in. Sound: the hum of a "
        "fridge, coffee pouring, rain against the window. No background music. Generate single "
        "shot."),
    "Wan 3.0": (
        "A rooftop garden in a city at dusk, string lights overhead. Shot 1 [0-4s]: wide shot, a "
        "man in a white shirt waters tomato plants while the skyline glows orange behind him; "
        "slow truck right. Shot 2 [4-8s]: close-up, his daughter, about ten, runs in holding a "
        "ripe tomato and says, excited and quick, in a bright child's voice: \"Look, the first "
        "one!\" Shot 3 [8-12s]: medium shot, he kneels, takes the tomato and laughs; static shot. "
        "Sound: distant traffic, water splashing on leaves, birdsong. Soft acoustic guitar in the "
        "background."),
    "MiniMax H3 FL2VA": (
        "How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns "
        "with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the "
        "6.00-second mark of the target video.\n\n"
        "integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium shot frames "
        "the potter from Picture 1 seated at her wheel, hands resting on a wet lump of grey clay. "
        "The camera pushes in with small amplitude at slow speed as she starts the wheel and "
        "presses her thumbs into the centre; the clay rises between her palms into a narrow "
        "cylinder, then widens as her fingers draw the walls outward. Water runs over her "
        "knuckles while the rim thins and steadies, and the finished bowl turns slowly to a stop "
        "in the shape, position and framing established by Picture 2.\n\n"
        "overall_soundscape: The steady whir of the potter's wheel, wet clay squelching under "
        "her fingers and water dripping into a bucket.\n\n"
        "non_diegetic_music: N/A"),
    "MiniMax H3 REF2VA": (
        "subject_definitions:\n"
        "<Subject 1> is the elderly man in <Picture 1>, with white hair, round glasses and a "
        "brown corduroy jacket.\n"
        "<Subject 2> is the old bookshop in <Picture 2>, with floor-to-ceiling wooden shelves and "
        "a green reading lamp.\n\n"
        "summary:\n"
        "[reference generation] <Subject 1> closes up <Subject 2> for the night and finds a "
        "forgotten letter inside a returned book.\n\n"
        "retention_analysis:\n"
        "<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - white hair, round "
        "glasses and brown corduroy jacket are kept.\n"
        "<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - wooden shelves and the "
        "green reading lamp are kept.\n\n"
        "detailed_description:\n"
        "The target video is in a quiet, realistic style with warm lamplight.\n"
        "[Shot 1] A medium wide shot shows <Subject 2> after closing time, ... [the real "
        "description continues shot by shot, 350-500 words] ...\n"
        "[Shot 2] At 00:05.000, the shot cuts to a close-up of <Subject 1> (S1) unfolding the "
        "letter; he murmurs in a soft, cracked voice, <d>[English] After all these years.</d>\n\n"
        "overall_soundscape:\n"
        "Pages rustling, the creak of the wooden floor and rain on the shop window.\n\n"
        "non_diegetic_music:\n"
        "A slow solo piano with long pauses, fading out at the end."),
    "Seedream 5.0": (
        "A vertical poster for a summer jazz festival by the sea. A saxophonist in a white linen "
        "suit plays on a small wooden stage at sunset, the orange sky mirrored in the calm water "
        "behind him and strings of warm bulbs swaying above a dancing crowd. Flat retro "
        "screen-print illustration in coral, teal and cream with a fine paper grain. At the top, "
        "the title \"BLUE TIDE JAZZ\" in bold rounded letters; at the bottom, \"12-14 July · "
        "Harbour Stage\" in small white capitals."),
    "Seedream 4.5 / 4.0": (
        "A tiny ramen stall in a narrow alley at night, seen from the street at eye level. An "
        "elderly cook in a white headband ladles broth into a red bowl while two office workers "
        "in loosened ties sit on stools at the counter. Steam rises into the light of a paper "
        "lantern that reads \"RAMEN\". Wet cobblestones reflect the warm glow, and a cat sleeps on "
        "a crate by the door. Realistic photograph, soft warm light, shallow depth of field."),
    "Seedream Edit": (
        "Dress the woman in Image 1 in the green wool coat from Image 2, matching its collar, "
        "buttons and length, and hang the brown leather bag from Image 3 on her left shoulder; "
        "keep her face, hairstyle, pose and the street background unchanged."),
    "GPT Image": (
        "Product ad for a craft coffee brand.\n"
        "Scene: a sunlit kitchen counter of pale oak, a window with soft morning light on the left.\n"
        "Subject: a matte black coffee bag standing upright, a ceramic cup of black coffee beside "
        "it with a thin curl of steam.\n"
        "Details: scattered roasted beans, a brass scoop, fine paper texture on the bag; "
        "photorealistic, shallow depth of field, eye-level.\n"
        "Text: on the bag, \"NORTH ROAST\" in bold white sans-serif capitals, centred - exact text, "
        "verbatim, no extra characters.\n"
        "Constraints: no watermark, no other text, no logos."),
    "Nano Banana": (
        "Create a photorealistic close-up of an elderly watchmaker at his cluttered workbench, "
        "leaning over an open pocket watch with a jeweller's loupe in his right eye and fine "
        "tweezers lifting a tiny brass gear. Warm light from a green-shaded desk lamp falls across "
        "his hands and the scattered springs, while the shop behind him fades into soft shadow "
        "with rows of wall clocks. Shot on an 85mm lens at eye level, shallow depth of field, rich "
        "film-like colour with deep greens and warm brass tones."),
    "Grok Imagine Image": (
        "A red vintage scooter stands on its kickstand on a narrow cobbled street in a hillside "
        "town at midday. Its chrome mirrors and cracked leather seat catch the light, and a wicker "
        "basket of lemons is strapped to the rear rack. Realistic travel photograph. Hard midday "
        "sun casts short, crisp shadows across the stones and keeps the scooter clearly readable. "
        "Warm palette of red, ochre and pale yellow walls. Low three-quarter view from the left, "
        "the scooter centred in the lower half of the frame."),
    "Flux 3": (
        "Editorial photograph of a ceramic teapot on a bleached oak table beside a window, "
        "afternoon light falling in from the left and casting a long soft shadow. A small paper "
        "tag tied to the handle reads \"OPEN LATE\" in bold black sans-serif capitals. Framed "
        "slightly from above with an 85mm lens, shallow depth of field."),
    "Kling 3.0": (
        "A rainy night market lined with neon signs, cinematic realism; a street vendor in a "
        "yellow raincoat and a hungry delivery rider.\n"
        "[Shot 1: Wide shot, 3s] The vendor in the yellow raincoat stirs a steaming pot under a "
        "dripping awning while scooters splash past; slow truck right.\n"
        "[Shot 2: Medium shot, 3s] The delivery rider in a black helmet stops at the stall and "
        "lifts his visor. Rider (tired, English): \"Anything still hot?\"\n"
        "[Shot 3: Close-up, 4s] The vendor in the yellow raincoat ladles soup into a bowl and "
        "smiles. Vendor (warm tone, English): \"Best soup in the city.\" Slow push-in.\n"
        "Wet reflections, warm and magenta neon light, shallow depth of field. Ambient: rain on "
        "tarpaulin, sizzling oil, distant traffic."),
    "Veo 3.1": (
        "Low-angle tracking shot: a lighthouse keeper in a heavy wool coat climbs a spiral iron "
        "staircase at dusk, a lantern swinging in his hand and throwing warm light across the "
        "curved stone walls. He stops at a narrow window, wipes the fogged glass with his sleeve "
        "and looks out at dark waves rolling in. He says quietly, \"The storm is early.\" Shallow "
        "depth of field, weathered documentary look, cold blue light outside against the warm "
        "lantern glow. SFX: boots ringing on iron steps. Ambient noise: wind whistling through "
        "the tower."),
    "Grok Imagine Video": (
        "A woman in a long grey coat stands on a rain-soaked rooftop at night, city lights glowing "
        "behind her. She slowly turns towards the camera, rain dripping from her hair, as the "
        "camera pushes in. Neon signs reflect in the puddles at her feet. She says softly, \"You "
        "came back.\" Steady light rain, distant thunder and the hum of the city."),
    "Seedance 2.5": (
        "Realistic coastal drama on a windy harbour pier at dusk: an old fisherman teaches his "
        "granddaughter to tie a knot, handheld medium shots.\n"
        "0s-4s: Medium shot. The fisherman, in his seventies with a grey beard and a yellow oilskin "
        "jacket, sits on an upturned crate and slowly loops a thick rope around his fingers; the "
        "girl, about eight, in a red raincoat, leans in to watch. Gulls cry, waves slap against the "
        "pilings.\n"
        "4s-8s: Close-up of their hands. The girl copies the loop, pulls too hard and the rope "
        "slips; she laughs. The fisherman's line (warm, amused, low raspy voice): \"Gently. The sea "
        "is never in a hurry.\"\n"
        "8s-12s: The camera pulls back slowly to a wide shot as she holds up a finished knot and he "
        "nods, smiling, fishing boats rocking in the grey water behind them.\n"
        "Slight handheld sway throughout, natural colours, soft overcast light, rich details. Wind "
        "and harbour sounds only, no BGM. No subtitles."),
    "Seedance 2.0": (
        "A young barista in a black apron prepares a latte for an elderly regular in a small "
        "sunlit café. Shot 1: Medium shot, fixed camera. She slowly pours steamed milk into the "
        "cup, tilting it gently as a leaf pattern forms; morning light falls across the counter. "
        "<the hiss of the steam wand> Shot 2: Cut to a medium close-up of the old man in a tweed "
        "cap. He leans forward, his eyes crinkling, and says in a warm, slow voice {You remembered "
        "the cinnamon}. Shot 3: Close-up of the barista; the camera pushes in slowly as she lowers "
        "her eyes, the corners of her mouth rising, and slides the cup towards him. (soft acoustic "
        "guitar in the background) Warm tones, natural light, cinematic texture, rich details. "
        "Faces stay stable without deformation, natural smooth motion. No subtitles, no text, no "
        "watermark, no logo."),
    "Seedance 1.5 / 1.0 Pro": (
        "In a cramped vintage record shop on a rainy afternoon, a tall man in his forties with a "
        "grey scarf slowly flips through a crate of records while the young owner with short pink "
        "hair watches from the counter. The camera makes a slow lateral slide along the shelves. "
        "The man pulls out a record, holds it up and says, surprised and delighted, at a quick "
        "pace: \"I've been looking for this one for twenty years!\" The owner smiles and replies "
        "calmly: \"Then it was waiting for you.\" Rain patters on the window and a record crackles "
        "softly in the background."),
    "Seedance Reference": (
        "Image 1 is Mara, the woman with short silver hair and a black leather jacket - use her "
        "face and outfit. Image 2 is the rooftop location - use the place and its neon light. "
        "Audio 1 is Mara's voice timbre.\n"
        "Mara hands her old partner a sealed envelope on a rain-wet rooftop at night; tense neon "
        "thriller, slow camera.\n"
        "Shot 1: Wide shot of the rooftop from Image 2, slow push-in. Mara (Image 1) walks to the "
        "edge, rain glinting in the neon light, and stops beside a man in a grey trench coat who "
        "stands with his back to the camera.\n"
        "Shot 2: Medium close-up of Mara. She pulls an envelope from her jacket and holds it out "
        "without looking at him. Mara's line (cold, quiet, the voice of Audio 1): \"Last job. Then "
        "we're even.\"\n"
        "Shot 3: Close-up of the envelope changing hands; the camera holds still as distant "
        "sirens rise.\n"
        "Mara's face and outfit stay consistent with Image 1 throughout; no duplicate characters. "
        "Rain and distant traffic, a low synth drone. No subtitles."),
}

# German texts for the node's language switch (web/grok_prompt_forge_i18n.js).
# Only what the user reads on the node; the system prompts stay English.
WORDS_DE = {
    "Krea 2": "60-200 Wörter (Krea-2-Doku: lange, detaillierte Prompts wirken am besten)",
    "Qwen-Image 2.1": "400-500 Wörter (offizieller Prompt-Umschreiber von Qwen-Image 2.1)",
    "Qwen-Image-Edit 2.1": "30-80 Wörter (Qwen nennt keine Zahl; Edit-Anweisungen bleiben kurz)",
    "Z-Image": "80-250 Wörter (Tongyi: lange, detaillierte Prompts; Beispiele 60-150)",
    "FLUX": "30-80 Wörter (BFL FLUX.2: 10-30 zum Ausprobieren, 30-80 für die meisten Bilder, 80+ für komplexe Szenen)",
    "Illustrious": "20-40 Tags (CLIP liest Abschnitte von 77 Tokens)",
    "Pony": "40-60 Wörter/Tags (Community-Praxis; Pony nennt keine Zahl)",
    "SDXL": "30-75 Wörter (CLIP liest Abschnitte von 77 Tokens)",
    "Wan 2.2": "60-200 Wörter Text-zu-Video, höchstens 100 Bild-zu-Video (offizieller Wan-2.2-Prompt-Erweiterer)",
    "Wan 2.7": "80-200 Wörter (Alibaba nennt keine Zahl)",
    "Wan 3.0": "80-250 Wörter (Alibaba nennt keine Zahl)",
    "MiniMax H3 FL2VA": "120-250 Wörter für integrated_multimodal_description (H3 nennt keine Zahl)",
    "MiniMax H3 REF2VA": "350-500 Wörter für detailed_description (offizieller H3-Leitfaden)",
    "Seedream 5.0": "40-150 Wörter, nie mehr als 600 (BytePlus: knapp und genau statt gehäufter Adjektive)",
    "Seedream 4.5 / 4.0": "40-150 Wörter, nie mehr als 600 (BytePlus: knapp und genau statt gehäufter Adjektive)",
    "Seedream Edit": "15-60 Wörter (BytePlus: knappe, eindeutige Edit-Anweisungen)",
    "GPT Image": "50-200 Wörter (OpenAI nennt keine Grenze; lange, gegliederte Prompts funktionieren)",
    "Nano Banana": "60-200 Wörter (Google nennt keine Zahl; ausführliche erzählende Absätze)",
    "Grok Imagine Image": "60-120 Wörter, etwa 4-6 Sätze (xAI-Leitfaden für Bild-Prompts)",
    "Flux 3": "30-100 Wörter (BFL: knapp beginnen, Details nur, wo du steuern willst)",
    "Seedance 2.5": "100-300 Wörter für 5-15 s, bis etwa 500 für 30 s (BytePlus nennt keine Zahl)",
    "Seedance 2.0": "80-250 Wörter (BytePlus nennt keine Zahl)",
    "Seedance 1.5 / 1.0 Pro": "40-150 Wörter (BytePlus nennt keine Zahl)",
    "Seedance Reference": "100-300 Wörter (BytePlus nennt keine Zahl)",
    "Kling 3.0": "50-200 Wörter, unter 2500 Zeichen (Kling nennt keine Wortzahl)",
    "Veo 3.1": "60-150 Wörter (Google nennt keine Zahl; Beispiele sind wenige Sätze)",
    "Grok Imagine Video": "40-120 Wörter (xAI nennt keine Zahl; sehr lange Prompts werden abgelehnt)",
}
ABOUT_DE = {
    "Krea 2": "Krea 2 Raw / Turbo und Fine-Tunes (natürliche Sprache, 60-200 Wörter). Der "
              "Negativprompt wirkt nur bei CFG > 1 (Raw); Turbo ignoriert ihn.",
    "Qwen-Image 2.1": "Qwen-Image 2.1 Text-zu-Bild (langer, beschreibender Absatz, ~400-500 "
                      "Wörter). Läuft in den ComfyUI-Vorlagen mit CFG 1, dort wird der "
                      "Negativprompt ignoriert.",
    "Qwen-Image-Edit 2.1": "Qwen-Image-2.1-Bearbeitung (Edit-Anweisung, <image1>..<image3>). "
                           "Die Eingangsbilder des Edits in derselben Reihenfolge an "
                           "image_1..image_3 anschließen. Kein Negativprompt (CFG 1).",
    "Z-Image": "Z-Image Turbo / Base (lange Beschreibung in natürlicher Sprache). Turbo hat "
               "keinen Negativprompt; er wirkt nur bei Base mit CFG 3-5.",
    "FLUX": "FLUX.2 [dev] / [klein], FLUX.2 [pro] / [max] / [flex] über API und FLUX.1 [dev] "
            "(natürliche Sprache, 30-80 Wörter). FLUX unterstützt keine Negativprompts.",
    "GPT Image": "OpenAI GPT Image 2 / 2.5 (flare, sunburst) und 1.5 über API: Erzeugen und "
                 "Bearbeiten mit Eingangsbildern. Kein Negativprompt; Größe und Qualität stellt "
                 "der Node ein.",
    "Nano Banana": "Google Nano Banana (Gemini 2.5 Flash Image), Nano Banana Pro (Gemini 3 Pro "
                   "Image), Nano Banana 2 / 2.1 und Lite über API: Erzeugen und Bearbeiten mit "
                   "Eingangsbildern. Kein Negativprompt.",
    "Grok Imagine Image": "xAI Grok Imagine Bild (grok-imagine-image 2.0, quality / pro) über API: "
                          "Erzeugen und Bearbeiten mit bis zu 5 Eingangsbildern. Kein Negativprompt.",
    "Flux 3": "Black Forest Labs Flux 3 Bild über API: Erzeugen und Bearbeiten mit bis zu 10 "
              "Bildern; das Modell erweitert Prompts selbst. Kein Negativprompt.",
    "Illustrious": "Illustrious XL und NoobAI-artige Modelle (Danbooru-Tags, ~20-40 Tags).",
    "Pony": "Pony Diffusion V6 XL und Pony-basierte Modelle (Score-Tags + kurze Beschreibung "
            "+ Tags). Der Workflow braucht CLIP skip 2.",
    "SDXL": "SDXL Base und fotorealistische Fine-Tunes wie Juggernaut XL (30-75 Wörter, "
            "CLIP-Abschnitte von 77 Tokens).",
    "Wan 2.2": "Wan 2.2 Text-zu-Video und Bild-zu-Video (umT5, 512 Tokens; Clips ~5 s). Für "
               "Bild-zu-Video das Startbild an image_1 anschließen. Offizieller Negativprompt; "
               "mit Lightning-LoRAs bei CFG 1 wird er ignoriert.",
    "Wan 2.7": "Wan 2.7 über API-Nodes (2-15 s, eigener Ton, mehrere Einstellungen, "
               "Referenz-zu-Video mit Image 1/2/3).",
    "Wan 3.0": "Wan 3.0 über API-Nodes (2-30 s, Ton, mehrsprachige Stimmen). Eigene "
               "Prompt-Regeln für 3.0 gibt es kaum; folgt dem Wan-2.7-Leitfaden.",
    "MiniMax H3 FL2VA": "MiniMax H3 Start-/Endbild zu Video+Ton: image_1 = Startbild, image_2 "
                        "= Endbild. Die Cliplänge in den Text schreiben (Standard 6 s). H3 "
                        "nutzt keinen Negativprompt.",
    "MiniMax H3 REF2VA": "MiniMax H3 Voll-Referenz Video+Ton: image_1..image_4 = "
                         "Referenzbilder (<Picture 1..4>). Referenzvideos oder -ton im Text "
                         "erwähnen. H3 nutzt keinen Negativprompt.",
    "Seedream 5.0": "ByteDance Seedream 5.0 Pro / Flash / Lite über API (natürliche Sprache, 40-150 "
                    "Wörter, Text in vielen Sprachen). Kein Negativprompt.",
    "Seedream 4.5 / 4.0": "ByteDance Seedream 4.5 und 4.0 über API (natürliche Sprache, 40-150 "
                          "Wörter). Kein Negativprompt.",
    "Seedream Edit": "ByteDance-Seedream-4.0-/4.5-/5.0-Bearbeitung und Mehrbild-Eingabe über API "
                     "(Edit-Anweisung, Image 1..4). Die Eingangsbilder in derselben Reihenfolge wie "
                     "im Seedream-Node an image_1..image_4 anschließen. Kein Negativprompt.",
    "Seedance 2.5": "ByteDance Seedance 2.5 über API (4-30 s, eigener Ton und Dialog in 10+ "
                    "Sprachen, Zeitangaben). Für Bild-zu-Video das Startbild an image_1 anschließen "
                    "(image_2 = Endbild). Kein Negativprompt.",
    "Seedance 2.0": "ByteDance Seedance 2.0 / 2.0 Fast / 2.0 Mini über API (4-15 s, eigener Ton, "
                    "Einstellungen ohne Zeitangaben). Für Bild-zu-Video das Startbild an image_1 "
                    "anschließen (image_2 = Endbild). Kein Negativprompt.",
    "Seedance 1.5 / 1.0 Pro": "ByteDance Seedance 1.5 Pro (Ton, Dialog) und 1.0 Pro / Pro Fast "
                              "(ohne Ton) über API (etwa 4-12 s). Für Bild-zu-Video das Startbild "
                              "an image_1 anschließen. Kein Negativprompt.",
    "Seedance Reference": "ByteDance Seedance 2.5 / 2.0 Referenz-zu-Video über API: image_1..image_4 "
                          "= Referenzbilder (Image 1..4) in derselben Reihenfolge wie im "
                          "Seedance-Node. Referenzvideos oder -ton (Video 1, Audio 1) im Text "
                          "erwähnen. Kein Negativprompt.",
    "Kling 3.0": "Kling 3.0 / O3 Omni über API (3-15 s, eigener Ton, bis zu 6 Einstellungen, "
                 "Referenzen @Image1..), auch Kling 2.6 (Ton) und 2.5 Turbo. Für Bild-zu-Video das "
                 "Startbild an image_1 anschließen (image_2 = Endbild). Der Negativprompt gilt für "
                 "die Text-/Bild-zu-Video-Nodes von 3.0 / 2.x; Omni hat keinen.",
    "Veo 3.1": "Google Veo 3.1 / 3.1 Fast / 3.1 Lite über API (4, 6 oder 8 s, eigener Ton und "
               "Dialog). Für Bild-zu-Video das Startbild an image_1 anschließen (image_2 = Endbild). "
               "Der Negativprompt gehört in das Feld negative_prompt des Nodes.",
    "Grok Imagine Video": "xAI Grok Imagine Video (grok-imagine-video, 1.5, 1.5 Lite) über API "
                          "(1-15 s, Ton mit Lippensynchronität, Referenzen @Image1..). Für "
                          "Bild-zu-Video das Startbild an image_1 anschließen. Kein Negativprompt.",
}


RECAST = """You are an expert prompt editor for image and video models in ComfyUI. The user gives an existing prompt - written for any target model, in any format (natural language, tag list, multi-section video format) - and usually a short instruction such as "replace the man with Person 1". The persons to put in are defined in the "Persons" section below.

## Task
Recast the prompt: swap the persons, keep everything else.
- Replace the persons the instruction names with the selected persons. Without an instruction, replace the main person with Person 1, the second person with Person 2, and so on.
- Use each new person's name, trigger and description exactly as defined. Remove the old person's identity traits (name, trigger, face, hair, body, age) completely.
- Adapt everything that depends on the person so the result is consistent: pronouns, gendered words and gendered details (beard, dress, "he"/"she"), and dialogue attribution or voice descriptions if the format has them.
- Keep everything else exactly: action, pose, setting, background, objects, composition, camera, lighting, style, mood, dialogue lines, timing, shot structure, format, syntax, special tokens (score tags, quality tags, <image1>, <Picture 1>, field labels) and the original's length.
- Do not improve, extend or shorten the prompt beyond the swap.

""" + COMMON


# Preset groups for the filter on the node (web/grok_prompt_forge.js); the
# user's own presets show up as "own".
GROUPS = {"image": "image", "tags": "image", "edit": "edit", "video": "video", "h3": "video"}


def _preset(description, system_prompt, negative, temperature, top_p, max_tokens, words="",
            description_de="", words_de="", group="tools"):
    return {
        "description": description,
        "system_prompt": system_prompt,
        "negative_prompt": negative,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "words": words,
        "description_de": description_de,
        "words_de": words_de,
        "group": group,
    }


def _model_prompt(target, task):
    label = target["label"]
    kind = target.get("kind", "image")
    if kind == "edit":
        if task == "idea":
            intro = (f"## Task\nThe user describes, in any language, what should change in the "
                     f"input image(s). Turn it into ONE optimal edit instruction for {label}.\n"
                     "- Keep every change the user asks for and nothing more.\n"
                     "- Look at the attached images to name the things to change precisely.")
        else:
            intro = (f"## Task\nThe user gives a caption or description of the desired RESULT "
                     f"image, written in any language. Write ONE optimal edit instruction for "
                     f"{label} that turns the input image(s) into that result.\n"
                     "- Compare the description with the attached input images (if any) and "
                     "change only what differs; everything else is preserved.\n"
                     "- Stay faithful to the description: add nothing it does not contain.")
    else:
        intro = (TASK_IDEA if task == "idea" else TASK_CAPTION).format(label=label)
        if task == "caption" and kind in ("video", "h3"):
            intro += "\n" + CAPTION_TO_VIDEO
    role = "edit instructions" if kind == "edit" else "prompts"
    example = EXAMPLES[label]
    return (f"You are an expert prompt writer for {label} in ComfyUI.\n\n{intro}\n\n"
            f"## How {label} wants its {role}\n{target['guide']}\n\n"
            f"## Example of a good result\nFor form, structure and length only - never copy its "
            f"content, subjects or wording.\n\n{example}\n\n{COMMON}")


def _build():
    presets = {
        "Custom system prompt": _preset(
            "Write your own system prompt (or connect custom_system_prompt). Empty = only "
            "the node's own rules are sent (the user's input is binding, optional word range).",
            "", "", 0.7, 1.0, 8192, "",
            "Eigenen Systemprompt schreiben (oder custom_system_prompt anschließen). Leer = "
            "nur die eigenen Regeln des Nodes werden gesendet (Eingabe ist verbindlich, "
            "optionale Wortzahl)."),
        "Caption ▸ LoRA training caption": _preset(
            "Refine a raw caption (e.g. JoyCaption) into a LoRA training caption. Put the "
            "trigger token into trigger_word (or leave it empty for none).",
            LORA_CAPTION, "", 0.2, 1.0, 8192,
            "no fixed range - keep the detail of the raw caption",
            "Eine Roh-Caption (z. B. von JoyCaption) zur LoRA-Trainings-Caption verfeinern. "
            "Den Trigger in trigger_word eintragen (oder leer lassen für keinen).",
            "keine feste Spanne - Detailgrad der Roh-Caption beibehalten"),
        "Caption ▸ Describe image": _preset(
            "Caption the image connected to image_1. Optional text: extra instructions or a "
            "question about the image.",
            DESCRIBE_IMAGE, "", 0.3, 1.0, 8192, "",
            "Das an image_1 angeschlossene Bild beschreiben. Optionaler Text: zusätzliche "
            "Anweisungen oder eine Frage zum Bild."),
        "Recast ▸ Swap persons": _preset(
            "Swap the persons in an existing prompt (e.g. from '📜 Load from archive...') for "
            "the persons selected in person_1..4 - action, background, style and format stay. "
            "Optional instruction in the text, e.g. 'replace the man with Person 1'.",
            RECAST, "", 0.2, 1.0, 8192,
            "no fixed range - keeps the length of the original prompt",
            "Die Personen in einem vorhandenen Prompt (z. B. aus '📜 Aus Archiv laden...') "
            "gegen die in person_1..4 gewählten tauschen - Handlung, Hintergrund, Stil und "
            "Format bleiben. Optionale Anweisung im Text, z. B. 'ersetze den Mann durch "
            "Person 1'.",
            "keine feste Spanne - behält die Länge des Original-Prompts"),
    }
    for task, prefix in (("idea", "Generation"), ("caption", "Caption")):
        for t in TARGETS:
            temperature, top_p = t[task]
            what = ("Expand a short idea" if task == "idea"
                    else "Rewrite an existing caption faithfully")
            what_de = ("Eine kurze Idee ausbauen" if task == "idea"
                       else "Eine vorhandene Caption treu umschreiben")
            presets[f"{prefix} ▸ {t['label']}"] = _preset(
                f"{what} into a prompt for {t['about']}",
                _model_prompt(t, task), t["negative"], temperature, top_p, t["max_tokens"],
                WORDS[t["label"]],
                f"{what_de} zu einem Prompt für {ABOUT_DE[t['label']]}",
                WORDS_DE[t["label"]], GROUPS[t.get("kind", "image")])
    return presets


BUILTIN = _build()
DEFAULT_PRESET = "Generation ▸ Krea 2"
