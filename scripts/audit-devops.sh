#!/usr/bin/env bash
# Read-only audit of the DevOps checklist (docs/devops-checklist.md).
# Needs: gh (authenticated), jq. Usage: scripts/audit-devops.sh [owner/repo]
set -uo pipefail

REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
BRANCH="${BRANCH:-main}"
fail=0

pass() { printf '  \033[32mPASS\033[0m  %s\n' "$1"; }
bad()  { printf '  \033[31mFAIL\033[0m  %s\n' "$1"; fail=$((fail + 1)); }
skip() { printf '  \033[33mSKIP\033[0m  %s\n' "$1"; }
check() { if eval "$2" >/dev/null 2>&1; then pass "$1"; else bad "$1"; fi; }

echo "Auditing $REPO (branch: $BRANCH)"

echo; echo "1. Source control"
if ! prot=$(gh api "repos/$REPO/branches/$BRANCH/protection" 2>/dev/null); then
  bad "$BRANCH has branch protection"
else
  pass "$BRANCH has branch protection"
  check "pull request reviews required" "echo '$prot' | jq -e '.required_pull_request_reviews'"
  check "required status checks configured" "echo '$prot' | jq -e '.required_status_checks.contexts | length > 0'"
  check "force pushes blocked" "echo '$prot' | jq -e '.allow_force_pushes.enabled == false'"
  check "branch deletion blocked" "echo '$prot' | jq -e '.allow_deletions.enabled == false'"
fi

echo; echo "2. Secrets, variables and environments"
secrets=$(gh secret list -R "$REPO" 2>/dev/null | cut -f1)
vars=$(gh variable list -R "$REPO" 2>/dev/null | cut -f1)
for s in NETLIFY_AUTH_TOKEN NETLIFY_SITE_ID CODECOV_TOKEN; do
  check "secret $s is set" "echo '$secrets' | grep -qx $s"
done
check "variable VITE_API_URL is set" "echo '$vars' | grep -qx VITE_API_URL"
check "environment 'production' exists" "gh api repos/$REPO/environments/production"

echo; echo "3. Repository security features"
sec=$(gh api "repos/$REPO" --jq '.security_and_analysis' 2>/dev/null || echo null)
check "secret scanning enabled" "echo '$sec' | jq -e '.secret_scanning.status == \"enabled\"'"
check "push protection enabled" "echo '$sec' | jq -e '.secret_scanning_push_protection.status == \"enabled\"'"
check "Dependabot security updates enabled" "echo '$sec' | jq -e '.dependabot_security_updates.status == \"enabled\"'"
check "CodeQL default setup configured" "gh api repos/$REPO/code-scanning/default-setup --jq '.state == \"configured\"' | grep -q true"

echo; echo "4. Files in the repo"
for f in .github/dependabot.yml .github/workflows/pipeline-lint.yml .github/workflows/scorecard.yml \
         codecov.yml .pre-commit-config.yaml backend/.env.example frontend/.env.example; do
  check "$f exists" "test -f $f"
done
check "workflows set 'permissions:'" "! grep -L '^permissions:' .github/workflows/*.yml | grep -q ."
check "workflows set 'timeout-minutes'" "! grep -L 'timeout-minutes' .github/workflows/*.yml | grep -q ."
check "no unpinned third-party actions (uses: x@vN)" \
  "! grep -hE 'uses: [^ ]+@v[0-9]' .github/workflows/*.yml | grep -q ."

echo; echo "5. Latest CI results on $BRANCH"
runs=$(gh run list -R "$REPO" --branch "$BRANCH" --limit 20 --json workflowName,conclusion 2>/dev/null || echo '[]')
if [ "$runs" = "[]" ]; then
  skip "no workflow runs found on $BRANCH yet"
else
  for w in $(echo "$runs" | jq -r '.[].workflowName' | sort -u | tr ' ' '_'); do
    name=${w//_/ }
    c=$(echo "$runs" | jq -r --arg n "$name" '[.[] | select(.workflowName == $n)][0].conclusion')
    if [ "$c" = "success" ]; then pass "latest '$name' run succeeded"; else bad "latest '$name' run: $c"; fi
  done
fi

echo; echo "6. Quality tools (latest commit on $BRANCH)"
sha=$(gh api "repos/$REPO/commits/$BRANCH" --jq .sha 2>/dev/null || true)
checks=$(gh api "repos/$REPO/commits/$sha/check-runs" --jq '[.check_runs[].name]' 2>/dev/null || echo '[]')
statuses=$(gh api "repos/$REPO/commits/$sha/status" --jq '[.statuses[].context]' 2>/dev/null || echo '[]')
all=$(jq -n --argjson a "$checks" --argjson b "$statuses" '$a + $b')
check "Codacy reported on the latest commit" "echo '$all' | jq -e 'map(test(\"codacy\"; \"i\")) | any'"
check "Codecov reported on the latest commit" "echo '$all' | jq -e 'map(test(\"codecov\"; \"i\")) | any'"

echo; echo "Manual checks (cannot be read from GitHub):"
echo "  - Each clone ran 'pre-commit install' (gitleaks hook is local, not visible to GitHub)"
echo "  - Netlify: Git auto-build is OFF (Site configuration > Build & deploy)"
echo "  - Neon: backups / point-in-time restore on, app uses a non-owner role"
echo "  - FastAPI Cloud: DATABASE_URL and CORS_ORIGINS set; logs reviewable"
echo "  - Rollback tried once: Netlify previous deploy, FastAPI Cloud redeploy, Neon restore"

echo; if [ "$fail" -eq 0 ]; then echo "All automated checks passed."; else echo "$fail automated check(s) failed."; fi
exit $(( fail > 0 ))
