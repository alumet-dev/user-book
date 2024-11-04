# The ALUMET User Book

This repository contains the "Alumet user book", a guide for the users for the users of the measurement tool: system administrators, researchers or engineers who want to measure things, etc.


## Reading the book

The book is available online (via GitHub pages) here: https://alumet-dev.github.io/user-book/

## Generating the book

The book is made with [mdBook](https://rust-lang.github.io/mdBook/).

First, you need to [install mdBook](https://rust-lang.github.io/mdBook/guide/installation.html#installation).

Then, run `mdbook`.
Example:

```sh
cd user
mdbook serve --open
```

As explained in the [mdBook documentation](https://rust-lang.github.io/mdBook/guide/creating.html#creating-a-book), `serve --open` will build the book, start a local web server and open the book in your default web browser. Modifying the source of the book will automatically reload the web page.
