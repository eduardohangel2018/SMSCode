from flask import jsonify, request, g, url_for, current_app
from . import api
from .decorators import permission_required
from .errors import forbidden
from .. import db
from ..models import Topic, Permission
from flask_login import current_user


@api.route('/topics/', methods=['GET'])
def get_topics():
    page = request.args.get('page', 1, type=int)
    pagination = Topic.query.paginate(
        page, per_page=current_app.config['FLASK_TOPICS_PER_PAGE'],
        error_out=False)
    topics = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_topics', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_topics', page=page+1)
    return jsonify({
            'topics': [topic.to_json() for topic in topics],
            'prev': prev,
            'next': next,
            'count': pagination.total
            })


@api.route('/topics/<int:id>', methods=['GET', 'POST'])
def get_topic(id):
    topic = Topic.query.get_or_404(id)
    return jsonify(topic.to_json())


@api.route('/topics/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_topic():
    topic = Topic.from_json(request.json)
    topic.author = current_user
    db.session.add(topic)
    db.commit()
    return jsonify(topic.to_json()), 201, {'Location': url_for('api.get_topic', id=topic.id)}


@api.route('/topics/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_topic(id):
    topic = Topic.query.get_or_404(id)
    if g.current_user != topic.author and not g.current_user.can(Permission.COMMENT):
        return forbidden('Usuário não possui permissao')
    topic.body = request.json.get('body', topic.body)
    db.session.add(topic)
    db.session.commit()
    return jsonify(topic.to_json())


