bekonos_codex_onboarding:
  last_updated: "2025-07-14"
  project: "bekonOS"
  instructions: |
    ## bekonOS 1-Click Project Setup (Codex)

    **Warning:**  
    - Never paste your GitHub token or secret into ChatGPT or any public chat.  
    - Always use environment variables or secure secrets.

    ### What Codex Will Do:
    1. Prompt you to **set your GitHub Personal Access Token** in your local terminal:
        ```
        export GITHUB_TOKEN=your_token_here
        ```
    2. Download and run the one-click setup script below.
    3. The script will:
        - Rename your repository to `bekonOS`
        - Update GitHub Pages config to serve from `gh-pages` branch and `/docs` folder
        - Set all repository-level variables for bekonOS brand colors and config

    ---
    ### 1-Click Codex Script (Save as `codex-setup.sh` and run locally)

    ```bash
    #!/bin/bash
    # bekonOS Codex 1-Click Repo Setup & Branding Script
    # Usage: export GITHUB_TOKEN=your_token_here; ./codex-setup.sh

    set -e

    GITHUB_USER=“asr319”.                     # <-- CHANGE THIS
    OLD_REPO="ScoutOSAI"                    # <-- CHANGE THIS if needed
    NEW_REPO="bekonOS"

    if [[ -z "$GITHUB_TOKEN" ]]; then
      echo "Error: Please set GITHUB_TOKEN environment variable before running this script."
      echo "Usage: export GITHUB_TOKEN=your_token_here"
      exit 1
    fi

    echo "=== [bekonOS] Codex 1-Click Repo Automation ==="

    # 1. Rename repository (if necessary)
    echo "--- Renaming repo (if required) ---"
    curl -s -X PATCH \
      -H "Authorization: token $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      https://api.github.com/repos/$GITHUB_USER/$OLD_REPO \
      -d "{\"name\":\"$NEW_REPO\"}" | grep -q "\"name\":\"$NEW_REPO\"" && echo "Repo renamed." || echo "Repo already correct or error."

    # 2. Update GitHub Pages source to gh-pages /docs
    echo "--- Updating GitHub Pages source ---"
    curl -s -X PUT \
      -H "Authorization: token $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github.switcheroo-preview+json" \
      https://api.github.com/repos/$GITHUB_USER/$NEW_REPO/pages \
      -d '{"source":{"branch":"gh-pages","path":"/docs"}}' > /dev/null && echo "GitHub Pages source updated."

    # 3. Set repository-level variables
    echo "--- Setting GitHub Actions variables ---"
    declare -A vars
    vars=(
      ["BRAND"]="bekonOS"
      ["PRIMARY_COLOR"]="#20467A"
      ["ACCENT_COLOR"]="#5376A6"
      ["GRAPHITE"]="#2D3137"
      ["YELLOW"]="#FFD94A"
      ["AQUA"]="#60C6C9"
      ["BG_COLOR"]="#F6F8FA"
    )

    for key in "${!vars[@]}"; do
      curl -s -X PUT \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github+json" \
        https://api.github.com/repos/$GITHUB_USER/$NEW_REPO/actions/variables/$key \
        -d "{\"name\":\"$key\",\"value\":\"${vars[$key]}\"}" > /dev/null
      echo "Set repo variable: $key"
    done

    echo "=== bekonOS Repo, Pages, and Actions variables are updated! ==="
    echo "Done! (If you just renamed the repo, update your remotes and verify your Pages build at:"
    echo "https://$GITHUB_USER.github.io/$NEW_REPO/ )"
    ```

    ---

    ### How to use this Codex onboarding:

    1. Open your local terminal.
    2. Run:
        ```
        export GITHUB_TOKEN=your_token_here
        ```
    3. Save the above script as `codex-setup.sh` in your repo root.
    4. Run:
        ```
        chmod +x codex-setup.sh
        ./codex-setup.sh
        ```
    5. All repo branding, variables, and Pages setup will be done automatically.

    ---
    **For security:** Never store your token in the repo, in code, or paste it into public tools.
    For more info on GitHub API auth, see: https://docs.github.com/en/rest
