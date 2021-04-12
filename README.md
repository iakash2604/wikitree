# wikitree
A simple script to visualise wikipedia hyperlinks (inspiration: https://www.youtube.com/watch?v=Q2DdmEBXTpo&t=83s). 

## Usage
1. Clone the repo onto your machine
2. pip install the requirements using `pip install -r requirements.txt`
3. Run `python .\main.py --wordbag_path .\words.txt --create_graph Y --stop_at_philosophy Y` to create all branches from words in wordbag. 
4. The `--stop_at_philosophy` tag stops growth of branch once it reaches philosophy (since the above video claims most branches go through philosophy, it seemed like a significant place to stop)
5. The `--create_graph` will create a networkx graph to visualise the branches. 
6. Run `python .\main.py --single_branch water --create_graph Y --stop_at_philosophy Y` to get the branch for a single word. Use wordbag and `--wordbag_path` for multiple words
