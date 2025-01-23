import re
import hashlib
from datetime import datetime
from typing_extensions import Self
from typing import Dict, List, Any, Optional
from sqlalchemy import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, JSON
from sqlalchemy.exc import NoResultFound

Base = declarative_base()


class SqlalchemyModelMeta(type(Base)):
    def __new__(cls, name, bases, attrs):
        if attrs.get("__abstract__") is True:
            return super().__new__(cls, name, bases, attrs)

        tablename = attrs.get("__tablename__")
        if not (isinstance(tablename, str) and tablename):
            raise ValueError(f"{name}.__tablename__ 非法赋值！")

        engine = attrs.get("__engine__")
        if not isinstance(engine, Engine):
            raise ValueError(f"{name}.__engine__ 非法赋值！")

        data_columns = attrs.get("__data_columns__")
        if not (isinstance(data_columns, list) and all(map(lambda _: isinstance(_, str), data_columns))):
            raise ValueError(f"{name}.__data_columns__ 非法赋值！")

        session = attrs.get("__session__")
        if session is None:
            __session__ = sessionmaker(bind=engine)()
        else:
            if not isinstance(session, Session):
                raise ValueError(f"{name}.__session__ 非法赋值！")

        return super().__new__(cls, name, bases, attrs)


class SqlalchemyModel(Base, metaclass=SqlalchemyModelMeta):
    __abstract__ = True

    __tablename__: str
    __engine__: Engine
    __data_columns__: List[str]
    __session__: Session

    id = Column(Integer, comment='ID', primary_key=True, autoincrement=True)
    data_id = Column(String(32), comment='数据ID', nullable=False, unique=True)
    data_columns = Column(JSON, comment='数据字段', nullable=False)
    data_status = Column(SmallInteger, comment='数据状态', default=1, index=True)
    data_create_time = Column(DateTime, comment='数据创建时间', default=datetime.utcnow)
    data_update_time = Column(DateTime, comment='数据更新时间', default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, data_id={self.data_id})>"

    def to_row(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    @classmethod
    def gen_data_id(cls, data: Dict[str, Any]) -> str:
        data_columns = cls.__data_columns__
        data_columns_value_strs = []
        for data_column in data_columns:
            if data_column in data:
                data_column_value_str = str(data[data_column])
                data_columns_value_strs.append(data_column_value_str)
            else:
                raise ValueError(f"data 必须提供 {data_column} 字段！")
        data_id = hashlib.md5("".join(data_columns_value_strs).encode()).hexdigest()
        return data_id

    @classmethod
    def get_data_id(cls, data: Dict[str, Any]) -> str:
        if "data_id" in data:
            if isinstance(data["data_id"], str) and re.match(r"^[0-9a-f]{32}$", data["data_id"]) is not None:
                return data["data_id"]
        return cls.gen_data_id(data)

    @classmethod
    def get_ins_by_data_id(cls, data: Dict[str, Any]) -> Optional[Self]:
        session = cls.__session__
        data_id = cls.get_data_id(data)
        try:
            ins: Self = session.query(cls).filter_by(data_id=data_id).one()
        except NoResultFound:
            return
        return ins

    @classmethod
    def get_row_by_data_id(cls, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        ins = cls.get_ins_by_data_id(data)
        if ins is None:
            return
        data = ins.to_row()
        return data

    @classmethod
    def save(cls, data: Dict[str, Any], update: Optional[bool] = None) -> bool:
        session = cls.__session__

        if not (update is None or isinstance(update, bool)):
            raise ValueError(f"update 值只能是 None 或 True 或 False！")

        ins = None
        if update is None:
            ins = cls.get_ins_by_data_id(data)
            update = False if ins is None else True

        if not update:
            ins = cls(
                data_id=cls.get_data_id(data),
                data_columns=cls.__data_columns__,
                **data
            )
            session.add(ins)
        else:
            if ins is None:
                ins = cls.get_by_data_id(data)
            for k, v in data.items():
                setattr(ins, k, v)

        session.commit()

        return update

    @classmethod
    def create_table(cls) -> None:
        Base.metadata.create_all(cls.__engine__)
