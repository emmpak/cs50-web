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
  query = request.POST.get('q')
  return redirect('wiki:entry', title=query)
  # return HttpResponseRedirect(reverse("wiki:entry", kwargs={'titel': query}))

