# Prompt Writer · LLM GGUF — installation and GPU guide

**Prompt Writer · LLM GGUF** does what Prompt Writer · Grok API does, with an uncensored **Qwen3.8-27B** running on your own NVIDIA GPU instead of the xAI API.

- It uses the same presets, persons, style blocks, archive and language switch.
- It needs no API key and costs nothing per prompt. After the one-time download it works completely offline.
- It understands images: every model comes with its vision projector (`mmproj`), which is always downloaded and loaded with it.

It needs one extra Python package: **llama-cpp-python with CUDA**. This guide installs it into ComfyUI Portable step by step and helps you pick the right model for your graphics card.

---

## 1. What you need

| | Minimum | Recommended |
|---|---|---|
| GPU | NVIDIA with **12 GB** VRAM | 24–32 GB VRAM |
| NVIDIA driver | recent enough for the CUDA build you install (see step 3) | latest Game Ready / Studio driver |
| System RAM | 16 GB | 32 GB or more |
| Free disk space | 9 GB (smallest model) | 20–25 GB per model |
| Python | the one in ComfyUI Portable (`python_embeded`), 3.10–3.14 | — |

You do **not** need the CUDA Toolkit or Visual Studio: the prebuilt packages below bring their own CUDA libraries.

AMD and Intel GPUs and Apple Silicon are not covered by this guide. llama.cpp supports them, but the packages are different.

---

## 2. Check what is already there

Open a command prompt **in your ComfyUI Portable folder** (the one containing `python_embeded` and `run_nvidia_gpu.bat`) and run:

```
python_embeded\python.exe -m pip show llama-cpp-python
```

- `WARNING: Package(s) not found` means you need to install it (step 3).
- A version is shown, e.g. `Version: 0.4.3+cu130`. The `+cuXXX` part means a CUDA build.
  - The node was tested with **0.4.0+cu130**. Versions from 0.4.0 on know Qwen3.8; older ones fail with `unknown model architecture: 'qwen35'`.
  - If the version has no `+cu…` part, it is a CPU-only build: install the CUDA build as in step 3.

Find out which CUDA version your driver supports:

```
nvidia-smi
```

The header shows `CUDA Version: 13.x` (or `12.x`). That is the **highest** CUDA build your driver can run.

---

## 3. Install llama-cpp-python with CUDA

The official PyPI package has no CUDA builds for Windows. The maintained builds with Qwen3.8 support come from **JamePeng/llama-cpp-python**: <https://github.com/JamePeng/llama-cpp-python/releases>

### 3.1 Pick the right file

Each release offers files named like this:

```
llama_cpp_python-0.4.3+cu130-cp312-cp312-win_amd64.whl
                   ^^^^^  ^^^^^
                   CUDA   Python version
```

**CUDA build:** it must not be higher than the `CUDA Version` shown by `nvidia-smi`.

| Your GPU | Use | Driver needs to show at least |
|---|---|---|
| RTX 50 series (5060 Ti … 5090) | `cu130` (or `cu128`) | CUDA 13.0 (12.8) |
| RTX 40 / 30 / 20 series | `cu128`, `cu126` or `cu124` | CUDA 12.8 / 12.6 / 12.4 |

RTX 50 cards **need** a CUDA 12.8 build or newer. Older builds fail with `no kernel image is available for execution on the device`.

**Python version:** `cp312` = Python 3.12, `cp313` = 3.13, and so on. Check yours with:

```
python_embeded\python.exe --version
```

Take the release tag ending in `-win-…`, open *Assets* and download the matching `.whl`.

### 3.2 Install it — with `--no-deps`

From the ComfyUI Portable folder, with the downloaded file in it:

```
python_embeded\python.exe -m pip install --no-deps llama_cpp_python-0.4.3+cu130-cp312-cp312-win_amd64.whl
python_embeded\python.exe -m pip install diskcache jinja2 huggingface_hub
```

**Why `--no-deps`:** llama-cpp-python declares an upper limit for `numpy` that is older than what current ComfyUI uses. Without `--no-deps`, pip would **downgrade numpy** and can break ComfyUI and other node packs. llama-cpp-python works fine with the newer numpy. The second line adds the few small packages it really needs; they are usually there already.

Restart ComfyUI afterwards.

### 3.3 Check that the GPU is used

1. Add **Prompt Writer · LLM GGUF** and run it once.
2. While it runs, watch the GPU in Task Manager (*Performance → GPU → Dedicated GPU memory*) or with `nvidia-smi`. VRAM use jumps by roughly the model size.

**Speed** is the clearest sign:

| Measured on an RTX 5090, Q4_K | Result |
|---|---|
| Generation | about 60 tokens/s |
| "Idea ▸ FLUX" incl. loading the model | about 20 s |
| "Idea ▸ Qwen-Image 2.1" (≈ 500 words) | about 45 s |

If one prompt takes several minutes, llama.cpp is running on the CPU: see Troubleshooting.

> `llama_cpp.llama_supports_gpu_offload()` can report `False` even with a working CUDA build, because the CUDA backend is loaded only when a model loads. Don't use it as a test.

---

## 4. Choose a model for your graphics card

The model list in the node shows every model with its file size. **✓** means it is already downloaded.

- **huihui (abliterated):** the refusals were removed directly from the weights. It is close to the original Qwen3.8.
- **HauhauCS (Aggressive):** uncensored by fine-tuning. It answers directly, with no preamble.

Both are Qwen3.8-27B with vision. The vision projector adds 0.9 GB on disk and about 1 GB VRAM.

**Rule of thumb:** model file + vision projector + context + about 1 GB overhead must fit into your **free** VRAM. Windows and other programs use some VRAM too (0.5–2 GB), so check `nvidia-smi` with ComfyUI idle.

| VRAM | Typical cards | Model (file size) | `context_length` | `max_tokens` |
|---|---|---|---|---|
| **12 GB** | RTX 3060 12GB, 4070, 5070 | huihui **UD-IQ2_S** (8.4 GB); HauhauCS **IQ2_M** (10.3 GB) is very tight | 8192 | 4096 |
| **16 GB** | RTX 4060 Ti 16GB, 4070 Ti Super, 4080, 5060 Ti 16GB, 5070 Ti, 5080 | huihui **UD-Q3_K_XL** (13.3 GB) or HauhauCS **Q3_K_P** (13.4 GB) | 8192–16384 | 4096–6144 |
| **24 GB** | RTX 3090, 4090 | huihui **Q4_K** (16.8 GB) / **UD-Q4_K_XL** (17.4 GB) or HauhauCS **Q4_K_P** (17.9 GB) | 16384–32768 | 8192 |
| **32 GB** | RTX 5090 | huihui **Q5_K** (19.5 GB) or HauhauCS **Q5_K_P** (20.2 GB); Q4 if you want room for more | 32768 | 8192+ |

Tips for 12–16 GB cards:

- **Quality:** the 2-bit models (IQ2) work, but write noticeably simpler prompts and follow long formats (MiniMax H3, Qwen-Image 2.1's 450 words) less reliably. Q3 is the sensible minimum for good results.
- **Thinking:** turn `thinking` off if prompts get cut off. Thinking needs room in `context_length` and `max_tokens`.
- **Partial offload:** `gpu_layers` = -1 (automatic) lets llama.cpp put as many layers on the GPU as fit and the rest in system RAM. That runs, but much slower.
  - You can also set a number yourself. Qwen3.8-27B has 65 layers; for example, try 50 on a 12 GB card with a Q3 model.
- **Images:** they cost context. Keep `max_side` at 1024 or lower, and use fewer reference images.
- **VRAM sharing:** keep `unload_after_run` **on**. The node then frees the VRAM after each run, so your image or video model can load afterwards. Before loading, the node also asks ComfyUI to unload its own models.

**24–32 GB cards:**

- Turning `unload_after_run` off keeps the model loaded, so the next prompt starts at once.
- Only do this if your image or video model fits into the VRAM that is left. Otherwise ComfyUI has to offload it, and that is slower than reloading the LLM.

---

## 5. Where the files go

On the first run of a model, the node downloads two files from Hugging Face:

```
ComfyUI/models/LLM_gguf/Huihui-Qwen3.8-27B-abliterated-GGUF/
    Huihui-Qwen3.8-27B-abliterated-Q4_K.gguf
    mmproj-model-bf16.gguf
ComfyUI/models/LLM_gguf/Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-MTP-GGUF/
    Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-Q4_K_P.gguf
    mmproj-Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-BF16.gguf
```

- **Progress:** the ComfyUI console shows the download progress. The first run takes a while: 17 GB took about 2.5 minutes on a fast connection.
- **Downloading by hand:** if you prefer, get the files from the model pages and put them into exactly these folders with exactly these names. The node then finds them and shows **✓**.
  - <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF>
  - <https://huggingface.co/HauhauCS/Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-MTP-GGUF>
- **One projector per repository:** the vision projector is shared by all quantizations of the same repository and is downloaded only once.

---

## 6. Troubleshooting

| Message / symptom | Cause | Fix |
|---|---|---|
| `llama-cpp-python is not installed (or not with CUDA)` | package missing | Step 3 |
| `unknown model architecture: 'qwen35'` | llama-cpp-python older than 0.4.0 | install a current build (step 3) |
| `no kernel image is available for execution on the device` | CUDA build too old for your GPU (RTX 50 needs ≥ cu128) | install cu128/cu130 |
| `DLL load failed` / `could not find module ...ggml-cuda.dll` | CUDA build newer than your driver supports | update the NVIDIA driver, or take a lower `cuXXX` build |
| ComfyUI breaks after installing, numpy errors | pip downgraded numpy | `python_embeded\python.exe -m pip install --upgrade numpy`, then reinstall llama-cpp-python with `--no-deps` |
| Very slow (minutes per prompt) | runs on the CPU: CPU-only build, or `gpu_layers` = 0 | check `pip show` for `+cuXXX`; set `gpu_layers` to -1 |
| `CUDA error: out of memory` / crash while loading | model + context don't fit | smaller quantization, lower `context_length`, `unload_after_run` on, close other GPU programs |
| `max_tokens was used up while the model was still thinking` | thinking ran out of room | raise `max_tokens` (and `context_length`), or turn `thinking` off |
| `Requested tokens (…) exceed context window` | the input alone (system prompt + images) is larger than `context_length` | raise `context_length`, lower `max_side`, use fewer images |
| Answers stop mid-sentence | `max_tokens` was shortened to what fits after the input | raise `context_length` |
| Output contains a short warning or disclaimer | rare with abliterated models | try the HauhauCS model, or add "no warnings" to your text |

---

## 7. Good to know

- **Quality:** a 27B model on your own GPU writes good prompts for most presets. On very long, strictly formatted tasks (MiniMax H3 REF2VA) Grok is still clearly stronger.
- **Examples:** every preset contains an example of a good result. Local models follow it far more closely than written rules alone.
- **Settings:** `temperature` and `top_p` come from the preset, just like on the Grok API node. `top_k` = 20 follows Qwen's recommendation. With `seed` set to *fixed*, the same input gives the same output.
- **Privacy:** after the download nothing leaves your computer. Persons, style blocks and the archive are shared with the Grok API node and stay in `ComfyUI/user/grok_prompt_forge/`.
- **Speed boost not included:** HauhauCS's "FastMTP" speed-up needs a patched llama.cpp and is not used here. Its models still work, at normal speed.
