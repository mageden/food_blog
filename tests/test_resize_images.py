from __future__ import annotations

from pathlib import Path

from PIL import Image

from tools.resize_images import iter_images, resize_image


def make_image(path: Path, size: tuple[int, int], mode: str = "RGB", fmt: str | None = None) -> Path:
    image = Image.new(mode, size, color=(255, 0, 0) if mode != "L" else 128)
    image.save(path, format=fmt)
    return path


def test_iter_images_yields_single_image_file(tmp_path: Path) -> None:
    image_path = make_image(tmp_path / "one.jpg", (10, 10), fmt="JPEG")
    other_path = tmp_path / "notes.txt"
    other_path.write_text("not an image", encoding="utf-8")

    assert list(iter_images([image_path, other_path])) == [image_path]


def test_iter_images_recurses_through_nested_directories(tmp_path: Path) -> None:
    top_image = make_image(tmp_path / "top.png", (10, 10), fmt="PNG")
    nested_dir = tmp_path / "nested" / "more"
    nested_dir.mkdir(parents=True)
    nested_image = make_image(nested_dir / "deep.jpeg", (10, 10), fmt="JPEG")
    (tmp_path / "nested" / "ignore.md").write_text("# ignore", encoding="utf-8")

    assert list(iter_images([tmp_path])) == [top_image, nested_image]


def test_resize_image_skips_small_images(tmp_path: Path) -> None:
    image_path = make_image(tmp_path / "small.jpg", (400, 200), fmt="JPEG")

    changed, status = resize_image(image_path, max_width=800, quality=80, overwrite=False)

    assert changed is False
    assert status == "skipped"
    assert not (tmp_path / "small-resized.jpg").exists()


def test_resize_image_writes_resized_copy_for_jpeg(tmp_path: Path) -> None:
    image_path = make_image(tmp_path / "large.jpg", (2000, 1000), fmt="JPEG")

    changed, status = resize_image(image_path, max_width=1000, quality=85, overwrite=False)

    resized_path = tmp_path / "large-resized.jpg"
    assert changed is True
    assert status == f"resized -> {resized_path}"
    assert resized_path.exists()

    with Image.open(resized_path) as resized:
        assert resized.size == (1000, 500)


def test_resize_image_overwrites_png(tmp_path: Path) -> None:
    image_path = make_image(tmp_path / "large.png", (1200, 600), fmt="PNG")

    changed, status = resize_image(image_path, max_width=600, quality=80, overwrite=True)

    assert changed is True
    assert status == f"resized -> {image_path}"

    with Image.open(image_path) as resized:
        assert resized.size == (600, 300)

