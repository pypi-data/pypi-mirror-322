from dbt.adapters.base import AdapterPlugin

from dbt.adapters.avrio.column import AvrioColumn  # noqa
from dbt.adapters.avrio.connections import AvrioConnectionManager  # noqa
from dbt.adapters.avrio.connections import AvrioCredentialsFactory
from dbt.adapters.avrio.relation import AvrioRelation  # noqa

from dbt.adapters.avrio.impl import AvrioAdapter  # isort: split
from dbt.include import avrio

Plugin = AdapterPlugin(
    adapter=AvrioAdapter,  # type: ignore
    credentials=AvrioCredentialsFactory,  # type: ignore
    include_path=avrio.PACKAGE_PATH,
)
