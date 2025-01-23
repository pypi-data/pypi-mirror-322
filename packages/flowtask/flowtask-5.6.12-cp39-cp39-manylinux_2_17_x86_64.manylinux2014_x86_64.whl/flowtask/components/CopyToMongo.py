import asyncio
from collections.abc import Callable
import math
import pandas as pd
from asyncdb import AsyncDB
from asyncdb.exceptions import (
    StatementError,
    DataError
)
from .CopyTo import CopyTo
from ..interfaces.dataframes import PandasDataframe
from ..exceptions import (
    ComponentError,
    DataNotFound
)
from ..conf import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USER,
    MONGO_PASSWORD,
    MONGO_DATABASE
)


class CopyToMongo(CopyTo, PandasDataframe):
    """
    CopyToMongo.

    Overview
        This component allows copying data into a MongoDB collection,
        using write functionality from AsyncDB MongoDB driver.

    .. table:: Properties
       :widths: auto

    +--------------+----------+-----------+--------------------------------------------+
    | Name         | Required | Summary                                                |
    +--------------+----------+-----------+--------------------------------------------+
    | tablename    |   Yes    | Name of the collection in                              |
    |              |          | MongoDB                                                |
    +--------------+----------+-----------+--------------------------------------------+
    | schema       |   Yes    | Name of the database                                   |
    |              |          | where the collection is located                        |
    +--------------+----------+-----------+--------------------------------------------+
    | truncate     |   Yes    | If true, the collection will be emptied                |
    |              |          | before copying new data                                |
    +--------------+----------+-----------+--------------------------------------------+
    | use_buffer   |   No     | When activated, optimizes performance                  |
    |              |          | for large volumes of data                              |
    +--------------+----------+-----------+--------------------------------------------+
    | key_field    |   No     | Field to use as unique identifier                      |
    |              |          | for upsert operations                                  |
    +--------------+----------+-----------+--------------------------------------------+
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.pk = []
        self.truncate: bool = False
        self.data = None
        self._engine = None
        self.tablename: str = ""  # collection name in MongoDB
        self.schema: str = ""     # database name in MongoDB
        self.use_chunks = False
        self._chunksize: int = kwargs.pop('chunksize', 1000)
        self._connection: Callable = None
        self._driver: str = 'mongodb'
        self.key_field: str = kwargs.pop('key_field', '_id')
        try:
            self.multi = bool(kwargs["multi"])
            del kwargs["multi"]
        except KeyError:
            self.multi = False
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    def default_connection(self):
        """default_connection.
        Default Connection to MongoDB.
        """
        try:
            kwargs: dict = {
                "host": MONGO_HOST,
                "port": int(MONGO_PORT),
                "database": MONGO_DATABASE
            }
            if MONGO_USER:
                kwargs.update({
                    "username": MONGO_USER,
                    "password": MONGO_PASSWORD
                })
            self._connection = AsyncDB(
                'mongodb',
                params=kwargs,
                loop=self._loop,
                **kwargs
            )
            return self._connection
        except Exception as err:
            raise ComponentError(
                f"Error configuring MongoDB Connection: {err!s}"
            ) from err

    async def _create_table(self):
        """Create a Collection in MongoDB if it doesn't exist."""
        try:
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                # MongoDB creates collections automatically when data is inserted
                # No explicit creation needed
        except Exception as err:
            raise ComponentError(
                f"Error creating MongoDB collection: {err}"
            ) from err

    async def _truncate_table(self):
        """Truncate the MongoDB collection."""
        async with await self._connection.connection() as conn:
            await conn.use(self.schema)
            await conn.execute(
                collection_name=self.tablename,
                operation='delete_many',
                filter={}
            )

    async def _copy_dataframe(self):
        """Copy a pandas DataFrame to MongoDB."""
        try:
            # Clean NA values from string fields
            str_cols = self.data.select_dtypes(include=["string", "object"])
            if not str_cols.empty:
                self.data[str_cols.columns] = str_cols.astype(object).where(
                    pd.notnull(str_cols), None
                )
            
            # Clean datetime fields
            datetime_cols = self.data.select_dtypes(include=['datetime64[ns]'])
            if not datetime_cols.empty:
                for col in datetime_cols.columns:
                    self.data[col] = self.data[col].apply(
                        lambda x: x.isoformat() if pd.notnull(x) else None
                    )
            
            # Convert DataFrame to list of dictionaries
            data_records = self.data.to_dict(orient='records')
            
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                await conn.write(
                    data=data_records,
                    table=self.tablename,
                    database=self.schema,
                    key_field=self.key_field,
                    if_exists="replace"
                )
        except StatementError as err:
            raise ComponentError(
                f"Statement error: {err}"
            ) from err
        except DataError as err:
            raise ComponentError(
                f"Data error: {err}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"{self.StepName} Error: {err!s}"
            ) from err

    async def _copy_iterable(self):
        """Copy an iterable to MongoDB."""
        try:
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                await conn.write(
                    data=self.data,
                    table=self.tablename,
                    database=self.schema,
                    key_field=self.key_field,
                    if_exists="replace"
                )
        except Exception as err:
            raise ComponentError(
                f"Error copying iterable to MongoDB: {err}"
            ) from err 