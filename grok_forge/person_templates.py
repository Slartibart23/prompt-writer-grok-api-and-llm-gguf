"""Template persons for the library ("📥 Add templates" in the persons dialog).

Fictional characters that differ clearly in origin, skin tone, age, height,
build and hair. Only the outer appearance is described, in words an image model
can show: no numbers for height or age, no clothing (that belongs to the
scene). The label is the real name (Kenji); the name written into the prompt
has one digit for a letter (K3nji) and so works as a trigger. A description
that starts with "A group of" makes the entry a group of named persons (see
forge_node.is_group); the group's label is not written into the prompt."""

from . import library

_PERSONS = {
    "S3an": "S3an is an Irish man in his early twenties with very pale, freckled skin that "
            "reddens easily on his cheeks and nose. He is tall and very slim, with narrow "
            "shoulders, long arms and a boyish face with a pointed chin. His bright copper-red "
            "hair falls in loose, unruly curls to his ears, and his eyes are a clear green under "
            "pale red eyebrows.",
    "R4fael": "R4fael is a Brazilian man in his late twenties with warm olive-brown skin and an "
              "athletic, well-proportioned build of average height. His dark brown hair is cut "
              "short, with tight curls on top and neatly faded sides. He has warm brown eyes, "
              "thick eyebrows, a thin dark moustache and a wide, easy smile.",
    "S1one": "S1one is a Samoan man in his early thirties with warm brown skin and a very tall, "
             "massive build with broad shoulders and a heavy, powerful frame. His long, thick "
             "black hair is tied back in a tight bun on the crown of his head. A dark traditional "
             "Samoan tattoo of dense geometric bands covers his left shoulder and upper arm, and "
             "he has a broad face, dark eyes and a short, neat black beard.",
    "K3nji": "K3nji is a Japanese man in his mid thirties with light skin with a warm undertone "
             "and a slim build of average height. His straight black hair is cut short, with a "
             "sharp side parting and a neat fringe that is slightly longer at the front. He has "
             "narrow dark brown eyes behind thin rectangular black-framed glasses, a smooth, "
             "clean-shaven face and a calm, focused expression.",
    "4rjun": "4rjun is a Punjabi man from India in his early forties with medium brown skin and a "
             "stocky build with a round belly, a little shorter than average. His thick black "
             "hair is wavy and swept back, with the first grey strands above his ears. He has a "
             "full, carefully groomed black moustache, dark expressive eyes under heavy brows and "
             "a broad, friendly face.",
    "Kw4me": "Kw4me is a Ghanaian man in his late forties with very dark, smooth skin; he is very "
             "tall, broad-shouldered and heavily muscular. His head is clean-shaven, and he wears "
             "a short, neatly trimmed black full beard with a few grey hairs on the chin. He has "
             "deep-set dark brown eyes, a wide nose and a strong, square jaw.",
    "K4rim": "K4rim is an Egyptian man in his late fifties with light olive skin and a short, "
             "heavyset build with a thick neck and a broad chest. He is bald on top, and the "
             "close-cropped hair left around his temples and the back of his head is grey. He "
             "has a prominent hooked nose, dark heavy-lidded eyes, deep lines around his mouth "
             "and dense grey stubble.",
    "0lav": "0lav is a Norwegian man in his late sixties with pale, weathered skin and a very "
            "tall, gaunt frame with long limbs and bony shoulders. His long silver-blond hair is "
            "pulled back into a loose ponytail, and a full grey beard reaches down to his chest. "
            "He has deep-set pale blue eyes, a long straight nose and deep wrinkles across his "
            "forehead and around his eyes.",
    "4mara": "4mara is a Nigerian woman in her mid twenties with smooth dark brown skin and a "
             "tall, slender build with long legs and a long, graceful neck. Her black hair is "
             "styled in long, thin box braids that fall to the middle of her back. She has high "
             "cheekbones, large dark brown eyes with long lashes, full lips and a wide, bright "
             "smile.",
    "J1woo": "J1woo is a Korean woman in her early fifties with light, fair skin and a petite, "
             "slight build, clearly shorter than most people around her. Her straight black hair "
             "is cut in a sharp chin-length bob streaked with silver-grey strands. She has a "
             "round face, dark brown eyes, fine laugh lines and neatly shaped eyebrows.",
}

_GROUPS = {
    "Group_of_men":
        "A group of six men, each clearly different from the others. B0ris is a Russian man in "
        "his fifties with pale skin and a very tall, barrel-chested build; his grey hair is cut "
        "in a short buzz cut, and his nose is flattened from an old break. M4teo is an Argentine "
        "man in his late twenties of average height and a wiry build, with light tan skin, "
        "slicked-back black hair and a dark three-day stubble. 0usmane is a Senegalese man in his "
        "thirties with very dark skin and a very tall, lanky frame; he wears his black hair in "
        "short twists and has a narrow, angular face. T4koda is a Lakota man in his forties with "
        "copper-brown skin and a broad, solid build; his long, straight black hair is worn in two "
        "braids over his shoulders. M1nh is a Vietnamese man in his early twenties, short and "
        "sinewy, with light golden skin and spiky hair dyed platinum blond. J4n is a Dutch man in "
        "his sixties, tall and heavy, with ruddy skin, a bald head and thick white mutton-chop "
        "sideburns.",
    "Group_of_women":
        "A group of four women, each clearly different from the others. S0fia is an Italian woman "
        "in her late thirties of average height with a curvy figure and olive skin; her long, "
        "dark brown hair falls in loose waves past her shoulders. Fre1ja is a Swedish woman in her "
        "early twenties, very tall and athletic, with fair skin, ice-blue eyes and a long "
        "platinum-blonde braid. L3ila is an Iranian woman in her forties, petite and slender, with "
        "light olive skin, thick dark eyebrows and dense black hair gathered in a low bun. Gr4ce "
        "is a Jamaican woman in her sixties, short and plump, with deep brown skin, a warm round "
        "face and short natural grey hair.",
}

# prompt name -> (label = real name, gender). The prompt name swaps the first a, e, i
# or o of the real name for 4, 3, 1 or 0 (see web/grok_prompt_forge.js triggerName).
_LABELS = {
    "S3an": ("Sean", "m"), "R4fael": ("Rafael", "m"), "S1one": ("Sione", "m"),
    "K3nji": ("Kenji", "m"), "4rjun": ("Arjun", "m"), "Kw4me": ("Kwame", "m"),
    "K4rim": ("Karim", "m"), "0lav": ("Olav", "m"), "4mara": ("Amara", "f"),
    "J1woo": ("Jiwoo", "f"),
}
_GROUP_GENDERS = {"Group_of_men": "m", "Group_of_women": "f"}

# Style blocks: short and concrete, only visible features, and only positive words.
# A style says what the picture is and how it was made (painted, drawn, computer-
# generated ...) - never what it is not: image models are pulled towards every word
# in a prompt, negated or not, so "not realistic" would bring realism back. The
# light is set separately on the writer node (light: daylight / night / free).
_STYLES = {
    "Natural daylight":
        "Natural photograph in clear, white, neutral daylight. The light falls evenly from the "
        "sky or a window and leaves soft shadows. The colours are true to life, calm and lightly "
        "saturated, just as the eye sees them.",
    "Cartoon":
        "Hand-drawn 2D cartoon illustration. Bold black outlines, flat bright colours and simple "
        "cel shading. Rounded, slightly exaggerated shapes and big expressive faces, drawn and "
        "coloured by hand.",
    "Oil painting":
        "Traditional oil painting on canvas, painted by hand with brushes. Visible brushstrokes "
        "and thick impasto in the highlights. Rich colours blended softly on the canvas, with the "
        "fine weave of the canvas showing in the thin, dark areas.",
    "Line drawing":
        "Clean black ink line drawing on plain white paper. Contours drawn with confident lines "
        "of even weight. Pure black lines on a bright white page.",
    "Watercolour":
        "Watercolour painting on textured white paper, painted by hand. Soft, transparent washes "
        "of colour that bleed into each other at the edges. Visible paper grain and open areas of "
        "bright white paper.",
    "Pencil sketch":
        "Graphite pencil sketch on off-white sketchbook paper, drawn by hand. Loose construction "
        "lines, hatched and cross-hatched shading and smudged soft tones, all in shades of grey.",
    "Anime":
        "Japanese anime illustration, drawn and coloured digitally. Clean line art, large "
        "expressive eyes, smooth cel shading with crisp shadow shapes and a bright, clean colour "
        "palette.",
    "Comic book":
        "Western comic book panel, inked and coloured by hand. Strong black ink lines, halftone "
        "dot shading and bold, saturated flat colours in a dynamic composition.",
    "3D render":
        "Stylised 3D CGI render, a computer-generated image in the look of a modern animated "
        "feature film. Smooth rounded shapes, soft subsurface materials and clean, simplified "
        "surfaces.",
    "Vintage film photo":
        "Photograph shot on 35mm colour film in the 1970s. Fine film grain, slightly faded warm "
        "colours and soft contrast. Natural, unposed framing.",
    "Van Gogh":
        "Oil painting in the style of Vincent van Gogh, painted by hand in thick impasto. Bold, "
        "swirling brushstrokes that follow every form, vivid complementary colours such as "
        "cobalt blue and chrome yellow, and raised ridges of paint across the whole canvas.",
    "Rembrandt":
        "Oil painting in the style of Rembrandt van Rijn, painted by hand in the manner of the "
        "Dutch Golden Age. Warm earthy browns, ochres and golds, a deep dark background and one "
        "soft beam of light that models the faces, with rich glazes and visible brushwork.",
    "Simpsons":
        "2D cartoon in the style of The Simpsons TV series, drawn and coloured as hand-made "
        "animation. Bright yellow skin, large round eyes with small black pupils, overbites, "
        "four-fingered hands, thick black outlines and flat, saturated colours.",
    "Pixar":
        "Computer-animated 3D image in the style of a Pixar feature film, a CGI render. Large "
        "expressive eyes, soft rounded stylised proportions, smooth glowing skin shading, "
        "simplified detailed textures and bright, cheerful colours.",
    "GTA VI":
        "Digital illustration in the style of the Grand Theft Auto VI cover art and loading "
        "screens, painted digitally. Bold stylised figures with crisp outlines, smooth painterly "
        "shading, saturated Miami colours of teal, magenta and orange, and a poster-like "
        "composition.",
}

# In the format of an exported library (library.import_entries): label -> entry.
# A single person's name is also their trigger.
TEMPLATES = {
    "persons": {
        **{_LABELS[name][0]: {"name": name, "gender": _LABELS[name][1], "trigger": name,
                              "description": text, "voice": ""} for name, text in _PERSONS.items()},
        **{label: {"name": "", "gender": _GROUP_GENDERS[label], "trigger": "",
                   "description": text, "voice": ""} for label, text in _GROUPS.items()},
    },
    "styles": {label: {"text": text} for label, text in _STYLES.items()},
}

# The style texts of the first 1.5.0 build. A style block that still holds one of
# them unchanged is updated by add_to_library; your own edits are never touched.
_OUTDATED_STYLES = {
    'Photorealistic photograph with an entirely natural look. Clear, white, neutral '
    'daylight lights the scene evenly. Shadows are soft and realistic, colours are true '
    'to life and unsaturated. No dramatic lighting, no golden hour, no colour grading, no'
    ' vignette and no artificial effects.',
    'Hand-drawn 2D cartoon illustration, clearly not a photograph. Bold black outlines, '
    'flat bright colours and simple cel shading. Slightly exaggerated, rounded shapes and'
    ' expressive faces. No photorealistic skin, textures or lighting.',
    'Traditional oil painting on canvas, clearly not a photograph. Visible brushstrokes '
    'and thick impasto in the highlights. Rich but natural colours, softly blended on the'
    ' canvas. The fine weave of the canvas shows through in the thin, dark areas.',
    'Clean black ink line drawing on plain white paper, clearly not a photograph. '
    'Contours only, drawn with confident lines of even weight. No shading, no colour and '
    'no background texture.',
    'Watercolour painting on textured white paper, clearly not a photograph. Soft, '
    'transparent washes of colour that bleed into each other at the edges. Visible paper '
    'grain and areas of untouched white paper.',
    'Graphite pencil sketch on off-white sketchbook paper, clearly not a photograph. '
    'Loose construction lines, hatched and cross-hatched shading, and smudged soft tones.'
    ' Monochrome grey only.',
    'Japanese anime illustration, clearly not a photograph. Clean line art, large '
    'expressive eyes, smooth cel shading with crisp shadow shapes and a bright, clean '
    'colour palette. No photorealistic textures.',
    'Western comic book panel, clearly not a photograph. Strong black ink lines, halftone'
    ' dot shading and bold, saturated flat colours. Dynamic composition with clear '
    'shapes.',
    'Stylised 3D CGI render, a computer-generated image and clearly not a photograph. '
    'Smooth rounded shapes, soft subsurface materials and clean studio-like surfaces, '
    'like a modern animated feature film.',
    'Photograph shot on 35mm colour film in the 1970s. Fine film grain, slightly faded '
    'warm colours and soft contrast. Natural, unposed framing.',
}


def add_to_library():
    """Add the templates to your library: new labels are added, style blocks that
    still hold an outdated template text unchanged are updated, everything else
    is left alone. Returns (added, updated, kept)."""
    styles = library.load()["styles"]
    updated = 0
    for label, entry in TEMPLATES["styles"].items():
        current = styles.get(label)
        if current and current["text"] in _OUTDATED_STYLES and current["text"] != entry["text"]:
            library.save("style", label, entry)
            updated += 1
    added, _, skipped = library.import_entries(TEMPLATES, False)
    return added, updated, skipped - updated
