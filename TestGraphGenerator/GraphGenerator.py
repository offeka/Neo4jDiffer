from TestGraphGenerator.GraphModels.BaseModels.Node import Node

a = Node(node_type="person")
a['test'] = 'value'
print(a.generate_query_str())
