# Installing Alumet agent

> ⚠️&nbsp;&nbsp;**Alumet is currently in Beta**.
>
> If you have trouble using Alumet, do not hesitate to [discuss with us](https://github.com/alumet-dev/alumet/discussions), we will help you find a solution.
> If you think that you have found a bug, please [open an issue](https://github.com/alumet-dev/alumet/issues) in the repository.

There are three main ways to install the standard Alumet agent[^agent-note]:

1. 📦 Download [a pre-built package for the last stable release](#installing-with-a-pre-built-package). This is the simplest method.
2. 🐳 Pull a [docker image for the last stable release](#installing-with-docker).
3. 🧑‍💻 Use `cargo` to [compile and install Alumet from source](#installing-from-source). This requires a Rust toolchain, but enables the use of the most recent version of the code without waiting for a new release.

[^agent-note]: See also [difference between Alumet core and Alumet agent](/plugins_core_agent.md).

## Installing with a pre-built package

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

To simplify maintainance, we don't release one package for each OS version, but we focus on LTS ones.

### My OS is not supported, what do I do?

Alumet should work fine on nearly all Linux distributions, but we do not provide packages for every single one of them.
Use another installation method (see below).

Alumet core is OS-agnostic, but the standard Alumet agent does not support Windows nor macOS yet[^agent-note].

## Installing with Docker

Every release is published to the container registry of the `alumet-dev` organization.
Go to the [`alumet-agent` image page](https://github.com/alumet-dev/alumet/pkgs/container/alumet-agent) to pull the docker image.

## Installing from source

**Prerequisite**: you need to [install the Rust toolchain](https://rustup.rs/).

Use `cargo` to compile the Alumet agent.

```sh
cargo install --git https://github.com/alumet-dev/alumet.git alumet-agent
```

It will be installed in the `~/.cargo/bin` directory.
Make sure to add it to your `PATH`.

To debug Alumet more easily, compile the agent in debug mode by adding the `--debug` flag (performance will decrease and memory usage will increase).
For more information on how to help us with this ambitious project, refer to the [Alumet Developer Book](https://alumet-dev.github.io/developer-book/).

## Post-install steps

Once the Alumet agent is installed, head over to [Running Alumet](./run.md).
