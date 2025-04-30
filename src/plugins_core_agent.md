# The main parts of Alumet: core, plugins, agents

One of the key features of the Alumet framework is its extensibility.
Thanks to a clear separation between the "core" and the "plugins", Alumet allows to build measure-made measurement tools for a wide range of situations.

This page offers a simple, high-level view of the main concepts.
For a more detailed explanation, read the [Alumet Architecture](https://alumet-dev.github.io/developer-book/intro/Alumet%20architecture.html) chapter of the Alumet Developer Book.

## Alumet core

The **core** of Alumet is a Rust library that implements:
- a generic and "universal" measurement model
- a concurrent measurement pipeline based on asynchronous tasks
- a plugin system to populate the pipeline with various elements
- a resilient way to handle errors
- and various utilities

## Alumet plugins

On top of this library, we build **plugins**, which use the core to provide environment-specific features such as:
- gathering measurements from the operating system
- reading data from hardware probes
- applying a statistical model on the data
- filtering the data
- writing the measurements to a file or database
- …

## Alumet agent(s)

But Alumet **core** and Alumet **plugins** are not executable!
You cannot run them to obtain your measurements.
To get an operational tool, we combine them in an **agent**: a runnable application.

We provide a "standard" agent that you can download and use right away.
See [Installing Alumet](start/install.md).
You can also build your own customized agent, it only takes a few lines of codes.
Refer to the [Developer Book](https://alumet-dev.github.io/developer-book/).

<!-- todo nice diagrams here -->
