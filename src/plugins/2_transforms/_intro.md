# Data Transforms

Data **transforms** are functions that modify the measurements as they arrive (online processing).

To get the measurements that you want, you should enable the relevant plugins.
This section documents the plugins that provide transforms.

## Order of the Transforms

<div class="warning">
The order in which the transform functions are applied matters.

Some transforms only work properly if they run after other transforms.
</div>

With the standard Alumet agent, the transforms order is set to the order of the plugins' configuration.

For instance, if you have two plugins that provide transforms, `a` and `b`, and you want transform `a` to always run before transform `b`, your configuration should look like this:

```toml
# Run transforms of plugin a first, then run transforms of plugin b.
[plugins.a]
# ...

[plugins.b]
# ...
```
