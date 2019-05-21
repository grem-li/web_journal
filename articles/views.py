import re
import json

from django.shortcuts import render
from django.http import HttpResponse
from .models import Article


name_re = re.compile(r"^(?P<format>(" + '|'.join([f[1] for f in Article.FORMAT_CHOICES]) + "))/(?P<slug>[^/\s]+)$")

def articles_list(request):
    if request.method != 'GET':
        return HttpResponse(f"Method {request.method} not supported", status=405)

    data, names, slugs = {}, [], set()
    # TODO в случае отсуствия names неплохо бы отдавать все статьи, но при наличии pagination
    for name in request.GET.get('names', '').split(','):
        if not name:
            continue
        match = name_re.match(name)
        if not match:
            return HttpResponse(f"Name '{name}' not supported", status=400)
        names.append(name)
        slugs.add(match.groupdict()['slug'])
    if slugs:
        for article in Article.objects.filter(slug__in=list(slugs)):
            data[str(article)] = article
        not_found_names = set(names) - set(data.keys())
        if not_found_names:
            return HttpResponse(f"Articles {list(not_found_names)} not found", status=404)

    return HttpResponse(
        json.dumps({'status': 'ok', 'data': [dict(data[name]) for name in names]}, indent=4),
        content_type="application/json"
    )
