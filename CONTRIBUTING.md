# Contributing Guide

Here are more information that you will probably need to work on the book itself.

## How to modify/update the mdBook theme

See the [mdBook documentation](https://rust-lang.github.io/mdBook/format/theme/index.html).

1. Regenerate the `theme` folder with default mdbook files. This allows the theme to be updated to the current version of mdbook.
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

5. Put additional files in `theme`, e.g. `pagetoc.css` and `pagetoc.html` ([mdBook-pagetoc](https://github.com/JorelAli/mdBook-pagetoc/tree/master/theme)).
Update `book.toml` accordingly:

```diff
+[output.html]
+additional-css = ["theme/pagetoc.css"]
+additional-js = ["theme/pagetoc.js"]
```
