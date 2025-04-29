<!-- markdownlint-disable first-line-h1 no-empty-links -->
[Introduction](intro.md)
[Why Alumet and not \<X\>?](why_alumet.md)
[Alumet plugins, core, agent](plugins_core_agent.md)

# Installation and Configuration

- [Installing Alumet](start/install.md)
- [Running Alumet](start/run.md)
- [Configuration file](start/config.md)
- [Distributed measurement with the "relay" mode]()

# Tutorials for common use cases

- [Measuring the energy consumption of an AI model training]()
- [Monitoring an entire system]()

# Plugins reference

- [Measurement Sources]()
  - [procfs: Linux system and process information]()
  - [rapl: x86 CPU energy consumption]()
  - [nvml: dedicated NVIDIA GPUs]()
  - [jetson: NVIDIA Jetson edge devices]()
  - [Integration with HPC batch schedulers]()
    - [oar3: measure OAR3 jobs]()
    - [oar2: measure OAR2 jobs]()
    - [slurm: measure Slurm jobs]()
  - [k8s: measure Kubernetes pods]()
- [Data Transforms]()
  - [aggregation: aggregate data]()
  - [energy-attribution: attribute the energy consumed by the hardware to the software]()
  - [energy-estimation-tdp: estimate the energy consumption when it cannot be measured]()
- [Measurement Outputs]()
  - [CSV files]()
  - [InfluxDB]()
  - [MongoDB]()
  - [ElasticSearch / OpenSearch]()
  - [OpenTelemetry](plugins/output/opentelemetry.md)
  - [Prometheus](plugins/output/prometheus.md)
- [Special plugins]()
  - [Relay client and server]()
  - [socket-control]()

# Community

- [Who is behind ALUMET?]()
- [Contributing]()
