# Installing Alumet

> ⚠️&nbsp;&nbsp;**Alumet is currently in Beta**.
>
> If you have trouble using Alumet, do not hesitate to [discuss with us](https://github.com/alumet-dev/alumet/discussions), we will help you find a solution.
> If you think that you have found a bug, please [open an issue](https://github.com/alumet-dev/alumet/issues) in the repository.

For the moment, the only way to use Alumet is to download its sources and to compile it (see below).
We intend to provide easy-to-use packages in the future.

## Compiling from source

**Prerequisite**: A recent version of Rust is required (**at least 1.76** for now). You can run `rustc --version` to check your version. The easiest way to install a recent version of Rust is to use [rustup](https://rustup.rs/).

Open a Terminal and clone the repository:

```sh
git clone https://github.com/alumet-dev/alumet.git
```

The Alumet repository contains multiple crates ("crates" are Rust libraries/packages).
To run Alumet, we are interested in `alumet-agent`: a crate that produces a runnable measurement tool by compiling the core of Alumet and a set of standard plugins into a single executable binary.

Let's compile the agent:
```sh
cargo build -p alumet-agent
```

The binary should be located in `target/debug/alumet-agent`. You can check this with a simple `ls`:
```sh
ls target/debug/alumet-agent
```

If the agent is there, you can run it. Otherwise, look into the target directory to find the agent.

For the first time, let's use `--help` to learn about the available arguments.
```sh
❯ ./target/debug/alumet-agent --help                                          
Alumet standard agent: measure energy and performance metrics

Usage: alumet-agent [OPTIONS] [COMMAND]

Commands:
  run      Run the agent and monitor the system
  exec     Execute a command and observe its process
  config   Manipulate the configuration
  plugins  Get plugins information
  help     Print this message or the help of the given subcommand(s)

Options:
      --config <CONFIG>
          Path to the config file
          
          [env: ALUMET_CONFIG=]
          [default: alumet-config.toml]

      --no-default-config
          If set, the config file must exist, otherwise the agent will fail
          to start with an error

      --config-override <CONFIG_OVERRIDE>
          Config options overrides.
          
          Use dots to separate TOML levels, ex. `plugins.rapl.poll_interval='1ms'`

      --plugins <PLUGINS>
          List of plugins to enable, separated by commas, ex. `csv,rapl`.
          
          All the other plugins will be disabled.

[...]
```

I have omitted some lines here, run the agent with the `--help` flag to discover the actual output :)

## Choosing the plugins that you need

The standard agent, which you have just compiled, contains multiple Alumet plugins.
Each plugin can measure things, compute additional values based on the measurements, and/or save the measurements to a storage.

To see which plugins are included in the agent, run:
```
❯ ./target/debug/alumet-agent plugins list
[...]
Available plugins:
- OAR3 v0.1.0
- csv v0.2.0
- influxdb v0.1.0
- k8s v0.1.0
- mongodb v0.1.0
- nvidia v0.3.0
- oar2-plugin v0.1.0
- perf v0.1.0
- procfs v0.1.0
- rapl v0.3.1
- relay-client v0.6.0
- relay-server v0.6.0
- socket-control v0.2.0

Edit the configuration file or use the --plugins flag to enable/disable plugins.
```

For your first time, let's enable a very simple set of plugins:
- `rapl`: a plugin that measures the energy consumption of your CPU
- `csv`: a plugin that saves all the measurements to a CSV file

Run Alumet with these plugins by using the `--plugins` flag:
```
❯ ./target/debug/alumet-agent --plugins rapl,csv
[2025-02-20T13:25:26Z INFO  alumet_agent] Starting Alumet agent 'alumet-agent' v0.8.0-6c72253-dirty (2025-02-20T12:40:49.666737256Z, rustc 1.84.0, debug=true)
[2025-02-20T13:25:26Z WARN  alumet_agent] DEBUG assertions are enabled, this build of Alumet is fine for debugging, but not for production.
[2025-02-20T13:25:26Z INFO  alumet::agent::builder] Initializing the plugins...
[2025-02-20T13:25:26Z INFO  alumet::agent::builder] 2 plugins initialized.
[2025-02-20T13:25:26Z INFO  alumet::agent::builder] Starting the plugins...
[2025-02-20T13:25:26Z INFO  plugin_rapl] Available RAPL domains: dram, package, platform, pp0, pp1
[2025-02-20T13:25:26Z INFO  alumet::agent::builder] Plugin startup complete.
    🧩 2 plugins started:
        - csv v0.2.0
        - rapl v0.3.1
    
    ⭕ 11 plugins disabled:
        - OAR3 v0.1.0
        - influxdb v0.1.0
        - k8s v0.1.0
        - mongodb v0.1.0
        - nvidia v0.3.0
        - oar2-plugin v0.1.0
        - perf v0.1.0
        - procfs v0.1.0
        - relay-client v0.6.0
        - relay-server v0.6.0
        - socket-control v0.2.0
    
    📏 1 metric registered:
        - rapl_consumed_energy: F64 (J)
    
    📥 1 source, 🔀 0 transform and 📝 1 output registered.
    
    🔔 0 metric listener registered.
    
[2025-02-20T13:25:26Z INFO  alumet::agent::builder] Running pre-pipeline-start hooks...
[2025-02-20T13:25:26Z INFO  alumet::agent::builder] Starting the measurement pipeline...
[2025-02-20T13:25:26Z INFO  alumet::pipeline::builder] Only one output and no transform, using a simplified and optimized measurement pipeline.
[2025-02-20T13:25:26Z INFO  alumet::agent::builder] 🔥 ALUMET measurement pipeline has started.
[2025-02-20T13:25:26Z INFO  alumet::agent::builder] Running post-pipeline-start hooks...
[2025-02-20T13:25:26Z INFO  alumet::agent::builder] 🔥 ALUMET agent is ready.
```

Alumet will start to monitor various hardware and software components. Notice how you can immediately see which plugins are used and which metrics they measure. Use Ctrl+C to shut the agent down.

If you get an error, refer to the following section.

## Obtaining required privileges

Measuring some metrics, like RAPL energy counters and perf_events, require specific privileges (because we read low-level data).
Alumet will warn you about missing privileges and will suggest commands to fix the issue (there are several options).

For example, if you get an error like this:
```
[2025-02-20T13:28:40Z WARN  plugin_rapl] I could not use perf_events to read RAPL energy counters: perf_event_open failed. Try to set kernel.perf_event_paranoid to 0 or -1, or to give CAP_PERFMON to the application's binary (CAP_SYS_ADMIN before Linux 5.8).

[...]
Error: startup failure

Caused by:
    0: plugin failed to start: rapl v0.3.1
    1: Could not open /sys/devices/virtual/powercap/intel-rapl/intel-rapl:1/energy_uj. Try to adjust file permissions.
    2: Permission denied (os error 13)
```

Read the logs and apply one of the proposed solutions.
The easiest one is to run this command before starting Alumet:
```sh
sudo sysctl -w kernel.perf_event_paranoid=0
```

You only need to run it once per boot:if you reboot the machine, you need to do it again. See `man sysctl.conf` for a way of making this setting permanent.

### Be careful about sudo

We recommend not to run the Alumet agent with `sudo`. It is better to give appropriate privileges to the agent binary or to make the system configuration more permissive.

In any case, please **never use `sudo cargo run`**, because that would compile the project with the root user, making it unusable for you.

## Tips

### Path to the binary

The binary produced by `cargo` is located, when building with a default target (which links to libc) and for the host architecture, at:
- `target/debug/alumet-agent` in debug mode
- `target/release/alumet-agent` in release mode

The aforementioned paths are relative to the root directory of the Git repository.

### Release mode

By default, the measurement tool is built in _debug mode_, which enables better diagnostics but disables many optimizations.
To deploy Alumet "in production", you should use the _release mode_ by adding `--release` to the cargo flags.

```sh
cargo build -p alumet-agent --release
```

The optimized agent will be saved to `target/release/alumet-agent`.

### CSV output file

The default CSV file used by the `csv` plugin is `alumet-output.csv`. You can change this by editing `alumet-config.toml`, or by using the `--output-file` flag.

### Configuration file

The configuration file is automatically created by Alumet if it does not exist.
Its content depends on the set of enabled plugins.

-> [Learn more about Alumet config here](./config.md).

### Multiple agents?

As of [PR#93](https://github.com/alumet-dev/alumet/pull/93) (merged in Alumet 0.8.0-d7565a6), we provide one standard agent with all the "official" plugins. You can still create your own custom agent in a separate crate. See the PR description for more information.
