import functools
from pathlib import Path
from typing import Optional

from click import ClickException
from snowflake.cli._plugins.connection.util import make_snowsight_url
from snowflake.cli._plugins.nativeapp.feature_flags import FeatureFlag
from snowflake.cli._plugins.streamlit.streamlit_entity_model import (
    StreamlitEntityModel,
)
from snowflake.cli._plugins.workspace.context import ActionContext
from snowflake.cli.api.entities.common import EntityBase, get_sql_executor
from snowflake.cli.api.secure_path import SecurePath
from snowflake.connector.cursor import SnowflakeCursor


class StreamlitEntity(EntityBase[StreamlitEntityModel]):
    """
    A Streamlit app.
    """

    def __init__(self, *args, **kwargs):
        if not FeatureFlag.ENABLE_NATIVE_APP_CHILDREN.is_enabled():
            raise NotImplementedError("Streamlit entity is not implemented yet")
        super().__init__(*args, **kwargs)

    @property
    def root(self):
        return self._workspace_ctx.project_root

    @property
    def artifacts(self):
        return self._entity_model.artifacts

    @functools.cached_property
    def _sql_executor(self):
        return get_sql_executor()

    @functools.cached_property
    def _conn(self):
        return self._sql_executor._conn  # noqa

    @property
    def model(self):
        return self._entity_model  # noqa

    def action_bundle(self, action_ctx: ActionContext, *args, **kwargs):
        return self.bundle()

    def action_deploy(self, action_ctx: ActionContext, *args, **kwargs):
        # After adding bundle map- we should use it's mapping here
        # To copy artifacts to destination on stage.

        return self._sql_executor.execute_query(self.get_deploy_sql())

    def action_drop(self, action_ctx: ActionContext, *args, **kwargs):
        return self._sql_executor.execute_query(self.get_drop_sql())

    def action_execute(
        self, action_ctx: ActionContext, *args, **kwargs
    ) -> SnowflakeCursor:
        return self._sql_executor.execute_query(self.get_execute_sql())

    def action_get_url(
        self, action_ctx: ActionContext, *args, **kwargs
    ):  # maybe this should be a property
        name = self._entity_model.fqn.using_connection(self._conn)
        return make_snowsight_url(
            self._conn, f"/#/streamlit-apps/{name.url_identifier}"
        )

    def bundle(self, output_dir: Optional[Path] = None):

        if not output_dir:
            output_dir = self.root / "output" / self._entity_model.stage

        artifacts = self._entity_model.artifacts

        output_dir.mkdir(parents=True, exist_ok=True)  # type: ignore

        output_files = []

        # This is far from , but will be replaced by bundlemap mappings.
        for file in artifacts:
            output_file = output_dir / file.name

            if file.is_file():
                SecurePath(file).copy(output_file)
            elif file.is_dir():
                output_file.mkdir(parents=True, exist_ok=True)
                SecurePath(file).copy(output_file, dirs_exist_ok=True)

                output_files.append(output_file)

        return output_files

    def action_share(
        self, action_ctx: ActionContext, to_role: str, *args, **kwargs
    ) -> SnowflakeCursor:
        return self._sql_executor.execute_query(self.get_share_sql(to_role))

    def get_deploy_sql(
        self,
        if_not_exists: bool = False,
        replace: bool = False,
        from_stage_name: Optional[str] = None,
        artifacts_dir: Optional[Path] = None,
        schema: Optional[str] = None,
        *args,
        **kwargs,
    ):
        if replace and if_not_exists:
            raise ClickException("Cannot specify both replace and if_not_exists")

        if replace:
            query = "CREATE OR REPLACE "
        elif if_not_exists:
            query = "CREATE IF NOT EXISTS "
        else:
            query = "CREATE "

        schema_to_use = schema or self._entity_model.fqn.schema
        query += f"STREAMLIT {self._entity_model.fqn.set_schema(schema_to_use).sql_identifier}"

        if from_stage_name:
            query += f"\nROOT_LOCATION = '{from_stage_name}'"
        elif artifacts_dir:
            query += f"\nFROM '{artifacts_dir}'"

        query += f"\nMAIN_FILE = '{self._entity_model.main_file}'"

        if self.model.imports:
            query += "\n" + self.model.get_imports_sql()

        if self.model.query_warehouse:
            query += f"\nQUERY_WAREHOUSE = '{self.model.query_warehouse}'"

        if self.model.title:
            query += f"\nTITLE = '{self.model.title}'"

        if self.model.comment:
            query += f"\nCOMMENT = '{self.model.comment}'"

        if self.model.external_access_integrations:
            query += "\n" + self.model.get_external_access_integrations_sql()

        if self.model.secrets:
            query += "\n" + self.model.get_secrets_sql()

        return query + ";"

    def get_share_sql(self, to_role: str) -> str:
        return f"GRANT USAGE ON STREAMLIT {self.model.fqn.sql_identifier} TO ROLE {to_role};"

    def get_execute_sql(self):
        return f"EXECUTE STREAMLIT {self._entity_model.fqn}();"

    def get_usage_grant_sql(self, app_role: str, schema: Optional[str] = None) -> str:
        entity_id = self.entity_id
        streamlit_name = f"{schema}.{entity_id}" if schema else entity_id
        return (
            f"GRANT USAGE ON STREAMLIT {streamlit_name} TO APPLICATION ROLE {app_role};"
        )
