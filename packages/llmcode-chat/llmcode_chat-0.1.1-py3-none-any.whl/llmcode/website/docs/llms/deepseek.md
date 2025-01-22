---
parent: Connecting to LLMs
nav_order: 500
---

# DeepSeek

Llmcode can connect to the DeepSeek.com API.
The DeepSeek Coder V2 model has a top score on llmcode's code editing benchmark.

```
python -m pip install -U llmcode-chat

export DEEPSEEK_API_KEY=<key> # Mac/Linux
setx   DEEPSEEK_API_KEY <key> # Windows, restart shell after setx

# Use DeepSeek Coder V2
llmcode --deepseek
```

