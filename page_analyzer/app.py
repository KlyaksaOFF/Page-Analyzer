import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from .database import (
    create_url,
    detail_url,
    get_url_checks,
    insert_url_checks,
    select_url,
    find_by_url_name
)
from .validate import validate_url

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

with app.app_context():
    from .database import init_db
    init_db()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def urls():
    urls = select_url()
    return render_template("urls.html", urls=urls)


@app.post('/urls')
def create_page():
    url = request.form.get('url')
    normal = validate_url(url)

    if not normal:
        flash("Некорректный URL", "danger")
        return redirect(url_for('index'))

    existing = find_by_url_name(normal)
    if existing:
        flash('Страница уже существует', 'info')
        return redirect(url_for('detail', url_id=existing['id']))
    url_id = create_url(normal)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('detail', url_id=url_id))

@app.route('/urls/<int:url_id>')
def detail(url_id):
    url_data = detail_url(url_id)
    if not url_data:
        return 'Сайт не найден', 404
    detail = {'id': url_data[0], 'name': url_data[1], 'created_at': url_data[2]}
    check = get_url_checks(url_id)
    return render_template("detail.html",
                           url_id=url_id, url=detail, check=check)


@app.post('/urls/<int:url_id>/checks')
def check_url(url_id):
    url_data = detail_url(url_id)

    if not url_data:
        return 'Сайт не найден', 404

    try:
        response = requests.get(url_data[1])
        status_code = response.status_code
        soup = BeautifulSoup(response.text, 'html.parser')

        h1_tag = soup.find('h1')
        h1 = h1_tag.text if h1_tag else ''
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else ''
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'] \
            if description_tag and description_tag.get('content') else ''

        if status_code >= 500:
            flash('Произошла ошибка при проверке', 'danger')
        else:
            if 400 <= status_code < 500:
                flash('Сервер ответил с ошибкой', 'warning')
            else:
                flash('Страница успешно проверена', 'success')
            insert_url_checks(url_id, status_code, h1, title, description)
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('detail', url_id=url_id))
