# Lab 4: TCP Congestion Control

To setup the necessary dependencies for this lab, run these commands:

```shell
$ sudo apt update
$ git clone https://github.com/mininet/mininet.git
$ cd mininet
$ git tag
$ git checkout <latest-stable-version>
$ PYTHON=python3 util/install.sh -fnv
```

The code files for this lab have been modified so as to support usage without Python 2.

Since `tcp_probe` is deprecated, I have attempted to implement a custom `tcp_reno_verbose` kernel module included in this directory (although it is not working yet since it simply captures and logs non-Mininet network events instead, such as browsing activity, software updates, etc.). For more information, check [this](https://github.com/mininet/mininet/issues/1045), [this](https://stackoverflow.com/a/66211468), and [this](https://github.com/janev94/verbose_reno). Do check out the officially deprecated `net/ipv4/tcp_probe.c` file as well for further reference materials (available on the numerous forks and clones of the [official Linux kernel repository](https://github.com/torvalds/linux/)). Please take note that this workaround is super hacky and it might break your entire Ubuntu/Debian installation (since it fiddles around with your Linux kernel)!
