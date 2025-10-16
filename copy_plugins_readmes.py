#!/usr/bin/env python3

from pathlib import Path
from typing import Iterator, Optional, Tuple
import sys, re

PLUGIN_NAME_REGEX: re.Pattern = re.compile("name = \"plugin-(.+)\"")

def extract_plugin_info(dir: Path, _dirnames: list[str], filenames: list[str]) -> Optional[str]:
    if "README.md" not in filenames or "Cargo.toml" not in filenames:
        return None

    crate_definition = dir.joinpath("Cargo.toml").read_text()
    for line in crate_definition.splitlines():
        m = PLUGIN_NAME_REGEX.match(line)
        if m is not None:
            plugin_name = m.group(1)
            return plugin_name

    return None

def find_plugins_in_rust_sources(alumet_repo_dir: Path) -> Iterator[Tuple[str, Path]]:
    plugins_dir = alumet_repo_dir.joinpath("plugins")
    for (dir, dirnames, filenames) in plugins_dir.walk():
        plugin_name = extract_plugin_info(dir, dirnames, filenames)
        if plugin_name is not None:
            readme_file = dir.joinpath("README.md")
            yield (plugin_name, readme_file)

def find_plugins_in_docs(book_src_dir: Path) -> Iterator[Tuple[str, Path]]:
    plugins_dir = book_src_dir.joinpath("plugins")
    for plugin_doc_file in plugins_dir.rglob("*.md"):
        plugin_name = plugin_doc_file.stem
        yield (plugin_name, plugin_doc_file)

def main():
    # parsing args
    # Repo dir: the directory where alumet-dev/alumet has been cloned
    arg_repo_dir = sys.argv[1]
    # Plugin name (optional): the name of the plugin to synchronize. If absent, sync all the plugins.
    arg_plugin_name = sys.argv[2] if len(sys.argv) > 2 else None

    print("Detecting documented plugins…")
    book_src_dir=Path("src")
    plugins_in_book = dict(find_plugins_in_docs(book_src_dir))
    print(f"In user book: {", ".join(plugins_in_book.keys())}")

    print("Detecting plugin libraries…")
    alumet_repo_dir=Path(arg_repo_dir)
    plugins_in_sources = dict(find_plugins_in_rust_sources(alumet_repo_dir))
    print(f"In Rust sources: {", ".join(plugins_in_sources.keys())}")

    for (plugin, readme_file) in plugins_in_sources.items():
        if arg_plugin_name is not None and arg_plugin_name != plugin:
            continue

        readme_content = readme_file.read_bytes()
        existing_doc_file = plugins_in_book.get(plugin)
        if existing_doc_file is None:
            # no existing doc: copy the readme in plugins/ and tell the user to move it
            new_doc_file = book_src_dir.joinpath(f"plugins/{plugin}.md")
            new_doc_file.write_bytes(readme_content)
            print(f"Created {new_doc_file} (to move)")
        else:
            # existing doc: overwrite the file with the readme and let the user fix it
            existing_doc_file.write_bytes(readme_content)
            print(f"Update {existing_doc_file} (to review)")

main()
