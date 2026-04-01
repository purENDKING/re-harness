from __future__ import annotations

from pathlib import Path

from jinja2 import Template


def render_template_to_file(template_path: Path, output_path: Path, context: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = Template(template_path.read_text(encoding="utf-8")).render(**context)
    output_path.write_text(content, encoding="utf-8")
