import requests
from bs4 import BeautifulSoup
import argparse
import networkx as nx
import matplotlib.pyplot as plt


def make_wiki_link_from_word(word):
    return "https://en.wikipedia.org/wiki/" + word.capitalize()


def get_first_link_in_wiki_article(link):

    resp = requests.get(link)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        p_s = soup.find_all('p')

        for p in p_s:
            a_s = p.find_all('a')
            for a in a_s:
                if a['href'].endswith(".ogg") or a['href'].endswith("NOTRS"):
                    continue
                try:
                    if a['href'].split("/")[-2] == "wiki":
                        ok = "https://en.wikipedia.org"+a['href']
                        return ok
                except:
                    continue

    return "failed at: "+link


def convert_edgeset_nodelist_data(edge_set):

    nodelist_data = []

    node_id = {}
    id_counter = 0
    for edge in edge_set:
        parent, child = edge
        if parent not in node_id.keys():
            node_id[parent] = id_counter
            id_counter = id_counter+1
        if child not in node_id.keys():
            node_id[child] = id_counter
            id_counter = id_counter + 1

        nodelist_data.append([node_id[child], child, node_id[parent], 2, 0])

    return nodelist_data


wordbag = ["Earring", "Insomnia", "Bottle", "Teacup",
           "Gradle", "Data", "Atom", "Control", "Music", "Squid"]
completed_words = []
edge_set = []

num = 0
for word in wordbag:
    num = num+1
    print("STATUS: "+str(num)+"/"+str(len(wordbag)))
    print("current word: "+word)
    link = make_wiki_link_from_word(word)
    new_link = get_first_link_in_wiki_article(link)

    if(new_link[:5] == "https"):
        new_word = new_link.split("/")[-1]
        print("new word: "+new_word)
        completed_words.append(word)
        edge_set.append([word, new_word])
        if ((new_word not in wordbag) and (new_word not in completed_words)):
            print("new word added: "+new_word)
            wordbag.append(new_word)
    else:
        print("word doesnt have future")

    print("##################")

g = nx.DiGraph()
g.add_edges_from(edge_set)
pos = nx.layout.spring_layout(g, iterations=60)

nx.draw_networkx(g, pos, node_size=node_size, bbox=dict(facecolor="skyblue",
                 edgecolor='black', boxstyle='round,pad=0.2'), font_size=10)
plt.show()
