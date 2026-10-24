"""Local GGUF models for Prompt Writer · LLM GGUF: catalog, download and the
loaded model.

Every catalog entry is one quantization of an uncensored Qwen3.8-27B with its
vision projector (mmproj). Both files are downloaded from Hugging Face on the
first run into ComfyUI/models/LLM_gguf/<repo name>/ and loaded with
llama-cpp-python (see docs/LOCAL_GGUF.md for installing it with CUDA)."""

import gc
import os
import re
import threading

LOG = "[Prompt Writer · LLM GGUF]"
DOWNLOADED = "✓ "  # prefix in the model list for files that are already on disk

_HUIHUI = ("huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF", "mmproj-model-bf16.gguf")
_HAUHAU = ("HauhauCS/Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-MTP-GGUF",
           "mmproj-Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-BF16.gguf")


def _entry(source, label, quant, filename, size_gb):
    repo, mmproj = source
    return {"label": f"{label} · {quant} · {size_gb:.1f} GB", "repo": repo, "file": filename,
            "mmproj": mmproj, "size_gb": size_gb}


# Sizes without the vision projector (another 0.9 GB per repo, downloaded once).
CATALOG = [
    _entry(_HUIHUI, "huihui Qwen3.8-27B abliterated", "Q4_K",
           "Huihui-Qwen3.8-27B-abliterated-Q4_K.gguf", 16.8),
    _entry(_HUIHUI, "huihui Qwen3.8-27B abliterated", "UD-Q4_K_XL",
           "Huihui-Qwen3.8-27B-abliterated-UD-Q4_K_XL.gguf", 17.4),
    _entry(_HUIHUI, "huihui Qwen3.8-27B abliterated", "Q5_K",
           "Huihui-Qwen3.8-27B-abliterated-Q5_K.gguf", 19.5),
    _entry(_HUIHUI, "huihui Qwen3.8-27B abliterated", "UD-IQ4_XS",
           "Huihui-Qwen3.8-27B-abliterated-UD-IQ4_XS.gguf", 14.4),
    _entry(_HUIHUI, "huihui Qwen3.8-27B abliterated", "UD-Q3_K_XL",
           "Huihui-Qwen3.8-27B-abliterated-UD-Q3_K_XL.gguf", 13.3),
    _entry(_HUIHUI, "huihui Qwen3.8-27B abliterated", "UD-IQ2_S",
           "Huihui-Qwen3.8-27B-abliterated-UD-IQ2_S.gguf", 8.4),
    _entry(_HAUHAU, "HauhauCS Qwen3.8-27B Aggressive", "Q4_K_P",
           "Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-Q4_K_P.gguf", 17.9),
    _entry(_HAUHAU, "HauhauCS Qwen3.8-27B Aggressive", "Q5_K_P",
           "Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-Q5_K_P.gguf", 20.2),
    _entry(_HAUHAU, "HauhauCS Qwen3.8-27B Aggressive", "IQ4_XS",
           "Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-IQ4_XS.gguf", 15.7),
    _entry(_HAUHAU, "HauhauCS Qwen3.8-27B Aggressive", "Q3_K_P",
           "Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-Q3_K_P.gguf", 13.4),
    _entry(_HAUHAU, "HauhauCS Qwen3.8-27B Aggressive", "IQ2_M",
           "Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-IQ2_M.gguf", 10.3),
]
DEFAULT_MODEL = CATALOG[0]["label"]


def models_root():
    try:
        import folder_paths
        base = folder_paths.models_dir
    except Exception:
        base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))), "models")
    return os.path.join(base, "LLM_gguf")


def entry_dir(entry):
    return os.path.join(models_root(), entry["repo"].split("/")[-1])


def is_downloaded(entry):
    d = entry_dir(entry)
    return all(os.path.isfile(os.path.join(d, f)) for f in (entry["file"], entry["mmproj"]))


def model_labels():
    """The model list, downloaded models marked with a check mark."""
    return [(DOWNLOADED if is_downloaded(e) else "") + e["label"] for e in CATALOG]


def find(label):
    label = (label or "").strip()
    if label.startswith(DOWNLOADED):
        label = label[len(DOWNLOADED):]
    return next((e for e in CATALOG if e["label"] == label), None)


def ensure_files(entry):
    """Download the model and its vision projector if they are missing.
    Returns (model path, mmproj path)."""
    d = entry_dir(entry)
    paths = []
    for name in (entry["mmproj"], entry["file"]):
        path = os.path.join(d, name)
        if not os.path.isfile(path):
            try:
                from huggingface_hub import hf_hub_download
            except ImportError as e:
                raise RuntimeError(f"{LOG} huggingface_hub is missing - install it with "
                                   "'python -m pip install huggingface_hub'.") from e
            os.makedirs(d, exist_ok=True)
            print(f"{LOG} downloading {entry['repo']}/{name} to {d} - this happens only once.")
            path = hf_hub_download(entry["repo"], name, local_dir=d)
        paths.append(path)
    mmproj, model = paths
    return model, mmproj


def split_thinking(content, thinking, finish_reason):
    """Return the answer without the model's <think> reasoning."""
    text = content or ""
    if "</think>" in text:
        return text.rsplit("</think>", 1)[1].strip()
    if thinking:
        if finish_reason == "length":
            raise RuntimeError(f"{LOG} max_tokens was used up while the model was still "
                               "thinking. Raise max_tokens (and context_length), or turn "
                               "thinking off.")
        # the chat template opens <think> itself; a reply without </think> is the answer
    return re.sub(r"^\s*<think>\s*", "", text).strip()


class LoadedModel:
    """One model kept in VRAM between runs (until unloaded)."""

    def __init__(self):
        self.lock = threading.Lock()
        self.key = None
        self.llm = None
        self.handler = None

    def get(self, model_path, mmproj_path, context_length, gpu_layers):
        key = (model_path, mmproj_path, int(context_length), int(gpu_layers))
        if self.llm is not None and self.key == key:
            return self.llm, self.handler
        self.unload()
        try:
            from llama_cpp import Llama
            from llama_cpp.llama_chat_format import Qwen35ChatHandler
        except ImportError as e:
            raise RuntimeError(
                f"{LOG} llama-cpp-python is not installed (or not with CUDA). See "
                "docs/LOCAL_GGUF.md in this node pack for the step-by-step installation.") from e
        _free_comfy_vram()
        print(f"{LOG} loading {os.path.basename(model_path)} (+ vision projector) ...")
        handler = Qwen35ChatHandler(mmproj_path=mmproj_path, verbose=False)
        layers = "auto" if int(gpu_layers) < 0 else int(gpu_layers)
        llm = Llama(model_path=model_path, n_gpu_layers=layers, n_ctx=int(context_length),
                    chat_handler=handler, verbose=False)
        self.llm, self.handler, self.key = llm, handler, key
        return llm, handler

    def unload(self):
        if self.llm is None:
            return
        for obj in (self.llm, self.handler):
            try:
                obj.close()
            except Exception:
                pass
        self.llm = self.handler = self.key = None
        gc.collect()
        print(f"{LOG} model unloaded from VRAM.")


def _free_comfy_vram():
    """Make room: ask ComfyUI to move its own models out of VRAM first."""
    try:
        import comfy.model_management as mm
        mm.unload_all_models()
        mm.soft_empty_cache()
    except Exception:
        pass


LOADED = LoadedModel()
