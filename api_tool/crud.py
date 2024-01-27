from sqlalchemy.orm import Session

from app.models import ShortenedUrl
from components.db_decorators import transaction
from components.string_utils import b58_hash_time


def get_shortened_url_by_link(
        link: str,
        db: Session
) -> str:
    """
    依照 url 取得短網址
    """
    return db.query(ShortenedUrl).filter(
        ShortenedUrl.link == link
    ).first().key


def get_original_url(
        shortened_url: str,
        db: Session
) -> str:
    """
    依照短網址取得原始網址
    """
    return db.query(ShortenedUrl).filter(
        ShortenedUrl.key == shortened_url
    ).first().link


@transaction
def create_shortened_url(
        url: str,
        db: Session,
) -> str:
    """
    產生一短網址
    寫入 db
    """
    hashed_key = b58_hash_time()
    shortened_url = ShortenedUrl(
        key=hashed_key,
        link=url
    )
    db.add(shortened_url)
    db.flush()
    return hashed_key
