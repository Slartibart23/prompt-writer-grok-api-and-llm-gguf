"""Prompt Writer · System Prompt Loader and Prompt Writer · Text File Loader."""

import os

from .api import find_comfy_root, pack_dir

CATEGORY = "Prompt Writer"


class GrokSystemPromptLoader:
    """Load a system prompt from a .txt file (absolute path, or relative to this
    node pack's system_prompts/ folder, or relative to the ComfyUI root)."""

    CATEGORY = CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt",)
    FUNCTION = "load"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_file": ("STRING", {
                    "default": "example_caption_refine.txt",
                    "tooltip":
                    "Name or path of a .txt file holding a system prompt. Bare "
                    "filenames are looked up in this node pack's system_prompts/ "
                    "folder, then in the ComfyUI root; absolute paths work too. "
                    "The node watches the file - edit and save it, and the next "
                    "run automatically uses the new content. Connect the output "
                    "to custom_system_prompt of a Prompt Writer node to override "
                    "its preset."}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, prompt_file):
        # Re-execute when the prompt file's content changes on disk
        try:
            for path in cls._candidate_paths(prompt_file):
                if os.path.isfile(path):
                    return os.path.getmtime(path)
        except Exception:
            pass
        return float("NaN")

    @staticmethod
    def _candidate_paths(prompt_file):
        p = prompt_file.strip()
        if os.path.isabs(p):
            return [p]
        return [os.path.join(pack_dir(), "system_prompts", p), os.path.join(find_comfy_root(), p)]

    def load(self, prompt_file):
        candidates = self._candidate_paths(prompt_file)
        for path in candidates:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    return (f.read(),)

        raise RuntimeError(
            f"[Prompt Writer · System Prompt Loader] File not found: {prompt_file} "
            f"(searched: {', '.join(candidates)})"
        )


class GrokTextFileLoader:
    """Sequentially load .txt files from any folder on any drive.

    Set the small control under `index` to "increment" and run the queue with a
    batch count equal to the number of files — each run loads the next file.
    Outputs the file's text plus its filename (without extension) so a save node
    can write the refined result under the same name.
    """

    CATEGORY = CATEGORY
    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("text", "filename", "file_path", "total_files")
    FUNCTION = "load"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "D:/captions", "tooltip":
                    "Folder to load text files from. Any drive, absolute path. "
                    "Files are sorted naturally (file2 before file10)."}),
                "index": ("INT", {
                    "default": 0, "min": 0, "max": 999999,
                    "control_after_generate": True, "tooltip":
                    "Which file to load (0 = first). Set the control below to "
                    "'increment' and queue a batch count equal to the number of "
                    "files - each run loads the next file automatically."}),
                "pattern": ("STRING", {"default": "*.txt", "tooltip":
                    "Filename filter, e.g. *.txt for all text files or "
                    "pose_*.txt for a specific subset."}),
                "include_subfolders": ("BOOLEAN", {"default": False, "tooltip":
                    "Also search all subfolders of folder_path."}),
                "loop_at_end": ("BOOLEAN", {"default": False, "tooltip":
                    "When the index passes the last file, wrap around to the "
                    "first instead of stopping with an error. Useful for "
                    "endless wildcard-style cycling through scene ideas."}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Folder contents can change between runs — never cache.
        return float("NaN")

    @staticmethod
    def _read_text(path):
        for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
            try:
                with open(path, "r", encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise RuntimeError(f"[Prompt Writer · Text File Loader] Could not decode: {path}")

    def load(self, folder_path, index, pattern="*.txt",
             include_subfolders=False, loop_at_end=False):
        import glob
        import re

        log = "[Prompt Writer · Text File Loader]"
        folder = folder_path.strip().strip('"')
        if not os.path.isdir(folder):
            raise RuntimeError(f"{log} Folder not found: {folder}")

        if include_subfolders:
            files = glob.glob(os.path.join(folder, "**", pattern), recursive=True)
        else:
            files = glob.glob(os.path.join(folder, pattern))

        def _natural_key(p):
            name = os.path.basename(p)
            return [int(t) if t.isdigit() else t.lower()
                    for t in re.split(r"(\d+)", name)]

        files = sorted((f for f in files if os.path.isfile(f)), key=_natural_key)

        total = len(files)
        if total == 0:
            raise RuntimeError(f"{log} No files matching '{pattern}' in: {folder}")

        if index >= total:
            if loop_at_end:
                index = index % total
            else:
                raise RuntimeError(
                    f"{log} Index {index} out of range — all {total} files processed. "
                    f"(Enable loop_at_end to wrap around, or reset index to 0.)"
                )

        path = files[index]
        text = self._read_text(path)
        stem = os.path.splitext(os.path.basename(path))[0]
        print(f"{log} {index + 1}/{total}: {os.path.basename(path)}")
        return (text, stem, path, total)
