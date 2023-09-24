from django.shortcuts import render, redirect
from django import forms
import markdown2
import random
from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    page_content = util.get_entry(title)
    if not page_content:
        return render(
            request, "encyclopedia/error.html", {"message": "Page not found."}
        )

    html_content = markdown2.markdown(page_content)
    return render(
        request,
        "encyclopedia/entry.html",
        {"title": title, "html_content": html_content},
    )


def search(request):
    query = request.GET["query"]
    entry_content = util.get_entry(query)
    if entry_content:
        return redirect("entry", title=query)
    else:
        search_results = []
        entries = util.list_entries()
        for entry in entries:
            if query.lower() in entry.lower():
                search_results.append(entry)
        return render(
            request,
            "encyclopedia/search.html",
            {"search_results": search_results, "query": query},
        )


def create_new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(
                    request,
                    "encyclopedia/error.html",
                    {"message": "Page already exists. Try again."},
                )
            util.save_entry(title, content)
            return redirect("entry", title=title)
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/create_new_page.html", {"form": form})


def edit_page(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("entry", title=title)
    else:
        content = util.get_entry(title)
        form = NewPageForm({"title": title, "content": content})
        return render(request, "encyclopedia/edit.html", {"title": title, "form": form})


def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect("entry", title=title)
