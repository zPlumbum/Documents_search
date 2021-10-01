from flask import Flask, request, jsonify
from elasticsearch_worker import ElasticsearchWorker
from db_worker import DbWorker


app = Flask(__name__)
elastic = ElasticsearchWorker()
db_worker = DbWorker()


@app.route('/documents/', methods=['GET'])
def get_documents_by_query():
    query = request.args.get('query')
    if query is None:
        return jsonify({'response': 'Please, input the search parameter'})

    docs_ids = elastic.search_documents_by_query(query)
    response = db_worker.get_documents_by_ids(docs_ids)
    return jsonify({'response': response})


@app.route('/documents/<int:doc_id>', methods=['DELETE'])
def delete_document_by_id(doc_id):
    e_res = elastic.delete_document_by_id(doc_id)
    db_res = db_worker.delete_document_by_id(doc_id)

    if e_res or db_res:
        return jsonify({'response': 'Document with this ID does not exist'})
    else:
        return jsonify({'response': 'Document has been deleted'})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
