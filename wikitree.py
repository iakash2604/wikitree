import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt


def make_wiki_link_from_word(word):

    if(word[:5] == "https"):
        return word
    return "https://en.wikipedia.org/wiki/" + word.capitalize()


def get_word_from_wiki_link(link):

    return link.split("/")[-1]


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


def make_single_branch(first_link):

    first_link = make_wiki_link_from_word(first_link)
    next_link = first_link
    edge_set = []
    completed_links = []
    while(next_link != "failed"):
        current_link = next_link
        completed_links.append(current_link)
        print(get_word_from_wiki_link(current_link))
        next_link = get_first_link_in_wiki_article(current_link)
        if (next_link in completed_links):
            break
        else:
            edge_set.append([get_word_from_wiki_link(
                current_link), get_word_from_wiki_link(next_link)])

    return edge_set


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


def make_growing_branch(wordbag):
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

    return edge_set


def draw_graph(edge_set):
    g = nx.DiGraph()
    g.add_edges_from(edge_set)
    pos = nx.layout.spring_layout(g, iterations=60)

    nx.draw_networkx(g, pos, node_size=1, bbox=dict(facecolor="skyblue",
                     edgecolor='black', boxstyle='round,pad=0.2'), font_size=10)
    plt.show()
