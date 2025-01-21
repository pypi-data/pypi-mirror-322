import base64
import gzip
from typing import Optional
from sqlalchemy import Boolean, Enum, Integer, Numeric
from doris_alchemy.orm_base import DorisBase
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import create_engine, Engine


class Tst(DorisBase):
    __tablename__ = 'test_doris_table_1'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[float] = mapped_column(Numeric(12, 2))



if __name__ == '__main__':
    pass