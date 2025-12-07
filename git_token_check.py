import os
import sys

TOKEN_NAME = "GITHUB_TOKEN"

token = os.getenv(TOKEN_NAME)

if not token:
    print(
        "❌ No GitHub token found.\n\n"
        "Please set the GITHUB_TOKEN environment variable.\n\n"
        "Examples:\n"
        "  PowerShell:\n"
        "    $env:GITHUB_TOKEN=\"your_token_here\"\n\n"
        "  Bash:\n"
        "    export GITHUB_TOKEN=\"your_token_here\"\n"
    )
    sys.exit(1)

print("✅ GitHub token found.")
