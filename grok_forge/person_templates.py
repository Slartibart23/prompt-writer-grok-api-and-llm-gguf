"""Template persons for the library ("📥 Add templates" in the persons dialog).

Fictional characters that differ clearly in origin, skin tone, age, height,
build and hair. Only the outer appearance is described, in words an image model
can show: no numbers for height or age, no clothing (that belongs to the
scene). Each name is also the trigger, with one digit for a letter. A
description that starts with "A group of" makes the entry a group of named
persons (see forge_node.is_group); the group's own name is only a label."""

_PERSONS = {
    "S34n": "S34n is an Irish man in his early twenties with very pale, freckled skin that "
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

# In the format of an exported library (library.import_entries). A single
# person's name is also their trigger; a group's name is only a label.
TEMPLATES = {"persons": {
    **{name: {"trigger": name, "description": text, "voice": ""} for name, text in _PERSONS.items()},
    **{name: {"trigger": "", "description": text, "voice": ""} for name, text in _GROUPS.items()},
}}
