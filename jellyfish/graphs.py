import networkx as nx
import fnss
import random
import copy

# I used this link to figure out random choices in Python
# https://stackoverflow.com/questions/26768065/how-to-extract-random-nodes-from-networkx-graph


def jellyfish(n, degree, num_hosts):
    """
    Generates a Jellyfish graph

    Parameters
    ----------
    n: int
      Number of switches

    degree: int
      degree for each switch (# of ports)
      Called "k" in jellyfish paper

    num_hosts: int
      number of edges dedicated to hosts per switch. Called "k-r" in jellyfish paper
      (r edges per switch go to other switches).

    Returns
    -------
    networkx.Graph
      A jellyfish graph
    """

    random.seed(42)

    #create all the switches
    G = nx.Graph()
    for i in range(n):
        G.add_node("switch_{}".format(i+1), type = "switch")

    switch_ports = degree-num_hosts # k - (k - r) = r
    print("Dedicated switch ports per switch: {}".format(switch_ports))

    while True: # randomly connect an edge between two unconnected switches

        #check if each switch already has no ports left open
        node_degrees = G.degree()
        raw_degrees = [val[1] for val in list(node_degrees)]
        min_degree = min(raw_degrees)
        if min_degree >= degree:
            break

        nodes_to_sample = [node for node in G.nodes() if node_degrees[node] < switch_ports]
        if len(nodes_to_sample) >= 2:
            random_nodes = random.sample(nodes_to_sample, 2)
        else:
            break

        if(G.has_edge(random_nodes[0], random_nodes[1])):
            # if all switches with open ports are already neighbors we can't add more edges
            finished = True
            for node1 in nodes_to_sample:
                #if there is a node to sample that is not already in neighbors
                for node2 in nodes_to_sample:
                    if node1 == node2:
                        continue
                    if node2 not in list(G.adj[node1]):
                        #then these nodes should be connected so we're not done
                        finished=False
            if(finished):
                break
        else:
            G.add_edge(random_nodes[0], random_nodes[1])

    for node in G.nodes(): # incorporate links with 2 or more open ports
        while switch_ports - G.degree()[node] >= 2:
            edge = random.choice(list(G.edges()))
            if(G.has_edge(node, edge[0])) or (G.has_edge(node, edge[1])):
                continue
            G.remove_edge(edge[0], edge[1])
            G.add_edge(node, edge[0])
            G.add_edge(node, edge[1])
            raw_degrees = [val[1] for val in list(G.degree())]

    # add @num_hosts servers to each switch
    expected_total_hosts = n*num_hosts
    hosts_added = 0
    pre_existing_nodes = copy.deepcopy(G.nodes())
    for node in pre_existing_nodes:
        for i in range(num_hosts):
            G.add_node("host_{}".format(hosts_added+1), type="host")
            G.add_edge("host_{}".format(hosts_added+1), node)
            hosts_added += 1

    print("Expected to add {} hosts".format(expected_total_hosts))
    print("Added {} hosts".format(hosts_added))

    switches = [node for node in G.nodes() if "switch" in node]
    hosts = [node for node in G.nodes() if "host" in node]
    for switch in switches:
        print("{} connected to: {}".format(switch, G.adj[switch]))
    for host in hosts:
        print("{} connected to: {}".format(host, G.adj[host]))

    return G

def fat_tree(k):
    """
    Generates a fat tree topology using: https://fnss.readthedocs.io/en/latest/apidoc/generated/fnss.topologies.datacenter.fat_tree_topology.html

    Parameters
    ----------
    k: int
      Number of ports per switch

    Returns
    -------
    fnss.DatacenterTopology
    """

    # Hacky patch to get fnss to work with networkx 2.3. a better
    # patch is submitted to fnss https://github.com/fnss/fnss/pull/27
    fnss.DatacenterTopology.node = property(lambda self: self.nodes)

    return fnss.fat_tree_topology(k)

def complete(n):
    """
    Generates a complete graph

    Parameters
    ----------
    n: int
      Number of nodes

    Returns
    -------
    networkx.Graph
      A complete graph
    """
    return nx.complete_graph(n)
