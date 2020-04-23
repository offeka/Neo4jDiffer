# Neo4jDiffer
Manages and checks for modifications in between 2 graphs.
Can also generate graphs for testing and model them as a sort of ogm.

## Usage
### GraphModeler
Allows you to create a random graph for testing and manage said graph in and out of neo4j.
#### Run as a cli 
download the project and run python `python GraphGenerator.py --help`
for example lets say we want to generate a graph with a high chance of connection and 
we'll run `python GraphGenerator.py generate -n PATH_TO_NAMES_FILE -o OUTPUT_FILE -c 10`
more info can be found in the cli help option
