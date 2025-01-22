import os
import subprocess
import sys

import uv


def install_llmcode():
    try:
        uv_bin = uv.find_uv_bin()
        subprocess.check_call(
            [
                uv_bin,
                "tool",
                "install",
                "--force",
                "--python",
                "python3.12",
                "llmcode-chat@latest",
            ]
        )
        subprocess.check_call([uv_bin, "tool", "update-shell"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install llmcode: {e}")
        sys.exit(1)


def main():
    install_llmcode()


if __name__ == "__main__":
    main()
