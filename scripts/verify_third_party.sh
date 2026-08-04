#!/bin/sh
set -eu

upstream_url=https://github.com/AlexKontorovich/PrimeNumberTheoremAnd.git
upstream_commit=0c7abf7be7765dc5ffd21afc1c37b018199ec3c9
repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
temp_root=${RUNNER_TEMP:-${TMPDIR:-"$repo_root/.audit-tmp"}}
mkdir -p "$temp_root"
checkout=$(mktemp -d "$temp_root/degree-diameter-third-party.XXXXXXXXXX")

cleanup() {
  rm -rf -- "$checkout"
}
trap cleanup EXIT HUP INT TERM

git -C "$checkout" init -q
git -C "$checkout" remote add origin "$upstream_url"
git -C "$checkout" fetch -q --depth 1 origin "$upstream_commit"
git -C "$checkout" checkout -q --detach FETCH_HEAD

python3 "$repo_root/scripts/verify_third_party.py" \
  "$repo_root" "$checkout" --show-diff
