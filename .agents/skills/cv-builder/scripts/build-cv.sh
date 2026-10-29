#!/usr/bin/env bash
# Render cv/*.yaml -> cv/PhamThanhTan-*.pdf
#
# Requires uv (https://docs.astral.sh/uv/). uvx provisions Python 3.12 + rendercv[full]
# automatically; nothing is added to this repo's environment.
#
# Usage:
#   .agents/skills/cv-builder/scripts/build-cv.sh            # build both editions
#   .agents/skills/cv-builder/scripts/build-cv.sh ENG        # English only
#   .agents/skills/cv-builder/scripts/build-cv.sh VIE        # Vietnamese only
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
CV_DIR="$REPO_ROOT/cv"
VERSION_PIN="rendercv[full]==2.8"

targets=("$@")
if [ ${#targets[@]} -eq 0 ]; then
  targets=(ENG VIE)
fi

if ! command -v uvx >/dev/null 2>&1; then
  echo "error: uvx not found. Install uv: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

status=0
for lang in "${targets[@]}"; do
  src="$CV_DIR/PhamThanhTan-$lang.yaml"
  out="$CV_DIR/PhamThanhTan-$lang.pdf"

  if [ ! -f "$src" ]; then
    echo "error: missing source $src" >&2
    status=1
    continue
  fi

  echo "==> rendering $lang"
  # NOTE: never pass --dont-generate-typst: the PDF is typeset from Typst, and the flag
  # also suppresses PDF output in rendercv 2.8.
  if ( cd "$CV_DIR" && uvx --python 3.12 --from "$VERSION_PIN" rendercv render "$(basename "$src")" \
      --pdf-path "$(basename "$out")" \
      --dont-generate-markdown \
      --dont-generate-html \
      --dont-generate-png ); then
    pages=$(uv run --python 3.12 --quiet --with pypdf python - "$out" <<'PY'
import sys
from pypdf import PdfReader
print(len(PdfReader(sys.argv[1]).pages))
PY
)
    echo "    -> $out (${pages} page(s))"
    if [ "$pages" -gt 2 ]; then
      echo "    warning: $lang CV is ${pages} pages; target is <= 2" >&2
    fi
  else
    echo "error: render failed for $lang" >&2
    status=1
  fi
done

# rendercv writes a rendercv_output/ folder next to the source; keep the repo clean.
rm -rf "$CV_DIR/rendercv_output" 2>/dev/null || true

exit $status
