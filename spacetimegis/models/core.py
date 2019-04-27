# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-27 10:49:42
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: core.py
'''

from spacetimegis import db
from sqlalchemy import (
    Boolean, Column, create_engine, DateTime, ForeignKey, Integer,
    MetaData, String, Table, Text,
)
from sqlalchemy.schema import UniqueConstraint

from .helpers import ImportMixin


class Database(db.Model, ImportMixin):

    """An ORM object that stores Database related information"""

    __tablename__ = 'dbs'
    type = 'table'
    __table_args__ = (UniqueConstraint('database_name'),)

    id = Column(Integer, primary_key=True)
    database_name = Column(String(250), unique=True)
    sqlalchemy_uri = Column(String(1024))

    # @property
    # def data(self):
    #     return {
    #         'id': self.id,
    #         'name': self.database_name,
    #         'sqlalchemy_uri': self.sqlalchemy_uri,
    #     }

    # @property
    # def unique_name(self):
    #     return self.database_name

    # @property
    # def url_object(self):
    #     return make_url(self.sqlalchemy_uri_decrypted)

    # @property
    # def backend(self):
    #     url = make_url(self.sqlalchemy_uri_decrypted)
    #     return url.get_backend_name()

    # @classmethod
    # def get_password_masked_url_from_uri(cls, uri):
    #     url = make_url(uri)
    #     return cls.get_password_masked_url(url)

    # @classmethod
    # def get_password_masked_url(cls, url):
    #     url_copy = deepcopy(url)
    #     if url_copy.password is not None and url_copy.password != PASSWORD_MASK:
    #         url_copy.password = PASSWORD_MASK
    #     return url_copy

    # def set_sqlalchemy_uri(self, uri):
    #     conn = sqla.engine.url.make_url(uri.strip())
    #     if conn.password != PASSWORD_MASK and not custom_password_store:
    #         # do not over-write the password with the password mask
    #         self.password = conn.password
    #     conn.password = PASSWORD_MASK if conn.password else None
    #     self.sqlalchemy_uri = str(conn)  # hides the password

    # def get_effective_user(self, url, user_name=None):
    #     """
    #     Get the effective user, especially during impersonation.
    #     :param url: SQL Alchemy URL object
    #     :param user_name: Default username
    #     :return: The effective username
    #     """
    #     effective_username = None
    #     if self.impersonate_user:
    #         effective_username = url.username
    #         if user_name:
    #             effective_username = user_name
    #         elif (
    #             hasattr(g, 'user') and hasattr(g.user, 'username') and
    #             g.user.username is not None
    #         ):
    #             effective_username = g.user.username
    #     return effective_username

    # @utils.memoized(
    #     watch=('impersonate_user', 'sqlalchemy_uri_decrypted', 'extra'))
    # def get_sqla_engine(self, schema=None, nullpool=True, user_name=None):
    #     extra = self.get_extra()
    #     url = make_url(self.sqlalchemy_uri_decrypted)
    #     url = self.db_engine_spec.adjust_database_uri(url, schema)
    #     effective_username = self.get_effective_user(url, user_name)
    #     # If using MySQL or Presto for example, will set url.username
    #     # If using Hive, will not do anything yet since that relies on a
    #     # configuration parameter instead.
    #     self.db_engine_spec.modify_url_for_impersonation(
    #         url,
    #         self.impersonate_user,
    #         effective_username)

    #     masked_url = self.get_password_masked_url(url)
    #     logging.info('Database.get_sqla_engine(). Masked URL: {0}'.format(masked_url))

    #     params = extra.get('engine_params', {})
    #     if nullpool:
    #         params['poolclass'] = NullPool

    #     # If using Hive, this will set hive.server2.proxy.user=$effective_username
    #     configuration = {}
    #     configuration.update(
    #         self.db_engine_spec.get_configuration_for_impersonation(
    #             str(url),
    #             self.impersonate_user,
    #             effective_username))
    #     if configuration:
    #         params['connect_args'] = {'configuration': configuration}

    #     DB_CONNECTION_MUTATOR = config.get('DB_CONNECTION_MUTATOR')
    #     if DB_CONNECTION_MUTATOR:
    #         url, params = DB_CONNECTION_MUTATOR(
    #             url, params, effective_username, security_manager)
    #     return create_engine(url, **params)

    # def get_reserved_words(self):
    #     return self.get_dialect().preparer.reserved_words

    # def get_quoter(self):
    #     return self.get_dialect().identifier_preparer.quote

    # def get_df(self, sql, schema):
    #     sqls = [six.text_type(s).strip().strip(';') for s in sqlparse.parse(sql)]
    #     engine = self.get_sqla_engine(schema=schema)

    #     def needs_conversion(df_series):
    #         if df_series.empty:
    #             return False
    #         if isinstance(df_series[0], (list, dict)):
    #             return True
    #         return False

    #     with closing(engine.raw_connection()) as conn:
    #         with closing(conn.cursor()) as cursor:
    #             for sql in sqls[:-1]:
    #                 self.db_engine_spec.execute(cursor, sql)
    #                 cursor.fetchall()

    #             self.db_engine_spec.execute(cursor, sqls[-1])

    #             df = pd.DataFrame.from_records(
    #                 data=list(cursor.fetchall()),
    #                 columns=[col_desc[0] for col_desc in cursor.description],
    #                 coerce_float=True,
    #             )

    #             for k, v in df.dtypes.items():
    #                 if v.type == numpy.object_ and needs_conversion(df[k]):
    #                     df[k] = df[k].apply(utils.json_dumps_w_dates)
    #             return df

    # def compile_sqla_query(self, qry, schema=None):
    #     engine = self.get_sqla_engine(schema=schema)

    #     sql = six.text_type(
    #         qry.compile(
    #             engine,
    #             compile_kwargs={'literal_binds': True},
    #         ),
    #     )

    #     if engine.dialect.identifier_preparer._double_percents:
    #         sql = sql.replace('%%', '%')

    #     return sql

    # def select_star(
    #         self, table_name, schema=None, limit=100, show_cols=False,
    #         indent=True, latest_partition=False, cols=None):
    #     """Generates a ``select *`` statement in the proper dialect"""
    #     eng = self.get_sqla_engine(schema=schema)
    #     return self.db_engine_spec.select_star(
    #         self, table_name, schema=schema, engine=eng,
    #         limit=limit, show_cols=show_cols,
    #         indent=indent, latest_partition=latest_partition, cols=cols)

    # def apply_limit_to_sql(self, sql, limit=1000):
    #     return self.db_engine_spec.apply_limit_to_sql(sql, limit, self)

    # def safe_sqlalchemy_uri(self):
    #     return self.sqlalchemy_uri

    # @property
    # def inspector(self):
    #     engine = self.get_sqla_engine()
    #     return sqla.inspect(engine)

    # def all_table_names(self, schema=None, force=False):
    #     if not schema:
    #         if not self.allow_multi_schema_metadata_fetch:
    #             return []
    #         tables_dict = self.db_engine_spec.fetch_result_sets(
    #             self, 'table', force=force)
    #         return tables_dict.get('', [])
    #     return sorted(
    #         self.db_engine_spec.get_table_names(schema, self.inspector))

    # def all_view_names(self, schema=None, force=False):
    #     if not schema:
    #         if not self.allow_multi_schema_metadata_fetch:
    #             return []
    #         views_dict = self.db_engine_spec.fetch_result_sets(
    #             self, 'view', force=force)
    #         return views_dict.get('', [])
    #     views = []
    #     try:
    #         views = self.inspector.get_view_names(schema)
    #     except Exception:
    #         pass
    #     return views

    # def all_schema_names(self):
    #     return sorted(self.db_engine_spec.get_schema_names(self.inspector))

    # @property
    # def db_engine_spec(self):
    #     return db_engine_specs.engines.get(
    #         self.backend, db_engine_specs.BaseEngineSpec)

    # @classmethod
    # def get_db_engine_spec_for_backend(cls, backend):
    #     return db_engine_specs.engines.get(backend, db_engine_specs.BaseEngineSpec)

    # def grains(self):
    #     """Defines time granularity database-specific expressions.

    #     The idea here is to make it easy for users to change the time grain
    #     form a datetime (maybe the source grain is arbitrary timestamps, daily
    #     or 5 minutes increments) to another, "truncated" datetime. Since
    #     each database has slightly different but similar datetime functions,
    #     this allows a mapping between database engines and actual functions.
    #     """
    #     return self.db_engine_spec.get_time_grains()

    # def grains_dict(self):
    #     """Allowing to lookup grain by either label or duration

    #     For backward compatibility"""
    #     d = {grain.duration: grain for grain in self.grains()}
    #     d.update({grain.label: grain for grain in self.grains()})
    #     return d

    # def get_extra(self):
    #     extra = {}
    #     if self.extra:
    #         try:
    #             extra = json.loads(self.extra)
    #         except Exception as e:
    #             logging.error(e)
    #     return extra

    # def get_table(self, table_name, schema=None):
    #     extra = self.get_extra()
    #     meta = MetaData(**extra.get('metadata_params', {}))
    #     return Table(
    #         table_name, meta,
    #         schema=schema or None,
    #         autoload=True,
    #         autoload_with=self.get_sqla_engine())

    # def get_columns(self, table_name, schema=None):
    #     return self.inspector.get_columns(table_name, schema)

    # def get_indexes(self, table_name, schema=None):
    #     return self.inspector.get_indexes(table_name, schema)

    # def get_pk_constraint(self, table_name, schema=None):
    #     return self.inspector.get_pk_constraint(table_name, schema)

    # def get_foreign_keys(self, table_name, schema=None):
    #     return self.inspector.get_foreign_keys(table_name, schema)

    # @property
    # def sqlalchemy_uri_decrypted(self):
    #     conn = sqla.engine.url.make_url(self.sqlalchemy_uri)
    #     if custom_password_store:
    #         conn.password = custom_password_store(conn)
    #     else:
    #         conn.password = self.password
    #     return str(conn)

    # @property
    # def sql_url(self):
    #     return '/superset/sql/{}/'.format(self.id)

    # def get_perm(self):
    #     return (
    #         '[{obj.database_name}].(id:{obj.id})').format(obj=self)

    # def has_table(self, table):
    #     engine = self.get_sqla_engine()
    #     return engine.has_table(
    #         table.table_name, table.schema or None)

    # @utils.memoized
    # def get_dialect(self):
    #     sqla_url = url.make_url(self.sqlalchemy_uri_decrypted)
    #     return sqla_url.get_dialect()()


# class Log(Model):

#     """ORM object used to log Superset actions to the database"""

#     __tablename__ = 'logs'

#     id = Column(Integer, primary_key=True)
#     action = Column(String(512))
#     user_id = Column(Integer, ForeignKey('ab_user.id'))
#     dashboard_id = Column(Integer)
#     slice_id = Column(Integer)
#     json = Column(Text)
#     user = relationship(
#         security_manager.user_model, backref='logs', foreign_keys=[user_id])
#     dttm = Column(DateTime, default=datetime.utcnow)
#     duration_ms = Column(Integer)
#     referrer = Column(String(1024))

#     @classmethod
#     def log_this(cls, f):
#         """Decorator to log user actions"""
#         @functools.wraps(f)
#         def wrapper(*args, **kwargs):
#             user_id = None
#             if g.user:
#                 user_id = g.user.get_id()
#             d = request.form.to_dict() or {}

#             # request parameters can overwrite post body
#             request_params = request.args.to_dict()
#             d.update(request_params)
#             d.update(kwargs)

#             slice_id = d.get('slice_id')
#             dashboard_id = d.get('dashboard_id')

#             try:
#                 slice_id = int(
#                     slice_id or json.loads(d.get('form_data')).get('slice_id'))
#             except (ValueError, TypeError):
#                 slice_id = 0

#             stats_logger.incr(f.__name__)
#             start_dttm = datetime.now()
#             value = f(*args, **kwargs)
#             duration_ms = (datetime.now() - start_dttm).total_seconds() * 1000

#             # bulk insert
#             try:
#                 explode_by = d.get('explode')
#                 records = json.loads(d.get(explode_by))
#             except Exception:
#                 records = [d]

#             referrer = request.referrer[:1000] if request.referrer else None
#             logs = []
#             for record in records:
#                 try:
#                     json_string = json.dumps(record)
#                 except Exception:
#                     json_string = None
#                 log = cls(
#                     action=f.__name__,
#                     json=json_string,
#                     dashboard_id=dashboard_id,
#                     slice_id=slice_id,
#                     duration_ms=duration_ms,
#                     referrer=referrer,
#                     user_id=user_id)
#                 logs.append(log)

#             sesh = db.session()
#             sesh.bulk_save_objects(logs)
#             sesh.commit()
#             return value

#         return wrapper