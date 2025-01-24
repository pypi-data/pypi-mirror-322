import io
import logging
from typing import Dict, Iterator, List, Union

import pandas as pd
import pyarrow as pa
from pyarrow.lib import ArrowInvalid

from odp.tabular_v2 import big, bsquare
from odp.tabular_v2.client import Table
from odp.tabular_v2.client.validation import validate_data_against_schema
from odp.tabular_v2.util import exp


class Transaction:
    def __init__(self, table: Table, tx_id: str, buf: big.Buffer):
        if not tx_id:
            raise ValueError("tx_id must not be empty")
        self._table = table
        self._id = tx_id
        self._buf: List[Union[pa.RecordBatch, List[Dict]]] = []
        self._buf_rows = 0
        self._big_buf = buf

    def select(self, query: Union[exp.Op, str, None] = None) -> Iterator[Dict]:
        for row in self._table.select(query).rows():
            yield row

    def replace(self, query: Union[exp.Op, str, None] = None, vars: Union[Dict, List, None] = None) -> Iterator[Dict]:
        """perform a two-step replace:
        rows that don't match the query are kept.
        rows that match are removed and sent to the caller.
        the caller might insert them again or do something else.
        """
        if query is None:
            raise ValueError("For your own safety, please provide a query like 1==1")
        assert self._buf_rows == 0  # FIXME: handle buffered data in replace/select
        for row in self._table._query_cursor(type="replace", query=query, vars=vars, tx_id=self._id).rows():
            yield row

    def delete(self, query: Union[exp.Op, str, None] = None) -> int:
        ct = 0
        for _ in self.replace(query):
            ct += 1
        return ct

    def flush(self):
        logging.info("flushing to stage %s", self._id)
        if len(self._buf) == 0:
            return

        buf = io.BytesIO()
        w = pa.ipc.RecordBatchStreamWriter(buf, self._table._inner_schema)

        for b in self._buf:
            if isinstance(b, list):
                b = pa.RecordBatch.from_pylist(b, schema=self._table._outer_schema)
            df = b.to_pandas()
            df = bsquare.encode(df, self._table._outer_schema)
            df = self._big_buf.encode(df)

            try:
                w.write_batch(pa.RecordBatch.from_pandas(df, schema=self._table._inner_schema))
            except ArrowInvalid as e:
                raise ValueError("Invalid arrow format") from e
        w.close()
        self._table._client._request(
            path="/api/table/v2/insert",
            params={
                "table_id": self._table._id,
                "tx_id": self._id,
            },
            data=buf.getvalue(),
        ).json()
        self._buf = []
        self._buf_rows = 0

    def insert(self, data: Union[Dict, List[Dict], pa.RecordBatch, pd.DataFrame]):
        """queue data to be inserted on flush()"""
        if isinstance(data, dict):
            data = [data]

        validate_data_against_schema(data, self._table._outer_schema)
        if isinstance(data, list):
            # we expand the last list if it's already a list
            last = self._buf[-1] if self._buf else None
            if last and isinstance(last, list):
                last.extend(data)
            else:
                self._buf.append(data)
            self._buf_rows += len(data)
        elif isinstance(data, pd.DataFrame):
            data = pa.RecordBatch.from_pandas(data, schema=self._table._outer_schema)
            self._buf.append(data)
            self._buf_rows += data.num_rows
        elif isinstance(data, pa.RecordBatch):
            self._buf.append(data)
            self._buf_rows += data.num_rows
        else:
            raise ValueError(f"unexpected type {type(data)}")

        if self._buf_rows >= 10_000:
            self.flush()
