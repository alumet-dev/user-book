# Running Alumet agent

To start using the Alumet agent, let us run it in a Terminal.

First, run `alumet-agent --help` to see the available commands and options.

There are two commands that allow to measure things with Alumet.
They correspond to two measurement "modes":

- The `run` mode monitors the system.
- The `exec` mode spawns a process and observes it.

## Monitoring the system with the `run` mode

In `run` mode, the Alumet agent uses its plugins to monitor the entire system (to the extent of what the plugins do).
To choose the plugins to run, pass the `--plugins` flag before the `run` command (this is because the list of plugins apply to every command of the agent, it's not specific to `run`).

Example:

```sh
alumet-agent --plugins procfs,csv run
```

This will start the agent with two plugins:

- `procfs`, which collects information about the processes
- `csv`, which stores the measurements in a local CSV file

### Stopping

To stop the agent, simply press `Ctrl+C`.

### CSV file

The default CSV file is `alumet-output.csv`.
To change the path of the file, use the `--output-file` option.

```sh
alumet-agent --plugins procfs,csv --output-file "measurements-experiment-1.csv" run
```

Unlike some other measurement tools, Alumet saves measurements periodically, and provides the full data (unless you use plugins to aggregate or filter the measurements that you want to save, of course).

### Default command

Since `run` is the default command, it can be omitted.
That is, the above example is equivalent to:

```sh
alumet-agent --plugins procfs,csv
```

## Observing a process with the `exec` mode

In `exec` mode, the Alumet agent spawns a single process and uses its plugins to observe it.

The plugins are informed that they must concentrate on the spawned process instead of monitoring the whole system.
For instance, the `procfs` plugin will mainly gather measurements related to the spawned process. It will also obtain some system measurements, but will not monitor all the processes of the system.

Example:

```sh
alumet-agent --plugins procfs,csv exec sleep 5
```

Everything after `exec` is part of the process to spawn, here `sleep 5`, which will do nothing for 5 seconds.
When the process exits, the Alumet agent stops automatically.

### One just before, one just after

To guarantee that you obtain interesting measurements even if the process is short-lived, some plugins (especially the ones that measure the energy consumption of the hardware) will perform one measurement just before the process is started and one measurement just after it terminates.

Of course, if the process lives long enough, the measurement sources will produce intermediate data points on top of those two "mandatory" measurements.

## Understanding the measurements: how to read the CSV file

The CSV file produced by this simple setup of Alumet looks like this.
The output has been aligned and spaced to make it easier to understand, scroll on the right to see it all.

```csv
metric                 ; timestamp                     ; value      ; resource_kind; resource_id; consumer_kind; consumer_id; __late_attributes
mem_total_kB           ; 2025-04-25T15:08:53.949565834Z; 16377356288; local_machine;            ; local_machine;            ; 
mem_free_kB            ; 2025-04-25T15:08:53.949565834Z;   884572160; local_machine;            ; local_machine;            ; 
mem_available_kB       ; 2025-04-25T15:08:53.949565834Z;  8152973312; local_machine;            ; local_machine;            ; 

kernel_new_forks       ; 2025-04-25T15:08:53.949919481Z;           2; local_machine;            ; local_machine;            ; 
kernel_n_procs_running ; 2025-04-25T15:08:53.949919481Z;           6; local_machine;            ; local_machine;            ; 
kernel_n_procs_blocked ; 2025-04-25T15:08:53.949919481Z;           0; local_machine;            ; local_machine;            ; 

process_cpu_time_ms    ; 2025-04-25T15:08:53.99636522Z ;           0; local_machine;            ; process      ;       65387; cpu_state=user
process_cpu_time_ms    ; 2025-04-25T15:08:53.99636522Z ;           0; local_machine;            ; process      ;       65387; cpu_state=system
process_cpu_time_ms    ; 2025-04-25T15:08:53.99636522Z ;           0; local_machine;            ; process      ;       65387; cpu_state=guest
process_memory_kB      ; 2025-04-25T15:08:53.99636522Z ;        2196; local_machine;            ; process      ;       65387; memory_kind=resident
process_memory_kB      ; 2025-04-25T15:08:53.99636522Z ;        2196; local_machine;            ; process      ;       65387; memory_kind=shared
process_memory_kB      ; 2025-04-25T15:08:53.99636522Z ;       17372; local_machine;            ; process      ;       65387; memory_kind=vmsize
```

The first line contains the name of the columns. Here is what they mean.

- `metric`: the unique name of the metric that has been measured. With the default configuration of the `csv` plugin, the unit of the metric is appended to its name in the CSV. For instance, `process_cpu_time` is in milliseconds. Some metrics, such as `kernel_n_procs_running`, have no unit, they're numbers without a dimension.
- `timestamp`: when the measurement has been obtained. Timestamps are serialized as [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6) date+time values with nanosecond resolution, in the UTC timezone (hence the `Z` at the end).
- `value`: the value of the measurement. For instance, `kernel_n_procs_running` has a value of `6` at `2025-04-25T15:08:53.949919481`.
- `resource_kind` and `resource_id` indicate the "resource" that this measurement is about. It's usually a piece of hardware. The special data `local_machine` (with an empty value for the resource id) means that this measurement is about the entire system. If a CPU-related plugin was enabled, it would have produced measurements with a resource kind of `cpu_package` and a resource id corresponding to that package.
- `consumer_kind` and `consumer_id` indicate the "consumer" that this measurement is about: who consumed the resource? It's usually a piece of software. For instance, `local_machine` means that there was no consumer, the measurement is a global system-level measurement such as the total amount of memory or the temperature of a component. `process;1` (kind `process`, id `65387`) means that this measurement concerns the consumption of the process with pid `65387`.

### Additional attributes in the CSV output

Alumet measurements can contain an arbitrary number of **additional key-value pairs**, called **attributes**.
If they are known early, they will show up as separate CSV columns.
However, it's not always the case. If an attribute appears after the CSV header has been written, it will end up in the `__late_attributes` column.
Attributes in `__late_attributes` should be treated just like attributes in separate CSV columns.

In the output example, measurements with the `process_cpu_time` metric have an additional attribute named `cpu_state`, with a string value.
It refines the perimeter of the measurement by indicating which type of CPU time the measurement is about.
In particular, Linux has separate counters for the time spent by the CPU for a particular process in user code or in kernel code.
