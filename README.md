# Neo4jDiffer
Manages and checks for modifications in between 2 graphs.
Can also generate graphs for testing and model them as an ogm (Object Graph Mapper).

## Usage
### GraphModeler
Allows you to create a random graph for testing and manage said graph in and out of neo4j.

#### Run as a cli 
Download the project and run python `python GraphGenerator.py`.

for example lets say we want to generate a graph with a high chance of connection and 
we'll run 

`python GraphGenerator.py -n PATH_TO_NAMES_FILE -o OUTPUT_FILE -c 10`

More info can be found in the builtin help funciton. just use `--help`

#### Run a module
Just import the `DatabaseGenerator` module and call `create_graph_map()` with a list of names 
from there you can use the `GraphModeler` to import or export the database.

### Neo4jManager
Allows you to load or clear neo4j database from a json file.

#### Run as a cli
In order to run the manager from the cli just run 
`python GraphManager.py` script. 

For example lets say we want to load a database json file to neo4j just run .

`python GraphManager.py load -u USERNAME -p PASSWORD -a DB_ADDRESS -d DATABASE_FILE` 

this will load the database json into neo4j from the file specified.

More info can be found in the builtin help funciton. just use `--help`

