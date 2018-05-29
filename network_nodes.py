#!/usr/bin/python3

from collections import deque
import random

class network_node:

  def __init__(self, node_id, tx_type):
    self.node_id   = node_id
    self.tx_type   = tx_type
    self.adj_nodes = set()

  def __eq__(self, other):
    return self.node_id == other.node_id    

  def __hash__(self):
    return hash(self.node_id)

  def __str__(self):
    return str(self.node_id)

  def __repr__(self):
    return self.__str__()

  def get_node_id(self):
    return self.node_id

  def has_room(self):
    return len(self.adj_nodes) < 8

  def set_tx_type(self, tx_type):
    self.tx_type = tx_type

  def get_tx_type(self):
    return self.tx_type

  def add_adj_node(self, adj_node):
    if(self.has_room()):
      self.adj_nodes.add(adj_node)

  def remove_adj_node(self, adj_node):
    if(adj_node in self.adj_nodes):
      self.adj_nodes.remove(adj_node)

  def is_adj(self, node):
    return node in self.adj_nodes

  def get_adj_nodes(self):
    return self.adj_nodes

  def print_adj_nodes(self):
    print("{ ", self.node_id, " - ", self.tx_type, " : ", end='', sep='')
    print(self.adj_nodes, end='', sep='')
    print(" }")

class network:

  def __init__(self, num_nodes):
    self.nodes    = {}
    self.node_ids = set()

    for i in range(1, num_nodes + 1):
      self.add_node(i, random.randint(0, 2))

  def add_node(self, node_id, tx_type):
    if(node_id not in self.node_ids):
      self.node_ids.add(node_id)
      self.nodes[node_id] = network_node(node_id, tx_type)

  def connect_nodes(self, a, b):
    if(a in self.node_ids and b in self.node_ids):
      node_a = self.nodes[a]
      node_b = self.nodes[b]

      if(node_a.get_tx_type() != node_b.get_tx_type() and node_a.has_room() and node_b.has_room()):
        node_a.add_adj_node(node_b)
        node_b.add_adj_node(node_a)

  def get_path(self, a, b):

    to_visit  = deque()
    visited   = set()
    traversed = {}
    path      = []
    found     = False

    to_visit.append(a)
    traversed[self] = self

    while(len(to_visit) and not found):
      node = to_visit.popleft()

      if(node == b): 
        while(node != a):
          path.append(node)
          node = traversed[node]

        path.append(a)
        path.reverse()
        print(path)
        found = True
      
      elif(node not in visited):
        visited.add(node)

        for i in node.get_adj_nodes():
          if(i not in to_visit and i not in visited):
            to_visit.append(i)
            traversed[i] = node

    return path

  def get_hop_count(self, a, b):
    
    return len(self.get_path(a, b))

  def get_average_hop_count(self):
    num_hops = 0

    for id_a in self.node_ids:          
      for id_b in self.node_ids:
        if(id_a == id_b):
          continue
        
        hop_count = self.get_hop_count(self.nodes[id_a], self.nodes[id_b])
        
        if(hop_count == 0):
          print("something is jacked")
          return 0

        num_hops += hop_count

    return num_hops / (len(self.node_ids))

  def has_room(self):
    for id_a in self.node_ids:
      node_a = self.nodes[id_a]

      if(node_a.has_room()):
        for id_b in self.node_ids:
          node_b = self.nodes[id_b]
          if(node_a == node_b):
            continue
          if(not node_a.is_adj(node_b) and node_b.has_room() and node_a.get_tx_type() != node_b.get_tx_type()):
            return True

    return False

  def print_nodes(self):
    for node_id in self.node_ids:
      node = self.nodes[node_id]
      node.print_adj_nodes()

for i in range(2, 4):

  best_net = ""
  best_hop = 10000
  num_best_hops = 0
  num_unreach = 0

  print(i)

  for j in range(0, 10):
    
    net = network(i)
    count = 0

    while(net.has_room() and count < 2000):
      count += 1

      id_a = random.randint(0, i)
      id_b = random.randint(0, i)

      if(id_a != id_b):
        net.connect_nodes(id_a, id_b)

    if(count >= 2000):
      print("Alg fucked on ", i, j)

    avg_hop = net.get_average_hop_count()

    if(avg_hop == 0):
      num_unreach += 1
    elif(avg_hop < best_hop):
      best_hop = avg_hop
      num_best_hops = 1
      best_net = net
    elif(avg_hop == best_hop):
      num_best_hops += 1
  
  dat = "num_nodes = " + str(i) + " best hop = " + str(best_hop) + " num times = " + str(num_best_hops)
  print(dat)
  best_net.print_nodes()

