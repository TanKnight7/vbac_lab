from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import JSON
from sqlalchemy.orm import sessionmaker, relationship
from contextlib import contextmanager
import json

engine = create_engine("sqlite:///D:/University/rm/mcp_database.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Scenario(Base):
    __tablename__ = "scenarios"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    is_tested = Column(Boolean, nullable=False, default=False)
    api_endpoint_id = Column(Integer, ForeignKey("api_endpoint.id"), index=True)
    api_endpoint = relationship("APIEndpoint", back_populates="scenarios")
    
    
    findings = relationship("Finding", back_populates="scenario", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Scenario(id={self.id}, title={self.title}, api_endpoint_id={self.api_endpoint_id})>"

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    is_vulnerable = Column(Boolean, nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), index=True)
    scenario = relationship("Scenario", back_populates="findings")
    
    def __repr__(self):
        return f"<Finding(id={self.id}, title={self.title}, is_vulnerable={self.is_vulnerable}, scenario_id={self.scenario_id})>"
    
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    role = relationship("Role", back_populates="accounts")
    
    cookies = relationship("Cookie", back_populates="account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Account(id={self.id}, username={self.username}, role_id={self.role_id})>"
    
class Cookie(Base):
    __tablename__ = "cookies"
    
    id = Column(Integer, primary_key=True, index=True)
    cookie_name = Column(String, nullable=False)
    cookie_value = Column(String, nullable=False)
    
    account_id = Column(Integer, ForeignKey("accounts.id"), index=True)
    account = relationship("Account", back_populates="cookies")
    
    def __repr__(self):
        return f"<Cookie(id={self.id}, cookie_name={self.cookie_name}, cookie_value={self.cookie_value}, account_id={self.account_id})>"

endpoint_allowed_roles = Table(
    "endpoint_allowed_roles",
    Base.metadata,
    Column("endpoint_id", Integer, ForeignKey("api_endpoint.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, nullable=False, unique=True)
    permissions = Column(JSON, default=json.dumps({}))
    accounts = relationship("Account", back_populates="role", cascade="all, delete-orphan")
    api_endpoints = relationship("APIEndpoint", back_populates="allowed_roles", secondary=endpoint_allowed_roles)
    
    def __repr__(self):
        return f"<Role(id={self.id}, role_name={self.role_name}), permissions={self.permissions}>"


class APIEndpoint(Base):
    __tablename__ = "api_endpoint"
    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, index=True)
    path = Column(String, index=True)
    headers = Column(JSON, default=json.dumps({}))
    query_params = Column(JSON, default=json.dumps({}))
    body = Column(JSON, default=json.dumps({}))
    
    scenarios = relationship("Scenario", back_populates="api_endpoint", cascade="all, delete-orphan")
    allowed_roles = relationship("Role", back_populates="api_endpoints", secondary=endpoint_allowed_roles)
    
    def __repr__(self):
        return f"<APIEndpoint(id={self.id}, method={self.method}, path={self.path}), headers={self.headers}, query_params={self.query_params}, body={self.body}>"

# Create database based on the models we defined.
Base.metadata.create_all(bind=engine)



from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session

T = TypeVar("T")
class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db_session: Session):
        self.model = model
        self.db = db_session
    
    def create(self, obj_in: Dict[str, Any]) -> T:
        """Create a new DB row from dict and return instance."""
        instance = self.model(**obj_in)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get(self, id: int) -> Optional[T]:
        return self.db.query(self.model).get(id)

    def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def filter_by(self, **kwargs) -> List[T]:
        return self.db.query(self.model).filter_by(**kwargs).all()

    def update(self, id: int, values: Dict[str, Any]) -> Optional[T]:
        instance = self.get(id)
        if not instance:
            return None
        for k, v in values.items():
            setattr(instance, k, v)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        instance = self.get(id)
        if not instance:
            return False
        self.db.delete(instance)
        self.db.commit()
        return True
    
class RoleRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Role, db_session)

    def get_by_name(self, role_name: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.role_name == role_name).one_or_none()

class AccountRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Account, db_session)

    def get_by_username(self, username: str) -> Optional[Account]:
        return self.db.query(Account).filter(Account.username == username).one_or_none()

    def create_with_role(self, username: str, password: str, role_id: int) -> Account:
        acc = Account(username=username, password=password, role_id=role_id)
        self.db.add(acc)
        self.db.commit()
        self.db.refresh(acc)
        return acc

class CookieRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Cookie, db_session)

class APIEndpointRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(APIEndpoint, db_session)

class ScenarioRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Scenario, db_session)

class FindingRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Finding, db_session)


# with SessionLocal() as db:
    # result = RoleRepository(db).create({'role_name': 'adminss', 'permissions': {"read": True, "write": True, "delete": True}})
    # print(result)
    # result = AccountRepository(db).create_with_role("admin", "admin", 1)
    # print(result)
    # result = AccountRepository(db).get(1)
    # print(result.role.accounts)
    # AccountRepository(db).create({'username': 'admin', 'password': 'admin', 'role_id': 1})
    # result = AccountRepository(db).get(2)
    # print(result)
    
# with get_db() as db:
#     repo = AccountRepository(db)
#     result = repo.get()
#     print(result)
