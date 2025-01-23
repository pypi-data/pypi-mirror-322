# Functions that will be used to detect the data types from ontology files

import logging

import pandas as pd
from pandas import DataFrame

from typing import List
from typing import Union
from typing import Optional

from rdflib import Graph

from .ddl import SHACL_ALL_DTYPES_QUERY as dtypes_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def shacl_datatypes_hunter(
    shacl_graph: Graph, shacl_query: Optional[Union[str, List[str]]] = dtypes_query
) -> DataFrame:
    """
    Query all the datatypes from the set of rules provided by the SHACL graph.

    There's two types of data type declarations that will be captured by the default query:
    1. rdf:datatype: default for rdf data
    2. stereotypes: when there's a specification of the types of the data

    On the second case, we want to filter out all the stereotypes that are not of the type Primitive.

    Args:
        shacl_graph (Graph): The shacl graph.
        shacl_query (Optional, Union[str, List[str]]): the SPARQL query or list of queries to be used
        for the validation
        field_id (str): name of attribute that was provided to the field on the query
        dtype_id (str): name of attribute that was provided to the datatype on the query

    Returns:
        DataFrame: A dataframe with the data types.
    """

    queries = [shacl_query] if isinstance(shacl_query, str) else shacl_query

    dfs_lst = [
        DataFrame(
            [
                {
                    "property": str(row.property).split("#")[-1],
                    "datatype": str(row.datatype).split("#")[-1].lower(),
                }
                for row in shacl_graph.query(query)
            ]
        )
        for query in queries
    ]

    df = pd.concat(dfs_lst, axis=0)

    logger.info(f"Found {df.shape[0]} datatypes in the SHACL.")

    return df
