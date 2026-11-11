#!/usr/bin/env bash
# Start the compute (Rust) and the reader app (Next.js) together.
# Usage: scripts/dev.sh [--prod]   (--prod: next build + next start instead of next dev)
# Env: COMPUTE_LISTEN (default 127.0.0.1:7700), APP_PORT (default 3000).
# Ctrl-C stops both. Only the compute writes book files (format.md 1.2).
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
listen="${COMPUTE_LISTEN:-127.0.0.1:7700}"
port="${APP_PORT:-3000}"
cd "$root"
cargo build -q -p compute
./target/debug/compute --books "$root/books" --books "$root/kernel" --listen "$listen" &
cpid=$!
trap 'kill $cpid ${apid:-} 2>/dev/null || true; wait 2>/dev/null || true' EXIT INT TERM
for _ in $(seq 1 50); do curl -sf "http://$listen/health" >/dev/null && break; sleep 0.2; done
curl -sf "http://$listen/health" >/dev/null || { echo "compute did not start (see its report above)"; exit 1; }
cd "$root/app"
[ -d node_modules ] || npm install
export COMPUTE_URL="http://$listen"
if [ "${1:-}" = "--prod" ]; then
  npx next build && npx next start -p "$port" &
else
  npx next dev -p "$port" &
fi
apid=$!
echo "compute: http://$listen   reader: http://127.0.0.1:$port"
wait $apid
