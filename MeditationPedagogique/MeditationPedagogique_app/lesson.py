def add_title(context, dirname, path):
    title = ''
    with open(dirname + path, 'r') as f:
        for line in f.readlines():
            title += line.strip()
    context['title'] = title
    return context
