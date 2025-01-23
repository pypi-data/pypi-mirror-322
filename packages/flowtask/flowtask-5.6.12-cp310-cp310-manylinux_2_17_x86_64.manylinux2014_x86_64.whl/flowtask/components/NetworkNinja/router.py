from collections.abc import Callable
import asyncio
import pandas as pd
import backoff
from datamodel.exceptions import ValidationError
from ...exceptions import ComponentError, DataError
from ...components import FlowComponent
from ...utils.json import json_encoder
from .models import Store, Client, Organization


NetworkNinja_Map = {
    "store": Store,
    "client": Client,
    "orgid": Organization
}


class NetworkNinja(FlowComponent):
    """
    NetworkNinja.

        Overview: Router for processing NetworkNinja Payloads.
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self._action: str = kwargs.pop('action', None)
        self.use_proxies: bool = kwargs.pop('use_proxies', False)
        self.paid_proxy: bool = kwargs.pop('paid_proxy', False)
        super(NetworkNinja, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.semaphore = asyncio.Semaphore(10)  # Adjust the limit as needed

    async def close(self):
        pass

    def _evaluate_input(self):
        if self.previous or self.input is not None:
            self.data = self.input

    def chunkify(self, lst, n):
        """Split list lst into chunks of size n."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    async def start(self, **kwargs):
        self._counter: int = 0
        self._evaluate_input()
        if not self._action:
            raise RuntimeError(
                'NetworkNinja component requires a *action* Function'
            )
        if not isinstance(self.data, dict):
            raise ComponentError(
                "NetworkNinja requires a Dictionary as Payload",
                status=404
            )
        return True

    async def run(self):
        """Run NetworkNinja Router."""
        tasks = []
        fn = getattr(self, self._action)
        self._result = {}
        if isinstance(self.data, dict):
            # Typical NN payload extract data from dictionary:
            tasks = [
                fn(
                    idx,
                    row,
                ) for idx, row in enumerate(self.data.get('data', []))
            ]
        elif isinstance(self.data, pd.DataFrame):
            tasks = [
                fn(
                    idx,
                    row,
                ) for idx, row in self.data.iterrows()
            ]
        # Execute tasks concurrently
        await self._processing_tasks(tasks)
        print('AQUI > ', self._result)
        # taking actions based on data:
        if self._action == 'process_payload':
            for data_type, data in self._result.items():
                table_name = data_type
                df = pd.DataFrame([obj.to_dict() for obj in data])
                await self.saving_payload(table_name, df)
        return self._result

    async def _processing_tasks(self, tasks: list) -> pd.DataFrame:
        """Process tasks concurrently."""
        results = []
        for chunk in self.chunkify(tasks, self.chunk_size):
            result = await asyncio.gather(*chunk, return_exceptions=True)
            if result:
                results.extend(result)
        return results

    @backoff.on_exception(
        backoff.expo,
        (asyncio.TimeoutError),
        max_tries=2
    )
    async def process_payload(
        self,
        idx,
        row
    ):
        async with self.semaphore:
            # Processing first the Metadata:
            metadata = row.get('metadata', {})
            payload = row.get('payload', {})
            client = metadata.get('client', None)
            data_type = metadata.get('type', None)
            if not data_type:
                raise DataError(
                    "NetworkNinja: Data Type not found in Metadata"
                )
            if data_type not in self._result:
                self._result[data_type] = []
            # Get the Model for the Data Type
            mdl = NetworkNinja_Map.get(data_type)
            if not mdl:
                raise DataError(
                    f"NetworkNinja: Model not found for Data Type: {data_type}"
                )
            error = None
            try:
                # First: adding client to payload:
                payload['org_name'] = client
                # Validate the Data
                data = mdl(**dict(payload))
                # print(f'Data: {data}')
                self._result[data_type].append(data)
                return data, error
            except ValidationError as e:
                print(' ==== ', e)
                error = e.payload
                print(f'Errors: {e.payload}')
                return None, error
            except Exception as e:
                print(f'Error: {e}')
                error = str(e)
                return None, error

    @backoff.on_exception(
        backoff.expo,
        (asyncio.TimeoutError),
        max_tries=2
    )
    async def saving_payload(
        self,
        tablename,
        data
    ):
        async with self.semaphore:
            print('DF > ', data)
