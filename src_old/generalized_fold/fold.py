import functools
import operator

def foldl(func, xs, initial):
  return functools.reduce(func, xs, initial)

def foldg(func_nodes, func_edges, graph, initial):
    newGraph = functools.reduce(func_nodes, graph.nodes, initial)
    return functools.reduce(func_edges, graph.edges, newGraph)

def foldt(func, tree, initial):
    for child in tree.getroot():
        new = func(child, initial)
        foldt(func, child, new)