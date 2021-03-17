from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .plot_generator import YoutubeAnalyzer, get_plot


def render_page(request):
    return render(request, "./analyzer/index.html")


def get_input(request):
    link = request.GET["youtube_link"]

    analyzer = YoutubeAnalyzer(link)
    dataset = analyzer.fetch_data()
    formated_dataset = analyzer.generate_data_set(dataset[0], analyzer.format_views(dataset[1]))
    formated_dataset_views = list(map(int, formated_dataset[1]))

    plot = get_plot(analyzer, formated_dataset_views, formated_dataset[0])

    return render(request, "analyzer/yt_details.html", {"plot": plot})





