"""
Define a class "PromptEngine" that takes an input string and returns a prompt string
that goes into the language model. We operate in string space, not token space.
This is a base class that can be subclassed to provide different prompt engines.

Subclasses should override both __init__ and get_prompt.
Possible subclasses:
- PromptEngine: the default, which just returns the input string
- PromptEnginePrefixSuffix: adds a prefix and suffix to the input string
- PromptEngineJSON: returns a JSON string with the input string as a field and ending with '"output": "'
"""

import re
import sys

class PromptEngine:
    """
    A base class for prompt engines. Subclasses should override both __init__ and get_prompt.
    """
    def __init__(self, args, **kwargs):
        pass

    def get_prompt(self, input_string):
        return input_string

class PromptEnginePrefixSuffix(PromptEngine):
    """
    A prompt engine that adds a prefix and suffix to the input string.
    """
    def __init__(self, prefix, suffix, **kwargs):
        self.prefix = prefix
        self.suffix = suffix

    def get_prompt(self, input_string):
        return self.prefix + input_string + self.suffix

class PromptEngineJSON(PromptEngine):
    """
    A prompt engine that returns a JSON string with the input string as a field and ending with '"output": "'
    """
    def __init__(self, **kwargs):
        pass

    def get_prompt(self, input_string):
        return '{{"input": "{}", "output": "'.format(input_string)
