# OpenTelemetry Output Plugin

## Description

[OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/) (OTEL) is an open source observability framework and toolset designed to ease the integration of observability backends such as Jaeger, Prometheus, Elasticsearch, OpenSearch and more. While it offers vendor/tool-agnostic and auto-instrumentation capabilities, the backend (storage) and the frontend (visualization) of telemetry data are intentionally left to other tools.

The plugin developed is an exporter (push) which can be connected to the OTEL framework via a receiver.

## Configuration

The plugin can be configured via the alumet's config.toml file with the following options:

```toml
[plugins.opentelemetry]
collector_host = "http://localhost:4317"
prefix = ""
suffix = "_alumet"
append_unit_to_metric_name = true
use_unit_display_name = true
add_attributes_to_labels = true
push_interval_seconds = 15
```

## Examples

The plugin has been tested on both, local environment using docker-compose.yaml and a K8s.

### OpenSearch local example

[OpenSearch](https://opensearch.org/docs/latest/getting-started/intro/) is a distributed search and analytics engine that can be used as vector database, full-text search and observability backend for logs, metrics and traces.

The connection to OpenSearch was done following the [official Data Prepper tutorial](https://github.com/opensearch-project/data-prepper/tree/main/examples/metrics-ingestion-OTEL) which is a recommended ingestion pipeline tool which can be connected to OTEL as recommended [here](https://opensearch.org/blog/distributed-tracing-pipeline-with-opentelemetry/).

Notes:
- For clarity, I disconnected traces and metrics from other sources to better visualize in OpenSearch what comes from alumet.
- Also, the "logging" exporter is deprecated and needs to be updated.

```yaml
# data-prepper/examples/metrics-ingestion-otel/otel-collector-config.yml
receivers:
  # hostmetrics:
  #   collection_interval: 60s
  #   scrapers:
  #     cpu:
  #     memory:
  # prometheus:
  #   config:
  #     scrape_configs:
  #       - job_name: data-prepper
  #         metrics_path: /metrics/sys
  #         scrape_interval: 60s
  #         static_configs:
  #           - targets: ['data-prepper:4900']
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

exporters:
  debug: # Appears as "logging" but is deprecated
    verbosity: detailed
```

Alumet was left with the default configuration and resulted in the correct population of the OpenSearch database and ability to explore the data via the dashboards as shown in the figure below.

![demo](../../images/opentelemetry-opensearch-demo.png)

### Thanos K8s example

[Thanos](https://github.com/thanos-io/thanos) is a set of components that can be composed into a highly available metric system with unlimited storage capacity for Time Series Data Base (TSDB), which can be added seamlessly on top of existing Prometheus deployments. The component "Thanos Receive" has the Prometheus Remote Write API built in, on top of the functionality for long-term-storage and downsampling. Since the OTEL Exporter natively implements the Prometheus Remote Write protocol, it can directly upload TSDB blocks to the object storage bucket of Thanos even without an underlying Prometheus.

Alumet was configured as following and deployed in the host of a single-node K8s cluster which had an OTEL collector [using the operator](https://open-telemetry.github.io/opentelemetry-helm-charts) and Thanos.

```toml
# Alumet config
[plugins.opentelemetry]
collector_host = "http://my-otel-collector-exposed-service"
prefix = ""
suffix = "_alumet"
append_unit_to_metric_name = true
use_unit_display_name = true
add_attributes_to_labels = true
push_interval_seconds = 15
```

```yaml
# Otel values.yaml
# Top level field related to the OpenTelemetry Operator
opentelemetry-operator:
  # Field indicating whether the operator is enabled or not
  enabled: true
  manager:
    collectorImage:
      repository: otel/opentelemetry-collector-contrib
  # Sub-field for admission webhooks configuration
  admissionWebhooks:
    # Use Helm to automatically generate self-signed certificate.
    certManager:
      enabled: false
    autoGenerateCert:
      enabled: true
collectors:
  otelgateway:
    suffix: gateway
    replicas: 1
    mode: deployment
    enabled: true
    config:
      receivers:
        otlp:
          protocols:
            grpc:
              endpoint: 0.0.0.0:4317
      processors:
        batch:
          send_batch_size: 1024
          timeout: 1s
      exporters:
        prometheusremotewrite:
          endpoint: "http://my-thanos-receive-service.monitoring.svc.cluster.local:19291/api/v1/receive"

      service:
        pipelines:
          metrics:
            receivers:
              - otlp
            processors:
              - batch
            exporters: 
              - prometheusremotewrite
```

### Others

- ElasticSearch natively supports the OpenTelemetry protocol and can be integrated to an OTEL collector via the APM, refer to the [official documentation](https://www.elastic.co/guide/en/observability/current/apm-open-telemetry.html) for an example.
