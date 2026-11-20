"""Seed-driven variation for the writer nodes.

A language model asked for "a random pose" picks its most likely pose - the same
one run after run, whatever the seed. So the node draws the open choices itself:
with the run's seed it picks a pose, an interaction, a camera angle, a framing, a
setting and (for video) a camera move from the lists below and adds them to the
system prompt. The input, the selected persons and attached images always win;
the variation only fills what they leave open. The same seed gives the same
variation, a new seed a new scene.
"""

import random

POSES = {
    "sfw": [
        "standing with the weight on one leg, one hand in a pocket",
        "sitting sideways on a chair, one arm over the backrest",
        "leaning against a wall, arms crossed",
        "kneeling on one knee, both hands resting on the raised thigh",
        "lying on the stomach, chin propped on both hands, feet raised",
        "walking towards the camera mid-stride",
        "crouching, forearms resting on the knees",
        "sitting on the floor, knees drawn up, arms wrapped around them",
        "stretching both arms above the head",
        "turning back over one shoulder towards the camera",
        "sitting cross-legged, hands resting in the lap",
        "lying on the back, one arm behind the head, one knee raised",
        "perched on the edge of a table, one leg swinging",
        "leaning forward with both hands on a railing",
        "reclining on one elbow, legs stretched out",
        "standing in profile, head tilted back, eyes closed",
    ],
    "nsfw": [
        "lying on the back, knees raised and spread, one hand between the thighs",
        "kneeling upright on the bed, back arched, hands sliding up the body",
        "on all fours, looking back over one shoulder",
        "sitting on the edge of the bed, legs apart, leaning back on both hands",
        "lying on one side, the top leg drawn up towards the chest",
        "standing with the back against a wall, one foot raised on a chair",
        "squatting low, knees wide apart, hands on the knees",
        "lying on the stomach, hips raised, cheek on the pillow",
        "reclining in an armchair, one leg hooked over the armrest",
        "kneeling and sitting back on the heels, hands on the chest",
        "lying on the back with the head hanging over the edge of the bed",
        "standing bent forward over a table, hands flat on it",
    ],
}

INTERACTIONS = {
    "sfw": [
        "one embraces the other from behind, arms around the waist",
        "facing each other, foreheads touching, hands joined between them",
        "one lifts the other off the ground in a hug",
        "sitting back to back on the floor, heads leaning together",
        "walking side by side, fingers linked",
        "dancing in close hold, one leading the other into a turn",
        "one whispers into the other's ear, a hand on the shoulder",
        "one lies with the head in the other's lap",
        "kissing, one hand on the other's cheek",
        "one pulls the other up by both hands",
        "sitting close on a bench, one arm around the other's shoulders",
        "playfully wrestling, one pinning the other's wrists",
        "one carries the other piggyback",
    ],
    "nsfw": [
        "missionary: one lies on the back, the other on top between the raised legs",
        "missionary with the legs over the partner's shoulders",
        "cowgirl: one rides the other, facing them, hands on the chest",
        "reverse cowgirl: one rides the other, facing away",
        "doggystyle: one on all fours, the other kneeling behind, hands on the hips",
        "standing from behind, one pressed against a wall",
        "spooning: both on their sides, one behind the other",
        "lotus: sitting face to face, legs wrapped around each other",
        "sixty-nine: lying head to hips, mouths on each other",
        "oral: one kneels in front of the other, who stands",
        "oral: one lies back with spread legs, the other's head between the thighs",
        "standing lift: one carries the other, legs wrapped around the waist",
        "prone bone: one lies flat on the stomach, the other on top from behind",
        "on a chair: one sits, the other straddles the lap",
        "at the edge of the bed: one lies back, the other stands between the legs",
    ],
}

ANGLES = ["eye level", "a low angle from below", "a high angle from above",
          "the side, in profile", "behind, over one shoulder", "a three-quarter view from the left",
          "a three-quarter view from the right", "straight above (bird's-eye view)",
          "the point of view of one person", "a slightly tilted (Dutch) angle"]

FRAMINGS = {
    "sfw": ["full body", "a medium shot from the thighs up", "a close-up of faces and hands",
            "a wide shot with the room or landscape around them", "a cowboy shot from mid-thigh",
            "a medium close-up from the chest up"],
    "nsfw": ["full body", "a medium shot from the thighs up", "a close-up of faces and hands",
             "a wide shot with the room around them", "a tight shot of the bodies' point of contact",
             "a medium close-up from the chest up"],
}

SETTINGS = {
    "sfw": ["a sunlit kitchen", "a hotel room with a view over a city", "a rooftop terrace",
            "a forest clearing", "a beach at low tide", "a library between tall shelves",
            "a small rowing boat on a lake", "a loft with brick walls", "a greenhouse full of plants",
            "a train compartment", "a mountain hut", "a corner table in a café",
            "an empty dance studio", "a laundromat"],
    "nsfw": ["a bedroom with white linen", "a leather sofa in a living room",
             "a shower with glass walls", "a large hotel bed", "a wooden sauna bench",
             "a kitchen counter", "a bathtub", "a desk in an office after hours",
             "the back seat of a car", "a lounger by a pool", "a cabin with a fur rug",
             "a hayloft", "a velvet armchair in a dressing room"],
}

CAMERA_MOVES = ["a slow push-in", "a slow orbit around the persons", "a handheld follow",
                "a static, locked-off frame", "a slow pull-back", "a tracking shot alongside",
                "a slow tilt from the feet up to the faces", "a slow crane down"]


def section(seed, content="sfw", video=False):
    """The "## Variation" section for one run: the same seed gives the same choices."""
    kind = "nsfw" if content == "nsfw" else "sfw"
    rng = random.Random(f"{int(seed or 0)}:{kind}:{int(video)}")
    lines = [
        f"- Pose of a single person: {rng.choice(POSES[kind])}.",
        f"- Interaction of two or more persons: {rng.choice(INTERACTIONS[kind])}.",
        f"- Camera angle: from {rng.choice(ANGLES)}.",
        f"- Framing: {rng.choice(FRAMINGS[kind])}.",
        f"- Place, only when the input names none: {rng.choice(SETTINGS[kind])}.",
    ]
    if video:
        lines.append(f"- Camera movement: {rng.choice(CAMERA_MOVES)}.")
    return ("## Variation for this run (binding where the input leaves it open)\n"
            "The input, the selected persons and attached images always win. Wherever they "
            "leave a detail open, use these choices instead of your usual first idea, and "
            "describe them fully in the result's own form; use only the lines that fit the "
            "scene (the interaction only with two or more persons):\n" + "\n".join(lines))
