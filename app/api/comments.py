from flask import request, url_for, jsonify, current_app, g
from . import api
from .decorators import permission_required
from ..models import Comment, Topic, Permission
from app.models import db


@api.route('comments/')
def get_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_comment', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_comments', page=page + 1)
    return jsonify({
        'comments': [comments.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/comments/<int:id>', methods=['GET'])
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/topics/<int:id>/comments/', methods=['GET', 'POST'])
@permission_required(Permission.COMMENT)
def new_topic_comment(id):
    topic = Topic.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.topic = topic
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, {'Location': url_for('api.get_comment', id=comment.id)}

