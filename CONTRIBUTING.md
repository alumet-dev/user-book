<!-- markdownlint-disable MD029 -->
# Contributing Guide

Here are more information that you will probably need to work on the book itself.

## How to synchronize the plugins docs with their READMEs

The script `copy_plugins_readme.py` can copy the plugins' README, found in the repository that contains their source code (`alumet-dev/alumet`), to the user book repository (this one).

Usage:

```sh
./copy_plugins_readmes.py ALUMET_REPO_PATH [PLUGIN_NAME]
```

To copy all the readmes (assuming that `alumet` and `user-book` have been cloned in the same parent directory):

```sh
./copy_plugins_readmes.py ../alumet
```

To copy one readme, for instance for plugin `rapl`:

```sh
./copy_plugins_readmes.py ../alumet rapl
```

The script will:
1. Find the `README.md` of each plugin.
2. Find the corresponding `.md` file in the sources of the user book.
3. Overwrite the user book doc with the content of the readme or, if there is no existing documentation in the user book, create a new `.md` file in the `plugins/` directory.

**You** should review the changes and make some adjustements, such as adding screenshots, explaining new concepts, moving the new `.md` files to the right section, etc.
In the case of a new plugin, don't forget to update `SUMMARY.md`.

## How to modify/update the mdBook theme

See the [mdBook documentation](https://rust-lang.github.io/mdBook/format/theme/index.html).

1. Regenerate the `theme` folder with default mdbook files. This allows the theme to be updated to the current version of mdbook.

```sh
mdbook init --theme
```

2. Cancel (with git) the modifications of `book.toml`
3. Remove all theme files except `index.hbs`

```sh
find ./theme -type f ! -name 'index.hbs' -delete
rmdir ./theme/fonts ./theme/css
```

4. Update `theme/` with the modifications that you want. For instance, for a page-level table of contents, modify `index.hbs` in this way:

```diff
<main>
+    <div class="content-wrap">
        {{{ content }}}
+    </div>
+    <div id="sidetoc">
+        <nav id="pagetoc"></nav>
+    </div>
</main>
```

5. Update the `pagetoc` addon (see the relevant section)

## How to update add-ons

The `addons` folder contains assets used by external preprocessors or other tools that add features to mdBook.

## Pagetoc

[`mdbook-pagetoc`](https://github.com/JorelAli/mdBook-pagetoc) provides page-level table of content with JS.

To update:
1. Download the [files from the repository](https://github.com/JorelAli/mdBook-pagetoc/tree/master/theme).
2. Replace `pagetoc.css` and `pagetoc.js` in `addons/`.

## Mermaid

[`mdbook-mermaid`](https://github.com/badboy/mdbook-mermaid) is a preprocessor that adds support for `mermaid.js` diagrams.

To update:
1. Download the new assets or obtain them by running `mdbook-mermaid install $(pwd)`.
2. Put the new assets in `addons/`.
3. Update the version of `mdbook-mermaid` that is used in the `deploy` workflow, by modifying [`deploy.yml`](.github/workflows/deploy.yml).
