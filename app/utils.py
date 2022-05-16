from app import db

from sqlalchemy import insert


def upsert(table, data, index_elements):

    stmt = insert(table).values(data)
    stmt = stmt.on_conflict_do_update(
        index_elements=index_elements,
        set_=data,
    )
    db.session.execute(stmt)
    db.session.commit()
