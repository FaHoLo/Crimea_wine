from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import pandas
import datetime
import collections


def coollect_goods_by_category():
    all_goods = pandas.read_excel('wine.xlsx', na_values=['nan'], keep_default_na=False).to_dict(orient='record')
    goods_by_category = collections.OrderedDict()
    for good in all_goods:
        try:
            goods_by_category[good['Категория']]
        except KeyError:
            goods_by_category.update({good['Категория']: []})
        finally:
            goods_by_category[good['Категория']].append({
                    'name': good['Название'],
                    'sort': good['Сорт'],
                    'price': good['Цена'],
                    'image': good['Картинка'],
                    'profitable': good['Акция'],
            })
    goods_by_category.move_to_end('Напитки')
    return goods_by_category

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

years_delta = datetime.datetime.now().year - datetime.datetime(year=1920, month=1, day=1).year

rendered_page = template.render(
    years_delta=years_delta,
    goods_by_category=coollect_goods_by_category(),
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
