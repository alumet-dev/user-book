# Measuring the energy consumption of an AI model during training & inference

This page explains how to monitor an AI model deployed locally during training and inference.

This provides plugin configuration examples. Depending on your hardware, the required plugins may slightly vary. Refer the page of each plugin to find the corresponding configuration to put in `alumet-config.toml`.

The 3 key components in an AI workflow that need monitoring are the **CPU**, the **RAM** and the **GPU** (if you have one).

## Energy consumption

For the **CPU** and **RAM**, you should enable the plugin `RAPL` if it is supported. \
If not supported, you should use `EnergyEstimationTdpPlugin`, which estimates the energy consumption of your processor based on its TDP (Thermal Design Power).

For the **GPU**, you should enable either the plugin **NVML** for NVIDIA GPUs or **AMD-GPU** for AMD GPUs.

## Component usage

If you want to monitor each component's usage, it is also possible !

For the **CPU** and **RAM**, the required plugin will vary depending on the environment:

* If the code runs inside a Kubernetes pod, a OAR or a Slurm job, you should enable respecively the `K8S`, `OAR` or `Slurm` plugin.
* For bare metal training & inference (as in : the code runs directly on your machine), you should enable the `cgroups` plugin.
* For Grid'5000 clusters, you should use `Kwollect-input` plugin

The relevant metrics are `cpu_time_delta`, `cpu_percent` for CPU usage and `memory_usage` for RAM usage.

For the **GPU**, `AMD` and `NVML` already provide different utilization metrics. \
There are different usage metrics corresponding to different parts of the GPU:

| Metric | Name (`NVML`) | Name (`AMD`) |
| - | - | - |
| GPU usage | `nvml_gpu_utilization` | `amd_gpu_activity_usage` (attribute "graphic_core") |
| SM (= compute units) usage | `nvml_sm_utilization` | `amd_gpu_process_compute_unit_occupancy` |
| VRAM usage | `nvml_memory_utilization` | `amd_gpu_activity_usage` (attribute "unified_memory_controller") |
| VRAM allocation | `nvml_gpu_memory_info` | `amd_gpu_memory_usage` (total) or `amd_gpu_process_memory_usage` (per process) |

## Configuration examples

Here are a few example of scenarios, and the corresponding Alumet plugins configuration:

**Scenario 1:**
* GPU: any NVIDIA GPU
* CPU : any RAPL compatible CPU
* Infra : Kubernetes

<details>
<summary>Alumet config file</summary>

```toml
[plugins.k8s]
k8s_api_url = "http://127.0.0.1:8080"
token_retrieval = "auto"
poll_interval = "5s"
annotate_foreign_measurements = false
annotate_containers = false

[plugins.rapl]
poll_interval = "1s"
flush_interval = "5s"
no_perf_events = false

[plugins.nvml]
poll_interval = "1s"
flush_interval = "5s"
skip_failed_devices = true
mode = "full"
```

</details>

**Scenario 2:**

* GPU: any AMD GPU
* CPU : any RAPL compatible CPU
* Bare metal (runs directly on your machine)

<details>
<summary>Alumet config file</summary>

```toml
[plugins.cgroups]
poll_interval = "5s"

[plugins.rapl]
poll_interval = "1s"
flush_interval = "5s"
no_perf_events = false

[plugins.amd-gpu]
poll_interval = "1s"
flush_interval = "5s"
skip_failed_devices = true
```

</details>

**Scenario 3:**
* GPU: any AMD GPU
* CPU : not RAPL compatible CPU
* Infra : Slurm

<details>
<summary>Alumet config file</summary>

```toml
[plugins.slurm]
poll_interval = "1s"
ignore_non_jobs = true
jobs_monitoring_level = "job"
add_source_in_pause_state = false
annotate_foreign_measurements = false

[plugins.rapl]
poll_interval = "1s"
flush_interval = "5s"
no_perf_events = false

[plugins.amd-gpu]
poll_interval = "1s"
flush_interval = "5s"
skip_failed_devices = true
```

</details>

| Component | GPU plugin | CPU plugin | Infra plugin |
| - | - | - | - |
| Scenario #1 | `NVML` | `RAPL` | `K8s` |
| Scenario #2 | `AMD` | `RAPL` | `Cgroups` |
| Scenario #3 | `AMD` | `RAPL` | `Slurm` |
