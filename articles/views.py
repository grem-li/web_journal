import re
import json

from django.shortcuts import render
from django.http import HttpResponse
from .models import Article


name_re = re.compile(r"^(?P<format>(news|faq|longread))/(?P<slug>[^/\s]+)$")

def articles_list(request):
    if request.method != 'GET':
        return HttpResponse(f"Method {request.method} not supported", status=405)

    data = []
    # TODO в случае отсуствия names неплохо бы отдавать все статьи, но при наличии pagination
    for name in request.GET.get('names', '').split(','):
        if not name:
            continue
        try:
            name_dict = name_re.match(name).groupdict()
            article = Article.objects.get(**name_dict)
        except AttributeError:
            return HttpResponse(f"Name '{name}' not supported", status=400)
        except Article.DoesNotExist:
            return HttpResponse(f"article '{name}' not exist", status=404)
        data.append({'id': article.id, 'slug': article.slug, 'format': article.format, 'title': article.title})

    return HttpResponse(json.dumps({'status': 'ok', 'data': data}, indent=4), content_type="application/json")
