from django.shortcuts import render
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

