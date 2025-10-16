# Measurement Sources

Measurement **sources** produce new measurements by obtaining information.

With numerous sources, Alumet can easily run on a wide range of hardware devices and in multiple software environments.
To get the measurements that you want, you should enable the relevant plugins.
This section documents the plugins that provide new sources.

## System-specific Requirements

In general, a plugin will only work if the corresponding hardware (such as a GPU) or software environment (such as K8S) is available.
Most plugins that provide sources are only available on Linux operating systems.

Plugins are free to implement sources how they see fit.
They can read low-level hardware registers, call a native library, read files, etc.
Therefore, some plugins may require extra permissions or external dependencies.

Refer to the documentation of a particular plugin to learn more about its requirements.
