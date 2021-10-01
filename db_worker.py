from sqlalchemy.orm import sessionmaker
from models import Document
import sqlalchemy as sq
import csv
from datetime import datetime


class DbWorker:
    DSN = 'postgresql://your_username:your_password@localhost:5432/your_database'
    _engine = sq.create_engine(DSN)
    _Session = sessionmaker(bind=_engine)
    _session = _Session()

    def create_table_in_db(self):
        with self._engine.connect() as connection:
            connection.execute('''CREATE TABLE if not exists Document (id serial primary key,
            rubrics varchar(200) not null, text text not null, created_date varchar(20) not null);''')

    def upload_data_to_db(self):
        raw_data = csv_reader('posts.csv')
        data = []
        for item in raw_data:
            document = Document(rubrics=item['rubrics'], text=item['text'], created_date=item['created_date'])
            data.append(document)
        self._session.add_all(data)
        self._session.commit()

    def get_document_by_id(self, doc_id):
        try:
            query = self._session.query(Document).filter(Document.id == doc_id)
            response = {
                'id': query[0].id,
                'text': query[0].text,
                'rubrics': query[0].rubrics,
                'created_date': query[0].created_date
            }
            return response
        except Exception as ex:
            print(ex)
            return {'error_message': 'Документа с таким id не существует'}

    def get_documents_by_ids(self, doc_ids_list):
        response = []
        for doc_id in doc_ids_list:
            query = self._session.query(Document).filter(Document.id == doc_id)
            response.append({
                'id': query[0].id,
                'text': query[0].text,
                'rubrics': query[0].rubrics,
                'created_date': query[0].created_date.isoformat().replace('T', ' ')
            })
        response = sorted(response, key=lambda x: datetime.strptime(x['created_date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
        return response

    def get_data_from_db(self):
        query = self._session.query(Document)
        data_list = []
        for item in query:
            data_list.append({
                'id': item.id,
                'text': item.text,
                'rubrics': item.rubrics,
                'created_date': item.created_date
            })
        return data_list

    def delete_document_by_id(self, doc_id):
        try:
            query = self._session.query(Document).filter(Document.id == doc_id).one()
            self._session.delete(query)
            self._session.commit()
            print('Документ удален')
        except Exception as ex:
            print(ex)
            return {'error_message': 'Документа с таким id не существует'}


def csv_reader(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    return rows


if __name__ == '__main__':
    worker = DbWorker()
    worker.upload_data_to_db()
