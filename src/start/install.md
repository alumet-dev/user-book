# Installing Alumet agent

> ⚠️&nbsp;&nbsp;**Alumet is currently in Beta**.
>
> If you have trouble using Alumet, do not hesitate to [discuss with us](https://github.com/alumet-dev/alumet/discussions), we will help you find a solution.
> If you think that you have found a bug, please [open an issue](https://github.com/alumet-dev/alumet/issues) in the repository.

There are three main ways to install the standard Alumet agent[^agent-note]:

1. 📦 Download [a pre-built package](#option-1-installing-with-a-pre-built-package). This is the simplest method.
2. 🐳 Pull a [docker image](#option-2-installing-with-podmandocker).
3. 🔵 Deploy in a K8S cluster [with a helm chart](#option-3-installing-in-a-k8s-cluster-with-helm).
4. 🧑‍💻 Use `cargo` to [compile and install Alumet from source](#option-4-installing-from-source). This requires a Rust toolchain, but enables the use of the most recent version of the code without waiting for a new release.

[^agent-note]: See also [difference between Alumet core and Alumet agent](/plugins_core_agent.md).

## Option 1: Installing with a pre-built package

[Go to the latest release](https://github.com/alumet-dev/alumet/releases/latest) on Alumet's GitHub page.
In the _Assets_ section, find the package that corresponds to your system.
For instance, if you run Ubuntu 22.04 on a 64-bits x86 CPU, download the file that ends with `amd64_ubuntu_22.04.deb`.

You can then install the package with your package manager.
For instance, on Ubuntu:

```sh
sudo apt install ./alumet-agent*amd64_ubuntu_22.04.deb
```

We currently have packages for multiples versions of Debian, Ubuntu, RHEL and Fedora.
We intend to provide even more packages in the future.

### What if I have a more recent OS?

The packages that contain the Alumet agent have very few dependencies, therefore an older package should work fine on a newer system.
For example, if you have Ubuntu 25.04, it's fine to download and install the package for Ubuntu 24.04.

To simplify maintenance, we don't release one package for each OS version, but we focus on LTS ones.

### My OS is not supported, what do I do?

Alumet should work fine on nearly all Linux distributions, but we do not provide packages for every single one of them.
Use another installation method (see below).

Alumet core is OS-agnostic, but the standard Alumet agent does not support Windows nor macOS yet[^agent-note].

## Option 2: Installing with Podman/Docker

Every release is published to the container registry of the `alumet-dev` organization.

Pull the latest image with the following command (replace `podman` with `docker` if you use docker):

```sh
podman pull ghcr.io/alumet-dev/alumet-agent
```

View more variants of the container image on the [`alumet-agent` image page](https://github.com/alumet-dev/alumet/pkgs/container/alumet-agent).

### Privileges required when running

Because Alumet has low-level interactions with the system, it requires some privileges.
The packages take care of this setup, but with a container image, you need to grant these capabilities manually.

To run `alumet-agent`, you need to execute (again, replace `podman` with `docker` if you use docker):

```sh
podman run --cap-add=CAP_PERFMON,CAP_SYS_NICE ghcr.io/alumet-dev/alumet-agent
```

### Launcher script (optional)

Let's simplify your work and make a shortcut: create a file `alumet-agent` somewhere.
We recommend `$HOME/.local/bin/` (make sure that it is in your path).

```sh
#!/usr/bin/bash
podman run --cap-add=CAP_PERFMON,CAP_SYS_NICE ghcr.io/alumet-dev/alumet-agent
```

Give it the permission to execute with `chmod +x $HOME/.local/bin/alumet-agent`, and voilà!
You should now be able to run the `alumet-agent` command directly.

## Option 3: Installing in a K8S cluster with Helm

To deploy Alumet in a Kubernetes cluster, you can use our [Helm](https://helm.sh/) chart to setup a database, an Alumet relay server, and multiple Alumet clients.
Please refer to [Distributed deployment with the relay mode](relay.md) for more information.

Quick install steps:

```sh
helm repo add alumet https://alumet-dev.github.io/helm-charts
helm install alumet-distributed alumet/alumet
```

Here, `alumet-distributed` is the name of your Helm release, you can put the name you want, or use `--generate-name` to obtain a new, unique name.
See the [Helm documentation](https://helm.sh/docs/intro/using_helm/).

## Option 4: Installing from source

**Prerequisite**: you need to [install the Rust toolchain](https://rustup.rs/).

Use `cargo` to compile the Alumet agent.

```sh
cargo install --git https://github.com/alumet-dev/alumet.git alumet-agent
```

It will be installed in the `~/.cargo/bin` directory.
Make sure to add it to your `PATH`.

To debug Alumet more easily, compile the agent in debug mode by adding the `--debug` flag (performance will decrease and memory usage will increase).
For more information on how to help us with this ambitious project, refer to the [Alumet Developer Book](https://alumet-dev.github.io/developer-book/).

### Privileges required

Because Alumet has low-level interactions with the system, it requires some privileges.
The packages take care of this setup, but with a container image, you need to grant these capabilities manually.

The easiest way to do is is to use `setcap` as `root` before running Alumet:

```sh
sudo setcap 'cap_perfmon=ep cap_sys_nice=ep' ~/.cargo/bin/alumet-agent
```

This grants the capabilities to the binary file `~/.cargo/bin/alumet-agent`.
You will then be able to run the agent directly.

Alternatively, you can also run the Alumet agent without doing `setcap`, and it will tell you what to do, depending on the plugins that you have enabled.

NOTE: running Alumet as root also works, but is not recommended.
A good practice regarding security is to grant the _least_ amount of privileges required.

## Post-install steps

Once the Alumet agent is installed, head over to [Running Alumet](./run.md).
