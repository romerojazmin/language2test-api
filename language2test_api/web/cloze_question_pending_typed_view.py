from flask import request
from flask import json, jsonify, Response, blueprints
from language2test_api.models.cloze_question_pending_typed import ClozeQuestionPendingTyped, ClozeQuestionPendingTypedSchema
from language2test_api.extensions import db, ma
from language2test_api.web.common_view import language2test_bp
from language2test_api.decorators.crossorigin import crossdomain
from language2test_api.decorators.authentication import authentication
from language2test_api.providers.base_provider import BaseProvider
from language2test_api.providers.cloze_provider import ClozeProvider

cloze_question_pending_typed_schema = ClozeQuestionPendingTypedSchema(many=False)
cloze_question_pending_typed_schema_many = ClozeQuestionPendingTypedSchema(many=True)

provider = BaseProvider()
cloze_provider = ClozeProvider()

@language2test_bp.route("/cloze_question_pending_typed/count/<cloze_question_id>", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_cloze_question_pending_typed_count_by_cloze_question_id(cloze_question_id):
    return cloze_provider.get_count(ClozeQuestionPendingTyped, cloze_question_id)

@language2test_bp.route("/cloze_question_pending_typed/count", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_cloze_question_pending_typed_count():
    return provider.get_count(ClozeQuestionPendingTyped)

@language2test_bp.route("/cloze_question_pending_typed/<cloze_question_id>", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_cloze_question_pending_typed_by_cloze_question_id(cloze_question_id):
    id = request.args.get('id')
    if id:
        properties = ClozeQuestionPendingTyped.query.filter_by(id=id).first()
        result = cloze_question_pending_typed_schema.dump(properties)
        return jsonify(result)

    text = request.args.get('text')
    if text:
        properties = ClozeQuestionPendingTyped.query.filter_by(text=text).first()
        result = cloze_question_pending_typed_schema.dump(properties)
        return jsonify(result)

    properties = cloze_provider.query_all(ClozeQuestionPendingTyped, cloze_question_id)
    result = cloze_question_pending_typed_schema_many.dump(properties)
    return jsonify(result)

@language2test_bp.route("/cloze_question_pending_typed", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_cloze_question_pending_typed():
    id = request.args.get('id')
    if id:
        properties = ClozeQuestionPendingTyped.query.filter_by(id=id).first()
        result = cloze_question_pending_typed_schema.dump(properties)
        return jsonify(result)

    text = request.args.get('text')
    if text:
        properties = ClozeQuestionPendingTyped.query.filter_by(text=text).first()
        result = cloze_question_pending_typed_schema.dump(properties)
        return jsonify(result)

    properties = provider.query_all(ClozeQuestionPendingTyped)
    result = cloze_question_pending_typed_schema_many.dump(properties)
    return jsonify(result)

@language2test_bp.route("/cloze_question_pending_typed", methods=['POST'])
@crossdomain(origin='*')
@authentication
def add_cloze_question_pending_typed():
    try:
        data = request.get_json()
        data['id'] = provider.generate_id(field=ClozeQuestionPendingTyped.id)
        cloze_question_pending_typed = ClozeQuestionPendingTyped(data)
        db.session.add(cloze_question_pending_typed)
        db.session.commit()
        result = cloze_question_pending_typed_schema.dump(cloze_question_pending_typed)
        response = jsonify(result)
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

@language2test_bp.route("/cloze_question_pending_typed", methods=['PUT'])
@crossdomain(origin='*')
@authentication
def update_cloze_question_pending_typed():
    try:
        data = request.get_json()
        cloze_question_pending_typed = ClozeQuestionPendingTyped.query.filter_by(id=data.get('id')).first()
        if not cloze_question_pending_typed:
            cloze_question_pending_typed = ClozeQuestionPendingTyped.query.filter_by(text=data.get('text')).first()
        if cloze_question_pending_typed:
            db.session.commit()
            response = Response(json.dumps(data), 200, mimetype="application/json")
        else:
            response = Response(json.dumps(data), 404, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

@language2test_bp.route("/cloze_question_pending_typed", methods=['DELETE'])
@crossdomain(origin='*')
@authentication
def delete_cloze_question_pending_typed():
    try:
        data = request.get_json()
        cloze_question_pending_typed = ClozeQuestionPendingTyped.query.filter_by(id=data.get('id')).first()
        if not cloze_question_pending_typed:
            cloze_question_pending_typed = ClozeQuestionPendingTyped.query.filter_by(text=data.get('text')).first()
        if cloze_question_pending_typed:
            db.session.delete(cloze_question_pending_typed)
            db.session.commit()
            response = Response(json.dumps(data), 200, mimetype="application/json")
        else:
            response = Response(json.dumps(data), 404, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response
