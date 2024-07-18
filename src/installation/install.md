# Installing Alumet

> ⚠️&nbsp;&nbsp;**Alumet is currently in Beta**.
>
> If you have trouble using Alumet, do not hesitate to [discuss with us](https://github.com/alumet-dev/alumet/discussions), we will help you find a solution.
> If you think that you have found a bug, please [open an issue](https://github.com/alumet-dev/alumet/issues) in the repository.

For the moment, the only way to use Alumet is to download its sources and to compile it (see below).
We intend to provide easy-to-use packages in the future.

## Compiling from source

**Prerequisite**: you need to [install the Rust toolchain](https://rustup.rs/).

Open a Terminal and download the repository:

```sh
git clone https://github.com/alumet-dev/alumet.git
```

The Alumet repository contains multiple crates ("crates" are Rust libraries/packages).
To run Alumet, we are interested in `app-agent`, which produces a runnable measurement tool by compiling the core of Alumet and a set of standard plugins into a single binary.

Let's compile this agent.
```sh
cd alumet/app-agent
cargo build
```

The binary should be located in `../target/debug/alumet-agent`. You can check this with a simple `ls`:
```sh
ls ../target/debug/alumet-agent
```

If the agent is there, you can run it. Otherwise, look into the target directory to find the agent.

For the first time, let's use `--help` to learn about the available arguments.
```sh
$ ../target/debug/alumet-agent
[2024-05-14T17:58:00Z INFO  alumet_agent] Starting ALUMET agent v0.4.1
Command line arguments

Usage: alumet-agent [OPTIONS] [COMMAND]

Commands:
  run           Run the agent and monitor the system
  exec          Execute a command and observe its process
  regen-config  Regenerate the configuration file and stop
  help          Print this message or the help of the given subcommand(s)

Options:
      --max-update-interval <MAX_UPDATE_INTERVAL>
          Maximum amount of time between two updates of the sources' commands.
          
          A lower value means that the latency of source commands will be lower, i.e. commands will be applied faster, at the cost of a higher overhead.

  -h, --help
          Print help (see a summary with '-h')
```

To observe your machine, the simplest way is to use the `run` command.

```sh
../target/debug/alumet-agent
```

Alumet will then start to observe your machine.

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
2. Modify `main.rs` to enable the plugin.

Here is how to do it with the NVIDIA plugin.
1. In the directory of `app-agent`, run `cargo add plugin-nvidia`
2. Open `src/main.rs`, locate the line that contains `static_plugins!` (line 31) and add `plugin_nvidia::NvidiaPlugin` to the list of plugins.
It should look like the following:
```rs
// Specifies the plugins that we want to load.
let plugins = static_plugins![RaplPlugin, CsvPlugin, SocketControlPlugin, PerfPlugin, plugin_nvidia::NvidiaPlugin];
```

Then, recompile the agent with `cargo build`.

> Note: if you want to run Alumet on a NVIDIA Jetson device,
> replace `cargo add plugin-nvidia` by `cargo add plugin-nvidia --features jetson --no-default-features`. 

## Tips

### Default command

Since `run` is the default command, you can also run the agent without any argument.
```sh
../target/debug/alumet-agent
```

### Path to the binary

The binary produced by `cargo` is located, when building with a default target (which links to libc) and for the host architecture, at:
- `../target/debug/alumet-agent` in debug mode
- `../target/release/alumet-agent` in release mode

The aforementioned paths are relative to the `app-agent` directory.

### Release mode

By default, the measurement tool is built in _debug mode_, which enables better diagnostics but disables many optimizations.
To deploy Alumet "in production", you would want to use the _release mode_ by adding `--release` to the cargo flags. For instance, use `cargo build --release` to produce the optimized binary and stop.
