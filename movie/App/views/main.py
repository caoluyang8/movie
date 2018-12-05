from flask import Blueprint,render_template,request,current_app,redirect,url_for
from flask.json import jsonify

from App.models import Movie
from flask_login import current_user
from App.extensions import cache

main = Blueprint('main',__name__)


@main.route('/')
def index():
    try:
        page = int(request.args.get('page',1))
    except:
        page = 1
    key = 'page'+str(page)
    value = cache.get(key)
    if not value:
        pagination = Movie.query.filter().paginate(page,current_app.config['PAGE_NUM'],False)
        data = pagination.items
        value = render_template('main/home.html',data=data,pagination=pagination)
        cache.set(key,value,timeout=60)
    return value

@main.route('/collections/')
def collections():
    data = current_user.favorites.all()
    return render_template('main/collections.html',data=data)

@main.route('/clear_cache/')
def clear_cache():
    cache.clear()
    return redirect(url_for('main.home'))

@main.route('/dofavorite/')
def dofavorite():
    try:
        id = request.args.get('id')
        if current_user.is_favorite(id):
            current_user.remove_favorite(id)
        else:
            current_user.add_favorite(id)
        return jsonify({'code': 200})
    except:
        return jsonify({'code': 500})