#!/usr/bin/env bash
# verify_deploy.sh — loop deploy-verify pentru zerohypelab.com (replicat din aponia, S124).
# 6 părți (Loop Engineering): trigger=manual post-deploy · context=DESIGN.md · unelte=curl
#   · verifier=script(nivel 1) · state=log pe disc
#
# DEPLOY: GitHub Pages (CNAME zerohypelab.com) — git push → auto-deploy (~1-2 min propagare).
# IZOLARE: zero referință Adrian/mindit; git identity local = anonim (vezi memoria zerohype).
# Rulează din repo root (html-ul e la root, SITE=".").
# Usage:  ./verify_deploy.sh [--pre|--live]
# Exit:  0 = verde · 1 = FAIL · 2 = INCONCLUSIV live

set -u
cd "$(dirname "$0")"
SITE="."
HOST="zerohypelab.com"
LOG="verify_deploy.log"
KEY_PAGES=(index.html about.html bullshit-detector/index.html guides/index.html)
mode="${1:-all}"
ts() { date "+%Y-%m-%d %H:%M:%S"; }
log() { echo "$1" | tee -a "$LOG"; }

log ""
log "===== verify_deploy $(ts) (mode=$mode) ====="
fail=0; inconcl=0

# ---------- PRE (local) ----------
if [ "$mode" = "all" ] || [ "$mode" = "--pre" ]; then
  log "--- PRE (local) ---"
  if git ls-files 2>/dev/null | grep -qi "\.DS_Store"; then
    log "  ❌ .DS_Store TRACKED în git — va fi publicat la push. git rm --cached + .gitignore"; fail=1
  else
    log "  ✅ .DS_Store untracked"
  fi
  # izolare guard — niciun nume real în paginile publice
  if grep -rIl -e "Peticila" -e "mindit" "${KEY_PAGES[@]}" 2>/dev/null | grep -q .; then
    log "  ❌ IZOLARE: nume real (Peticila/mindit) într-o pagină publică ZeroHype"; fail=1
  else
    log "  ✅ izolare: niciun nume real în paginile cheie"
  fi
  for p in "${KEY_PAGES[@]}"; do
    n=$( { grep -o "application/ld+json" "$SITE/$p" 2>/dev/null || true; } | wc -l | tr -d ' ')
    if [ "$n" -ge 1 ]; then log "  ✅ schema: $p"; else log "  ⚠️  schema LIPSĂ: $p"; fi
  done
fi

# ---------- LIVE (post-deploy) ----------
if [ "$mode" = "all" ] || [ "$mode" = "--live" ]; then
  log "--- LIVE ($HOST) ---"
  for p in "${KEY_PAGES[@]}"; do
    url="https://$HOST/${p%index.html}"
    code=$(curl -s -o /tmp/zh_body.$$ -w '%{http_code}' --max-time 12 "$url" 2>/dev/null)
    bytes=$(wc -c < /tmp/zh_body.$$ 2>/dev/null | tr -d ' '); rm -f /tmp/zh_body.$$
    if [ "$code" = "000" ]; then
      log "  ⚠️  $url → fără conexiune (LuLu/DNS/offline) — verifică din browser preview"; inconcl=1
    elif [ "$code" = "200" ] && [ "${bytes:-0}" -gt 1000 ]; then
      log "  ✅ $url → 200, ${bytes}b"
    else
      log "  ❌ $url → HTTP $code, ${bytes}b (gol/eroare)"; fail=1
    fi
  done
  ds=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "https://$HOST/.DS_Store" 2>/dev/null)
  if [ "$ds" = "200" ]; then log "  ❌ /.DS_Store EXPUS (HTTP 200)"; fail=1
  else log "  ✅ /.DS_Store → $ds"; fi
fi

# ---------- verdict ----------
log "--- VERDICT ---"
[ "$fail" -eq 1 ] && { log "  FAIL: check critic picat. NU declara done."; exit 1; }
[ "$inconcl" -eq 1 ] && { log "  INCONCLUSIV: curl live blocat. Confirmă prin browser preview."; exit 2; }
log "  OK: deploy-verify verde."
exit 0
