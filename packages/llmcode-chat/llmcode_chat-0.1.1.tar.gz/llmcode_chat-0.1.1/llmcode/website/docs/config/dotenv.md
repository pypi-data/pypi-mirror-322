---
parent: Configuration
nav_order: 20
description: Using a .env file to store LLM API keys for llmcode.
---

# Config with .env

You can use a `.env` file to store API keys and other settings for the
models you use with llmcode.
You can also set many general llmcode options
in the `.env` file.

Llmcode will look for a `.env` file in these locations:

- Your home directory.
- The root of your git repo.
- The current directory.
- As specified with the `--env-file <filename>` parameter.

If the files above exist, they will be loaded in that order. Files loaded last will take priority.

{% include keys.md %}

## Sample .env file

Below is a sample `.env` file, which you
can also
[download from GitHub](https://github.com/khulnasoft/llmcode/blob/main/llmcode/website/assets/sample.env).

<!--[[[cog
from llmcode.args import get_sample_dotenv
from pathlib import Path
text=get_sample_dotenv()
Path("llmcode/website/assets/sample.env").write_text(text)
cog.outl("```")
cog.out(text)
cog.outl("```")
]]]-->
```
##########################################################
# Sample llmcode .env file.
# Place at the root of your git repo.
# Or use `llmcode --env <fname>` to specify.
##########################################################

#################
# LLM parameters:
#
# Include xxx_API_KEY parameters and other params needed for your LLMs.
# See https://llmcode.khulnasoft.com/docs/llms.html for details.

## OpenAI
#OPENAI_API_KEY=

## Anthropic
#ANTHROPIC_API_KEY=

##...

#############
# Main model:

## Specify the model to use for the main chat
#LLMCODE_MODEL=

## Use claude-3-opus-20240229 model for the main chat
#LLMCODE_OPUS=

## Use claude-3-5-sonnet-20241022 model for the main chat
#LLMCODE_SONNET=

## Use claude-3-5-haiku-20241022 model for the main chat
#LLMCODE_HAIKU=

## Use gpt-4-0613 model for the main chat
#LLMCODE_4=

## Use gpt-4o model for the main chat
#LLMCODE_4O=

## Use gpt-4o-mini model for the main chat
#LLMCODE_MINI=

## Use gpt-4-1106-preview model for the main chat
#LLMCODE_4_TURBO=

## Use gpt-3.5-turbo model for the main chat
#LLMCODE_35TURBO=

## Use deepseek/deepseek-chat model for the main chat
#LLMCODE_DEEPSEEK=

## Use o1-mini model for the main chat
#LLMCODE_O1_MINI=

## Use o1-preview model for the main chat
#LLMCODE_O1_PREVIEW=

########################
# API Keys and settings:

## Specify the OpenAI API key
#LLMCODE_OPENAI_API_KEY=

## Specify the Anthropic API key
#LLMCODE_ANTHROPIC_API_KEY=

## Specify the api base url
#LLMCODE_OPENAI_API_BASE=

## (deprecated, use --set-env OPENAI_API_TYPE=<value>)
#LLMCODE_OPENAI_API_TYPE=

## (deprecated, use --set-env OPENAI_API_VERSION=<value>)
#LLMCODE_OPENAI_API_VERSION=

## (deprecated, use --set-env OPENAI_API_DEPLOYMENT_ID=<value>)
#LLMCODE_OPENAI_API_DEPLOYMENT_ID=

## (deprecated, use --set-env OPENAI_ORGANIZATION=<value>)
#LLMCODE_OPENAI_ORGANIZATION_ID=

## Set an environment variable (to control API settings, can be used multiple times)
#LLMCODE_SET_ENV=

## Set an API key for a provider (eg: --api-key provider=<key> sets PROVIDER_API_KEY=<key>)
#LLMCODE_API_KEY=

#################
# Model settings:

## List known models which match the (partial) MODEL name
#LLMCODE_LIST_MODELS=

## Specify a file with llmcode model settings for unknown models
#LLMCODE_MODEL_SETTINGS_FILE=.llmcode.model.settings.yml

## Specify a file with context window and costs for unknown models
#LLMCODE_MODEL_METADATA_FILE=.llmcode.model.metadata.json

## Add a model alias (can be used multiple times)
#LLMCODE_ALIAS=

## Verify the SSL cert when connecting to models (default: True)
#LLMCODE_VERIFY_SSL=true

## Timeout in seconds for API calls (default: None)
#LLMCODE_TIMEOUT=

## Specify what edit format the LLM should use (default depends on model)
#LLMCODE_EDIT_FORMAT=

## Use architect edit format for the main chat
#LLMCODE_ARCHITECT=

## Specify the model to use for commit messages and chat history summarization (default depends on --model)
#LLMCODE_WEAK_MODEL=

## Specify the model to use for editor tasks (default depends on --model)
#LLMCODE_EDITOR_MODEL=

## Specify the edit format for the editor model (default: depends on editor model)
#LLMCODE_EDITOR_EDIT_FORMAT=

## Only work with models that have meta-data available (default: True)
#LLMCODE_SHOW_MODEL_WARNINGS=true

## Soft limit on tokens for chat history, after which summarization begins. If unspecified, defaults to the model's max_chat_history_tokens.
#LLMCODE_MAX_CHAT_HISTORY_TOKENS=

#################
# Cache settings:

## Enable caching of prompts (default: False)
#LLMCODE_CACHE_PROMPTS=false

## Number of times to ping at 5min intervals to keep prompt cache warm (default: 0)
#LLMCODE_CACHE_KEEPALIVE_PINGS=false

###################
# Repomap settings:

## Suggested number of tokens to use for repo map, use 0 to disable
#LLMCODE_MAP_TOKENS=

## Control how often the repo map is refreshed. Options: auto, always, files, manual (default: auto)
#LLMCODE_MAP_REFRESH=auto

## Multiplier for map tokens when no files are specified (default: 2)
#LLMCODE_MAP_MULTIPLIER_NO_FILES=true

################
# History Files:

## Specify the chat input history file (default: .llmcode.input.history)
#LLMCODE_INPUT_HISTORY_FILE=.llmcode.input.history

## Specify the chat history file (default: .llmcode.khulnasoft.com.history.md)
#LLMCODE_CHAT_HISTORY_FILE=.llmcode.khulnasoft.com.history.md

## Restore the previous chat history messages (default: False)
#LLMCODE_RESTORE_CHAT_HISTORY=false

## Log the conversation with the LLM to this file (for example, .llmcode.llm.history)
#LLMCODE_LLM_HISTORY_FILE=

##################
# Output settings:

## Use colors suitable for a dark terminal background (default: False)
#LLMCODE_DARK_MODE=false

## Use colors suitable for a light terminal background (default: False)
#LLMCODE_LIGHT_MODE=false

## Enable/disable pretty, colorized output (default: True)
#LLMCODE_PRETTY=true

## Enable/disable streaming responses (default: True)
#LLMCODE_STREAM=true

## Set the color for user input (default: #00cc00)
#LLMCODE_USER_INPUT_COLOR=#00cc00

## Set the color for tool output (default: None)
#LLMCODE_TOOL_OUTPUT_COLOR=

## Set the color for tool error messages (default: #FF2222)
#LLMCODE_TOOL_ERROR_COLOR=#FF2222

## Set the color for tool warning messages (default: #FFA500)
#LLMCODE_TOOL_WARNING_COLOR=#FFA500

## Set the color for assistant output (default: #0088ff)
#LLMCODE_ASSISTANT_OUTPUT_COLOR=#0088ff

## Set the color for the completion menu (default: terminal's default text color)
#LLMCODE_COMPLETION_MENU_COLOR=

## Set the background color for the completion menu (default: terminal's default background color)
#LLMCODE_COMPLETION_MENU_BG_COLOR=

## Set the color for the current item in the completion menu (default: terminal's default background color)
#LLMCODE_COMPLETION_MENU_CURRENT_COLOR=

## Set the background color for the current item in the completion menu (default: terminal's default text color)
#LLMCODE_COMPLETION_MENU_CURRENT_BG_COLOR=

## Set the markdown code theme (default: default, other options include monokai, solarized-dark, solarized-light, or a Pygments builtin style, see https://pygments.org/styles for available themes)
#LLMCODE_CODE_THEME=default

## Show diffs when committing changes (default: False)
#LLMCODE_SHOW_DIFFS=false

###############
# Git settings:

## Enable/disable looking for a git repo (default: True)
#LLMCODE_GIT=true

## Enable/disable adding .llmcode* to .gitignore (default: True)
#LLMCODE_GITIGNORE=true

## Specify the llmcode ignore file (default: .llmcodeignore in git root)
#LLMCODE_LLMCODEIGNORE=.llmcodeignore

## Only consider files in the current subtree of the git repository
#LLMCODE_SUBTREE_ONLY=false

## Enable/disable auto commit of LLM changes (default: True)
#LLMCODE_AUTO_COMMITS=true

## Enable/disable commits when repo is found dirty (default: True)
#LLMCODE_DIRTY_COMMITS=true

## Attribute llmcode code changes in the git author name (default: True)
#LLMCODE_ATTRIBUTE_AUTHOR=true

## Attribute llmcode commits in the git committer name (default: True)
#LLMCODE_ATTRIBUTE_COMMITTER=true

## Prefix commit messages with 'llmcode: ' if llmcode authored the changes (default: False)
#LLMCODE_ATTRIBUTE_COMMIT_MESSAGE_AUTHOR=false

## Prefix all commit messages with 'llmcode: ' (default: False)
#LLMCODE_ATTRIBUTE_COMMIT_MESSAGE_COMMITTER=false

## Commit all pending changes with a suitable commit message, then exit
#LLMCODE_COMMIT=false

## Specify a custom prompt for generating commit messages
#LLMCODE_COMMIT_PROMPT=

## Perform a dry run without modifying files (default: False)
#LLMCODE_DRY_RUN=false

## Skip the sanity check for the git repository (default: False)
#LLMCODE_SKIP_SANITY_CHECK_REPO=false

## Enable/disable watching files for ai coding comments (default: False)
#LLMCODE_WATCH_FILES=false

########################
# Fixing and committing:

## Lint and fix provided files, or dirty files if none provided
#LLMCODE_LINT=false

## Specify lint commands to run for different languages, eg: "python: flake8 --select=..." (can be used multiple times)
#LLMCODE_LINT_CMD=

## Enable/disable automatic linting after changes (default: True)
#LLMCODE_AUTO_LINT=true

## Specify command to run tests
#LLMCODE_TEST_CMD=

## Enable/disable automatic testing after changes (default: False)
#LLMCODE_AUTO_TEST=false

## Run tests, fix problems found and then exit
#LLMCODE_TEST=false

############
# Analytics:

## Enable/disable analytics for current session (default: random)
#LLMCODE_ANALYTICS=

## Specify a file to log analytics events
#LLMCODE_ANALYTICS_LOG=

## Permanently disable analytics
#LLMCODE_ANALYTICS_DISABLE=false

############
# Upgrading:

## Check for updates and return status in the exit code
#LLMCODE_JUST_CHECK_UPDATE=false

## Check for new llmcode versions on launch
#LLMCODE_CHECK_UPDATE=true

## Show release notes on first run of new version (default: None, ask user)
#LLMCODE_SHOW_RELEASE_NOTES=

## Install the latest version from the main branch
#LLMCODE_INSTALL_MAIN_BRANCH=false

## Upgrade llmcode to the latest version from PyPI
#LLMCODE_UPGRADE=false

########
# Modes:

## Specify a single message to send the LLM, process reply then exit (disables chat mode)
#LLMCODE_MESSAGE=

## Specify a file containing the message to send the LLM, process reply, then exit (disables chat mode)
#LLMCODE_MESSAGE_FILE=

## Run llmcode in your browser (default: False)
#LLMCODE_GUI=false

## Enable automatic copy/paste of chat between llmcode and web UI (default: False)
#LLMCODE_COPY_PASTE=false

## Apply the changes from the given file instead of running the chat (debug)
#LLMCODE_APPLY=

## Apply clipboard contents as edits using the main model's editor format
#LLMCODE_APPLY_CLIPBOARD_EDITS=false

## Do all startup activities then exit before accepting user input (debug)
#LLMCODE_EXIT=false

## Print the repo map and exit (debug)
#LLMCODE_SHOW_REPO_MAP=false

## Print the system prompts and exit (debug)
#LLMCODE_SHOW_PROMPTS=false

#################
# Voice settings:

## Audio format for voice recording (default: wav). webm and mp3 require ffmpeg
#LLMCODE_VOICE_FORMAT=wav

## Specify the language for voice using ISO 639-1 code (default: auto)
#LLMCODE_VOICE_LANGUAGE=en

## Specify the input device name for voice recording
#LLMCODE_VOICE_INPUT_DEVICE=

#################
# Other settings:

## specify a file to edit (can be used multiple times)
#LLMCODE_FILE=

## specify a read-only file (can be used multiple times)
#LLMCODE_READ=

## Use VI editing mode in the terminal (default: False)
#LLMCODE_VIM=false

## Specify the language to use in the chat (default: None, uses system settings)
#LLMCODE_CHAT_LANGUAGE=

## Always say yes to every confirmation
#LLMCODE_YES_ALWAYS=

## Enable verbose output
#LLMCODE_VERBOSE=false

## Load and execute /commands from a file on launch
#LLMCODE_LOAD=

## Specify the encoding for input and output (default: utf-8)
#LLMCODE_ENCODING=utf-8

## Line endings to use when writing files (default: platform)
#LLMCODE_LINE_ENDINGS=platform

## Specify the .env file to load (default: .env in git root)
#LLMCODE_ENV_FILE=.env

## Enable/disable suggesting shell commands (default: True)
#LLMCODE_SUGGEST_SHELL_COMMANDS=true

## Enable/disable fancy input with history and completion (default: True)
#LLMCODE_FANCY_INPUT=true

## Enable/disable multi-line input mode with Meta-Enter to submit (default: False)
#LLMCODE_MULTILINE=false

## Enable/disable detection and offering to add URLs to chat (default: True)
#LLMCODE_DETECT_URLS=true

## Specify which editor to use for the /editor command
#LLMCODE_EDITOR=
```
<!--[[[end]]]-->
