import sys

from langchain.schema import Document

from transwarp_hippo_api.hippo_client import *
from transwarp_hippo_api.hippo_type import *
import logging
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.base import VectorStore
from typing import Any, Iterable, List, Optional, Tuple, Dict
import random

logger = logging.getLogger(__name__)

# Default connection
DEFAULT_HIPPO_CONNECTION = {
    "host": "172.18.128.48",
    "port": "8922",
    "username": "shiva",
    "password": "shiva"
}


class Hippo(VectorStore):
    def __init__(
            self,
            embedding_function: Embeddings,
            table_name: str = "zdc_test_langchain01",
            database_name: str = "default",
            number_of_shards: int = 1,
            number_of_replicas: int = 1,
            connection_args: Optional[Dict[str, Any]] = None,
            index_params: Optional[dict] = None,
            drop_old: Optional[bool] = False,
    ):

        self.number_of_shards = number_of_shards
        self.number_of_replicas = number_of_replicas
        self.embedding_func = embedding_function
        self.table_name = table_name
        self.database_name = database_name
        self.index_params = index_params

        # In order for a collection to be compatible, pk needs to be auto'id and int
        self._primary_field = "pk"
        # In order for compatiblility, the text field will need to be called "text"
        self._text_field = "text"
        # In order for compatbility, the vector field needs to be called "vector"
        self._vector_field = "vector"
        self.fields: List[str] = []
        # Create the connection to the server
        if connection_args is None:
            connection_args = DEFAULT_HIPPO_CONNECTION
        self.hc = self._create_connection_alias(connection_args)
        self.col = Optional[HippoTable]

        # If the collection exists, delete it
        try:
            if self.hc.get_table(self.table_name, self.database_name) and drop_old:
                self.hc.delete_table(self.table_name, self.database_name)
        except:
            pass

        try:
            if self.hc.get_table(self.table_name, self.database_name):
                self.col = self.hc.get_table(self.table_name, self.database_name)
        except:
            pass

        # Initialize the vector database
        self._init()

    def _create_connection_alias(self, connection_args: dict) -> HippoClient:
        """Create the connection to the Hippo server."""
        # Grab the connection arguments that are used for checking existing connection
        host: str = connection_args.get("host", None)
        port: int = connection_args.get("port", None)
        username: str = connection_args.get("username", "shiva")
        password: str = connection_args.get("password", "shiva")

        # Order of use is host/port, uri, address
        if host is not None and port is not None:
            if "," in host:
                hosts = host.split(',')
                given_address = ','.join([f'{h}:{port}' for h in hosts])
            else:
                given_address = str(host) + ":" + str(port)
        else:
            logger.debug("Missing standard address type for reuse atttempt")

        try:
            logger.info(f"create HippoClient[{given_address}]")
            return HippoClient([given_address], username=username, pwd=password)
        except Exception as e:
            logger.error("Failed to create new connection")
            raise e

    def _init(
            self, embeddings: Optional[list] = None, metadatas: Optional[List[dict]] = None
    ) -> None:
        logger.info(f"init ...")
        if embeddings is not None:
            logger.info(f"create collection")
            self._create_collection(embeddings, metadatas)
        self._extract_fields()
        self._create_index()
        # self._create_search_params()

    def _create_collection(
            self, embeddings: list, metadatas: Optional[List[dict]] = None
    ) -> None:

        # Determine embedding dim
        dim = len(embeddings[0])
        logger.debug(f"[_create_collection] dim: {dim}")
        fields = []

        # Create the primary key field
        fields.append(
            HippoField(self._primary_field, True, HippoType.STRING)
        )

        # Create the text field

        fields.append(
            HippoField(self._text_field, False, HippoType.STRING)
        )

        # Create the vector field, supports binary or float vectors
        # TODO 二进制向量类型待开发
        fields.append(
            HippoField(self._vector_field, False, HippoType.FLOAT_VECTOR, type_params={"dimension": dim})
        )
        # TODO Determine metadata schema hippo中没有类似于 milvus 中 infer_dtype_bydata 数据类型推断的方法,所以目前将非向量类型的数据均转化为string类型。

        if metadatas:
            #     # Create FieldSchema for each entry in metadata.
            for key, value in metadatas[0].items():
                #         # Infer the corresponding datatype of the metadata
                if isinstance(value, list):
                    value_dim = len(value)
                    fields.append(HippoField(key, False, HippoType.FLOAT_VECTOR, type_params={"dimension": value_dim}))
                else:
                    fields.append(HippoField(key, False, HippoType.STRING))

        logger.debug(f"[_create_collection] fields: {fields}")

        # Create the collection
        self.hc.create_table(name=self.table_name, auto_id=True, fields=fields,
                             database_name=self.database_name,
                             number_of_shards=self.number_of_shards,
                             number_of_replicas=self.number_of_replicas)
        self.col = self.hc.get_table(self.table_name, self.database_name)
        logger.info(f"[_create_collection] : create table {self.table_name} in {self.database_name} successfully")

    def _extract_fields(self) -> None:
        """Grab the existing fields from the Collection"""
        if isinstance(self.col, HippoTable):
            schema: List[HippoField] = self.col.schema
            logger.debug(f"[_extract_fields] schema:{schema}")
            for x in schema:
                self.fields.append(x.name)
            logger.debug(f"04 [_extract_fields] fields:{self.fields}")

    # TODO 目前只针对列名为 vector 的字段（自动创建的向量字段）进行索引校验，其他向量类型的列需要自行创建索引
    def _get_index(self) -> Optional[Dict[str, Any]]:
        """Return the vector index information if it exists"""
        if isinstance(self.col, HippoTable):
            table_info = self.hc.get_table_info(self.table_name, self.database_name).get(self.table_name, {})
            embedding_indexes = table_info.get('embedding_indexes', None)
            if embedding_indexes is None:
                return None
            else:
                for x in self.hc.get_table_info(self.table_name, self.database_name)[self.table_name][
                    'embedding_indexes']:
                    logger.debug(f"[_get_index] embedding_indexes {embedding_indexes}")
                    if x['column'] == self._vector_field:
                        return x

    # TODO 只能为self._vector_field 字段创建索引
    def _create_index(self) -> None:
        """Create a index on the collection"""

        if isinstance(self.col, HippoTable) and self._get_index() is None:
            if self._get_index() is None:
                if self.index_params is None:
                    self.index_params = {
                        "index_name": "langchain_auto_create",
                        "metric_type": MetricType.L2,
                        "index_type": IndexType.IVF_FLAT,
                        "nlist": 10,
                    }

                    self.col.create_index(
                        self._vector_field,
                        self.index_params['index_name'],
                        self.index_params['index_type'],
                        self.index_params['metric_type'],
                        nlist=self.index_params['nlist'],
                    )
                    logger.debug(self.col.activate_index(self.index_params['index_name']))
                    logger.info("create index successfully")
                else:

                    index_dict = {
                        "IVF_FLAT": IndexType.IVF_FLAT,
                        "FLAT": IndexType.FLAT,
                        "IVF_SQ": IndexType.IVF_SQ,
                        "IVF_PQ": IndexType.IVF_PQ,
                        "HNSW": IndexType.HNSW
                    }

                    metric_dict = {
                        "ip": MetricType.IP,
                        "IP": MetricType.IP,
                        "l2": MetricType.L2,
                        "L2": MetricType.L2
                    }
                    self.index_params['metric_type'] = metric_dict[self.index_params['metric_type']]

                    if self.index_params['index_type'] == "FLAT":
                        self.index_params['index_type'] = index_dict[self.index_params['index_type']]
                        self.col.create_index(
                            self._vector_field,
                            self.index_params['index_name'],
                            self.index_params['index_type'],
                            self.index_params['metric_type'],
                        )
                        logger.debug(self.col.activate_index(self.index_params['index_name']))
                    elif self.index_params['index_type'] == "IVF_FLAT" or self.index_params['index_type'] == "IVF_SQ":
                        self.index_params['index_type'] = index_dict[self.index_params['index_type']]
                        self.col.create_index(
                            self._vector_field,
                            self.index_params['index_name'],
                            self.index_params['index_type'],
                            self.index_params['metric_type'],
                            nlist=self.index_params.get("nlist", 10),
                            nprobe=self.index_params.get("nprobe", 10)
                        )
                        logger.debug(self.col.activate_index(self.index_params['index_name']))
                    elif self.index_params['index_type'] == "IVF_PQ":
                        self.index_params['index_type'] = index_dict[self.index_params['index_type']]
                        self.col.create_index(
                            self._vector_field,
                            self.index_params['index_name'],
                            self.index_params['index_type'],
                            self.index_params['metric_type'],
                            nlist=self.index_params.get("nlist", 10),
                            nprobe=self.index_params.get("nprobe", 10),
                            nbits=self.index_params.get("nbits", 8),
                            m=self.index_params.get("m")
                        )
                        logger.debug(self.col.activate_index(self.index_params['index_name']))
                    elif self.index_params['index_type'] == "HNSW":
                        self.index_params['index_type'] = index_dict[self.index_params['index_type']]
                        self.col.create_index(
                            self._vector_field,
                            self.index_params['index_name'],
                            self.index_params['index_type'],
                            self.index_params['metric_type'],
                            M=self.index_params.get("M"),
                            ef_construction=self.index_params.get("ef_construction"),
                            ef_search=self.index_params.get("ef_search")
                        )
                        logger.debug(self.col.activate_index(self.index_params['index_name']))
                    else:
                        raise ValueError(
                            "Index name does not match, please enter the correct index name. (FLAT, IVF_FLAT, IVF_PQ, IVF_SQ, HNSW)")

    def add_texts(
            self,
            texts: Iterable[str],
            metadatas: Optional[List[dict]] = None,
            timeout: Optional[int] = None,
            batch_size: int = 1000,
            **kwargs: Any,
    ) -> List[str]:

        """
                Add text to the collection.

                Args:
                    texts: An iterable that contains the text to be added.
                    metadatas: An optional list of dictionaries, each dictionary contains the metadata associated with a text.
                    timeout: Optional timeout, in seconds.
                    batch_size: The number of texts inserted in each batch, defaults to 1000.
                    **kwargs: Other optional parameters.

                Returns:
                    A list of strings, containing the unique identifiers of the inserted texts.

                Note:
                    If the collection has not yet been created, this method will create a new collection.
        """

        if not texts or all(t == "" for t in texts):
            logger.debug("Nothing to insert, skipping.")
            return []
        texts = list(texts)

        logger.debug(f"[add_texts] texts: {texts}")

        try:
            embeddings = self.embedding_func.embed_documents(texts)
        except NotImplementedError:
            embeddings = [self.embedding_func.embed_query(x) for x in texts]

        if len(embeddings) == 0:
            logger.debug("Nothing to insert, skipping.")
            return []

        logger.debug(f"[add_texts] len_embeddings:{len(embeddings)}")

        # 如果还没有创建collection则创建collection
        if not isinstance(self.col, HippoTable):
            self._init(embeddings, metadatas)

        # Dict to hold all insert columns
        insert_dict: Dict[str, list] = {
            self._text_field: texts,
            self._vector_field: embeddings,
        }
        logger.debug(f"[add_texts] metadatas:{metadatas}")
        logger.debug(f"[add_texts] fields:{self.fields}")
        if metadatas is not None:
            for d in metadatas:
                for key, value in d.items():
                    if key in self.fields:
                        insert_dict.setdefault(key, []).append(value)

        logger.debug(insert_dict[self._text_field])

        # Total insert count
        vectors: list = insert_dict[self._vector_field]
        total_count = len(vectors)

        self.fields.remove("pk")

        logger.debug(f"[add_texts] total_count:{total_count}")
        for i in range(0, total_count, batch_size):
            # Grab end index
            end = min(i + batch_size, total_count)
            # Convert dict to list of lists batch for insertion
            insert_list = [insert_dict[x][i:end] for x in self.fields]
            try:
                res = self.col.insert_rows(insert_list)
                logger.info(f"05 [add_texts] insert {res}")
            except Exception as e:
                logger.error(
                    "Failed to insert batch starting at entity: %s/%s", i, total_count
                )
                raise e
        return [""]

    def similarity_search(
            self,
            query: str,
            k: int = 4,
            param: Optional[dict] = None,
            expr: Optional[str] = None,
            timeout: Optional[int] = None,
            **kwargs: Any,
    ) -> List[Document]:

        """
                Perform a similarity search on the query string.

                Args:
                    query (str): The text to search for.
                    k (int, optional): The number of results to return. Default is 4.
                    param (dict, optional): Specifies the search parameters for the index. Defaults to None.
                    expr (str, optional): Filtering expression. Defaults to None.
                    timeout (int, optional): Time to wait before a timeout error. Defaults to None.
                    kwargs: Keyword arguments for Collection.search().

                Returns:
                    List[Document]: The document results of the search.
        """

        if self.col is None:
            logger.debug("No existing collection to search.")
            return []
        res = self.similarity_search_with_score(
            query=query, k=k, param=param, expr=expr, timeout=timeout, **kwargs
        )
        return [doc for doc, _ in res]

    def similarity_search_with_score(
            self,
            query: str,
            k: int = 4,
            param: Optional[dict] = None,
            expr: Optional[str] = None,
            timeout: Optional[int] = None,
            **kwargs: Any,
    ) -> List[Tuple[Document, float]]:

        """
                Performs a search on the query string and returns results with scores.

                Args:
                    query (str): The text being searched.
                    k (int, optional): The number of results to return. Default is 4.
                    param (dict): Specifies the search parameters for the index. Default is None.
                    expr (str, optional): Filtering expression. Default is None.
                    timeout (int, optional): The waiting time before a timeout error. Default is None.
                    kwargs: Keyword arguments for Collection.search().

                Returns:
                    List[float], List[Tuple[Document, any, any]]:
        """

        if self.col is None:
            logger.debug("No existing collection to search.")
            return []

        # Embed the query text.
        embedding = self.embedding_func.embed_query(query)

        ret = self.similarity_search_with_score_by_vector(
            embedding=embedding, k=k, param=param, expr=expr, timeout=timeout, **kwargs
        )
        return ret

    def similarity_search_with_score_by_vector(
            self,
            embedding: List[float],
            k: int = 4,
            param: Optional[dict] = None,
            expr: Optional[str] = None,
            timeout: Optional[int] = None,
            **kwargs: Any,
    ) -> List[Tuple[Document, float]]:

        """
                Performs a search on the query string and returns results with scores.

                Args:
                    embedding (List[float]): The embedding vector being searched.
                    k (int, optional): The number of results to return. Default is 4.
                    param (dict): Specifies the search parameters for the index. Default is None.
                    expr (str, optional): Filtering expression. Default is None.
                    timeout (int, optional): The waiting time before a timeout error. Default is None.
                    kwargs: Keyword arguments for Collection.search().

                Returns:
                    List[Tuple[Document, float]]: Resulting documents and scores.
        """
        if self.col is None:
            logger.debug("No existing collection to search.")
            return []

        # if param is None:
        #     param = self.search_params

        # Determine result metadata fields.
        output_fields = self.fields[:]
        output_fields.remove(self._vector_field)

        # Perform the search.
        logger.debug(f"search_field:{self._vector_field}")
        logger.debug(f"vectors:{[embedding]}")
        logger.debug(f"output_fields:{output_fields}")
        logger.debug(f"topk:{k}")
        logger.debug(f"dsl:{expr}")

        res = self.col.query(
            search_field=self._vector_field,
            vectors=[embedding],
            output_fields=output_fields,
            topk=k,
            dsl=expr
        )
        # Organize results.
        logger.debug(f"[similarity_search_with_score_by_vector] res:{res}")
        score_col = self._text_field + "%scores"
        ret = []
        count = 0
        for items in zip(*[res[0][field] for field in output_fields]):
            # 使用字典推导从字段名和对应的值创建元数据字典
            meta = {field: value for field, value in zip(output_fields, items)}
            # 创建 Document 对象，并从元数据字典中移除文本字段
            doc = Document(page_content=meta.pop(self._text_field), metadata=meta)
            # 获取对应的分数
            logger.debug(f"[similarity_search_with_score_by_vector] res[0][score_col]:{res[0][score_col]}")
            score = res[0][score_col][count]
            count += 1
            # 创建元组并添加到结果列表
            ret.append((doc, score))

        return ret

    @classmethod
    def from_texts(
            cls,
            texts: List[str],
            embedding: Embeddings,
            metadatas: Optional[List[dict]] = None,
            table_name: str = "default",
            database_name: str = "default",
            connection_args: Dict[str, Any] = DEFAULT_HIPPO_CONNECTION,
            index_params: dict = None,
            search_params=None,
            drop_old: bool = False,
            **kwargs: Any) -> VectorStore:

        """
                Creates an instance of the VectorStore class from the given texts.

                Args:
                    texts (List[str]): List of texts to be added.
                    embedding (Embeddings): Embedding model for the texts.
                    metadatas (List[dict], optional): List of metadata dictionaries for each text. Defaults to None.
                    table_name (str): Name of the table. Defaults to "default".
                    database_name (str): Name of the database. Defaults to "default".
                    connection_args (dict[str, Any]): Connection parameters. Defaults to DEFAULT_HIPPO_CONNECTION.
                    index_params (dict): Indexing parameters. Defaults to None.
                    search_params (dict): Search parameters. Defaults to an empty dictionary.
                    drop_old (bool): Whether to drop the old collection. Defaults to False.
                    kwargs: Other arguments.

                Returns:
                    VectorStore: An instance of the VectorStore class.
        """

        if search_params is None:
            search_params = {}
        logger.info("00 [from_texts] init the class of Hippo")
        vector_db = cls(
            embedding_function=embedding,
            table_name=table_name,
            database_name=database_name,
            connection_args=connection_args,
            index_params=index_params,
            drop_old=drop_old,
            **kwargs,
        )
        logger.debug(f"[from_texts] texts:{texts}")
        logger.debug(f"[from_texts] metadatas:{metadatas}")
        vector_db.add_texts(texts=texts, metadatas=metadatas)
        return vector_db
