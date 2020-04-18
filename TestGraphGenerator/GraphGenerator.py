from TestGraphGenerator.GraphModels.BaseModels.Node import Node

a = Node(node_type="person")
a['test'] = 'value'
print(a._generate_query_str())
