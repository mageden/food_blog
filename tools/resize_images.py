from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def iter_images(paths: Iterable[Path]) -> Iterable[Path]:
    for base in paths:
        if base.is_file():
            if base.suffix.lower() in IMAGE_EXTENSIONS:
                yield base
            continue

        if base.is_dir():
            for path in base.rglob("*"):
                if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
                    yield path


def resize_image(path: Path, max_width: int, quality: int, overwrite: bool) -> tuple[bool, str]:
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        width, height = img.size

        if width <= max_width:
            return False, "skipped"

        new_height = round(height * max_width / width)
        resized = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        save_path = path if overwrite else path.with_name(f"{path.stem}-resized{path.suffix}")
        save_kwargs = {"optimize": True}

        suffix = path.suffix.lower()
        if suffix in {".jpg", ".jpeg"}:
            if resized.mode not in ("RGB", "L"):
                resized = resized.convert("RGB")
            save_kwargs.update({"quality": quality, "progressive": True})
            resized.save(save_path, **save_kwargs)
        elif suffix == ".png":
            resized.save(save_path, **save_kwargs)
        else:
            return False, "unsupported"

    return True, f"resized -> {save_path}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Resize blog images to a maximum width.")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["assets"],
        help="Files or folders to process. Defaults to assets/.",
    )
    parser.add_argument("--max-width", type=int, default=1600)
    parser.add_argument("--quality", type=int, default=80)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the original file instead of writing a -resized copy.",
    )
    args = parser.parse_args()

    roots = [Path(p) for p in args.paths]
    processed = 0
    resized = 0

    for path in iter_images(roots):
        processed += 1
        changed, status = resize_image(path, args.max_width, args.quality, args.overwrite)
        if changed:
            resized += 1
        print(f"{path}: {status}")

    print(f"Processed {processed} image(s); resized {resized}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
