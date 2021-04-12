import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import random


def make_wiki_link_from_word(word):

    if(word[:5] == "https"):
        return word
    return "https://en.wikipedia.org/wiki/" + word.capitalize()


def get_word_from_wiki_link(link):

    if(link[:5] == "https"):
        return link.split("/")[-1]
    return link.capitalize()


def import_words(wordbag_path):

    f = open(wordbag_path, "r")
    words = []
    for line in f:
        if line is None:
            continue
        word = line.rstrip()
        word = word.capitalize()
        words.append(word)

    return words


def check_parenthesis(href, p):

    p = str(p)
    index = p.find(href)
    closed_brackets = 0
    open_brackets = 0
    while(index >= 0):
        index = index-1
        if(p[index] == "("):
            open_brackets = open_brackets+1
        if(p[index] == ")"):
            closed_brackets = closed_brackets+1

        if open_brackets > closed_brackets:
            return False

    return True


def get_first_link_in_wiki_article(link):

    resp = requests.get(link)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        try:
            table = soup.find('table')
            table.clear()
        except:
            pass
        p_s = soup.find_all('p')

        for p in p_s:
            a_s = p.find_all('a')

            for a in a_s:
                href = a['href']
                if href.endswith(".ogg") or href.endswith("NOTRS"):
                    continue
                try:
                    if href.split("/")[-2] == "wiki":
                        if(check_parenthesis(href, p)):
                            ok = "https://en.wikipedia.org"+href
                            return ok
                        else:
                            continue
                except:
                    continue

    return "failed"


def get_nodes_from_edge_set(edge_set):
    nodes = []
    for nodea, nodeb in edge_set:
        if(nodea not in nodes):
            nodes.append(nodea)
        if(nodeb not in nodes):
            nodes.append(nodeb)
    return nodes


def make_single_branch(first_link, stop_at_philosophy, hex_color):

    print("MAKING BRANCH FOR: "+get_word_from_wiki_link(first_link))
    first_link = make_wiki_link_from_word(first_link)
    next_link = first_link
    edge_set = []
    completed_links = []
    it = 0
    while(next_link != "failed"):
        current_link = next_link
        completed_links.append(current_link)
        it = it+1
        print(str(it)+". "+get_word_from_wiki_link(current_link))
        next_link = get_first_link_in_wiki_article(current_link)
        if (next_link in completed_links):
            break
        else:
            edge_set.append([get_word_from_wiki_link(
                current_link), get_word_from_wiki_link(next_link), hex_color])
            if stop_at_philosophy is not None and get_word_from_wiki_link(next_link) == "Philosophy":
                print("Philosophy")
                break
    print("BRANCH END")
    print("##################")
    return edge_set


def colored_growing_branch(wordbag, stop_at_philosophy):

    edge_set_total = []
    # colors = {
    #     'maroon': '#800000',
    #     'darkgreen': '#006400',
    #     'darkblue': '#00008b',
    #     'mediumorchid': '#ba55d3',
    #     'darkorange': '#ff8c00',
    #     'dodgerblue': '#1e90ff',
    #     'salmon': '#fa8072',
    #     'deeppink': '#ff1493',
    #     'lime': '#00ff00',
    # }

    colors = ['#800000', '#006400', '#00008b', '#ba55d3',
              '#ff8c00', '#1e90ff', '#fa8072', '#ff1493', '#00ff00', ]

    for i, word in enumerate(wordbag):
        hex_color = colors[i]

        edge_set_total = edge_set_total + \
            make_single_branch(word, stop_at_philosophy, hex_color)
        print(">>>>>>>>>>>>>>>>>REMAINING: "+str(len(wordbag)-1-i))
    return edge_set_total


def make_growing_branch(wordbag, stop_at_philosophy):
    completed_words = []
    edge_set = []

    num = 0
    for word in wordbag:
        num = num+1
        print("STATUS: "+str(num)+"/"+str(len(wordbag)))
        print("current word: "+word)
        if stop_at_philosophy is not None and word.capitalize() == "Philosophy":
            print("Skipping philosophy")
            print("##################")
            continue
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

    return edge_set


def draw_graph(edge_set):
    g = nx.DiGraph()
    color = []
    edges = []
    for edge in edge_set:
        color.append(edge[-1])
        edges.append(edge[:-1])

    g.add_edges_from(edges)
    pos = nx.layout.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_size=800, node_color="none")
    nx.draw_networkx_labels(g, pos, font_size=9, bbox=dict(
        facecolor="yellow", pad=0.2, alpha=0.15))
    nx.draw_networkx_edges(g, pos, connectionstyle='arc3, rad = 0.1',
                           width=1, arrows=True, edge_color=color, alpha=0.8)

    plt.show()


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
