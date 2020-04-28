# Jellyfish Reproduction

Hi! If you're trying to replicate these results, please scroll down to the Getting
Started subsection from the originally supplied starter code before continuing.
This README assumes that you have read everything from the originally forked repo's
README.
That information is available starting at the Overview subsection. There should
also be a disclaimer marking the information I added to the README and the
original README directly above the original README.

# Part 1: Paper Understanding

1. What are the main claims of the Jellyfish paper?

Jellyfish is a method of constructing data center topologies using random regular graphs that is more cost efficient than a fat tree topology. Jellyfish also supports as many as 27% more servers when running at full capacity than a fat tree topology for the same equipment with a scale for more than 900 servers. Further the authors claim that Jellyfish can support a larger number of servers using the same equipment setup for all of capacity, path length, and resilience at the same time.

2. What is the specific algorithm Jellyfish uses to generate a network?

The specific Jellyfish algorithm for generating a topology is given on the right side of page 3 as follows: "One can simply pick a random pair of switches with free ports (for the switch-pairs are not already neighbors), join them with a link, and repeat until no further links can be added. If a switch remains with ≥ 2 free ports (p1, p2) — which includes the case of incremental expansion by adding a new switch — these can be incorporated by removing a uniform-random existing link (x,y), and adding links (p1,x) and (p2,y). Thus only a single unmatched port might remain across the whole network."

3. If Jellyfish generates a network with parameters N=20, k=10, r=1, how many servers are connected to the network in total? How many other switches is each switch connected to? What about with N=20, k=10, r=5?

On page 3 it says, "With N racks, the network supports N(k − r) servers." Thus for N=20, k=10, r=1, there are 20(10-1) = 180 servers. Because r = 1, each ToR switch is connected to 1 other ToR switch. Note the paper says, "Each ToR switch i has some number ki of ports, of which it uses ri to connect to other ToR switches". For N=20, k=10, r=5 there are 20(10-5) = 100 servers and each switch is connected to 5 other switches since r = 5.

4. How might the process in Sec 4.2 that Jellyfish uses to incrementally expand a graph in Sec. 4.2 differ from a random regular graph? What complications might this difference present in implementing Jellyfish?

The Jellyfish expansion from the paper is as follows from page 7: "As an example, consider an expansion from an RRG(N, k, r) topology to RRG(N + 1, k, r). In other words, we are adding one rack of servers, with its ToR switch u, to the existing network. We pick a random link (v,w) such that this new ToR switch is not already con- nected with either v or w, remove it, and add the two links (u, v) and (u, w), thus using 2 ports on u. This process is repeated until all ports are filled (or a single odd port re- mains, which could be matched with another free port on an existing rack, used for a server, or left free). This completes incorporation of the rack, and can be repeated for as many new racks as desired." According to the [wikipedia article](https://en.wikipedia.org/wiki/Random_regular_graph), to create a random r-regular graph of size nr, you would randomly partition nr points into n buckets with r random points.

One problem might arise in that the method of expanding a Jellyfish topology might not yield a graph that can be properly modeled as a true RRG. The Jellyfish paper even notes their method for incremental expansion might not produce uniform random r-regular graphs, saying, "We note that our expansion procedures (like our con- struction procedure) may not produce uniform-random RRGs." This is potentially a major issue, as many of the assumptions and numerical models in the paper use the RRG model for estimating the effectiveness of Jellyfish.


5. What is a fat tree network? How many servers are in a fat tree network if each switch has degree four?
For more information, here is the original Fat tree paper and a paper about using fat trees in data centers

A fat tree network is a hierarchical topology modeled as a tree (traditionally a complete binary tree it seems). Links closer to the root of the tree have higher bandwidth than links closer to the leaves of the tree. The [second paper](http://www.cs.kent.edu/~javed/class-CXNET09S/papers-CXNET-2009/FaLV08-DataCenter-interconnect-p63-alfares.pdf) notes that "In general, a fat-tree built with k-port switches supports k^(3)/4 hosts." Thus for a fat tree network with degree four there would be 4^(3)/4 = 16 servers.

6. What is Bisection Bandwidth?

The paper defines bisection bandwidth; "Bisection bandwidth, a common measure of network capacity, is the worst-case bandwidth spanning any two equal-size partitions of a network."

7. What intuition does the paper give for why Jellyfish has higher bisection bandwidth than the fat tree network?

The paper states that a Jellyfish RRG topology can support higher bandwidth than a fat tree topology because the average path length in a jellyfish topology is shorter than the average path length in a fat tree. This is important because the average path length can be thought of as the "amount of network capacity consumed to deliver each byte". Obviously if one topology achieves the same throughput while using less capacity, it will be able to achieve greater throughput from the same capacity.

8. What is a graph with short paths (say a constant path length independent of the number of nodes, like three or four) but poor bisection bandwidth?

One example of a graph with with short paths but poor bisection bandwidth is a graph with degree 1, where each switch is connected to only one other switch. This will yield poor bisection bandwidth, because many flows will be bottlenecked by the links crossing the bisection partition, forcing the worst case bandwidth is be worse than if the degree were higher.


9. What are some of the challenges with building a Jellyfish network in practice (both mentioned by the paper, and others you can think of)? Does the paper do a good job addressing these challenges? Put it another way–suppose you were responsible for building a large datacenter. Would you use a jellyfish network? Why or why not?

Among practical challenges with a Jellyfish network mentioned by the paper, cabling is probably the least problematic. The paper details that mis-wiring is a small expense and even recoverable and that shorter wires can be used if switches are located together. The one exception to this statement is for massive data centers, where the number of containers requires expensive optical connectors that significantly increase cabling costs. However, this obstacle can also be larger overcome as detailed in the paper.

Outside of practical concerns the paper mentions, I would imagine it would be harder to tailor policy, monitoring, and remediation tools in a network environment that is configured randomly. Without the ability to probably control their network in a deterministic fashion, some operators might be turned off by the Jellyfish topology. If specific servers or switches must be physically grouped together, for training ML models online in production for example, a Jellyfish topology also wouldn't work as those elements would be randomly connected instead of deliberately grouped.

#Part 2: Paper Reproduction

1. This part was tricky to implement as the paper was underspecified. It seems possible that more than one unmatched port might remain in the case where there
are many switches with one unmatched remaining port. However, for the final version
of my implementation I couldn't seem to produce that error, so it's more likely
the algorithm in the paper is correct.

2. To generate figures 1a and 1b, run make figures (as detailed in the starter code
README). Note that the starter code seems to assume that each Jellyfish switch has the same number of linked hosts and that the starter code Makefile only used 16
switches instead of the 20 switches the fat tree topology uses. As Bruce mentioned
on Piazza, I did not change the original makefile and I used the starter code
assumption that each Jellyfish switch has the same number of linked hosts. For Figure 1b,
I colored all the switches blue and all the hosts red since it was hard to distinguish
between them with the starter code suggestion. Since it sometimes looks like
the topology is incorrect due to the way matplotlib draws the graph, I print to
stdout the connections of each switch and each host.

3. For 686 hosts on a fat tree k-nary topology we know that k=14 since k^(3)/4 = 686, k=14.
Thus we know that there will be 5(k/2)^(2) = 245 total switches (I used [this website](https://packetpushers.net/demystifying-dcn-topologies-clos-fat-trees-part2/) as a reference). Note that 686/245 = 2.8 hosts per switch. Since the starter code implementation relies on the
assumption that a constant number of hosts is attached to each switch, we round ```num_hosts``` (also called k-r) in the paper up to 3. This actually results in 735 hosts
for the jellyfish graph instead of 686 hosts for the fat tree graph. As result I tried a
different approach after initially implementing the above approach. I also tried n=98, degree = 14, and num_hosts = 7, since 98*7=686 and this gives us exactly 686 hosts.
This better approximates the number of hosts for 'same-equipment', while the prior attempt
better approximates the number of used switches for 'same-equipment'. In general
this approach seemed better and was almost identical to the given suggestion
in the assignment writeup.  You can modify the code
in figures.py on line 9 to ```jg = graphs.jellyfish(245, 14, 3)``` instead of ```jg = graphs.jellyfish(98, 14, 7)``` to generate the alternative graph.

4. For this part I used the suggest Bollobas lower bound from the assignment writeup.
I varied the num_hosts value for a constant N (this is equivalent to the \@n arg
for the jellyfish implementation) and a constant k (this is equivalent to a constant
\@degree arg for the jellyfish implementation). I substituted |S| (cardinality of S) in the
given equation for n/2, where n is the number of switches because we know each host is
connected to a switch and should not cross the partition and in a bisection partition the number ofswitches would be halved. I assumed that each link was the same bandwidth and that thus the normalized bisection
bandwidth should be equal to the number of links crossing the bisection (or the cardinality
of delta S) divided by the number of links between servers and switches within a given
network bisection partition. I was inspired by [this](https://piazza.com/class/k7m53jbmw0n6qf?cid=63) piazza post!
I also really tried to get the point markers to appear hollow by the ```markeredgecolor```
and ```markerfillcolor``` arguments for ```ax.plot``` made the markers themselves go
away entirely.

5. Figure 2b was harder to replicate than other figures. From a discussion during
office hours this weekend, this seems to be a common thread. To start, I assumed
the y-axis represented the number of ports in thousands, which the axis is labeled
as. However, the axis is also labeled as the equipment cost, which the paper
does not define well. Next, the paper mentions that this graph is for a full
bisection bandwidth, so I used the Bollobas approximation from the prior part
and found the lowest value of r for a given k, such that the normalized bisection
bandwidth was at least 1. This can be seen more precisely in code. Precisely, I found
that lowest value r such that ((1-sqrt(ln(2)/r))\*(r/2))/(k-r) >= 1. This follows
from the definition of bisection bandwidth from the previous problem. The slopes of
each Jellyfish line were lower than they appeared in the paper, but the lines were
in the correct order and gave the same intuition the figure in the paper sought to
inspire; that Jellyfish can provide as useful a network as Fat trees, but with fewer
switches (lower cost).

6. This graph was also difficult to reproduce. I used the same Jellyfish(98,14,7)
topology that uses 686 servers from part 3. The paper seems to rank about 2700 links
and this graph only had 2058 links, but the paper explicitly states that it is using
a Jellyfish topology with 686 hosts for the same equipment as a fat tree topology with
686 hosts. After going through this process, it seems the authors may have actually
used a Jellyfish topology with ```graphs.jellyfish(245, 14, 3)``` instead of ``` graphs.jellyfish(98, 14, 7)```, but this would give values that are too high for the
axis of the graph in the paper. I believe they might have randomly sampled. In
addition, this would mean the definition of "same equipment" changes throughout
the paper, so I will try to remain consistent in my wording if I am correct in this
hypothesis.
I initially tried computing paths using the networkx library, but these function calls never returned, even after
walking away from my computer and returning. I wanted to sort all paths, but this did not seem computationally feasible. As Bruce suggested on [Piazza](https://piazza.com/class/k7m53jbmw0n6qf?cid=43) I found all shortest paths instead for ECMP8, ECMP64, and
8-shortest paths. For efficiency's sake, I also randomly permuted the hosts twice
and matched one host and the source and the other as the destination by index,
generating paths for each source, destination pair. Generating all paths, the algorithm
took killed my kernel all three times I ran it. This optimization way suggested in
office hours if I remember correctly, and by Jeyla Aranjo.

#Part 3: Paper Extension

1. I read through all the given material

2. This was pretty confusing to start with but most of my errors were syntactical.

3. Getting routing working has been a huge pain. Even when I run the ```sudo jellyfish mn --graph='fat_tree' -k 4``` command specified in the README, everytime I run ```pingall``` at least one of the
switches does not connect to anything despite it being clear that the links were
added in the print statements above. I reloaded the vagrant VM but it does not seem
to work. I got it to work for k=2 for fat tree, but not for larger k. The test
itself does seem correct, it just mostly fails because something isn't working
correctly with mininet and/or the pox controller in the background. If you run
the test several times, it should return true at least once. I'm not sure if
it's totally random, but when it was behaving badly I would have to run the test
more than 10 times for it to complete. For some reason, it seems to return true
more often for ```G = jellyfish.graphs.jellyfish(20,4,1)``` than for ```G = jellyfish.graphs.jellyfish(16,4,1)```.

4. 

__Everything below this point is forked from the originally supplied starter code README.__
______________________________________________________________________________________________________________________
## Overview

This is the starter code for the [CS244 guided reproduction](https://docs.google.com/document/d/1vYp_pjUhnYvBnKkvGeUV7yh6g3UndBrVRNcMLRtMEw4/edit?usp=sharing) of [Jellyfish](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final82.pdf).

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

There are placeholder methods in `jellyfish/figures.py` for each figure you'll need to implement. Once implemented, you can generate a particular figure by runnning (e.g.):
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

[Jupyter](https://jupyter.org/) lets you run interactive Python notebooks, in which you can write python and draw graphs inline. We find that it dramatically improves our productivity over running a stand-alone script, especially if it takes a while to generate the data and we're making slight changes to graphs.

You are welcome to work on the project however you want, but if we were working on this project, we would make all the graphs in Jupyter and then move the code to `jellyfish/figures.py`. This would help get each graph done faster, and then we would be able to easily test and generate all the figures before turning in the project.

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

If you want to play around with mininet, it is installed in the usual way. You can do things like:
```
vagrant@ubuntu-bionic:/vagrant$ sudo mn
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2
*** Adding switches:
s1
*** Adding links:
(h1, s1) (h2, s1)
*** Configuring hosts
h1 h2
*** Starting controller
c0
*** Starting 1 switches
s1 ...
*** Starting CLI:
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2
h2 -> h1
*** Results: 0% dropped (2/2 received)
```

### Running tests

There are some very basic tests written for your Jellyfish graph generator in `tests/`. You will also need to write your own routing test. You can run the files on their own, or run them all together by running
```
vagrant@ubuntu-bionic:/vagrant$ make test
test_correct_degree (tests.test_jellyfish.TestJellyfishGenerator) ... ok
test_correct_number_hosts (tests.test_jellyfish.TestJellyfishGenerator) ... ok
test_correct_number_switches (tests.test_jellyfish.TestJellyfishGenerator) ... ok
test_jellyfish_hosts_reachable (tests.test_routing.TestRouting) ... ok

----------------------------------------------------------------------
Ran 4 tests in 1.191s

OK
```
