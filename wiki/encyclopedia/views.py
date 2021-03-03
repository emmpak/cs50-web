from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2

from . import util


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
      "title": title.capitalize()
  })
  else:
    return render(request, "encyclopedia/error.html",{
      "title": title.capitalize()
    })

def search(request):
  query = request.POST.get('q').lower()
  entries = [entry.lower() for entry in util.list_entries()]
  if query in entries: 
    return redirect('wiki:entry', title=query)
  else:
    filtered = [entry for entry in entries if entry.startswith(query)]
    return render(request, "encyclopedia/search.html", {
      "entries": filtered
    })
  # return HttpResponseRedirect(reverse("wiki:entry", kwargs={'titel': query}))



# [entry.lower() for entry in entries] - map
# [entry for entry in entries if entry.lower().startswith('cs')] - filter