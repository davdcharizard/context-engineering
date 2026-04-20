#!/usr/bin/env python3
"""Count Claude input tokens for a file or directory.

Uses the Anthropic `messages.count_tokens` endpoint to measure how many input
tokens a given text file (or every text file under a directory) would consume
for a chosen Claude model.

Requires:
    - ANTHROPIC_API_KEY set in the environment
    - `pip install anthropic`
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.stderr.write(
        "error: the `anthropic` Python package is not installed.\n"
        "       install it with:  pip install anthropic\n"
    )
    sys.exit(1)


def preflight() -> None:
    """Fail fast with actionable messages before doing any work."""
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        sys.stderr.write(
            "error: ANTHROPIC_API_KEY is not set.\n"
            "       Export it in your shell, e.g.:\n"
            "           export ANTHROPIC_API_KEY='sk-ant-...'\n"
            "       Get a key from https://console.claude.com/settings/keys\n"
        )
        sys.exit(1)
    if not key.startswith("sk-"):
        sys.stderr.write(
            "warning: ANTHROPIC_API_KEY does not start with 'sk-'. "
            "Double-check that you exported an Anthropic key (not another provider's).\n"
        )


DEFAULT_MODEL = "claude-opus-4-7"

DEFAULT_EXTS = {".md", ".txt"}

TEXT_EXTS = DEFAULT_EXTS | {
    ".py", ".ipynb",
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".go", ".rs", ".java", ".kt", ".swift", ".rb", ".php", ".lua", ".r",
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".hh",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".sh", ".bash", ".zsh", ".fish",
    ".html", ".htm", ".css", ".scss", ".sass",
    ".sql", ".graphql", ".proto",
    ".tex", ".rst", ".adoc",
}


def parse_exts(raw: str) -> set[str]:
    out: set[str] = set()
    for piece in raw.split(","):
        piece = piece.strip().lower()
        if not piece:
            continue
        out.add(piece if piece.startswith(".") else "." + piece)
    return out


def iter_files(path: Path, exts: set[str] | None) -> list[Path]:
    if path.is_file():
        return [path]
    out: list[Path] = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            p = Path(root) / name
            if exts is None or p.suffix.lower() in exts:
                out.append(p)
    out.sort()
    return out


def count_file(client: "anthropic.Anthropic", model: str, text: str) -> int:
    resp = client.messages.count_tokens(
        model=model,
        messages=[{"role": "user", "content": text}],
    )
    return resp.input_tokens


def relative(p: Path, root: Path) -> Path:
    try:
        return p.relative_to(root)
    except ValueError:
        return p


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Count Claude input tokens for a file or directory.",
    )
    ap.add_argument("path", help="File or directory to measure.")
    ap.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model id (default: {DEFAULT_MODEL}). "
             "Examples: claude-opus-4-7, claude-sonnet-4-6, claude-haiku-4-5-20251001.",
    )
    ap.add_argument(
        "--ext",
        default=",".join(sorted(DEFAULT_EXTS)),
        help="Comma-separated extensions to include when walking a directory "
             "(default: .md,.txt). Ignored for single-file input.",
    )
    ap.add_argument(
        "--all",
        action="store_true",
        help="Walk all common text extensions (code + docs + configs).",
    )
    args = ap.parse_args()

    preflight()

    path = Path(args.path).resolve()
    if not path.exists():
        sys.stderr.write(f"error: path not found: {path}\n")
        return 2

    exts: set[str] | None
    if path.is_file():
        exts = None
    elif args.all:
        exts = TEXT_EXTS
    else:
        exts = parse_exts(args.ext)

    files = iter_files(path, exts)
    if not files:
        shown = "any extension" if exts is None else ", ".join(sorted(exts))
        sys.stderr.write(
            f"error: no files matched under {path} (extensions: {shown}).\n"
            "       try --all to include all common text/code extensions, "
            "or pass --ext '.md,.py,...'\n"
        )
        return 1

    sys.stderr.write(
        f"counting {len(files)} file(s) with model={args.model} ...\n"
    )

    client = anthropic.Anthropic()

    display_root = path if path.is_dir() else path.parent

    rows: list[tuple[Path, int]] = []
    total = 0
    width = max(len(str(relative(p, display_root))) for p in files)

    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            sys.stderr.write(f"skip {p}: {e}\n")
            continue
        if not text.strip():
            n = 0
        else:
            try:
                n = count_file(client, args.model, text)
            except anthropic.AuthenticationError as e:
                sys.stderr.write(
                    f"error: authentication failed ({e}).\n"
                    "       Check that ANTHROPIC_API_KEY is a valid Anthropic key.\n"
                )
                return 1
            except anthropic.NotFoundError as e:
                sys.stderr.write(
                    f"error: model '{args.model}' not found ({e}).\n"
                    "       See https://platform.claude.com/docs/en/about-claude/models/overview\n"
                )
                return 1
            except anthropic.RateLimitError as e:
                sys.stderr.write(
                    f"error: rate limited by the token counting endpoint ({e}).\n"
                    "       Wait a minute and retry, or upgrade your usage tier.\n"
                )
                return 1
            except anthropic.APIError as e:
                sys.stderr.write(f"error: API request failed while counting {p}: {e}\n")
                return 1
        rows.append((p, n))
        total += n
        rel = relative(p, display_root)
        print(f"{n:>10,}  {str(rel):<{width}}", flush=True)

    print("-" * (12 + width))
    print(f"{total:>10,}  TOTAL  ({len(rows)} files, model={args.model})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
