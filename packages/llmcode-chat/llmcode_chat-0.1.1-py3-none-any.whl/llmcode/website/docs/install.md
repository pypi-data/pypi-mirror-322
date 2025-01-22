---
title: Installation
has_children: true
nav_order: 20
description: How to install and get started pair programming with llmcode.
---

# Installation
{: .no_toc }


## Get started quickly with llmcode-install

{% include get-started.md %}

This will install llmcode in its own separate python environment.
If needed, 
llmcode-install will also install a separate version of python 3.12 to use with llmcode.

Once llmcode is installed,
there are also some [optional install steps](/docs/install/optional.html).

See the [usage instructions](https://llmcode.khulnasoft.com/docs/usage.html) to start coding with llmcode.

## One-liners

These one-liners will install llmcode, along with python 3.12 if needed.
They are based on the 
[uv installers](https://docs.astral.sh/uv/getting-started/installation/).

#### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://llmcode.khulnasoft.com/install.ps1 | iex"
```

#### Mac & Linux

Use curl to download the script and execute it with sh:

```bash
curl -LsSf https://llmcode.khulnasoft.com/install.sh | sh
```

If your system doesn't have curl, you can use wget:

```bash
wget -qO- https://llmcode.khulnasoft.com/install.sh | sh
```


## Install with uv

You can install llmcode with uv:

```bash
python -m pip install uv  # If you need to install uv
uv tool install --force --python python3.12 llmcode-chat@latest
```

This will install uv using your existing python version 3.8-3.13,
and use it to install llmcode.
If needed, 
uv will automatically install a separate python 3.12 to use with llmcode.

Also see the
[docs on other methods for installing uv itself](https://docs.astral.sh/uv/getting-started/installation/).

## Install with pipx

You can install llmcode with pipx:

```bash
python -m pip install pipx  # If you need to install pipx
pipx install llmcode-chat
```

You can use pipx to install llmcode with python versions 3.9-3.12.

Also see the
[docs on other methods for installing pipx itself](https://pipx.pypa.io/stable/installation/).

## Other install methods

You can install llmcode with the methods described below, but one of the above
methods is usually safer.

#### Install with pip

If you install with pip, you should consider
using a 
[virtual environment](https://docs.python.org/3/library/venv.html)
to keep llmcode's dependencies separated.


You can use pip to install llmcode with python versions 3.9-3.12.

```bash
# Install llmcode
python -m pip install -U --upgrade-strategy only-if-needed llmcode-chat

# To work with GPT-4o:
llmcode --4o --openai-api-key sk-xxx...

# To work with Claude 3.5 Sonnet:
llmcode --sonnet --anthropic-api-key sk-xxx...
```

{% include python-m-llmcode.md %}

#### Installing with package managers

It's best to install llmcode using one of methods
recommended above.
While llmcode is available in a number of system package managers,
they often install llmcode with incorrect dependencies.

## Next steps...

There are some [optional install steps](/docs/install/optional.html) you could consider.
See the [usage instructions](https://llmcode.khulnasoft.com/docs/usage.html) to start coding with llmcode.

