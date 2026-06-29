# Measuring the energy consumption of an AI model during training & inference

This page explains how to monitor an AI model deployed locally during training and inference.

This provides plugin configuration examples. Depending on your hardware, the required plugins may slightly vary. Refer the page of each plugin to find the corresponding configuration to put in `alumet-config.toml`.

The 3 key components in an AI workflow that need monitoring are the **CPU**, the **RAM** and the **GPU** (if you have one).

## Energy consumption

For the **CPU** and **RAM**, you should enable the plugin **RAPL** if it is supported. \
If not supported, you should use **EnergyEstimationTdpPlugin**, which estimates the energy consumption of your processor based on its TDP (Thermal Design Power).

For the **GPU**, you should enable either the plugin **NVML** for NVIDIA GPUs or **AMD-GPU** for AMD GPUs.

## Component usage

If you want to monitor each component's usage, it is also possible !

For the **CPU** and **RAM**, the required plugin will vary depending on the environment:

* If the code runs inside a Kubernetes pod, a OAR or a Slurm job, you should enable respecively the **K8S**, **OAR** or **Slurm** plugin.
* For baremetal training & inference (as in : the code runs directly on your machine), you should enable the **cgroups** plugin.
* For Grid'5000 clusters, you should use **Kwollect-input** plugin

The relevant metrics are `cpu_time_delta`, `cpu_percent` for CPU usage and `memory_usage` for RAM usage.

For the **GPU**, **AMD** and **NVML** already provide different utilization metrics. \
There are different usage metrics corresponding to different parts of the GPU:

| Metric | Name (NVML) | Name (AMD) |
| - | - | - |
| GPU usage | `nvml_gpu_utilization` | `amd_gpu_activity_usage` (attribute "graphic_core") |
| SM (= compute units) usage | `nvml_sm_utilization` | `amd_gpu_process_compute_unit_occupancy` |
| VRAM usage | `nvml_memory_utilization` | `amd_gpu_activity_usage` (attribute "unified_memory_controller") |
| VRAM allocation | `nvml_gpu_memory_info` | `amd_gpu_memory_usage` (total) or `amd_gpu_process_memory_usage` (per process) |
