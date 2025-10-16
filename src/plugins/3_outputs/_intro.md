# Measurement Outputs

Measurement **outputs** store the measurements or send them elsewhere.

To store/send the measurements where you want, you should enable the relevant plugins.
This section documents the plugins that provide outputs.

## Outputs in the pipeline

After all the [transforms](../transform/_intro.md) have processed a batch of measurements, it is given to the outputs.

Multiple outputs can be enabled at the same time.
Each output sees the same data.
