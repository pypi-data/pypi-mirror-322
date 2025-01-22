To use llmcode with pipx on replit, you can run these commands in the replit shell:

```bash
pip install pipx
pipx run llmcode-chat ...normal llmcode args...
```

If you install llmcode with pipx on replit and try and run it as just `llmcode` it will crash with a missing `libstdc++.so.6` library.

