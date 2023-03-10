import logging
from contextlib import contextmanager, AbstractContextManager
from dataclasses import dataclass
from typing import Callable

from sqlalchemy import create_engine, orm
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session

logger = logging.getLogger(__name__)


@dataclass
class Database:
    """
    class to handle tha database connection
    """

    def __init__(self, db_url: str) -> None:
        self._engine: Engine = create_engine(
            db_url,
            pool_pre_ping=True,
            # echo=True,
            pool_size=20,
            max_overflow=0
        )
        self._session_factory: scoped_session = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        """
        dependency inject database session to repositories
        :return: database session
        :rtype: Callable[..., AbstractContextManager[Session]]
        """
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
