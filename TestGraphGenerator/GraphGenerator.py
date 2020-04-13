from TestGraphGenerator.GraphModels.PersonNode import Person
from TestGraphGenerator.QueryGenerator.ClassConverter import generate_query_string

a = Person('test')
generate_query_string(a)
