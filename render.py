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
                name = get_name(line)
                return name


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
            print(f'links index = {post_index}')
        if post_index and links_index:
            break

    if post_index <= 0:
        raise Exception('could not find post start')

    to_render = sorted((
        fname
        for fname in os.listdir('templates')
        if fname != 'template.html'),
        reverse=True
    )

    posts = sorted(
        f'posts/{post}.html'
        for fname in to_render
        for post in [fname.split('.')[0]]
    )

    names = [
        get_posttitle(os.path.join('templates', post))
        for post in to_render
    ]

    items = list(zip(to_render, posts, names))
    print('rendering:', items)
    first = True
    for filename, post, name in items:
        with open(os.path.join('templates', filename)) as f:
            lines = f.readlines()
        post_contents = template[:i] + lines + template[i+1:]
        text = ''.join(post_contents)

        with open(post, 'w') as f:
            f.write(text)
        if first:
            with open(f'index.html', 'w') as f:
                f.write(text)
                links = populate_lines(names, filename)
