from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
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

class NewPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(
        widget=forms.Textarea()
    )

def add(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            title = form.cleaned_data['title']
            if title in entries:
                return render(request, "encyclopedia/add.html", {
                    "form": form,
                    "error": "Entry exists!"
                })
            else:
                content = form.cleaned_data['content']
                f = open(f"entries/{title}.md", "w")
                f.write(content)
                f.close()
                return render(request, "encyclopedia/entry.html", {
                    "entry": util.get_entry(title),
                    "title": title
                })
    return render(request, "encyclopedia/add.html",{
        "form" : NewPageForm()
    })