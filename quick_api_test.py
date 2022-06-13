#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pprint as pp
import time

import openai

env_var = os.environ.get("GOOSE")
openai.api_key = env_var
openai.api_base = "https://api.goose.ai/v1"

# 'gpt-neo-20b'
if __name__ == "__main__":
    # List Engines (Models)
    engines = openai.Engine.list()
    # Print all engines IDs
    for engine in engines.data:
        pp.pprint(engine)

    # test the api
    # Create a completion, return results streaming as they are generated. Run with `python3 -u` to ensure unbuffered output.
    st = time.perf_counter()
    completion = openai.Completion.create(
        engine="gpt-j-6b",
        prompt="I was smiling to myself, thinking about the next time I would be able to visit the inner city bus stop and",
        max_tokens=160,
    )
    rt = time.perf_counter() - st
    # Print the first result

    maybe_a_bus = completion.choices[0].text
    print(f"response has type {type(maybe_a_bus)} and is:\n{maybe_a_bus}")
    print(f"response took {rt} seconds")
