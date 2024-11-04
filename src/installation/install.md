# Installing Alumet

> ⚠️&nbsp;&nbsp;**Alumet is currently in Beta**.
>
> If you have trouble using Alumet, do not hesitate to [discuss with us](https://github.com/alumet-dev/alumet/discussions), we will help you find a solution.
> If you think that you have found a bug, please [open an issue](https://github.com/alumet-dev/alumet/issues) in the repository.

For the moment, the only way to use Alumet is to download its sources and to compile it (see below).
We intend to provide easy-to-use packages in the future.

## Compiling from source

**Prerequisite**: A recent version of Rust is required (**at least 1.76** for now). You can run `rustc --version` to check your version. The easiest way to install a recent version of Rust is to use [rustup](https://rustup.rs/).

Open a Terminal and download the repository:

```sh
git clone https://github.com/alumet-dev/alumet.git
```

The Alumet repository contains multiple crates ("crates" are Rust libraries/packages).
To run Alumet, we are interested in `app-agent`, which produces a runnable measurement tool by compiling the core of Alumet and a set of standard plugins into a single binary. The crate `app-agent` contains multiple standard agents, as described in [the corresponding README](https://github.com/alumet-dev/alumet/blob/main/app-agent/README.md).

Let's compile the simplest agent, the "local" one.
```sh
cd alumet/app-agent
cargo build --bin alumet-local-agent --features local_x86
```

The binary should be located in `../target/debug/alumet-local-agent`. You can check this with a simple `ls`:
```sh
ls ../target/debug/alumet-local-agent
```

If the agent is there, you can run it. Otherwise, look into the target directory to find the agent.

For the first time, let's use `--help` to learn about the available arguments.
```sh
$ ../target/debug/alumet-local-agent
[2024-10-15T17:58:00Z INFO  alumet_local_agent] Starting ALUMET agent v0.6.1
Command line arguments

Usage: alumet-local-agent [OPTIONS] [COMMAND]

Commands:
  run           Run the agent and monitor the system
  exec          Execute a command and observe its process
  regen-config  Regenerate the configuration file and stop
  help          Print this message or the help of the given subcommand(s)

Options:
      --config <CONFIG>
          Path to the config file
          
          [default: alumet-config.toml]
          
[...]
```

I have omitted some lines here, run the command to discover the actual output :)

To observe your machine, the simplest way is to use the `run` command.

```sh
../target/debug/alumet-local-agent
```

Alumet will start to monitor various hardware and software components.

## Required privileges

Measuring some metrics, like RAPL energy counters and perf_events, require specific privileges.
Alumet will warn you about missing privileges and will suggest commands to fix the issue (there are several options).

In any case, please **do not use `sudo cargo run`**, because that would compile the project with the root user, making it unusable for your user account.

## Output file and configuration

With the standard set of plugins, the measurements are saved in a CSV file.
By default, this is `alumet-output.csv`. You can change this by editing `alumet-config.toml`. Note that the configuration file is automatically created by Alumet if it does not exist.

[Learn more about Alumet config here](./config.md).

## Enabling more plugins

By default, only some plugins are enabled. To enable a plugin and include it in the Alumet agent binary, perform these two steps:
1. Add a dependency on the plugin.
2. Modify `local.rs` to enable the plugin.

Here is how to do it with the NVIDIA plugin.
1. In the directory of `app-agent`, run `cargo add plugin-nvidia`
2. Open `src/bin/local.rs`, locate the line that contains `static_plugins!` and add `plugin_nvidia::NvidiaPlugin` to the list of plugins.

```diff
let plugins = static_plugins![
    // ...
+   plugin_nvidia::NvidiaPlugin,
];
```

Then, recompile the agent with `cargo build`.

> Note: if you want to run Alumet on a NVIDIA Jetson device,
> replace `cargo add plugin-nvidia` by `cargo add plugin-nvidia --features jetson --no-default-features`. 

## Tips

### Default command

Since `run` is the default command, you can also run the agent without any argument.
```sh
../target/debug/alumet-local-agent
```

### Path to the binary

The binary produced by `cargo` is located, when building with a default target (which links to libc) and for the host architecture, at:
- `../target/debug/alumet-local-agent` in debug mode
- `../target/release/alumet-local-agent` in release mode

The aforementioned paths are relative to the `app-agent` directory.

### Release mode

By default, the measurement tool is built in _debug mode_, which enables better diagnostics but disables many optimizations.
To deploy Alumet "in production", you would want to use the _release mode_ by adding `--release` to the cargo flags.

For instance:
```sh
cd alumet/app-agent
cargo build --bin alumet-local-agent --features local_x86 --release
```

The optimized agent will be saved to `target/release/alumet-local-agent`.
