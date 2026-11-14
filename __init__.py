"""Prompt Writer – Grok API & LLM GGUF: ComfyUI nodes that write prompts for image
and video models, with the xAI Grok API or a local uncensored Qwen3.8-27B (GGUF).

The node class IDs are the ones of comfyui-grok-prompt-forge, which this pack
replaces, so workflows saved with it load unchanged."""

from .grok_forge import models, routes
from .grok_forge.forge_node import GrokPromptForge
from .grok_forge.loader_nodes import GrokSystemPromptLoader, GrokTextFileLoader
from .grok_forge.local_node import LocalPromptForgeGGUF
from .grok_forge.persons_node import PromptWriterPersons
from .grok_forge.show_node import GrokShowPrompt
from .grok_forge.system_prompt_node import PromptWriterSystemPrompt

__version__ = "1.5.1"

NODE_CLASS_MAPPINGS = {
    "GrokPromptForge": GrokPromptForge,
    "LocalPromptForgeGGUF": LocalPromptForgeGGUF,
    "GrokShowPrompt": GrokShowPrompt,
    "PromptWriterPersons": PromptWriterPersons,
    "PromptWriterSystemPrompt": PromptWriterSystemPrompt,
    "GrokSystemPromptLoader": GrokSystemPromptLoader,
    "GrokTextFileLoader": GrokTextFileLoader,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GrokPromptForge": "Prompt Writer · Grok API",
    "LocalPromptForgeGGUF": "Prompt Writer · LLM GGUF",
    "GrokShowPrompt": "Prompt Writer · Show Prompt",
    "PromptWriterPersons": "Prompt Writer · Persons",
    "PromptWriterSystemPrompt": "Prompt Writer · System Prompt",
    "GrokSystemPromptLoader": "Prompt Writer · System Prompt Loader",
    "GrokTextFileLoader": "Prompt Writer · Text File Loader",
}

WEB_DIRECTORY = "./web"

routes.register()
models.start_background_refresh()

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
