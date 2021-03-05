from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from random import choice
import markdown2

from . import util

class NewEntryForm(forms.Form):
  title = forms.CharField(label="Title")
  markdown = forms.CharField(label="Markdown", widget=forms.Textarea)

class EditMarkdownForm(forms.Form):
  markdown = forms.CharField(label="Markdown", widget=forms.Textarea)

def is_part_of_entries(entry):
  entries = [entry.lower() for entry in util.list_entries()]
  return entry.lower() in entries

def index(request):
  return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
  })

def entry(request, title):
  markdown = util.get_entry(title)
  if(markdown):
    html = markdown2.markdown(markdown)
    return render(request, "encyclopedia/entry.html", {
      "entry": html,
      "title": title
  })
  else:
    return render(request, "encyclopedia/error.html",{
      "title": title
    })

def search(request):
  query = request.POST.get('q').lower()
  entries = [entry.lower() for entry in util.list_entries()]
  filtered = [entry for entry in entries if entry.startswith(query)]
  if query in filtered: 
    return redirect('wiki:entry', title=query)
  else:
    return render(request, "encyclopedia/search.html", {
      "entries": filtered
    })
  # return HttpResponseRedirect(reverse("wiki:entry", kwargs={'titel': query}))

def add(request):
  if request.method == 'POST':
    form = NewEntryForm(request.POST)
    if form.is_valid():
      title = form.cleaned_data['title']
      markdown = form.cleaned_data['markdown']
      if util.get_entry(title):
        return render(request, "encyclopedia/entry_exists_error.html")
      util.save_entry(title, markdown)
      return redirect('wiki:add')
    else:
      return render(request, "encyclopedia/add.html", {
        "form": form
      })
  else:
    return render(request, "encyclopedia/add.html",{
      "form": NewEntryForm()
    })

def random(request):
  return redirect('wiki:entry', title=choice(util.list_entries()))

def edit(request, title):
  if request.method == 'POST':
    form = EditMarkdownForm(request.POST)
    if form.is_valid():
      util.save_entry(title, form.cleaned_data['markdown'])
      return redirect('wiki:entry', title=title)
  else:
    markdown = util.get_entry(title)
    if(markdown):
      return render(request, "encyclopedia/edit.html", {
        "form": EditMarkdownForm(initial={'markdown': markdown}),
        "title": title
      })




# [entry.lower() for entry in entries] - map
# [entry for entry in entries if entry.lower().startswith('cs')] - filter