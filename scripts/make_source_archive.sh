#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "usage: make_source_archive.sh /ABSOLUTE/OUTPUT.zip" >&2
  exit 2
fi

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
archive=$1

case "$archive" in
  /*) ;;
  *)
    echo "archive output path must be absolute: $archive" >&2
    exit 1
    ;;
esac

if [ -e "$archive" ] || [ -e "$archive.sha256" ]; then
  echo "refusing to overwrite an existing archive or hash file: $archive" >&2
  exit 1
fi

git -C "$repo_root" diff --quiet
git -C "$repo_root" diff --cached --quiet
commit=$(git -C "$repo_root" rev-parse --verify HEAD)

git -C "$repo_root" archive \
  --format=zip \
  --prefix="AsymptoticallyAttainingTheMooreBound_4august2026-$commit/" \
  --output="$archive" \
  "$commit"

python3 "$repo_root/scripts/verify_source_archive.py" "$archive"
archive_directory=$(dirname -- "$archive")
archive_basename=$(basename -- "$archive")
(
  CDPATH= cd -- "$archive_directory"
  sha256sum "$archive_basename" >"$archive_basename.sha256"
  sha256sum -c "$archive_basename.sha256"
)
cat "$archive.sha256"
