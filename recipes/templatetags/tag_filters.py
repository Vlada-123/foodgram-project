from django import template

register = template.Library()


@register.filter
def tags_list(get):
    return get.getlist('tags')


@register.filter
def set_tag_qs(request, tag):
    new_request = request.GET.copy()
    tags = set(request.GET.getlist('tags'))
    if tag.name in tags:
        tags.remove(tag.name)
    else:
        tags.add(tag.name)
    new_request.setlist('tags', list(tags))
    return new_request.urlencode()


@register.filter
def tags_to_url_params(tags):
    url_param_tags = [f'tags={tag}' for tag in tags]
    return '&' + '&'.join(url_param_tags)
