"""HTTP routes used by web/grok_prompt_forge.js (all under /grok_prompt_forge/)."""

from . import archive, library, models, person_templates, presets, system_prompts

LOG = "[Prompt Writer]"


def register():
    try:
        from aiohttp import web
        from server import PromptServer
    except Exception as e:  # pragma: no cover
        print(f"{LOG} routes not registered: {e}")
        return

    srv = PromptServer.instance
    if getattr(srv, "_grok_forge_routes_registered", False):
        return
    srv._grok_forge_routes_registered = True
    no_store = {"Cache-Control": "no-store"}

    @srv.routes.get("/grok_prompt_forge/presets")
    async def grok_forge_presets(request):
        return web.json_response({"presets": presets.all_presets()}, headers=no_store)

    @srv.routes.post("/grok_prompt_forge/presets")
    async def grok_forge_save_preset(request):
        try:
            body = await request.json()
            preset = presets.save(body.get("name"), body.get("values") or {})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response({"preset": preset, "presets": presets.all_presets()})

    @srv.routes.post("/grok_prompt_forge/presets/delete")
    async def grok_forge_delete_preset(request):
        try:
            body = await request.json()
            removed = presets.delete(body.get("name") or "")
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response({"removed": removed, "presets": presets.all_presets()})

    # ---------------------------------------------------- persons and styles
    def library_payload():
        return {"library": library.load(), "persons": library.names("person"),
                "styles": library.names("style")}

    @srv.routes.get("/grok_prompt_forge/library")
    async def grok_forge_library(request):
        return web.json_response(library_payload(), headers=no_store)

    @srv.routes.post("/grok_prompt_forge/library")
    async def grok_forge_save_entry(request):
        try:
            body = await request.json()
            kind = body.get("kind")
            if kind not in library.KINDS:
                raise ValueError(f"Unknown kind: {kind}")
            name = library.save(kind, body.get("name"), body.get("values") or {},
                                body.get("old_name"))
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response(dict(library_payload(), name=name))

    @srv.routes.post("/grok_prompt_forge/library/delete")
    async def grok_forge_delete_entry(request):
        try:
            body = await request.json()
            kind = body.get("kind")
            if kind not in library.KINDS:
                raise ValueError(f"Unknown kind: {kind}")
            removed = library.delete(kind, body.get("name") or "")
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response(dict(library_payload(), removed=removed))

    @srv.routes.post("/grok_prompt_forge/library/import")
    async def grok_forge_import(request):
        try:
            body = await request.json()
            added, replaced, skipped = library.import_entries(
                body.get("data"), bool(body.get("overwrite")))
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response(dict(library_payload(), added=added, replaced=replaced,
                                      skipped=skipped))

    @srv.routes.post("/grok_prompt_forge/library/templates")
    async def grok_forge_templates(request):
        # adds the template persons; names you already have are never touched
        try:
            added, _, skipped = library.import_entries(person_templates.TEMPLATES, False)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response(dict(library_payload(), added=added, skipped=skipped))

    # --------------------------------------------------------- system prompts
    @srv.routes.get("/grok_prompt_forge/system_prompts")
    async def grok_forge_system_prompts(request):
        return web.json_response({"prompts": system_prompts.load()}, headers=no_store)

    @srv.routes.post("/grok_prompt_forge/system_prompts")
    async def grok_forge_save_system_prompt(request):
        try:
            body = await request.json()
            label = system_prompts.save(body.get("label"), body.get("text"))
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response({"label": label, "prompts": system_prompts.load()})

    @srv.routes.post("/grok_prompt_forge/system_prompts/delete")
    async def grok_forge_delete_system_prompt(request):
        try:
            body = await request.json()
            removed = system_prompts.delete(body.get("label") or "")
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response({"removed": removed, "prompts": system_prompts.load()})

    @srv.routes.get("/grok_prompt_forge/archive")
    async def grok_forge_archive(request):
        try:
            limit = min(int(request.query.get("limit", "200")), 2000)
        except ValueError:
            limit = 200
        return web.json_response({"entries": archive.entries(limit, request.query.get("q", ""))},
                                 headers=no_store)

    @srv.routes.get("/grok_prompt_forge/models")
    async def grok_forge_models(request):
        if request.query.get("refresh"):
            import asyncio
            try:
                await asyncio.get_running_loop().run_in_executor(None, models.refresh)
            except Exception as e:
                return web.json_response({"error": str(e), "models": models.model_list()},
                                         status=502)
        return web.json_response({"models": models.model_list()}, headers=no_store)
