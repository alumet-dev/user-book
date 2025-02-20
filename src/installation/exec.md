# Execution mode

When started with the `exec` command, the Alumet agent spawns a new process with the specified command and stops when the process exits.

The execution mode automatically make some plugins, such as the `perf` plugin, gather more metrics about the spawned process.

## Example

Let's try this feature with a simple `sleep` command.

```sh
alumet-agent exec sleep 1
```

With the standard plugins (rapl, perf, csv), the resulting CSV file looks like the following (formatted to make it easier to read).
```csv
metric                       ;timestamp                      ;value             ;resource_kind ;resource_id ;consumer_kind ;consumer_id ;__late_attributes
perf_hardware_REF_CPU_CYCLES ;2024-05-14T21:28:49.416768909Z ; 0                ;local_machine ;            ;process       ;     728039 ;
perf_hardware_CACHE_MISSES   ;2024-05-14T21:28:49.416768909Z ; 0                ;local_machine ;            ;process       ;     728039 ;
perf_hardware_BRANCH_MISSES  ;2024-05-14T21:28:49.416768909Z ; 0                ;local_machine ;            ;process       ;     728039 ;
perf_cache_LL_READ_MISS      ;2024-05-14T21:28:49.416768909Z ; 0                ;local_machine ;            ;process       ;     728039 ;
rapl_consumed_energy_J       ;2024-05-14T21:28:50.389874134Z ; 0.89825439453125 ;dram          ;          0 ;local_machine ;            ;domain=dram
rapl_consumed_energy_J       ;2024-05-14T21:28:50.389874134Z ; 5.779296875      ;cpu_package   ;          0 ;local_machine ;            ;domain=pp0
rapl_consumed_energy_J       ;2024-05-14T21:28:50.389874134Z ;50.3060302734375  ;local_machine ;            ;local_machine ;            ;domain=platform
rapl_consumed_energy_J       ;2024-05-14T21:28:50.389874134Z ; 0                ;cpu_package   ;          0 ;local_machine ;            ;domain=pp1
rapl_consumed_energy_J       ;2024-05-14T21:28:50.389874134Z ;10.3299560546875  ;cpu_package   ;          0 ;local_machine ;            ;domain=package
```

There are several things to note here.

First, as expected, a simple `sleep` does not use any cpu cycle. This is reported by the `perf_hardware_REF_CPU_CYCLES` metric.

Second, the computer consumed some energy during the `sleep`. This is reported by the `rapl_consumed_energy_J` metric. The `J` indicates that the measurements are in Joules. Note that `perf_hardware_REF_CPU_CYCLES` does not have a unit suffix, because it's a dimensionless value: a counter. In any case, the CSV plugin can be configured not to include the suffix in the resulting file. But let's go back to the RAPL metric. Here, the metric is given five times, because five different RAPL domains are available on this machine (dram, pp0, pp1, package and platform).

⚠️ As indicated by the value `local_machine` in the `consumer_kind` column, the metric `rapl_consumed_energy_J` does not report the energy consumed by the process spawned with `alumet-agent exec`, but the total energy consumption of the associated RAPL domain (since the previous measurement of the metric, but here we only have one value).

Finally, the timestamps are serialized in the UTC timezone, hence the `Z` suffix.
