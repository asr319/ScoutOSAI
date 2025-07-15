
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
 
