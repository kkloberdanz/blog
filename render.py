#!/usr/bin/env python3


import os


def get_name(line):
    n_lt = 0
    n_gt = 0
    name = []
    for c in line:
        if c == '<':
            n_lt += 1
        elif c == '>':
            n_gt += 1
        elif (n_gt == n_lt) and (n_lt > 0):
            if c == '<':
                break;
            else:
                name.append(c)
    return ''.join(name)


def get_posttitle(filename):
    with open(filename) as f:
        for line in f:
            if 'class="posttitle"' in line:
                name = get_name(line).strip()
                return name


def populate_links(names):
    l = []
    for postname, postfile in names:
        dt = postfile.split('.')[0]
        s = f'<li><a href="{postfile}">[{dt}] {postname}</a></li>'
        l.append(s)
    return '\n'.join(l)


if __name__ == '__main__':
    template = open('templates/template.html').readlines()
    post_index = 0
    links_index = 0
    for i, line in enumerate(template):
        if line.strip() == '!POST!':
            post_index = i
            print(f'post index = {post_index}')
        elif line.strip() == '!LINKS!':
            links_index = i
            print(f'links index = {links_index}')
        if post_index and links_index:
            break

    if post_index <= 0:
        raise Exception('could not find post start')

    to_render = [
        fname
        for fname in os.listdir('templates')
        if fname != 'template.html'
    ]

    posts = sorted((
        f'{post}.html'
        for fname in to_render
        for post in [fname.split('.')[0]]),
        reverse=True
    )

    names = [
        (title, post)
        for post in to_render
        for title in [get_posttitle(os.path.join('templates', post))]
        if title is not None
    ]

    print('rendering:', names)
    first = True
    links = populate_links(names)
    print('links =', links)
    for name, filename in names:
        with open(os.path.join('templates', filename)) as f:
            lines = f.readlines()
        post_contents = template[:post_index] + lines + template[post_index+1:links_index] + [links] + template[links_index+1:]
        text = ''.join(post_contents)

        with open(filename, 'w') as f:
            f.write(text)
        if first:
            first = False
            with open(f'index.html', 'w') as f:
                f.write(text)
