from django.shortcuts import render
from django import forms
from . import util
from random import randint

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
class EditForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control col-md-5'})
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

def edit(request,title):
    f = open(f"entries/{title}.md", "r")
    content = f.read()
    f.close()
    form = EditForm(initial={'content':content})
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            f = open(f"entries/{title}.md", "w")
            f.write(content)
            f.close()
            return render(request, "encyclopedia/entry.html", {
                "entry": util.get_entry(title),
                "title": title
            })
    return render(request, "encyclopedia/edit.html", {
        "form": form
    })

def random(request):
    entries = util.list_entries()
    index = randint(0, len(entries) - 1)
    title = entries[index]
    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title),
        "title": title
    })