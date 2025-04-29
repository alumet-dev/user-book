# The main parts of Alumet: core, plugins, agents

One of the key features of the Alumet framework is its extensibility.
Thanks to a clear separation between the "core" and the "plugins", Alumet allows to build measure-made measurement tools for a wide range of situations.

The _core_ of Alumet is a Rust library that implements:
- a generic and "universal" measurement model
- a concurrent measurement pipeline based on asynchronous tasks
- a plugin system to populate the pipeline with various elements
- a resilient way to handle errors
- and various utilities

On top of this library, we build _plugins_, which use the core to provide environment-specific features such as:
- gathering measurements from the operating system
- reading data from hardware probes
- applying a statistical model on the data
- filtering the data
- writing the measurements to a file or database

But Alumet _core_ and Alumet _plugins_ are not executable!
You cannot run them to obtain your measurements.
To get an operational tool, we combine them in an _agent_: a runnable application.

We provide a "standard" agent that you can download and use right away.
See [Installing Alumet](start/install.md).
You can also build your own customized agent, it only takes a few lines of codes.
