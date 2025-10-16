<!-- markdownlint-disable first-line-h1 no-empty-links -->
[Introduction](intro.md)
[Alumet core, plugins, agent](plugins_core_agent.md)

# Installation and Configuration

- [Installing Alumet](start/install.md)
- [Running Alumet](start/run.md)
- [Configuration file](start/config.md)
- [Distributed measurement with the "relay" mode]()

# Tutorials for common use cases

- [Measuring the energy consumption of an AI model training]()
- [Monitoring an entire system]()

# Plugins reference

- [Measurement Sources](plugins/1_sources/_intro.md)
  - [grace-hopper: Grace and Grace Hopper superchips](plugins/1_sources/grace-hopper.md)
  - [nvidia-jetson: NVIDIA Jetson edge devices](plugins/1_sources/nvidia-jetson.md)
  - [nvidia-nvml: dedicated NVIDIA GPUs](plugins/1_sources/nvidia-nvml.md)
  - [perf: fine-grained Linux performance counters](plugins/1_sources/perf.md)
  - [procfs: system and per-process measurements](plugins/1_sources/procfs.md)
  - [quarch: query a Quarch module](plugins/1_sources/quarch.md)
  - [rapl: x86 CPU energy consumption](plugins/1_sources/rapl.md)
  - [raw-cgroups: Linux control groups accounting](plugins/1_sources/raw-cgroups.md)
  - [Integration with HPC platforms]()
    - [oar: measure OAR jobs](plugins/1_sources/oar.md)
    - [slurm: measure Slurm jobs](plugins/1_sources/slurm.md)
    - [kwollect-input: pull measurements from kwollect](plugins/1_sources/kwollect-input.md)
  - [k8s: measure Kubernetes pods](plugins/1_sources/k8s.md)
- [Data Transforms](plugins/2_transforms/_intro.md)
  <!-- - [aggregation: aggregate data]() -->
  - [energy-attribution: attribute the energy consumed by the hardware to the software](plugins/2_transforms/energy-attribution.md)
  - [energy-estimation-tdp: estimate the energy consumption when it cannot be measured](plugins/2_transforms/energy-estimation-tdp.md)
  - [process-to-cgroup-bridge: Turn per-process data into per-cgroup data](plugins/2_transforms/process-to-cgroup-bridge.md)
- [Measurement Outputs](plugins/3_outputs/_intro.md)
  - [CSV files](plugins/3_outputs/csv.md)
  - [ElasticSearch / OpenSearch](plugins/3_outputs/elasticsearch.md)
  - [InfluxDB](plugins/3_outputs/influxdb.md)
  - [Kwollect API](plugins/3_outputs/kwollect-output.md)
  - [MongoDB](plugins/3_outputs/mongodb.md)
  - [OpenTelemetry](plugins/3_outputs/opentelemetry.md)
  - [Prometheus](plugins/3_outputs/prometheus-exporter.md)
- [Special plugins](plugins/special/_intro.md)
  - [Relay client and server](plugins/special/relay.md)
  - [socket-control](plugins/special/socket-control.md)

# Community

- [Who is behind ALUMET?]()
- [Contributing]()
