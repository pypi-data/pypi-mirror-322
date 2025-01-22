import os.path
import uuid
import zipfile
import sqlalchemy as sa
import yaml
from pydantic import AnyUrl

from mitm_tooling.extraction.sql.data_models import DBMetaInfo
from mitm_tooling.extraction.sql.db import create_sa_engine, connect_and_reflect
from mitm_tooling.utilities.io_utils import DataSink, FilePath, ByteSink, use_bytes_io
from mitm_tooling.representation import MITMData, mk_sqlite, mk_db_schema
from mitm_tooling.representation.sql_representation import MITMData, mk_sqlite, mk_db_schema, \
    SQL_REPRESENTATION_DEFAULT_SCHEMA

from mitm_tooling.data_types import MITMDataType

from .dataset_definition import SupersetTableDef, SupersetColumnDef, SupersetDatabaseDef, SupersetDef, SupersetDefFile


def tentative_superset_mount_url(db_name: str) -> AnyUrl:
    return AnyUrl(f'sqlite:////mounted-files/{db_name}.sqlite?check_same_thread=false')


def write_superset_def_as_zip(target: ByteSink, superset_def: SupersetDef):
    folder_structure = superset_def.to_folder_structure()
    with use_bytes_io(target, expected_file_ext='.zip', mode='wb', create_file_if_necessary=True) as f:
        with zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED) as zf:
            def mk_node(arg, prefix: str | None = None):
                if isinstance(arg, SupersetDefFile):
                    fn = f'{arg.filename}.yaml'
                    if prefix:
                        fn = os.path.join(prefix, fn)
                    dump = arg.model_dump(by_alias=True, mode='python')
                    s = yaml.dump(dump, default_flow_style=False)

                    zf.writestr(fn, s)
                    # with zf.open(fn, 'w') as df:
                    #    yaml.dump(dump, df)
                elif isinstance(arg, list):
                    for arg in arg:
                        mk_node(arg, prefix=prefix)
                elif isinstance(arg, dict):
                    for folder, folder_content in arg.items():
                        path = None
                        if folder != '.' and prefix:
                            path = os.path.join(prefix, folder)
                        elif prefix:
                            path = prefix
                        elif folder != '.':
                            path = folder
                        if folder != '.':
                            zf.mkdir(path)
                        mk_node(folder_content, prefix=path)

            mk_node(folder_structure)


def write_superset_def(output_path: FilePath, superset_def: SupersetDef):
    write_superset_def_as_zip(output_path, superset_def)


def infer_superset_dataset_def(sqlite_file_path: FilePath) -> SupersetDef:
    engine = create_sa_engine(AnyUrl(f'sqlite:///{str(sqlite_file_path)}'))
    meta, _ = connect_and_reflect(engine)
    db_meta = DBMetaInfo.from_sa_meta(meta, default_schema=SQL_REPRESENTATION_DEFAULT_SCHEMA)

    database_uuid = uuid.uuid4()
    datasets = []
    for schema_name, schema_tables in db_meta.db_structure.items():
        for table_name, table in schema_tables.items():
            cols = []
            for c in table.columns:
                dt = table.column_properties[c].mitm_data_type

                cols.append(
                    SupersetColumnDef(column_name=c,
                                      is_dttm=dt is MITMDataType.Datetime,
                                      groupby=dt not in {MITMDataType.Json,
                                                         MITMDataType.Numeric,
                                                         MITMDataType.Datetime},
                                      type=(dt.sa_sql_type or MITMDataType.Text.sa_sql_type).compile(
                                          dialect=engine.dialect)
                                      ))
            datasets.append(
                SupersetTableDef(table_name=table_name, schema_name=schema_name, uuid=uuid.uuid4(), database_uuid=database_uuid, columns=cols))

    db_name = os.path.splitext(os.path.basename(sqlite_file_path))[0]
    return SupersetDef(
        database=SupersetDatabaseDef(database_name=db_name,
                                     sqlalchemy_uri=tentative_superset_mount_url(db_name),
                                     uuid=database_uuid),
        datasets=datasets)


def mk_inferred_superset_dataset_def(output_path: FilePath, sqlite_file_path: FilePath):
    write_superset_def(output_path, infer_superset_dataset_def(sqlite_file_path))


def mk_superset_dataset_def(mitm_data: MITMData, sqlite_file_path: str | None = ':memory:',
                            definition_file_path: str | None = 'superset_definition.zip'):
    engine, sql_rep_schema = mk_sqlite(mitm_data, file_path=sqlite_file_path)
    mk_inferred_superset_dataset_def(definition_file_path, sqlite_file_path)
