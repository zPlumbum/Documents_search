from elasticsearch import Elasticsearch
from db_worker import DbWorker


class ElasticsearchWorker:
    es = Elasticsearch(HOST="http://localhost", PORT=9200)
    _worker = DbWorker()

    def add_documents_to_index(self):
        if not self.es.indices.exists(index='documents'):
            self.create_index('documents')

        db_data = self._worker.get_data_from_db()
        for document in db_data:
            self.es.index(index='documents', doc_type='info', id=document['id'], document={'text': document['text']})
            print(f'Документ {document["id"]} добавлен в индекс')

    def search_document_by_id(self, doc_id):
        try:
            doc = self.es.get(index='documents', doc_type='info', id=doc_id)
            return doc
        except Exception as ex:
            print(ex)
            return {'error_message': 'Документа с таким id не существует'}

    def search_documents_by_query(self, query):
        try:
            body = {
                'size': 20,
                'query': {
                    'match': {
                        'text': query
                    }
                }
            }
            raw_docs = self.es.search(index='documents', body=body)['hits']['hits']

            docs_ids = []
            for raw_doc in raw_docs:
                docs_ids.append(int(raw_doc['_id']))
            return docs_ids
        except Exception as ex:
            print(ex)
            return {'error_message': 'Индекса с таким названием не существует'}

    def match_all_documents(self):
        body = {'size': 1500, 'query': {'match_all': {}}}
        try:
            raw_docs = self.es.search(index='documents', body=body)['hits']['hits']
            docs_ids = []
            for raw_doc in raw_docs:
                docs_ids.append(raw_doc['_id'])
            return docs_ids
        except Exception as ex:
            print(ex)
            return {'error_message': 'Индекса с таким названием не существует'}

    def delete_document_by_id(self, doc_id):
        try:
            self.es.delete(index='documents', doc_type='info', id=doc_id)
            print('Документ удален')
        except Exception as ex:
            print(ex)
            return {'error_message': 'Документа с таким id не существует'}

    def create_index(self, index_name):
        self.es.indices.create(index=index_name)


if __name__ == '__main__':
    elastic = ElasticsearchWorker()
    elastic.add_documents_to_index()
