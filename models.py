import sqlalchemy as sq
from sqlalchemy.orm import declarative_base


_DSN = 'postgresql://your_username:your_password@localhost:5432/your_database'
_engine = sq.create_engine(_DSN)

_Base = declarative_base()


class Document(_Base):
    __tablename__ = 'document'

    id = sq.Column(sq.Integer, primary_key=True)
    rubrics = sq.Column(sq.String(200), nullable=False)
    text = sq.Column(sq.Text, nullable=False)
    created_date = sq.Column(sq.DateTime, nullable=False)

    def __repr__(self):
        return f"Document with date {self.created_date}"


if __name__ == '__main__':
    _Base.metadata.create_all(_engine)
