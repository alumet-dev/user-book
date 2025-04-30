# Configuration file

Alumet and its plugins can be configured by modifying a [TOML](https://toml.io/en/) file.
If you don't know TOML, it's a configuration format that aims to be "a config file for humans", easy to read and to modify.

## Where is the configuration file?

### Packaged Alumet agent

Pre-built Alumet packages contain a default configuration file that applies to every Alumet agent on the system.
It is located at `/etc/alumet/alumet-config.toml`.

### Standalone binary or Docker image

Installing the Alumet agent with `cargo` or using one of our Docker images (see [Installing Alumet](./install.md)) does not set up a default global configuration file.

Instead, the agent automatically generates a local configuration file `alumet-config.toml`, in its working directory, on startup.
The content of the configuration depends on the plugins that you enable with the `--plugins` flag.

## Overriding the configuration file 📄

You can override the configuration file in two ways:
- Pass the `--config` argument.
- Set the environment variable `ALUMET_CONFIG`.

The flag takes precedence over the environment variable.

If you specify a path that does not exist, the Alumet agent will attempt to create it with a set of default values.

Example with the flag:

```sh
alumet-agent --plugins procfs,csv --config my-config.toml exec sleep 1
```

Example with the environment variable:

```sh
ALUMET_CONFIG='my-config.toml' alumet-agent --plugins procfs,csv exec sleep 1
```

## Regenerating the configuration file 🔁

If the config file does not exist, it will be automatically generated.

But it is sometimes useful to manually generate the configuration file, for instance when you want to review or modify the configuration before using it. It is also useful when you change your environment in a way that is potentially incompatible with the current configuration, for example when updating the agent to the next major version.

The following command regenerates the configuration file:

```sh
alumet-agent config regen
```

It takes into account, among others, the list of plugins that must be enabled (specified by `--plugins`).
Disabled plugins will not be present in the generated config.

## Common plugin options

Each plugin is free to declare its own configuration options.
Nevertheless, some options are very common and can be found in multiple plugins.

Please refer to the documentation of each plugin for an accurate description of its possible configuration settings.

### Source trigger options

Plugins that provide measurements sources often do so by delegating the trigger management to Alumet.
In other words, it is Alumet (core) that wakes up the measurement sources when needed, and then the sources do what they need to do to gather the data.

In that case, the plugin will most likely provide the following settings:
- `poll_interval`: the interval between each "wake up" of the plugin's measurement source.
- `flush_interval`: how long to wait before sending the measurements to the next step in Alumet's pipeline (if there is at least one transform in the pipeline, the next step is the transform step, otherwise it's directly the output step).

These two settings are given as a **string with a special syntax** that represent a duration.
For example, the value `"1s"` means one second, and the value `"1ms"` means one millisecond.

Here is an example with the `rapl` plugin, which provide one measurement source:

```toml
[plugins.rapl]
# Interval between each measurement of the RAPL plugin.
# Most plugins that provide measurement sources also provide this configuration option.
poll_interval = "1s"

# Measurements are kept in a buffer and are only sent to the next step of the Alumet
# pipeline when the flush interval expires.
flush_interval = "5s"

# Another option (specific to the RAPL plugin, included for exhaustivity purposes)
no_perf_events = false
```

Note that the `rapl` plugin defines a specific option `no_perf_events` on top of the common configuration options for measurement sources.

### Output formatting options

Plugins that provide outputs are often able to slightly modify the data before it is finally exported.
Here are some options that are quite common among output plugins:
- `append_unit_to_metric_name` (boolean): If set to `true`, append the unit of the metric to its name.
- `use_unit_display_name` (boolean): If set to `true`, use the human-readable display name of the metric unit when appending it to its name. If set to `false`, use the machine-readable ASCII name of the unit. This distinction is based on the [Unified Code for Units of Measure](https://ucum.org/), aka UCUM. This setting does nothing if `append_unit_to_metric_name` is `false`.
  - Example: the human-readable _display name_ of the "microsecond" unit is `µs`, while its machine-readable _unique name_ is `us`.

Here is an example with the `csv` plugin, which exports measurements to a local CSV file.

```toml
[plugins.csv]
# csv-specific: path to the CSV file
output_path = "alumet-output.csv"

# csv-specific: always flush the buffer after each operation
# (this makes the data visible in the file with less delay)
force_flush = true

# Common options, described above
append_unit_to_metric_name = true
use_unit_display_name = true

# csv-specific: column delimited
csv_delimiter = ";"
```
