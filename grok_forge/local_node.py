"""Prompt Writer · LLM GGUF: Prompt Writer · Grok API with a local, uncensored
Qwen3.8-27B (GGUF, llama-cpp-python) instead of the xAI API.

Presets, persons, style blocks, word range, archive and the language switch
work exactly as on Prompt Writer · Grok API; only the model fields differ. The model
and its vision projector are downloaded on the first run."""

from . import local_models
from .forge_node import (GrokPromptForge, _selected, archive_result, log_counts, prepare,
                         user_content)

LOG = local_models.LOG

# Fields of Prompt Writer · Grok API that only make sense for the xAI API.
API_ONLY = ("api_key", "api_key_file", "base_url", "timeout_seconds")

MODEL_TOOLTIP = (
    "Local uncensored Qwen3.8-27B (GGUF) with vision. ✓ = already downloaded. Otherwise the "
    "model and its vision projector (mmproj, 0.9 GB) are downloaded on the first run into "
    "ComfyUI/models/LLM_gguf/. Bigger quantization = better quality, more VRAM. Rough guide "
    "with the default context: 12 GB VRAM -> IQ2, 16 GB -> Q3 / IQ4_XS, 24 GB -> Q4, 32 GB -> "
    "Q4 / Q5. huihui = abliterated; HauhauCS = Aggressive uncensored fine-tune. Needs "
    "llama-cpp-python with CUDA - see docs/LOCAL_GGUF.md.")
LOCAL_OPTIONS = {
    "thinking": ("BOOLEAN", {"default": True, "tooltip":
        "On: the model thinks before answering (better prompts, slower - typically 10-40 s on "
        "a fast card). Off: answers directly. The thinking is never part of the output."}),
    "unload_after_run": ("BOOLEAN", {"default": True, "tooltip":
        "On: the model leaves VRAM after every run, so your image or video model has room "
        "again (the next run loads it again, ~5-20 s from an SSD). Off: it stays loaded and "
        "the next run starts at once - only if your VRAM fits both."}),
    "context_length": ("INT", {"default": 32768, "min": 2048, "max": 262144, "step": 1024,
        "tooltip": "Working memory in tokens: system prompt + images + thinking + answer. "
                   "More costs VRAM. 32768 suits all presets; with 12-16 GB VRAM use "
                   "8192-16384 and lower max_tokens to match."}),
    "gpu_layers": ("INT", {"default": -1, "min": -1, "max": 999, "tooltip":
        "-1 = automatic: llama.cpp puts as many layers on the GPU as fit (recommended). "
        "0 = CPU only (very slow). A number = that many layers on the GPU, the rest in RAM - "
        "for cards that are too small for the whole model."}),
    "top_k": ("INT", {"default": 20, "min": 0, "max": 200, "tooltip":
        "Considers only the k most likely next words. Qwen recommends 20; 0 = off."}),
}


class LocalPromptForgeGGUF:
    CATEGORY = "Prompt Writer"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompt", "negative_prompt")
    FUNCTION = "forge"
    DESCRIPTION = ("Prompt Writer · Grok API with a local uncensored Qwen3.8-27B (GGUF) instead of "
                   "the xAI API: same presets, persons, style blocks and archive. The model is "
                   "downloaded on the first run.")

    @classmethod
    def INPUT_TYPES(cls):
        spec = GrokPromptForge.INPUT_TYPES()
        required = dict(spec["required"])
        labels = local_models.model_labels()
        # the default as it appears in the list (with ✓ once downloaded)
        default = next(l for l in labels if local_models.find(l)["label"] == local_models.DEFAULT_MODEL)
        required["model"] = (labels, {"default": default, "tooltip": MODEL_TOOLTIP})
        optional = {k: v for k, v in spec["optional"].items() if k not in API_ONLY}
        max_side = optional["max_side"]
        optional["max_side"] = (max_side[0], dict(max_side[1], default=1024))
        optional.update(LOCAL_OPTIONS)
        optional["image_4"] = optional.pop("image_4")  # added in 1.2.0: after everything else
        return {"required": required, "optional": optional}

    @classmethod
    def VALIDATE_INPUTS(cls, preset, model, person_1=None, person_2=None, person_3=None,
                        person_4=None, style_1=None, style_2=None):
        # Like Prompt Writer · Grok API; the model list also changes (✓ once downloaded).
        return True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return GrokPromptForge.IS_CHANGED(**kwargs)

    def forge(self, preset, text, system_prompt, negative_prompt, model, temperature, top_p,
              max_tokens, seed=0, custom_system_prompt=None, image_1=None, image_2=None,
              image_3=None, trigger_word="", min_words=0, max_words=0, max_side=1024,
              fallback_to_input=True, image_n_is_person_n=False, archive=True, thinking=True,
              unload_after_run=True, context_length=32768, gpu_layers=-1, top_k=20,
              image_4=None, **slots):
        job = prepare(text, negative_prompt, system_prompt, custom_system_prompt, trigger_word,
                      (image_1, image_2, image_3, image_4), slots, image_n_is_person_n,
                      min_words, max_words, log=LOG)
        if job is None:
            return ("", negative_prompt or "")

        entry = local_models.find(model)
        try:
            if entry is None:
                raise RuntimeError(f"{LOG} unknown model '{model}' - pick one from the list.")
            model_path, mmproj_path = local_models.ensure_files(entry)
            with local_models.LOADED.lock:
                try:
                    llm, handler = local_models.LOADED.get(
                        model_path, mmproj_path, context_length, gpu_layers)
                    handler.extra_template_arguments["enable_thinking"] = bool(thinking)
                    messages = [{"role": "system", "content": job.system},
                                {"role": "user",
                                 "content": user_content(job.text, job.images, max_side, log=LOG)}]
                    response = llm.create_chat_completion(
                        messages=messages, temperature=float(temperature), top_p=float(top_p),
                        top_k=int(top_k), min_p=0.0, max_tokens=int(max_tokens),
                        seed=int(seed) % 2**31)
                finally:
                    if unload_after_run:
                        local_models.LOADED.unload()
            choice = response["choices"][0]
            result = local_models.split_thinking(
                (choice.get("message") or {}).get("content"), thinking, choice.get("finish_reason"))
            if not result:
                raise RuntimeError(f"{LOG} the model returned empty text.")
            usage = response.get("usage") or {}
            print(f"{LOG} OK ({entry['label']}, tokens={usage.get('total_tokens', '?')}).")
            log_counts(result, min_words, max_words, log=LOG)
        except Exception as e:
            if fallback_to_input:
                print(f"{e} - falling back to input text.")
                return (job.text, job.negative)
            raise
        if archive:
            archive_result(job, preset, entry["label"], result, temperature, top_p,
                           min_words, max_words, log=LOG)
        return (result, job.negative)
