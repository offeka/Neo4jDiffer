from dataclasses import dataclass, asdict

from TestGraphGenerator.GraphModels.PersonNode import Person


def generate_query_string(obj) -> str:
    for key, value in asdict(Person('test')).items():
        print(key, type(value))
