# wikitree
A simple script to visualise wikipedia hyperlinks (inspiration: https://www.youtube.com/watch?v=Q2DdmEBXTpo&t=83s). 

## Usage
1. Clone the repo onto your machine
2. pip install the requirements using `pip install -r requirements.txt`
3. Run `python .\main.py --wordbag_path .\words.txt --create_graph Y --stop_at_philosophy Y` to create all branches from words in wordbag. The output will look like this: ![alt text](https://github.com/iakash2604/wikitree/blob/master/img/multi_branch.png)
4. The `--stop_at_philosophy` tag stops growth of branch once it reaches philosophy (since the above video claims most branches go through philosophy, it seemed like a significant place to stop)
5. The `--create_graph` will create a networkx graph to visualise the branches. 
6. Run `python .\main.py --single_branch water --create_graph Y` to get the branch for a single word. Use wordbag and `--wordbag_path` for multiple words. The single_branch for water is shown below. A loop happens over the Science node since we haven't used `--stop_at_philosophy Y`. ![alt text](https://github.com/iakash2604/wikitree/blob/master/img/single_branch.png)


### Todo
1. Make graph look prettier. Avoid overlaps. Maybe use google charts and create webpage
2. Give graph nodes on a branch the same color (like edge)
3. 
