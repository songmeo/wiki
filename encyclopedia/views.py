from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title),
        "title": title
    })

def search(request):
    title = request.GET.get('q')
    entries = util.list_entries()
    if title in entries:
        return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title),
        "title": title
    })
    else:
        results = [e for e in entries if title in e]
        return render(request, "encyclopedia/search_result.html", {
            "results":  results
        })