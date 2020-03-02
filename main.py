from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import pandas
import argparse
import collections
from datetime import datetime


def main():
    parser = configure_parser()
    template = collect_index_template()
    render_index_page(template, parser)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

def configure_parser():
    parser = argparse.ArgumentParser(description='Программа запустит сайт авторского вина. В качестве аргумента передайте путь к Excel-файлу с данными о товарах.')
    parser.add_argument('goods_path', help='Путь к Excel-файлу с данными о товарах')
    return parser

def collect_index_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    return template

def render_index_page(template, parser):
    goods_path = parser.parse_args().goods_path
    years_delta = datetime.now().year - 1920
    rendered_page = template.render(
        years_delta=years_delta,
        goods_by_category=collect_goods_by_category(goods_path),
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

def collect_goods_by_category(goods_path):
    all_goods = pandas.read_excel(goods_path, na_values=['nan'], keep_default_na=False).to_dict(orient='record')
    goods_by_category = collections.OrderedDict()
    for good in all_goods:
        goods_by_category.setdefault(good['Категория'], []).append({
                'name': good['Название'],
                'sort': good['Сорт'],
                'price': good['Цена'],
                'image': good['Картинка'],
                'profitable': good['Акция'],
        })
    goods_by_category.move_to_end('Напитки')
    return goods_by_category

if __name__ == "__main__":
    main()
