from typing import Dict, List, Union, Tuple
import json
import os
from uuid import uuid4
from datetime import date

from .lectric_types import HashAlgo
from requests import Response
from functools import wraps

from .models.input_data import InputData
from .models.index_in_spec import IndexInSpec
from .models.collection import Collection
from .models.collection_in_spec import CollectionInSpec
from .models.query_spec import QuerySpec
from .models.vector_query_spec import VectorQuerySpec
from .models.query_response import QueryResponse
from .models.collection_metadata import CollectionMetadata
from .models.exact_collection_entry import ExactCollectionEntry
from .models.schema_info_exact_schema_info_get_response_schema_info_exact_schema_info_get import SchemaInfoExactSchemaInfoGetResponseSchemaInfoExactSchemaInfoGet
from lectric.models.set_ttls_exact_ttls_collection_name_put_ttls import SetTtlsExactTtlsCollectionNamePutTtls

from .helpers import *
from .client import AuthenticatedClient
from .types import File as fastAPIFile

# defaults
from .api.default import  root_get, root_auth_auth_get, list_connections_connections_get

# collections
from .api.collection import (
    create_collection_collection_create_post,
    exists_collection_collection_exists_name_get,
    is_empty_collection_collection_empty_name_get,
    get_collection_collection_get_name_get,
    list_collections_collection_list_get,
    get_indexes_collection_indexes_name_get,
    drop_collection_collection_delete,
    sizeof_collection_collection_size_name_get,
    delete_entities_collection_entities_delete,
    sample_collection_sample_get,
    get_url_collection_get_url_get
)

# ingest
from .api.ingest import ingest_ingest_post
from .api.ingest import ingest_w_file_ingest_file_post

# index
from .api.index import create_index_create_post, delete_index_collection_name_field_name_delete

# query
from .api.query import query_query_fields_post, query_query_vectors_post

# exact
from .api.exact import (
    create_collection_exact_create_collection_post,
    put_entry_by_uri_exact_hash_collection_name_uri_put,
    put_entry_by_file_exact_hash_collection_name_file_put,
    lookup_by_uri_exact_lookup_hash_uri_collection_name_get,
    lookup_by_file_exact_lookup_file_collection_name_post,
    list_collections_exact_list_get,
    get_available_algos_exact_algos_get,
    is_algo_available_exact_available_algo_get,
    info_exact_info_get,
    has_revlookup_exact_revlookup_get,
    revlookup_list_exact_revlookup_list_get,
    has_dupecounter_exact_dupecounter_get,
    dupes_list_exact_counter_dupes_get,
    raw_query_exact_experimental_raw_query_post,
    ping_exact_ping_post,
    schema_info_exact_schema_info_get,
    hard_delete_collection_exact_collection_hard_delete_delete,
    hard_delete_entries_by_file_exact_entries_by_file_hard_delete_delete,
    hard_delete_entries_exact_entries_hard_delete_delete,
    soft_delete_collection_exact_collection_soft_delete_delete,
    soft_delete_entries_by_file_exact_entries_by_file_soft_delete_delete,
    soft_delete_entries_exact_entries_soft_delete_delete,
    select_entries_exact_select_post,
    get_collection_metadata_exact_collection_metadata_get,
    restore_entries_exact_entries_restore_patch,
    restore_collection_exact_collection_restore_patch,
    trashcan_entries_exact_trashcan_entries_get,
    get_exact_collection_entries_exact_collection_entries_get,
    set_ttls_exact_ttls_collection_name_put,
    get_ttls_exact_ttls_collection_name_get,
    ttls_cleanup_exact_ttls_cleanup_post
)

from .models.body_put_entry_by_file_exact_hash_collection_name_file_put import BodyPutEntryByFileExactHashCollectionNameFilePut
from .models.body_lookup_by_file_exact_lookup_file_collection_name_post import BodyLookupByFileExactLookupFileCollectionNamePost
from .models.body_ingest_w_file_ingest_file_post import BodyIngestWFileIngestFilePost
from .models.body_hard_delete_entries_by_file_exact_entries_by_file_hard_delete_delete import BodyHardDeleteEntriesByFileExactEntriesByFileHardDeleteDelete
from .models.body_hard_delete_entries_exact_entries_hard_delete_delete import BodyHardDeleteEntriesExactEntriesHardDeleteDelete
from .models.body_soft_delete_entries_by_file_exact_entries_by_file_soft_delete_delete import BodySoftDeleteEntriesByFileExactEntriesByFileSoftDeleteDelete
from .models.body_soft_delete_entries_exact_entries_soft_delete_delete import BodySoftDeleteEntriesExactEntriesSoftDeleteDelete

def propagate_exception(func):
    @wraps(func)
    def propagator(*args, **kwargs):

        response = func(*args, **kwargs)

        if response:
            if response.status_code == HTTPStatus.OK:
                return response.parsed
            else:
                raise RuntimeError(f"HTTP Code: {response.status_code}, {response}")
        else:
            raise RuntimeError("No response")

    return propagator


class LectricClient:

    def __init__(self, api_url: str, api_key: str=None,
                    cookies: Dict[str, str]={}, timeout:int=60000) -> None:
        """The Lectric client class

        Args:
            api_url (str): The base url for the api service
            api_key (str, optional): The API key for the service. Defaults to None.
            cookies (Dict[str, str], optional): Optional cookies to be maintained. Defaults to {}.
            timeout (int, optional): Request timeout. Defaults to 60000.
        """
        self.api_url = api_url

        self.client = AuthenticatedClient(base_url=self.api_url,
                                    token=api_key, cookies=cookies,
                                    headers={"X-API-KEY": api_key} if api_key else {},
                                    timeout=timeout)

        response_dict = json.loads(self.verify_connection(api_key is not None).content)

        self.api_build_id = response_dict.get("lectric-build-id")
        self.backend_db = response_dict.get("lectric-vdb-backend")

    def verify_connection(self, is_authenticated: bool=False) -> Response:
        """Test the connection to the Lectric server

        Returns:
            bool|RuntimeError: Either True for success or failure
        """

        if is_authenticated:
            response = root_auth_auth_get.sync_detailed(client=self.client)
        else:
            response = root_get.sync_detailed(client=self.client)

        if response.status_code != HTTPStatus.OK.value:
            raise RuntimeError(f"HTTP Code: {response.status_code}, {response}")

        return response

    @propagate_exception
    def list_connections(self) -> List[str]:
        """List the connections created within the vector db

        Returns:
            List[str]: A list of the connection names
        """
        return list_connections_connections_get.sync_detailed(client=self.client)


    ########################## collections ###############################

    @propagate_exception
    def create_collection(self, coll_in_spec: CollectionInSpec,
                                    with_reverse_lookup: bool=False,
                                    with_dupe_counter: bool=False,
                                    hash_algo: HashAlgo =HashAlgo.md5
                                    ) -> Collection:
        """Create an exact OR vector collection. If `coll_in_spec.approx == True` then the collection created will be a vector/approximate collection; if not it will be an exact one

        Args:
            coll_in_spec (CollectionInSpec): The collection specification to be created
            with_reverse_lookup (bool): Only relevant to exact collections. Creates a sidecar collection to do reverse lookups. Defaults to False to False.
            with_dupe_counter (bool): Only relevant to exact collections. Adds a counting attribute to each member of the collection for tracking and counting.
            hash_algo (HashAlgo): The hash algorithm to use for exact collections. Default is HashAlgo.md5

        Returns:
            Collection: An object representing the created collection
        """
        if coll_in_spec.approx:
            return create_collection_collection_create_post.sync_detailed(client=self.client, body=coll_in_spec)
        return create_collection_exact_create_collection_post.sync_detailed(client=self.client,
                                                                                body=coll_in_spec,
                                                                                with_reverse_lookup=with_reverse_lookup,
                                                                                with_dupe_counter=with_dupe_counter,
                                                                                hash_algo=hash_algo.name)


    @propagate_exception
    def collection_exists(self, name: str, exact: bool=False) -> bool:
        """Check if a collection exists

        Args:
            name (str): The name of the collection
            exact (bool): Looking for an exact collection?

        Returns:
            bool: True if the collection exist, else False
        """
        return exists_collection_collection_exists_name_get.sync_detailed(client=self.client, name=name, exact=exact)


    @propagate_exception
    def is_collection_empty(self, name: str) -> bool:
        """Check if the collection has data or is empty

        Args:
            name (str): The name of the collection

        Returns:
            bool: True if the collection is empty, else False
        """
        return is_empty_collection_collection_empty_name_get.sync_detailed(client=self.client, name=name)


    @propagate_exception
    def get_collection(self, name: str) -> Collection:
        """Get a collection by name. Each collection has a unique, user defined name

        Args:
            name (str): The name of the collection.

        Returns:
            Collection: A representation of the collection
        """
        return get_collection_collection_get_name_get.sync_detailed(client=self.client, name=name)


    @propagate_exception
    def get_indexes(self, collection_name: str) -> List[str]:
        """Get a list of the field names for which indexes are defined

        Args:
            collection_name (str): The name of the collection for which indexes are queried

        Returns:
            List[str]: A list of the field names for which indexes are defined
        """
        return get_indexes_collection_indexes_name_get.sync_detailed(client=self.client, name=collection_name)


    @propagate_exception
    def list_collections(self, exact_only: bool=False) -> List[str]:
        """List the names of the collections

        Returns:
            List[str]: The collection names
        """
        if exact_only:
            res = list_collections_exact_list_get.sync_detailed(client=self.client)
            return res
        return list_collections_collection_list_get.sync_detailed(client=self.client)


    @propagate_exception
    def hard_drop_collection(self, collection_name: str, exact: bool=False) -> None:
        """Drop (delete) a collection by name

        Args:
            name (str): The name of the collection to be dropped
            exact (bool): The collection is exact

        Returns:
            _type_: None
        """
        if not exact:
            return drop_collection_collection_delete.sync_detailed(client=self.client, name=collection_name)
        else:
            return hard_delete_collection_exact_collection_hard_delete_delete.sync_detailed(client=self.client, collection_name=collection_name)

    @propagate_exception
    def soft_drop_collection(self, collection_name: str, exact: bool=False, deleter: str=None) -> None:
        """Drop (delete) a collection by name

        Args:
            name (str): The name of the collection to be dropped
            exact (bool): The collection is exact

        Returns:
            _type_: None
        """
        if not exact:
            raise NotImplementedError("Soft-delete entries has not been implemented for approx yet")
        else:
            return soft_delete_collection_exact_collection_soft_delete_delete.sync_detailed(client=self.client, collection_name=collection_name, deleter=deleter)

    @propagate_exception
    def soft_delete_entities(self, collection_name: str,
                ids: Union[List[str], List[int]]=None,
                urls: List[str]=None,
                file: Union[BinaryIO, bytes, str]=None,
                is_approx: bool=True,
                deleter: str=None) -> None:
        """Delete entities by Primary key ID, or (for exact:) by file or URI

        Args:
            collection_name (str): The collection name
            ids (Union[List[str], List[int]], optional): The list of IDs for which is to happen
            urls (List[str], optional): A list of URLs to be hashed & potentially deleted. Defaults to None.
            file (Union[BinaryIO, bytes, str], optional): File to be hashed & potentially deleted. Defaults to None.
            is_approx (bool): Is the collection approximate or exact?

        Returns:
            _type_: None
        """
        if is_approx:
            raise NotImplementedError("Soft-delete entries has not been implemented for approx yet")
        else:
            # Exact
            if ids:
                return soft_delete_entries_exact_entries_soft_delete_delete.sync_detailed(
                    client=self.client, collection_name=collection_name,
                    body=BodySoftDeleteEntriesExactEntriesSoftDeleteDelete(entry_ids=ids),
                    deleter=deleter
                )
            if urls:
                return soft_delete_entries_exact_entries_soft_delete_delete.sync_detailed(
                    client=self.client, collection_name=collection_name,
                    body=BodySoftDeleteEntriesExactEntriesSoftDeleteDelete(urls=urls),
                    deleter=deleter
                )
            if file:
                return soft_delete_entries_by_file_exact_entries_by_file_soft_delete_delete.sync_detailed(
                    client=self.client, collection_name=collection_name,
                    multipart_data=BodySoftDeleteEntriesByFileExactEntriesByFileSoftDeleteDelete(
                        file=fastAPIFile(payload=get_tmp_file(file), file_name=str(uuid4()),
                                                mime_type="image/jpg")
                    ),
                    deleter=deleter
                )

    @propagate_exception
    def get_trashcan_entries(self,
                             deleter: str=None,
                             exact: bool=True,
                             start_date: date=None,
                             end_date: date=None,
                             order_by: str=None,
                             desc: bool=True,
                             limit: int=1000):
        if not exact:
            raise NotImplementedError("Getting trash can entries is not supported for approx.")
        else:
            return trashcan_entries_exact_trashcan_entries_get.sync_detailed(client=self.client,
                                                                             deleter=deleter,
                                                                             start_date=start_date,
                                                                             end_date=end_date,
                                                                             order_by=order_by,
                                                                             desc=desc,
                                                                             limit=limit)
        
    @propagate_exception
    def hard_delete_entities(self, collection_name: str,
                ids: Union[List[str], List[int]]=None,
                urls: List[str]=None,
                file: Union[BinaryIO, bytes, str]=None,
                is_approx: bool=True) -> None:
        """Delete entities by Primary key ID, or (for exact:) by file or URI

        Args:
            collection_name (str): The collection name
            ids (Union[List[str], List[int]], optional): The list of IDs for which is to happen
            urls (List[str], optional): A list of URLs to be hashed & potentially deleted. Defaults to None.
            file (Union[BinaryIO, bytes, str], optional): File to be hashed & potentially deleted. Defaults to None.
            is_approx (bool): Is the collection approximate or exact?

        Returns:
            _type_: None
        """
        if is_approx:
            return delete_entities_collection_entities_delete.sync_detailed(
                client=self.client, name=collection_name, body=ids)
        else:
            # Exact
            if ids:
                return hard_delete_entries_exact_entries_hard_delete_delete.sync_detailed(
                    client=self.client, collection_name=collection_name,
                    body=BodyHardDeleteEntriesExactEntriesHardDeleteDelete(entry_ids=ids)
                )
            if urls:
                return hard_delete_entries_exact_entries_hard_delete_delete.sync_detailed(
                    client=self.client, collection_name=collection_name,
                    body=BodyHardDeleteEntriesExactEntriesHardDeleteDelete(urls=urls),
                )
            if file:
                return hard_delete_entries_by_file_exact_entries_by_file_hard_delete_delete.sync_detailed(
                    client=self.client, collection_name=collection_name,
                    multipart_data=BodyHardDeleteEntriesByFileExactEntriesByFileHardDeleteDelete(
                        file=fastAPIFile(payload=get_tmp_file(file), file_name=str(uuid4()),
                                                mime_type="image/jpg")
                    )
                )

    @propagate_exception
    def sample_entities(self, collection_name: str, max_samples: int = 20):
        """Sample entities of a collection

        Args:
            collection_name (str): The collection name
            max_samples (int, optional): The maximum number of entities to sample. Defaults to 20.

        Returns:
            _type_: _description_
        """

        return sample_collection_sample_get.sync_detailed(client=self.client,
                collection_name=collection_name, max_samples=max_samples)


    @propagate_exception
    def sizeof(self, name: str, exact: bool=False) -> int:
        """Get the size of (number of entities) in a collection

        Args:
            name (str): The collection name
            exact (bool): is the collection an exact lookup?

        Raises:
            RuntimeError: If collection does not exist

        Returns:
            int: The size of the collection
        """
        return sizeof_collection_collection_size_name_get.sync_detailed(client=self.client, name=name, exact=exact)


    @propagate_exception
    def ingest(self, data: InputData) -> None:
        """Ingest data into a collection

        Args:
            data (InputData): The data to be ingested

        Returns:
            _type_: None
        """
        return ingest_ingest_post.sync_detailed(client=self.client, body=data)


    @propagate_exception
    def ingest_with_file(self, collection_name: str, json_input_data: str,
                    file: Union[str, bytes, BinaryIO]=None) -> None:
        """Ingest *a single* element with a file into a collection

        Args:
            collection_name (str): The unique name of the collection
            json_input_data (str): A json string formatted input identical to that of InputData
            file (Union[str, bytes, BinaryIO], optional): _description_. Defaults to None.

        Returns:
            _type_: None
        """

        file_name: str = "tmpfile"
        if isinstance(file, str):
            try:
                file_name = os.path.basename(file)
            except:
                pass # we did our best \_(ツ)_/¯

        return ingest_w_file_ingest_file_post.sync_detailed(client=self.client, multipart_data=BodyIngestWFileIngestFilePost(
            file=fastAPIFile(payload=get_tmp_file(file), file_name=file_name, mime_type="image/jpg")),
            collection_name=collection_name, json_input_data=json_input_data
        )

    @propagate_exception
    def create_index(self, index_spec: IndexInSpec) -> None:
        """Create an index for one field within the collection

        Args:
            index_spec (IndexInSpec): The creation spec of the index

        Returns:
            _type_: None
        """
        return create_index_create_post.sync_detailed(client=self.client, body=index_spec)


    @propagate_exception
    def drop_index(self, collection_name: str, field_name: str) -> None:
        """Drop (delete) a previously created index

        Args:
            collection_name (str): The collection name
            field_name (str): The field name on which the index is defined

        Returns:
            _type_: None
        """
        return delete_index_collection_name_field_name_delete.sync_detailed(client=self.client, collection_name=collection_name, field_name=field_name)

    @propagate_exception
    def query(self, query_spec: Union[QuerySpec, VectorQuerySpec]) -> Union[List[Dict], QueryResponse]:
        """Query a collection using either a vector, a batch of vectors or query on the fields

        Args:
            query_spec (Union[QuerySpec, VectorQuerySpec]): The specification of the query

        Raises:
            RuntimeError: If the query spec is non conformant, this is raised.

        Returns:
            Union[List[Dict], QueryResponse]: Either a list with the queried fields or a QueryResponse object from a vector query
        """

        if isinstance(query_spec, QuerySpec):
            return query_query_fields_post.sync_detailed(client=self.client, body=query_spec)
        elif isinstance(query_spec, VectorQuerySpec):
            return query_query_vectors_post.sync_detailed(client=self.client, body=query_spec)
        else:
            raise RuntimeError(f"Unable to query with given query spec of type {type(query_spec)}")

    @propagate_exception
    def recover_collection(self, collection_name: str, is_approx: bool = False) -> None:
        if is_approx:
            raise NotImplementedError("Approximate collections not yet supported")
        return restore_collection_exact_collection_restore_patch.sync_detailed(client=self.client, name=collection_name)

    @propagate_exception
    def restore_entries(self, collection_name: str,
                ids: Union[List[str], List[int]]=None,
                is_approx: bool=True) -> None:
        if is_approx:
            raise NotImplementedError("Approximate collections not yet supported")
        if ids:
            return restore_entries_exact_entries_restore_patch.sync_detailed(
                client=self.client, collection_name=collection_name,
                body=ids
            )

    @propagate_exception
    def put_exact(self, collection_name: str,
                    foreign_key: Union[str, int]=None,
                    file: Union[str, bytes, BinaryIO]=None,
                    uri: str=None,
                    metadata: dict=None,
                    upsert: bool = False,
                    timestamp: str = None,
                    store_raw_data: bool = False,
                    ingestor: str=None
                    ) -> str:
        """Put an entry into an exact store collection

        Args:
            collection_name (str): The collection name
            foreign_key (Union[str, int], optional): Foreign. key Defaults to None.
            file (Union[str, bytes, BinaryIO], optional): The file containing the data. Defaults to None.
            uri (str, optional): The URI of input data. Defaults to None.
            metadata (dict, optional): Dictionary of additional metadata to store with entry. Defaults to None.
            upsert (bool, optional): Update entry if it already exists. Defaults to None.
            timestamp (str, optional): Timestamp to associate with entry. Defaults to None.
            store_raw_data(bool, optional): Store the raw data directly in lectric. Defaults to False.

        Raises:
            RuntimeError: When input file or URI is unprocessable

        Returns:
            str: The inserted hash
        """
        if uri:
            return put_entry_by_uri_exact_hash_collection_name_uri_put.sync_detailed(
                collection_name=collection_name, client=self.client,
                foreign_key=foreign_key, uri=uri,
                upsert=upsert,
                metadata=None if not metadata else json.dumps(metadata),
                timestamp=timestamp,
                store_raw_data=store_raw_data,
                ingestor=ingestor)
        elif file:
            return put_entry_by_file_exact_hash_collection_name_file_put.sync_detailed(
                collection_name=collection_name, client=self.client,
                multipart_data=BodyPutEntryByFileExactHashCollectionNameFilePut(
                        file=fastAPIFile(payload=get_tmp_file(file), file_name="tmpfile", mime_type="image/jpg")
                    ), foreign_key = foreign_key, metadata=None if not metadata else json.dumps(metadata),
                        upsert=upsert, timestamp=timestamp,
                        store_raw_data=store_raw_data,
                        ingestor=ingestor
                )

    @propagate_exception
    def lookup_exact(self, collection_name: str,
                    file: Union[str, bytes, BinaryIO]=None,
                    uri: str=None,
                    fk: str=None,
                    caller: str=None) -> Union[List[str], None]:
        """Lookup exact entry in a collection

        Args:
            collection_name (str): The name of the collection
            file (Union[str, bytes, BinaryIO], optional): Input file data. Defaults to None.
            uri (str, optional): Input URI data. Defaults to None.

        Raises:
            RuntimeError: When input file or URI is unprocessable

        Returns:
            Union[List[str], None]: The found match or None
        """
        if uri:
            return lookup_by_uri_exact_lookup_hash_uri_collection_name_get.sync_detailed(
                collection_name=collection_name, client=self.client, uri=uri, fk=fk, caller=caller
            )
        elif file:
            return lookup_by_file_exact_lookup_file_collection_name_post.sync_detailed(
                collection_name=collection_name, client=self.client,
                multipart_data=BodyLookupByFileExactLookupFileCollectionNamePost(
                        file=fastAPIFile(payload=get_tmp_file(file), file_name="tmpfile", mime_type="image/jpg")
                    )
                )

    @propagate_exception
    def get_exact_hash_algos(self) -> List[str]:
        """Get a list of the available hashing algorithms

        Returns:
            List[str]: A list of the hash algos
        """
        return get_available_algos_exact_algos_get.sync_detailed(client=self.client)

    @propagate_exception
    def is_exact_algos_available(self, algo: str) -> bool:
        """Determine whether a specific hashing algorithm is supported

        Args:
            algo (str): The algorithm name

        Returns:
            bool: True if the algorithm is supported/available for use
        """
        return is_algo_available_exact_available_algo_get.sync_detailed(client=self.client)

    @propagate_exception
    def get_exact_collection_entries(self,
                    collection_name: str,
                    ingestor: str = None,
                    start_date: date = None,
                    end_date: date = None,
                    ingest_source: str = None,
                    traits: str = None,
                    order_by: str = None,
                    desc: bool = True,
                    limit: int = 1000) -> List[ExactCollectionEntry]:
        """
        Get exact entries in a collection_name

        Args:
            ingestor (str): Email address of the ingestor
            collection_name (str): Collection Name
            start_date (date): Start date (UTC)
            end_date (date): End date (UTC)
            order_by (str): Order the results by this field. Defaults to None.
            desc (bool): Order descending? or ascending. Defaults to True.
            limit (int): the max results to return. Defaults to 1000.

        Returns:
            List[Dict]: entries in a given collection_name collection, ingested by ingestor (if provided), contained within the date ranges (if provided).
        """
        return get_exact_collection_entries_exact_collection_entries_get.sync_detailed(client=self.client,
                                                                                       collection_name=collection_name,
                                                                                       ingestor=ingestor,
                                                                                       start_date=start_date,
                                                                                       end_date=end_date,
                                                                                       ingest_source=ingest_source,
                                                                                       traits=traits,
                                                                                       order_by=order_by,
                                                                                       desc=desc,
                                                                                       limit=limit)

    @propagate_exception
    def exact_select(self, collection_name: str,
                        what: str = "*",
                        where: str = None,
                        order_by: str = None,
                        desc: bool = True,
                        limit: int = 10000) -> List[Dict]:
        """Select from collection using SQL logic

        Args:
            collection_name (str): The unique name of the collection
            what (str, optional): what columns/fields to select. Defaults to "*".
            where (str, optional): the where predicate. Defaults to None.
            order_by (str, optional): order the results by this field. Defaults to None.
            desc (bool, optional): order descending? or ascending. Defaults to True.
            limit (int, optional): the max results to return. Defaults to 10000.

        Returns:
            List[Dict]: entries matching the query from the database
        """

        return select_entries_exact_select_post.sync_detailed(
            client=self.client, collection_name=collection_name,
            what=what, where=where, order_by=order_by, desc=desc, limit=limit
        )

    def _pformat_collection(self, collection: Collection) -> str:
        return f"""
                Collection name: {collection.name}
                Size (estimated): {self.sizeof(collection.name)}
                Index(es): {self.get_indexes(collection.name)}
                {pformat_collection_schema(collection.coll_schema)}
                """

    @propagate_exception
    def _exact_info(self, collection_name: str):
         return info_exact_info_get.sync_detailed(client=self.client, name=collection_name)


    def info(self, collection_name: str, exact: bool = False) -> str:
        """Get info on a collection

        Args:
            collection_name (str): The unique name of the collection
            exact (bool, optional): Exact collections only? Defaults to False.
        """
        if exact:
            return self._exact_info(collection_name)
        else:
            return self._pformat_collection(self.get_collection(collection_name))

    @propagate_exception
    def has_reverse_lookup(self, collection_name: str) -> bool:
        """Does the exact collection have reverse lookup enabled

        Args:
            collection_name (str): The unique name of the exact collection

        Returns:
            bool: True if so, else False
        """
        return has_revlookup_exact_revlookup_get.sync_detailed(client=self.client, name=collection_name)


    @propagate_exception
    def reverse_lookup(self, collection_name: str, limit: int = None) -> List[Tuple]:
        """Get elements from the reverse lookup

        Args:
            collection_name (str): The unique name of the collection
            limit (int, optional): Limit the number of outputs. Defaults to None.

        Returns:
            List[Tuple]: The returned elements in the reverse lookup
        """

        return revlookup_list_exact_revlookup_list_get.sync_detailed(
                        client=self.client, name=collection_name, limit=limit)

    @propagate_exception
    def has_dupe_counter(self, collection_name: str) -> bool:
        """Does the exact collection have duplicate counting enabled

        Args:
            collection_name (str): The unique name of the exact collection

        Returns:
            bool: True if so, else False
        """
        return has_dupecounter_exact_dupecounter_get.sync_detailed(client=self.client, name=collection_name)


    @propagate_exception
    def get_dupes(self, collection_name: str, limit: int = None, total_only: bool=False) -> Union[List[Tuple], int]:
        """Get duplicates from exact collections with counter enabled

        Args:
            collection_name (str): The unique name of the collection
            limit (int, optional): The maximum number of entries to return. Defaults to None.
            total_only (bool, optional): Provide only the total count of duplicates. Defaults to False.

        Returns:
            Union[List[Tuple], int]: Either the duplicates requested or the total only
        """

        return dupes_list_exact_counter_dupes_get.sync_detailed(
                                client=self.client, name=collection_name, limit=limit, total_only=total_only)

    @propagate_exception
    def raw_query(self, query: str) -> List[Tuple]:
        """EXPERIMENTAL: Query directly into the underlying storage for data. Use SQL syntax

        Args:
            query (str): The query string

        Returns:
            List[Tuple]: Database rows response
        """
        return raw_query_exact_experimental_raw_query_post.sync_detailed(client=self.client, query=query)

    @propagate_exception
    def has_exact_engine(self) -> bool:
        """Check if the client has an exact engine active

        Returns:
            bool: If the exact engine is configured and available
        """
        return  ping_exact_ping_post.sync_detailed(client=self.client)

    @propagate_exception # TODO: Hack! We should use get_collection and populate accordingly
    def get_schema_info(self, collection_name: str) -> SchemaInfoExactSchemaInfoGetResponseSchemaInfoExactSchemaInfoGet:
        """Get the underlying storage schema

        Args:
            collection_name (str): The name of the collection

        Returns:
            SchemaInfoExactSchemaInfoGetResponseSchemaInfoExactSchemaInfoGet: A representation of each column in the schema with its type
        """
        return schema_info_exact_schema_info_get.sync_detailed(client=self.client, name=collection_name)

    @propagate_exception
    def get_url(self, path: str, validity_period_days: int=1) -> str:
        """Get the URL of data stored within Lectric given a file path. Obtain the file path through a query on an collection that has a link field schema

        Args:
            path (str): The file path within the collection
        Returns:
            str: a fully defined url
        """

        return get_url_collection_get_url_get.sync_detailed(client=self.client, path=path, validity_period_days=validity_period_days)

    @propagate_exception
    def get_collection_metadata(self, collection_name: str, is_approx: bool=False) -> CollectionMetadata:
        """Retrieves the collection metadata, which includes the ETag stored in the form of the last updated timestamp.

        Args:
            collection_name (str): Collection Name
            is_approx (bool): Is the collection an approximate one or not
        Returns:
            str: Collection Metadata
        """
        if is_approx:
            raise NotImplementedError("Approximate collections not yet supported")
        else:
            return get_collection_metadata_exact_collection_metadata_get.sync_detailed(
                                        client=self.client, collection_name=collection_name)

    @propagate_exception
    def set_collection_ttls(self, collection_name: str, ttls: Dict[str, int]={}, is_approx: bool=False) -> Dict:
        """Set the TTLs for the collection

        Args:
            collection_name (str): The name of the collection
            ttls (Dict[str, int]): A dictionary of the TTLs for each field

        Returns:
            Dict: The updated TTLs
        """
        if is_approx:
            raise NotImplementedError("Approximate setting TTLs is not yet supported")
        else:
            return set_ttls_exact_ttls_collection_name_put.sync_detailed(client=self.client, collection_name=collection_name,
                                                                        body=SetTtlsExactTtlsCollectionNamePutTtls.from_dict(ttls))

    @propagate_exception
    def get_collection_ttls(self, collection_name, is_approx: bool=False) -> Dict:
        """Get the TTLs for the collection

        Args:
            collection_name (str): The name of the collection
            is_approx (bool): Is the collection approximate or not

        Returns:
            Dict: The TTLs for the collection
        """
        if is_approx:
            raise NotImplementedError("Approximate getting TTLs is not yet supported")  
        else:
            return get_ttls_exact_ttls_collection_name_get.sync_detailed(client=self.client, collection_name=collection_name)

    @propagate_exception
    def ttls_cleanup(self, collection_names: List[str], is_approx: bool=False) -> List[str]:
        """Cleanup TTLs for the collection fields that have expired

        Args:
            collection_names (List[str]): The collection names for whch TTLs are to be cleaned up
            is_approx (bool, optional): Consider approximate collections? Defaults to False.

        Returns:
            List[str]: The status of the cleanup by collection
        """
        if is_approx:
            raise NotImplementedError("Approximate TTL cleanup is not yet supported")  
        else:
            return ttls_cleanup_exact_ttls_cleanup_post.sync_detailed(client=self.client, body=collection_names)