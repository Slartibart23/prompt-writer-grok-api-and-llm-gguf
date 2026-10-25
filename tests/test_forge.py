"""
Offline tests (no API key, no network, no ComfyUI). Run from the pack folder with
ComfyUI's Python, which has numpy and Pillow:

    python -m unittest discover -s tests -v
"""

import codecs
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import types
import unittest
from unittest import mock

import numpy as np

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = tempfile.mkdtemp(prefix="grok_forge_test_")


def _install_stubs():
    fp = types.ModuleType("folder_paths")
    fp.base_path = TMP
    os.makedirs(os.path.join(TMP, "user"), exist_ok=True)
    fp.get_user_directory = lambda: os.path.join(TMP, "user")
    fp.models_dir = os.path.join(TMP, "models")
    sys.modules["folder_paths"] = fp


def _load_pack():
    os.environ.pop("XAI_API_KEY", None)
    spec = importlib.util.spec_from_file_location(
        "grokpack", os.path.join(PACK, "__init__.py"), submodule_search_locations=[PACK])
    pack = importlib.util.module_from_spec(spec)
    sys.modules["grokpack"] = pack
    with mock.patch("requests.get", side_effect=RuntimeError("no network in tests")):
        spec.loader.exec_module(pack)
    return pack


_install_stubs()
PACK_MODULE = _load_pack()
from grokpack.grok_forge import api, archive, builtin_presets, forge_node, library, models, presets  # noqa: E402
from grokpack.grok_forge import local_models, local_node  # noqa: E402


def tearDownModule():
    shutil.rmtree(TMP, ignore_errors=True)


class FakeResponse:
    def __init__(self, status, body):
        self.status_code = status
        self._body = body
        self.text = json.dumps(body)

    def json(self):
        return self._body


def ok(content, finish="stop"):
    return FakeResponse(200, {
        "choices": [{"message": {"content": content}, "finish_reason": finish}],
        "usage": {"total_tokens": 42, "completion_tokens_details": {"reasoning_tokens": 30}},
    })


class BuiltinPresetTests(unittest.TestCase):
    def test_every_preset_is_complete(self):
        for name, p in builtin_presets.BUILTIN.items():
            with self.subTest(name=name):
                for field in presets.FIELDS:
                    self.assertIn(field, p)
                self.assertEqual(presets.clean(p), {k: p[k] for k in presets.FIELDS})
                self.assertGreaterEqual(p["max_tokens"], 2048, "reasoning needs room")

    def test_every_target_preset_recommends_a_length(self):
        for name, p in builtin_presets.BUILTIN.items():
            if name.startswith(("Generation ▸", "Caption ▸ ")) and "LoRA" not in name and "Describe" not in name:
                self.assertRegex(p["words"], r"\d", name)

    def test_every_preset_has_german_texts(self):
        for name, p in builtin_presets.BUILTIN.items():
            self.assertTrue(p["description_de"], name)
            self.assertEqual(bool(p["words"]), bool(p["words_de"]), name)

    def test_default_preset_exists(self):
        self.assertIn(builtin_presets.DEFAULT_PRESET, builtin_presets.BUILTIN)

    def test_all_requested_targets_present(self):
        names = " ".join(builtin_presets.BUILTIN)
        for target in ("Krea 2", "Qwen-Image 2.1", "Qwen-Image-Edit 2.1", "Z-Image", "FLUX",
                       "Illustrious", "Pony", "SDXL", "Wan 2.2", "Wan 2.7", "Wan 3.0",
                       "MiniMax H3 FL2VA", "MiniMax H3 REF2VA", "Seedream 5.0",
                       "Seedream 4.5 / 4.0", "Seedream Edit", "Seedance 2.5", "Seedance 2.0",
                       "Seedance 1.5 / 1.0 Pro", "Seedance Reference", "GPT Image", "Nano Banana",
                       "Grok Imagine Image", "Flux 3", "Kling 3.0", "Veo 3.1",
                       "Grok Imagine Video"):
            self.assertIn(f"Generation ▸ {target}", names)
            self.assertIn(f"Caption ▸ {target}", names)
        self.assertIn("Caption ▸ LoRA training caption", names)
        self.assertIn("Caption ▸ Describe image", names)

    def test_every_preset_has_a_filter_group(self):
        groups = {p["group"] for p in builtin_presets.BUILTIN.values()}
        self.assertEqual(groups, {"image", "edit", "video", "tools"})
        self.assertEqual(builtin_presets.BUILTIN["Generation ▸ Seedream Edit"]["group"], "edit")
        self.assertEqual(builtin_presets.BUILTIN["Caption ▸ Kling 3.0"]["group"], "video")
        self.assertEqual(builtin_presets.BUILTIN["Caption ▸ Describe image"]["group"], "tools")
        # the group reaches the browser, also for a saved override of a built-in preset
        user = presets.all_presets()
        self.assertTrue(all(p["group"] for p in user if p["builtin"]))

    def test_api_models_without_negative_prompt(self):
        for target in ("Seedream 5.0", "Seedance 2.5", "GPT Image", "Nano Banana", "Flux 3",
                       "Grok Imagine Video"):
            self.assertEqual(builtin_presets.BUILTIN[f"Generation ▸ {target}"]["negative_prompt"], "")

    def test_everything_neutral(self):
        # names that must never ship, rot13-encoded so they don't ship here either
        text = json.dumps(builtin_presets.BUILTIN).lower()
        for encoded in ("z3y4avr", "zrynavr"):
            self.assertNotIn(codecs.decode(encoded, "rot13"), text)

    def test_output_always_english(self):
        for name, p in builtin_presets.BUILTIN.items():
            if p["system_prompt"]:
                self.assertIn("English", p["system_prompt"], name)


class StripWrappingTests(unittest.TestCase):
    def test_fences_quotes_and_lone_full_stop(self):
        self.assertEqual(api.strip_wrapping("```\nhello\n```"), "hello")
        self.assertEqual(api.strip_wrapping('"hello"'), "hello")
        self.assertEqual(api.strip_wrapping("1girl, solo, garden\n."), "1girl, solo, garden")
        self.assertEqual(api.strip_wrapping("A cat.\n\nA dog."), "A cat.\n\nA dog.")


class PresetStoreTests(unittest.TestCase):
    def setUp(self):
        path = os.path.join(api.user_dir(), "presets.json")
        if os.path.exists(path):
            os.remove(path)

    def test_save_list_delete_user_preset(self):
        presets.save("My Flux", {"system_prompt": "X", "temperature": 5, "max_tokens": "3000",
                                 "bogus": 1})
        p = presets.get("My Flux")
        self.assertEqual(p["system_prompt"], "X")
        self.assertEqual(p["temperature"], 2.0)  # clamped
        self.assertEqual(p["max_tokens"], 3000)
        self.assertNotIn("bogus", p)
        self.assertFalse(p["builtin"])
        self.assertEqual(presets.names()[-1], "My Flux")
        self.assertTrue(presets.delete("My Flux"))
        self.assertIsNone(presets.get("My Flux"))
        self.assertFalse(presets.delete("My Flux"))

    def test_override_and_restore_builtin(self):
        name = builtin_presets.DEFAULT_PRESET
        original = builtin_presets.BUILTIN[name]["system_prompt"]
        presets.save(name, {"system_prompt": "mine"})
        p = presets.get(name)
        self.assertTrue(p["builtin"] and p["overridden"])
        self.assertEqual(p["system_prompt"], "mine")
        self.assertEqual(p["temperature"], builtin_presets.BUILTIN[name]["temperature"])
        self.assertEqual(presets.names().count(name), 1)
        presets.delete(name)
        self.assertEqual(presets.get(name)["system_prompt"], original)

    def test_values_saved_under_the_old_idea_name_carry_over(self):
        with open(os.path.join(api.user_dir(), "presets.json"), "w", encoding="utf-8") as f:
            json.dump({"version": 1, "presets": {
                "Idea ▸ FLUX": {"system_prompt": "old flux"},
                "Idea ▸ Krea 2": {"system_prompt": "old krea"},
                "Generation ▸ Krea 2": {"system_prompt": "new krea"},
                "Idea ▸ my own": {"system_prompt": "mine"}}}, f)
        self.assertEqual(presets.get("Generation ▸ FLUX")["system_prompt"], "old flux")
        self.assertTrue(presets.get("Generation ▸ FLUX")["overridden"])
        self.assertEqual(presets.get("Generation ▸ Krea 2")["system_prompt"], "new krea")
        self.assertIsNone(presets.get("Idea ▸ FLUX"))
        self.assertEqual(presets.get("Idea ▸ my own")["system_prompt"], "mine")  # own name kept
        self.assertTrue(presets.delete("Generation ▸ FLUX"))  # also removes the old entry
        self.assertFalse(presets.get("Generation ▸ FLUX")["overridden"])

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            presets.save("  ", {})

    def test_broken_file_is_ignored(self):
        with open(os.path.join(api.user_dir(), "presets.json"), "w") as f:
            f.write("{nope")
        self.assertEqual(len(presets.names()), len(builtin_presets.BUILTIN))


class ForgeNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = forge_node.GrokPromptForge()
        self.base = dict(preset=builtin_presets.DEFAULT_PRESET, text="eine Katze im Regen",
                         system_prompt="SYS {trigger}", negative_prompt="NEG",
                         model=api.DEFAULT_MODEL, temperature=0.9, top_p=0.95,
                         max_tokens=4096, api_key="test-key")

    def run_node(self, response=None, **kw):
        args = dict(self.base, **kw)
        with mock.patch("requests.post", return_value=response or ok("a cat in the rain")) as post:
            out = self.node.forge(**args)
        return out, post

    def test_basic_request(self):
        out, post = self.run_node()
        self.assertEqual(out, ("a cat in the rain", "NEG"))
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["model"], "grok-4.20-0309-reasoning")
        self.assertEqual(payload["top_p"], 0.95)
        self.assertNotIn("presence_penalty", payload)
        system = payload["messages"][0]["content"]
        self.assertTrue(system.startswith("SYS (none)\n\n## The user's input is binding"))
        self.assertNotIn("## Length", system)
        self.assertEqual(payload["messages"][1]["content"], "eine Katze im Regen")

    def test_custom_system_prompt_wins_and_trigger(self):
        _, post = self.run_node(custom_system_prompt="CUSTOM {trigger}", trigger_word="ohwx")
        system = post.call_args.kwargs["json"]["messages"][0]["content"]
        self.assertTrue(system.startswith("CUSTOM ohwx\n\n"))
        self.assertIn(forge_node.BINDING_RULE, system)

    def test_empty_system_prompt_still_gets_rules(self):
        _, post = self.run_node(system_prompt="", min_words=10, max_words=20)
        system = post.call_args.kwargs["json"]["messages"][0]["content"]
        self.assertTrue(system.startswith("## The user's input is binding"))
        self.assertIn("between 10 and 20 words", system)

    def test_length_rule_variants(self):
        rule = forge_node.length_rule
        self.assertEqual(rule(0, 0), "")
        self.assertIn("between 30 and 80 words", rule(80, 30))  # swapped
        self.assertIn("at least 50 words", rule(50, 0))
        self.assertIn("at most 120 words", rule(0, 120))
        self.assertIn("overrides any length given above", rule(1, 2))

    def test_empty_custom_prompt_is_ignored(self):
        _, post = self.run_node(custom_system_prompt="   ")
        self.assertTrue(post.call_args.kwargs["json"]["messages"][0]["content"].startswith("SYS"))

    def test_top_p_one_not_sent(self):
        _, post = self.run_node(top_p=1.0)
        self.assertNotIn("top_p", post.call_args.kwargs["json"])

    def test_images_keep_slot_numbers(self):
        img = np.zeros((2, 8, 8, 3), dtype=np.float32)
        _, post = self.run_node(image_1=img, image_3=img, image_4=img)
        content = post.call_args.kwargs["json"]["messages"][1]["content"]
        texts = [c["text"] for c in content if c["type"] == "text"]
        self.assertEqual(texts[0], "Attached images: Image 1, Image 3, Image 4.")
        self.assertIn("Image 4:", texts)
        self.assertEqual(sum(c["type"] == "image_url" for c in content), 3)
        self.assertTrue(texts[-1].endswith("eine Katze im Regen"))

    def test_image_without_text(self):
        img = np.zeros((1, 8, 8, 3), dtype=np.float32)
        out, post = self.run_node(text="", image_1=img)
        self.assertEqual(out[0], "a cat in the rain")
        content = post.call_args.kwargs["json"]["messages"][1]["content"]
        self.assertIn("no text", content[-1]["text"])

    def test_nothing_to_do(self):
        out, post = self.run_node(text="  ")
        self.assertEqual(out, ("", "NEG"))
        post.assert_not_called()

    def test_fallback_on_error(self):
        out, _ = self.run_node(response=FakeResponse(403, {"error": "no"}))
        self.assertEqual(out, ("eine Katze im Regen", "NEG"))
        with self.assertRaises(RuntimeError):
            self.run_node(response=FakeResponse(403, {"error": "no"}), fallback_to_input=False)

    def test_reasoning_used_up_max_tokens(self):
        with self.assertRaisesRegex(RuntimeError, "Raise max_tokens"):
            self.run_node(response=ok("", finish="length"), fallback_to_input=False)

    def test_rejected_param_is_stripped_and_resent(self):
        rejected = FakeResponse(400, {"error": "Model x does not support parameter topP."})
        with mock.patch("requests.post", side_effect=[rejected, ok("fine")]) as post:
            out = self.node.forge(**self.base)
        self.assertEqual(out[0], "fine")
        self.assertNotIn("top_p", post.call_args.kwargs["json"])

    def test_input_types_and_validation(self):
        spec = forge_node.GrokPromptForge.INPUT_TYPES()
        self.assertEqual(spec["required"]["preset"][0], presets.names())
        self.assertEqual(spec["required"]["model"][1]["default"], "grok-4.20-0309-reasoning")
        self.assertEqual(spec["required"]["model"][0][0], "grok-4.20-0309-reasoning")
        for n in (1, 2, 3, 4):
            self.assertEqual(spec["optional"][f"image_{n}"][0], "IMAGE")
        for f in ("min_words", "max_words"):
            self.assertEqual(spec["optional"][f][1]["default"], 0)
        # widget order of 3.0.x must stay a prefix, or saved workflows shift
        v300 = ["preset", "text", "system_prompt", "negative_prompt", "model", "temperature",
                "top_p", "max_tokens", "seed", "custom_system_prompt", "image_1", "image_2",
                "image_3", "trigger_word", "max_side", "api_key", "api_key_file", "base_url",
                "fallback_to_input", "timeout_seconds"]
        order = list(spec["required"]) + list(spec["optional"])
        self.assertEqual(order[:len(v300)], v300)
        v310 = v300 + ["min_words", "max_words"]
        self.assertEqual(order[:len(v310)], v310)
        self.assertEqual(order[len(v310):], ["person_1", "person_2", "person_3", "person_4",
                                             "image_n_is_person_n", "style_1", "style_2",
                                             "archive", "image_4"])
        self.assertTrue(forge_node.GrokPromptForge.VALIDATE_INPUTS(
            "unknown", "unknown", person_1="Nobody", style_2="Gone"))


def _reset_user_files():
    for name in ("library.json", "archive.jsonl"):
        path = os.path.join(api.user_dir(), name)
        if os.path.exists(path):
            os.remove(path)


class LibraryTests(unittest.TestCase):
    def setUp(self):
        _reset_user_files()

    def test_save_rename_delete(self):
        library.save("person", " Alice ", {"trigger": "ohwx woman", "description": "red hair",
                                           "voice": "", "bogus": "x"})
        self.assertEqual(library.names("person"), [library.NONE, "Alice"])
        self.assertEqual(library.get("person", "Alice"),
                         {"trigger": "ohwx woman", "description": "red hair", "voice": ""})
        library.save("person", "Alice B.", {"trigger": "ohwx"}, old_name="Alice")
        self.assertEqual(library.names("person"), [library.NONE, "Alice B."])
        self.assertTrue(library.delete("person", "Alice B."))
        self.assertFalse(library.delete("person", "Alice B."))
        self.assertIsNone(library.get("person", library.NONE))

    def test_reserved_and_empty_names(self):
        for bad in ("", "  ", library.NONE):
            with self.assertRaises(ValueError):
                library.save("style", bad, {"text": "x"})

    def test_import_keeps_or_replaces(self):
        library.save("style", "Film", {"text": "mine"})
        payload = {"styles": {"Film": {"text": "theirs"}, "Noir": {"text": "dark"}},
                   "persons": {"Bob": {"trigger": "sks man"}, "": {"trigger": "x"}}}
        self.assertEqual(library.import_entries(payload), (2, 0, 2))
        self.assertEqual(library.get("style", "Film")["text"], "mine")
        self.assertEqual(library.import_entries(payload, overwrite=True), (0, 3, 1))
        self.assertEqual(library.get("style", "Film")["text"], "theirs")
        with self.assertRaises(ValueError):
            library.import_entries(["not", "a", "dict"])


class PersonRuleTests(unittest.TestCase):
    def setUp(self):
        _reset_user_files()
        library.save("person", "Alice", {"trigger": "ohwx woman", "description": "short red hair",
                                         "voice": "warm alto"})
        library.save("person", "Bob", {"trigger": "", "description": "grey beard"})
        library.save("style", "Film", {"text": "shot on 35mm film, grain"})
        self.node = forge_node.GrokPromptForge()
        self.base = dict(preset=builtin_presets.DEFAULT_PRESET, text="beide im Café",
                         system_prompt="SYS", negative_prompt="", model=api.DEFAULT_MODEL,
                         temperature=0.8, top_p=0.95, max_tokens=8192, api_key="k")

    def system_of(self, **kw):
        with mock.patch("requests.post", return_value=ok("result")) as post:
            self.node.forge(**dict(self.base, **kw))
        return post.call_args.kwargs["json"]["messages"][0]["content"]

    def test_persons_and_styles_are_appended(self):
        system = self.system_of(person_1="Alice", person_3="Bob", style_2="Film")
        self.assertIn("## Persons (binding)", system)
        self.assertIn("NAME must appear in the result", system)
        self.assertIn("Person 1:\n- Name: Alice", system)
        self.assertIn("Trigger: ohwx woman", system)
        self.assertIn("Voice: warm alto", system)
        self.assertIn("Person 3:\n- Name: Bob", system)
        self.assertNotIn("labels only", system)
        self.assertIn("- shot on 35mm film, grain", system)
        self.assertLess(system.index("## Persons"), system.index("## Style blocks"))

    def test_image_link_follows_slots_and_switch(self):
        img = np.zeros((1, 8, 8, 3), dtype=np.float32)
        system = self.system_of(person_1="Alice", person_2="Bob", image_1=img,
                                image_n_is_person_n=True)
        self.assertIn("Image 1 shows this person", system)
        self.assertNotIn("Image 2 shows", system)
        system = self.system_of(person_1="Alice", image_1=img, image_n_is_person_n=False)
        self.assertNotIn("shows this person", system)
        system = self.system_of(person_4="Bob", image_4=img, image_n_is_person_n=True)
        self.assertIn("Image 4 shows this person", system)  # person 4 has an image now
        spec = forge_node.GrokPromptForge.INPUT_TYPES()
        self.assertFalse(spec["optional"]["image_n_is_person_n"][1]["default"])  # off for new nodes

    def test_name_that_is_the_trigger_is_not_repeated(self):
        library.save("person", "Zed", {"trigger": "zed", "description": "tall"})
        system = self.system_of(person_2="Zed")
        self.assertIn("- Name: Zed", system)
        self.assertIn("The name is also the trigger.", system)
        self.assertNotIn("Trigger: zed", system)

    def test_unknown_person_is_skipped(self):
        system = self.system_of(person_1="Nobody")
        self.assertNotIn("## Persons", system)

    def test_persons_alone_are_enough_input(self):
        with mock.patch("requests.post", return_value=ok("result")) as post:
            out = self.node.forge(**dict(self.base, text="", person_1="Alice"))
        self.assertEqual(out[0], "result")
        self.assertIn("selected persons", post.call_args.kwargs["json"]["messages"][1]["content"])

    def test_is_changed_follows_edited_description(self):
        before = forge_node.GrokPromptForge.IS_CHANGED(person_1="Alice")
        library.save("person", "Alice", {"trigger": "ohwx woman", "description": "long hair"})
        self.assertNotEqual(before, forge_node.GrokPromptForge.IS_CHANGED(person_1="Alice"))

    def test_archive_written_and_searchable(self):
        self.system_of(person_1="Alice", text="Alice am Strand")
        self.system_of(archive=False, text="nicht archivieren")
        entries = archive.entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["persons"], ["Alice"])
        self.assertEqual(entries[0]["prompt"], "result")
        self.assertEqual(len(archive.entries(query="STRAND")), 1)
        self.assertEqual(archive.entries(query="mond"), [])

    def test_recast_preset(self):
        p = builtin_presets.BUILTIN["Recast ▸ Swap persons"]
        self.assertIn("Persons", p["system_prompt"])
        self.assertLessEqual(p["temperature"], 0.3)


class ShowPromptTests(unittest.TestCase):
    def test_passes_text_through_and_shows_it(self):
        cls = PACK_MODULE.NODE_CLASS_MAPPINGS["GrokShowPrompt"]
        self.assertTrue(cls.OUTPUT_NODE)
        self.assertEqual(list(cls.INPUT_TYPES()["required"]), ["text"])
        out = cls().show("a, b. c!")
        self.assertEqual(out, {"ui": {"text": ["a, b. c!"]}, "result": ("a, b. c!",)})
        self.assertEqual(cls().show(None)["result"], ("",))


class FakeLlama:
    """Stand-in for llama_cpp.Llama: records calls, answers with thinking + result."""
    instances = []

    def __init__(self, model_path, n_gpu_layers, n_ctx, chat_handler, verbose):
        self.args = dict(model_path=model_path, n_gpu_layers=n_gpu_layers, n_ctx=n_ctx)
        self.handler = chat_handler
        self.calls = []
        self.closed = False
        self.reply = "<think>\nplanning the prompt\n</think>\n\nA fox in the forest."
        self.finish = "stop"
        FakeLlama.instances.append(self)

    def create_chat_completion(self, **kw):
        self.calls.append(kw)
        return {"choices": [{"message": {"role": "assistant", "content": self.reply},
                             "finish_reason": self.finish}], "usage": {"total_tokens": 99}}

    def close(self):
        self.closed = True


class FakeHandler:
    def __init__(self, mmproj_path, verbose):
        self.mmproj_path = mmproj_path
        self.extra_template_arguments = {}

    def close(self):
        pass


def _fake_llama_cpp():
    llama_cpp = types.ModuleType("llama_cpp")
    llama_cpp.Llama = FakeLlama
    chat_format = types.ModuleType("llama_cpp.llama_chat_format")
    chat_format.Qwen35ChatHandler = FakeHandler
    return {"llama_cpp": llama_cpp, "llama_cpp.llama_chat_format": chat_format}


class LocalModelTests(unittest.TestCase):
    def setUp(self):
        _reset_user_files()
        shutil.rmtree(local_models.models_root(), ignore_errors=True)
        local_models.LOADED.unload()
        FakeLlama.instances.clear()
        self.entry = local_models.CATALOG[0]

    def fake_download(self):
        """Put empty model + mmproj files where the download would put them."""
        d = local_models.entry_dir(self.entry)
        os.makedirs(d, exist_ok=True)
        for name in (self.entry["file"], self.entry["mmproj"]):
            open(os.path.join(d, name), "wb").close()

    def run_node(self, **kw):
        p = presets.get("Generation ▸ FLUX")
        args = dict(preset="Generation ▸ FLUX", text="ein Fuchs im Wald", system_prompt=p["system_prompt"],
                    negative_prompt="", model=self.entry["label"], temperature=0.7, top_p=0.95,
                    max_tokens=8192, fallback_to_input=False)
        args.update(kw)
        with mock.patch.dict(sys.modules, _fake_llama_cpp()):
            return local_node.LocalPromptForgeGGUF().forge(**args)

    def test_catalog_labels_and_lookup(self):
        labels = local_models.model_labels()
        self.assertEqual(len(labels), len(local_models.CATALOG))
        self.assertFalse(any(l.startswith(local_models.DOWNLOADED) for l in labels))
        self.fake_download()
        self.assertTrue(local_models.model_labels()[0].startswith(local_models.DOWNLOADED))
        self.assertIs(local_models.find(local_models.model_labels()[0]), self.entry)
        self.assertIs(local_models.find(self.entry["label"]), self.entry)
        self.assertIsNone(local_models.find("nope"))
        for e in local_models.CATALOG:
            self.assertTrue(e["mmproj"].startswith("mmproj"), e["label"])

    def test_download_only_missing_files(self):
        calls = []

        def fake_hub(repo, name, local_dir):
            calls.append(name)
            path = os.path.join(local_dir, name)
            open(path, "wb").close()
            return path

        hub = types.ModuleType("huggingface_hub")
        hub.hf_hub_download = fake_hub
        with mock.patch.dict(sys.modules, {"huggingface_hub": hub}):
            model, mmproj = local_models.ensure_files(self.entry)
            self.assertEqual(calls, [self.entry["mmproj"], self.entry["file"]])
            self.assertTrue(model.endswith(self.entry["file"]))
            self.assertEqual(os.path.dirname(model), os.path.dirname(mmproj))
            local_models.ensure_files(self.entry)
            self.assertEqual(len(calls), 2)  # nothing downloaded twice

    def test_split_thinking(self):
        split = local_models.split_thinking
        self.assertEqual(split("<think>a</think>\n\nResult.", True, "stop"), "Result.")
        self.assertEqual(split("reasoning only\n</think>\nResult.", True, "stop"), "Result.")
        self.assertEqual(split("Direct answer.", False, "stop"), "Direct answer.")
        with self.assertRaisesRegex(RuntimeError, "still thinking"):
            split("thinking without end", True, "length")

    def test_run_strips_thinking_and_unloads(self):
        self.fake_download()
        out = self.run_node(person_1="(none)")
        self.assertEqual(out, ("A fox in the forest.", ""))
        llm = FakeLlama.instances[-1]
        self.assertTrue(llm.closed)  # unload_after_run defaults to on
        self.assertEqual(llm.args["n_gpu_layers"], "auto")
        self.assertEqual(llm.args["n_ctx"], 32768)
        self.assertTrue(llm.handler.mmproj_path.endswith(self.entry["mmproj"]))
        call = llm.calls[0]
        self.assertEqual(call["top_k"], 20)
        self.assertTrue(call["messages"][0]["content"].startswith("You are an expert prompt writer for FLUX"))
        self.assertIn("## Example of a good result", call["messages"][0]["content"])
        self.assertIn("## The user's input is binding", call["messages"][0]["content"])
        self.assertTrue(llm.handler.extra_template_arguments["enable_thinking"])
        self.assertEqual(archive.entries()[0]["model"], self.entry["label"])

    def test_model_stays_loaded_when_asked(self):
        self.fake_download()
        self.run_node(unload_after_run=False, thinking=False)
        self.run_node(unload_after_run=False, thinking=False, text="noch einer")
        self.assertEqual(len(FakeLlama.instances), 1)  # loaded once, used twice
        self.assertFalse(FakeLlama.instances[0].closed)
        self.assertFalse(FakeLlama.instances[0].handler.extra_template_arguments["enable_thinking"])
        local_models.LOADED.unload()
        self.assertTrue(FakeLlama.instances[0].closed)

    def test_images_and_persons_reach_the_model(self):
        self.fake_download()
        library.save("person", "Alice", {"trigger": "ohwx woman", "description": "red hair"})
        img = np.zeros((1, 8, 8, 3), dtype=np.float32)
        self.run_node(image_1=img, person_1="Alice")
        call = FakeLlama.instances[-1].calls[0]
        self.assertIn("- Name: Alice", call["messages"][0]["content"])
        content = call["messages"][1]["content"]
        self.assertEqual(sum(c["type"] == "image_url" for c in content), 1)

    def test_missing_llama_cpp_is_explained(self):
        self.fake_download()
        with mock.patch.dict(sys.modules, {"llama_cpp": None}):
            with self.assertRaisesRegex(RuntimeError, "LOCAL_GGUF.md"):
                local_node.LocalPromptForgeGGUF().forge(
                    preset="Generation ▸ FLUX", text="x", system_prompt="S", negative_prompt="",
                    model=self.entry["label"], temperature=0.7, top_p=0.95, max_tokens=512,
                    fallback_to_input=False)
            out = local_node.LocalPromptForgeGGUF().forge(
                preset="Generation ▸ FLUX", text="x", system_prompt="S", negative_prompt="N",
                model=self.entry["label"], temperature=0.7, top_p=0.95, max_tokens=512)
            self.assertEqual(out, ("x", "N"))  # fallback_to_input keeps batch runs alive

    def test_input_types(self):
        spec = local_node.LocalPromptForgeGGUF.INPUT_TYPES()
        names = list(spec["required"]) + list(spec["optional"])
        for gone in local_node.API_ONLY:
            self.assertNotIn(gone, names)
        for new in ("thinking", "unload_after_run", "context_length", "gpu_layers", "top_k"):
            self.assertIn(new, spec["optional"])
        # image_4 (1.2.0) comes after the local options, so their saved values keep their place
        self.assertEqual(names[-6:], [*local_node.LOCAL_OPTIONS, "image_4"])
        self.assertEqual(spec["required"]["model"][0], local_models.model_labels())
        self.assertTrue(local_node.LocalPromptForgeGGUF.VALIDATE_INPUTS("x", "y", person_1="z"))

    def test_every_target_has_an_example(self):
        for t in builtin_presets.TARGETS:
            self.assertIn(t["label"], builtin_presets.EXAMPLES)


class ModelListTests(unittest.TestCase):
    def test_refresh_puts_default_first_and_caches(self):
        body = {"models": [{"id": "grok-9"}, {"id": "grok-4.20-0309-reasoning"}, {"id": "grok-1"},
                           {"id": "grok-4.20-multi-agent-0309"}]}
        with mock.patch.dict(os.environ, {"XAI_API_KEY": "k"}), \
                mock.patch("requests.get", return_value=FakeResponse(200, body)):
            result = models.refresh()
        self.assertEqual(result, ["grok-4.20-0309-reasoning", "grok-1", "grok-9"])
        with open(os.path.join(api.user_dir(), "models.json")) as f:
            self.assertEqual(json.load(f)["models"], result)
        self.assertEqual(models.model_list(), result)


class PackTests(unittest.TestCase):
    def test_nodes_and_names(self):
        self.assertEqual(PACK_MODULE.NODE_DISPLAY_NAME_MAPPINGS, {
            "GrokPromptForge": "Prompt Writer · Grok API",
            "LocalPromptForgeGGUF": "Prompt Writer · LLM GGUF",
            "GrokShowPrompt": "Prompt Writer · Show Prompt",
            "GrokSystemPromptLoader": "Prompt Writer · System Prompt Loader",
            "GrokTextFileLoader": "Prompt Writer · Text File Loader",
        })
        for cls in PACK_MODULE.NODE_CLASS_MAPPINGS.values():
            self.assertEqual(cls.CATEGORY, "Prompt Writer")
        self.assertNotIn("GrokTextRefine", PACK_MODULE.NODE_CLASS_MAPPINGS)

    def test_text_file_loader(self):
        folder = os.path.join(TMP, "texts")
        os.makedirs(folder, exist_ok=True)
        for name in ("file10.txt", "file2.txt"):
            with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
                f.write(name)
        loader = PACK_MODULE.NODE_CLASS_MAPPINGS["GrokTextFileLoader"]()
        self.assertEqual(loader.load(folder, 0)[:2], ("file2.txt", "file2"))  # natural order
        self.assertEqual(loader.load(folder, 3, loop_at_end=True)[1], "file10")

    def test_system_prompt_loader_finds_the_example(self):
        loader = PACK_MODULE.NODE_CLASS_MAPPINGS["GrokSystemPromptLoader"]()
        self.assertIn("LoRA training", loader.load("example_caption_refine.txt")[0])


if __name__ == "__main__":
    unittest.main()
