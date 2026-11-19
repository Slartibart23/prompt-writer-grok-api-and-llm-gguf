"""Prompt Writer · Persons: chooses up to six persons from your library outside
the writer nodes. Its `persons` output goes to the `persons` input of
Prompt Writer · Grok API / LLM GGUF, which then locks its own person_1..6."""

import json

from . import library
from .forge_node import PERSON_SLOTS, person_input, selected_persons

LOG = "[Prompt Writer · Persons]"


class PromptWriterPersons:
    CATEGORY = "Prompt Writer"
    RETURN_TYPES = ("PW_PERSONS",)
    RETURN_NAMES = ("persons",)
    OUTPUT_TOOLTIPS = ("Connect to the 'persons' input of Prompt Writer · Grok API or "
                       "LLM GGUF - one Persons node can feed several writer nodes.",)
    FUNCTION = "select"
    DESCRIPTION = ("Chooses up to six persons (or groups) from your library for one or more "
                   "Prompt Writer nodes. While it is connected, the writer's own person "
                   "fields are locked.")

    @classmethod
    def INPUT_TYPES(cls):
        names = library.names("person")
        return {"required": {
            f"person_{n}": person_input(names, n) for n in range(1, PERSON_SLOTS + 1)}}

    @classmethod
    def VALIDATE_INPUTS(cls, person_1=None, person_2=None, person_3=None, person_4=None,
                        person_5=None, person_6=None):
        # persons live in your own library: unknown names are skipped, not errors
        return True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # same name but an edited description must run again
        return json.dumps(selected_persons(kwargs, log=LOG), sort_keys=True)

    def select(self, **kwargs):
        return (selected_persons(kwargs, log=LOG),)
