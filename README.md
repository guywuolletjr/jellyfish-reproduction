# Starter Code for Jellyfish Reproduction

## Overview

This is the starter code for the CS244 guided reproduction of [Jellyfish](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final82.pdf).

It provides a vagrant box with most of the tools you will need installed, and some structure for the project.

The code is structured as follows:
```
./Makefile - runs things
./tests - directory for tests
./tests/test_routing.py - test you will need to write to check mininet routing
./tests/test_jellyfish.py - basic tests for jellyfish graph generator
./jellyfish - source directory
./jellyfish/mininet.py - starts up mininet
./jellyfish/cli.py - does all the cli stuff so the jellyfish command works
./jellyfish/figures.py - generates the figures from paper
./jellyfish/graphs.py - generate graphs (jellyfish/fat tree/etc...)
./jellyfish/__init__.py - part of the jellyfish package
./README.md - This file
./setup.py - python packaging stuff so we can have a jellyfish command
./figures - directory for the figures you will make
./figures/complete_graph.png - a picture of a complete graph, generated by the example notebook.
./Vagrantfile - configuration for vagrant
./notebooks - directory for your notebooks
./notebooks/Example Notebook.ipynb - example notebook
./requirements.txt - python dependencies
```

## Getting Started

1. Install [git](https://git-scm.com/)
1. Install [Virtualbox](https://www.virtualbox.org/), tested with 6.0.18.
1. Install [Vagrant](https://www.vagrantup.com/), tested with Vagrant 2.2.7
1. Open up a terminal
1. Clone this repo, `$ git clone https://github.com/brucespang/jellyfish-reproduction.git`
1. `$ cd jellyfish-reproduction`
1. Run `$ vagrant up` to create your Vagrant box. This takes some time--it will download a VM from vagrant and set it up. For me, it took about 3 minutes.
1. Run `$ vagrant ssh` to log into the newly created box.

You should see something like this:
```
$ vagrant ssh
...
vagrant@ubuntu-bionic:~$ ls
mininet  pox
vagrant@ubuntu-bionic:~ ls /vagrant
figures  jellyfish  Makefile  notebooks  README.md requirements.txt  setup.py	tests  Vagrantfile
```

All the code in the `jellyfish-reproduction` repo should be available in the `/vagrant` directory in the virtual machine. You should be able to edit files on your host machine using your favorite editor, and vagrant will automatically sync them.

### Generating figures

There are placeholder methods in `jellyfish/figures.py` for each figure you'll need to implement. You can generate a particular figure by runnning (for example):
```
vagrant@ubuntu-bionic:/vagrant$ jellyfish figure_1c figures/figure_1c.png
```

You can generate all the figures by running
```
vagrant@ubuntu-bionic:/vagrant$ make figures
jellyfish figure_1c figures/figure_1c.png
jellyfish figure_2a figures/figure_2a.png
jellyfish figure_2b figures/figure_2b.png
jellyfish figure_9 figures/figure_9.png
jellyfish figure_1c_mininet figures/figure_1c_mininet.png
jellyfish table_1 figures/table_1.txt
```

### Running Jupyter

[Jupyter](https://jupyter.org/) is a way to run an interactive Python notebook, you can write python and draw graphs inline. We find that it dramatically improves our productivity over running a stand-alone script, especially if it takes a while to generate the data and we're making slight changes to a standalone script.

You are welcome to work on the project however you want, but if we were working on this project, we would make all the graphs in Jupyter and then move the code to `jellyfish/figures.py`. This would help get each graph done faster, and then we would be able to easily generate all the figures before turning in the project.

You can start the jupyter notebook server by running the following. There's an example notebook in `notebooks/Example Notebook.ipynb`

```
vagrant@ubuntu-bionic:/vagrant$ jupyter notebook --ip=0.0.0.0
```

You should be able to access the notebook server from your *host* computer using one of the URLs. For me, the url looks like [http://127.0.0.1:8888/?token=40d8fdab98ce2be96ac5cafa6ed610a509b7e5c977c60fd1](http://127.0.0.1:8888/?token=40d8fdab98ce2be96ac5cafa6ed610a509b7e5c977c60fd1) but your token will be different.

*Note:* This works by forwarding port 8888 on the host machine to port 8888 on the local machine, and is configured in the Vagrantfile. It's important that you use the `--ip=0.0.0.0` so that Jupyter listens on all interfaces and that the port forwarding works.

### Running mininet

There's some placeholder code in `jellyfish/mininet.py` you will need to fill in which turns the graph you generated in part 2 of the assignment into a mininet topology. Once you have, you can start mininet by running
```
vagrant@ubuntu-bionic:/vagrant$ sudo jellyfish mn --graph='fat_tree' -k 4
...
*** Starting CLI:
mininet>
```

### Running tests

There are some very basic tests written for your Jellyfish graph generator in `tests/`. You will also need to write your own routing test. You can run the files on their own, or run them all together by running
```
vagrant@ubuntu-bionic:/vagrant$ make test
sudo python tests/test_routing.py
.
----------------------------------------------------------------------
Ran 1 test in 1.265s

OK
python tests/test_jellyfish.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.037s

OK```