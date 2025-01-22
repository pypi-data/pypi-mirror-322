#!/bin/bash

docker run \
       -it --rm \
       --add-host=host.docker.internal:host-gateway \
       -v `pwd`:/llmcode \
       -v `pwd`/tmp.benchmarks/.:/benchmarks \
       -e OPENAI_API_KEY=$OPENAI_API_KEY \
       -e HISTFILE=/llmcode/.bash_history \
       -e PROMPT_COMMAND='history -a' \
       -e HISTCONTROL=ignoredups \
       -e HISTSIZE=10000 \
       -e HISTFILESIZE=20000 \
       -e LLMCODE_DOCKER=1 \
       -e LLMCODE_BENCHMARK_DIR=/benchmarks \
       llmcode-benchmark \
       bash
