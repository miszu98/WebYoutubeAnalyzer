from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import matplotlib
import random

import base64
from io import BytesIO


class YoutubeAnalyzer(object):
    def __init__(self, url):
        self.url = url

        options = Options()
        options.headless = True
        self.page = webdriver.Chrome(options=options, executable_path="C:\\Users\\micha\\Desktop\\ChromeDriver\\chromedriver.exe")
        self.page.get(url)
        self.soup = BeautifulSoup(self.page.page_source, "html.parser")

    def fetch_data(self):
        titles = self.soup.find_all("a", id="video-title")
        ts = [t.text for t in titles]
        views = self.soup.find_all("span", class_="style-scope ytd-grid-video-renderer")
        vs = [v.text.split("\xa0") for v in views]
        return ts, vs

    def format_views(self, list):
        formated_views = []

        for i in range(0, len(list), 2):
            if "." in list[i][1]:
                z = list[i][1].split(".")
            else:
                z = list[i][1].split(" ")
            if z[0] == "tys":
                if len(list[i][0]) <= 3:
                    if "," in str(list[i][0]):
                        formated_views.append(str(list[i][0]).replace(",", "") + "00")
                    else:
                        formated_views.append(str(list[i][0]) + "000")
            elif z[0] == "mln":
                if "," in str(list[i][0]):
                    how_many = 7 - len(str(list[i][0]).replace(",", ""))
                elif len(str(list[i][0])) == 1:
                    how_many = 7 - len(str(list[i][0]).replace(",", ""))
                else:
                    how_many = 8 - len(str(list[i][0]))
                formated_views.append(list[i][0].replace(",", "") + how_many * "0")
        return formated_views

    def generate_data_set(self, titles, views):
        return titles, views


def create_plot(analyzer, x, y):
    matplotlib.rc("font", **{"size": 16})
    fig, ax = plt.subplots(figsize=(22, 19))
    plt.ylabel("Movie titles", fontsize=35, labelpad=60)
    plt.xlabel("Views", fontsize=35, labelpad=30)
    ax.set_title(analyzer.soup.title.text, pad=50, fontsize=35)
    fig.subplots_adjust(left=0.4)
    colors = [(random.random(), random.random(), random.random()) for _ in range(len(x))]
    ax.barh(y, x, color=colors, align="center")
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph


def get_plot(analyzer, x, y):
    plt.switch_backend("AGG")
    create_plot(analyzer, x, y)
    graph = get_graph()
    return graph

