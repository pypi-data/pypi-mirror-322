"""
Type annotations for kafka service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kafka.client import KafkaClient

    session = get_session()
    async with session.create_client("kafka") as client:
        client: KafkaClient
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListClientVpcConnectionsPaginator,
    ListClusterOperationsPaginator,
    ListClusterOperationsV2Paginator,
    ListClustersPaginator,
    ListClustersV2Paginator,
    ListConfigurationRevisionsPaginator,
    ListConfigurationsPaginator,
    ListKafkaVersionsPaginator,
    ListNodesPaginator,
    ListReplicatorsPaginator,
    ListScramSecretsPaginator,
    ListVpcConnectionsPaginator,
)
from .type_defs import (
    BatchAssociateScramSecretRequestRequestTypeDef,
    BatchAssociateScramSecretResponseTypeDef,
    BatchDisassociateScramSecretRequestRequestTypeDef,
    BatchDisassociateScramSecretResponseTypeDef,
    CreateClusterRequestRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateClusterV2RequestRequestTypeDef,
    CreateClusterV2ResponseTypeDef,
    CreateConfigurationRequestRequestTypeDef,
    CreateConfigurationResponseTypeDef,
    CreateReplicatorRequestRequestTypeDef,
    CreateReplicatorResponseTypeDef,
    CreateVpcConnectionRequestRequestTypeDef,
    CreateVpcConnectionResponseTypeDef,
    DeleteClusterPolicyRequestRequestTypeDef,
    DeleteClusterRequestRequestTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteConfigurationRequestRequestTypeDef,
    DeleteConfigurationResponseTypeDef,
    DeleteReplicatorRequestRequestTypeDef,
    DeleteReplicatorResponseTypeDef,
    DeleteVpcConnectionRequestRequestTypeDef,
    DeleteVpcConnectionResponseTypeDef,
    DescribeClusterOperationRequestRequestTypeDef,
    DescribeClusterOperationResponseTypeDef,
    DescribeClusterOperationV2RequestRequestTypeDef,
    DescribeClusterOperationV2ResponseTypeDef,
    DescribeClusterRequestRequestTypeDef,
    DescribeClusterResponseTypeDef,
    DescribeClusterV2RequestRequestTypeDef,
    DescribeClusterV2ResponseTypeDef,
    DescribeConfigurationRequestRequestTypeDef,
    DescribeConfigurationResponseTypeDef,
    DescribeConfigurationRevisionRequestRequestTypeDef,
    DescribeConfigurationRevisionResponseTypeDef,
    DescribeReplicatorRequestRequestTypeDef,
    DescribeReplicatorResponseTypeDef,
    DescribeVpcConnectionRequestRequestTypeDef,
    DescribeVpcConnectionResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetBootstrapBrokersRequestRequestTypeDef,
    GetBootstrapBrokersResponseTypeDef,
    GetClusterPolicyRequestRequestTypeDef,
    GetClusterPolicyResponseTypeDef,
    GetCompatibleKafkaVersionsRequestRequestTypeDef,
    GetCompatibleKafkaVersionsResponseTypeDef,
    ListClientVpcConnectionsRequestRequestTypeDef,
    ListClientVpcConnectionsResponseTypeDef,
    ListClusterOperationsRequestRequestTypeDef,
    ListClusterOperationsResponseTypeDef,
    ListClusterOperationsV2RequestRequestTypeDef,
    ListClusterOperationsV2ResponseTypeDef,
    ListClustersRequestRequestTypeDef,
    ListClustersResponseTypeDef,
    ListClustersV2RequestRequestTypeDef,
    ListClustersV2ResponseTypeDef,
    ListConfigurationRevisionsRequestRequestTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsRequestRequestTypeDef,
    ListConfigurationsResponseTypeDef,
    ListKafkaVersionsRequestRequestTypeDef,
    ListKafkaVersionsResponseTypeDef,
    ListNodesRequestRequestTypeDef,
    ListNodesResponseTypeDef,
    ListReplicatorsRequestRequestTypeDef,
    ListReplicatorsResponseTypeDef,
    ListScramSecretsRequestRequestTypeDef,
    ListScramSecretsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVpcConnectionsRequestRequestTypeDef,
    ListVpcConnectionsResponseTypeDef,
    PutClusterPolicyRequestRequestTypeDef,
    PutClusterPolicyResponseTypeDef,
    RebootBrokerRequestRequestTypeDef,
    RebootBrokerResponseTypeDef,
    RejectClientVpcConnectionRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBrokerCountRequestRequestTypeDef,
    UpdateBrokerCountResponseTypeDef,
    UpdateBrokerStorageRequestRequestTypeDef,
    UpdateBrokerStorageResponseTypeDef,
    UpdateBrokerTypeRequestRequestTypeDef,
    UpdateBrokerTypeResponseTypeDef,
    UpdateClusterConfigurationRequestRequestTypeDef,
    UpdateClusterConfigurationResponseTypeDef,
    UpdateClusterKafkaVersionRequestRequestTypeDef,
    UpdateClusterKafkaVersionResponseTypeDef,
    UpdateConfigurationRequestRequestTypeDef,
    UpdateConfigurationResponseTypeDef,
    UpdateConnectivityRequestRequestTypeDef,
    UpdateConnectivityResponseTypeDef,
    UpdateMonitoringRequestRequestTypeDef,
    UpdateMonitoringResponseTypeDef,
    UpdateReplicationInfoRequestRequestTypeDef,
    UpdateReplicationInfoResponseTypeDef,
    UpdateSecurityRequestRequestTypeDef,
    UpdateSecurityResponseTypeDef,
    UpdateStorageRequestRequestTypeDef,
    UpdateStorageResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("KafkaClient",)

class Exceptions(BaseClientExceptions):
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class KafkaClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KafkaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#generate_presigned_url)
        """

    async def batch_associate_scram_secret(
        self, **kwargs: Unpack[BatchAssociateScramSecretRequestRequestTypeDef]
    ) -> BatchAssociateScramSecretResponseTypeDef:
        """
        Associates one or more Scram Secrets with an Amazon MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/batch_associate_scram_secret.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#batch_associate_scram_secret)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a new MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#create_cluster)
        """

    async def create_cluster_v2(
        self, **kwargs: Unpack[CreateClusterV2RequestRequestTypeDef]
    ) -> CreateClusterV2ResponseTypeDef:
        """
        Creates a new MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_cluster_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#create_cluster_v2)
        """

    async def create_configuration(
        self, **kwargs: Unpack[CreateConfigurationRequestRequestTypeDef]
    ) -> CreateConfigurationResponseTypeDef:
        """
        Creates a new MSK configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#create_configuration)
        """

    async def create_replicator(
        self, **kwargs: Unpack[CreateReplicatorRequestRequestTypeDef]
    ) -> CreateReplicatorResponseTypeDef:
        """
        Creates the replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_replicator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#create_replicator)
        """

    async def create_vpc_connection(
        self, **kwargs: Unpack[CreateVpcConnectionRequestRequestTypeDef]
    ) -> CreateVpcConnectionResponseTypeDef:
        """
        Creates a new MSK VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/create_vpc_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#create_vpc_connection)
        """

    async def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterRequestRequestTypeDef]
    ) -> DeleteClusterResponseTypeDef:
        """
        Deletes the MSK cluster specified by the Amazon Resource Name (ARN) in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#delete_cluster)
        """

    async def delete_cluster_policy(
        self, **kwargs: Unpack[DeleteClusterPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the MSK cluster policy specified by the Amazon Resource Name (ARN) in
        the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_cluster_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#delete_cluster_policy)
        """

    async def delete_configuration(
        self, **kwargs: Unpack[DeleteConfigurationRequestRequestTypeDef]
    ) -> DeleteConfigurationResponseTypeDef:
        """
        Deletes an MSK Configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#delete_configuration)
        """

    async def delete_replicator(
        self, **kwargs: Unpack[DeleteReplicatorRequestRequestTypeDef]
    ) -> DeleteReplicatorResponseTypeDef:
        """
        Deletes a replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_replicator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#delete_replicator)
        """

    async def delete_vpc_connection(
        self, **kwargs: Unpack[DeleteVpcConnectionRequestRequestTypeDef]
    ) -> DeleteVpcConnectionResponseTypeDef:
        """
        Deletes a MSK VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/delete_vpc_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#delete_vpc_connection)
        """

    async def describe_cluster(
        self, **kwargs: Unpack[DescribeClusterRequestRequestTypeDef]
    ) -> DescribeClusterResponseTypeDef:
        """
        Returns a description of the MSK cluster whose Amazon Resource Name (ARN) is
        specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#describe_cluster)
        """

    async def describe_cluster_v2(
        self, **kwargs: Unpack[DescribeClusterV2RequestRequestTypeDef]
    ) -> DescribeClusterV2ResponseTypeDef:
        """
        Returns a description of the MSK cluster whose Amazon Resource Name (ARN) is
        specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_cluster_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#describe_cluster_v2)
        """

    async def describe_cluster_operation(
        self, **kwargs: Unpack[DescribeClusterOperationRequestRequestTypeDef]
    ) -> DescribeClusterOperationResponseTypeDef:
        """
        Returns a description of the cluster operation specified by the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_cluster_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#describe_cluster_operation)
        """

    async def describe_cluster_operation_v2(
        self, **kwargs: Unpack[DescribeClusterOperationV2RequestRequestTypeDef]
    ) -> DescribeClusterOperationV2ResponseTypeDef:
        """
        Returns a description of the cluster operation specified by the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_cluster_operation_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#describe_cluster_operation_v2)
        """

    async def describe_configuration(
        self, **kwargs: Unpack[DescribeConfigurationRequestRequestTypeDef]
    ) -> DescribeConfigurationResponseTypeDef:
        """
        Returns a description of this MSK configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#describe_configuration)
        """

    async def describe_configuration_revision(
        self, **kwargs: Unpack[DescribeConfigurationRevisionRequestRequestTypeDef]
    ) -> DescribeConfigurationRevisionResponseTypeDef:
        """
        Returns a description of this revision of the configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_configuration_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#describe_configuration_revision)
        """

    async def describe_replicator(
        self, **kwargs: Unpack[DescribeReplicatorRequestRequestTypeDef]
    ) -> DescribeReplicatorResponseTypeDef:
        """
        Describes a replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_replicator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#describe_replicator)
        """

    async def describe_vpc_connection(
        self, **kwargs: Unpack[DescribeVpcConnectionRequestRequestTypeDef]
    ) -> DescribeVpcConnectionResponseTypeDef:
        """
        Returns a description of this MSK VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/describe_vpc_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#describe_vpc_connection)
        """

    async def batch_disassociate_scram_secret(
        self, **kwargs: Unpack[BatchDisassociateScramSecretRequestRequestTypeDef]
    ) -> BatchDisassociateScramSecretResponseTypeDef:
        """
        Disassociates one or more Scram Secrets from an Amazon MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/batch_disassociate_scram_secret.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#batch_disassociate_scram_secret)
        """

    async def get_bootstrap_brokers(
        self, **kwargs: Unpack[GetBootstrapBrokersRequestRequestTypeDef]
    ) -> GetBootstrapBrokersResponseTypeDef:
        """
        A list of brokers that a client application can use to bootstrap.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_bootstrap_brokers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_bootstrap_brokers)
        """

    async def get_compatible_kafka_versions(
        self, **kwargs: Unpack[GetCompatibleKafkaVersionsRequestRequestTypeDef]
    ) -> GetCompatibleKafkaVersionsResponseTypeDef:
        """
        Gets the Apache Kafka versions to which you can update the MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_compatible_kafka_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_compatible_kafka_versions)
        """

    async def get_cluster_policy(
        self, **kwargs: Unpack[GetClusterPolicyRequestRequestTypeDef]
    ) -> GetClusterPolicyResponseTypeDef:
        """
        Get the MSK cluster policy specified by the Amazon Resource Name (ARN) in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_cluster_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_cluster_policy)
        """

    async def list_cluster_operations(
        self, **kwargs: Unpack[ListClusterOperationsRequestRequestTypeDef]
    ) -> ListClusterOperationsResponseTypeDef:
        """
        Returns a list of all the operations that have been performed on the specified
        MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_cluster_operations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_cluster_operations)
        """

    async def list_cluster_operations_v2(
        self, **kwargs: Unpack[ListClusterOperationsV2RequestRequestTypeDef]
    ) -> ListClusterOperationsV2ResponseTypeDef:
        """
        Returns a list of all the operations that have been performed on the specified
        MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_cluster_operations_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_cluster_operations_v2)
        """

    async def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestRequestTypeDef]
    ) -> ListClustersResponseTypeDef:
        """
        Returns a list of all the MSK clusters in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_clusters)
        """

    async def list_clusters_v2(
        self, **kwargs: Unpack[ListClustersV2RequestRequestTypeDef]
    ) -> ListClustersV2ResponseTypeDef:
        """
        Returns a list of all the MSK clusters in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_clusters_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_clusters_v2)
        """

    async def list_configuration_revisions(
        self, **kwargs: Unpack[ListConfigurationRevisionsRequestRequestTypeDef]
    ) -> ListConfigurationRevisionsResponseTypeDef:
        """
        Returns a list of all the MSK configurations in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_configuration_revisions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_configuration_revisions)
        """

    async def list_configurations(
        self, **kwargs: Unpack[ListConfigurationsRequestRequestTypeDef]
    ) -> ListConfigurationsResponseTypeDef:
        """
        Returns a list of all the MSK configurations in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_configurations)
        """

    async def list_kafka_versions(
        self, **kwargs: Unpack[ListKafkaVersionsRequestRequestTypeDef]
    ) -> ListKafkaVersionsResponseTypeDef:
        """
        Returns a list of Apache Kafka versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_kafka_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_kafka_versions)
        """

    async def list_nodes(
        self, **kwargs: Unpack[ListNodesRequestRequestTypeDef]
    ) -> ListNodesResponseTypeDef:
        """
        Returns a list of the broker nodes in the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_nodes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_nodes)
        """

    async def list_replicators(
        self, **kwargs: Unpack[ListReplicatorsRequestRequestTypeDef]
    ) -> ListReplicatorsResponseTypeDef:
        """
        Lists the replicators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_replicators.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_replicators)
        """

    async def list_scram_secrets(
        self, **kwargs: Unpack[ListScramSecretsRequestRequestTypeDef]
    ) -> ListScramSecretsResponseTypeDef:
        """
        Returns a list of the Scram Secrets associated with an Amazon MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_scram_secrets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_scram_secrets)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_tags_for_resource)
        """

    async def list_client_vpc_connections(
        self, **kwargs: Unpack[ListClientVpcConnectionsRequestRequestTypeDef]
    ) -> ListClientVpcConnectionsResponseTypeDef:
        """
        Returns a list of all the VPC connections in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_client_vpc_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_client_vpc_connections)
        """

    async def list_vpc_connections(
        self, **kwargs: Unpack[ListVpcConnectionsRequestRequestTypeDef]
    ) -> ListVpcConnectionsResponseTypeDef:
        """
        Returns a list of all the VPC connections in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/list_vpc_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#list_vpc_connections)
        """

    async def reject_client_vpc_connection(
        self, **kwargs: Unpack[RejectClientVpcConnectionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Returns empty response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/reject_client_vpc_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#reject_client_vpc_connection)
        """

    async def put_cluster_policy(
        self, **kwargs: Unpack[PutClusterPolicyRequestRequestTypeDef]
    ) -> PutClusterPolicyResponseTypeDef:
        """
        Creates or updates the MSK cluster policy specified by the cluster Amazon
        Resource Name (ARN) in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/put_cluster_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#put_cluster_policy)
        """

    async def reboot_broker(
        self, **kwargs: Unpack[RebootBrokerRequestRequestTypeDef]
    ) -> RebootBrokerResponseTypeDef:
        """
        Reboots brokers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/reboot_broker.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#reboot_broker)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to the specified MSK resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the tags associated with the keys that are provided in the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#untag_resource)
        """

    async def update_broker_count(
        self, **kwargs: Unpack[UpdateBrokerCountRequestRequestTypeDef]
    ) -> UpdateBrokerCountResponseTypeDef:
        """
        Updates the number of broker nodes in the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_broker_count.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_broker_count)
        """

    async def update_broker_type(
        self, **kwargs: Unpack[UpdateBrokerTypeRequestRequestTypeDef]
    ) -> UpdateBrokerTypeResponseTypeDef:
        """
        Updates EC2 instance type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_broker_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_broker_type)
        """

    async def update_broker_storage(
        self, **kwargs: Unpack[UpdateBrokerStorageRequestRequestTypeDef]
    ) -> UpdateBrokerStorageResponseTypeDef:
        """
        Updates the EBS storage associated with MSK brokers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_broker_storage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_broker_storage)
        """

    async def update_configuration(
        self, **kwargs: Unpack[UpdateConfigurationRequestRequestTypeDef]
    ) -> UpdateConfigurationResponseTypeDef:
        """
        Updates an MSK configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_configuration)
        """

    async def update_connectivity(
        self, **kwargs: Unpack[UpdateConnectivityRequestRequestTypeDef]
    ) -> UpdateConnectivityResponseTypeDef:
        """
        Updates the cluster's connectivity configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_connectivity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_connectivity)
        """

    async def update_cluster_configuration(
        self, **kwargs: Unpack[UpdateClusterConfigurationRequestRequestTypeDef]
    ) -> UpdateClusterConfigurationResponseTypeDef:
        """
        Updates the cluster with the configuration that is specified in the request
        body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_cluster_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_cluster_configuration)
        """

    async def update_cluster_kafka_version(
        self, **kwargs: Unpack[UpdateClusterKafkaVersionRequestRequestTypeDef]
    ) -> UpdateClusterKafkaVersionResponseTypeDef:
        """
        Updates the Apache Kafka version for the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_cluster_kafka_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_cluster_kafka_version)
        """

    async def update_monitoring(
        self, **kwargs: Unpack[UpdateMonitoringRequestRequestTypeDef]
    ) -> UpdateMonitoringResponseTypeDef:
        """
        Updates the monitoring settings for the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_monitoring.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_monitoring)
        """

    async def update_replication_info(
        self, **kwargs: Unpack[UpdateReplicationInfoRequestRequestTypeDef]
    ) -> UpdateReplicationInfoResponseTypeDef:
        """
        Updates replication info of a replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_replication_info.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_replication_info)
        """

    async def update_security(
        self, **kwargs: Unpack[UpdateSecurityRequestRequestTypeDef]
    ) -> UpdateSecurityResponseTypeDef:
        """
        Updates the security settings for the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_security.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_security)
        """

    async def update_storage(
        self, **kwargs: Unpack[UpdateStorageRequestRequestTypeDef]
    ) -> UpdateStorageResponseTypeDef:
        """
        Updates cluster broker volume size (or) sets cluster storage mode to TIERED.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/update_storage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#update_storage)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_client_vpc_connections"]
    ) -> ListClientVpcConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cluster_operations"]
    ) -> ListClusterOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cluster_operations_v2"]
    ) -> ListClusterOperationsV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_clusters"]
    ) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_clusters_v2"]
    ) -> ListClustersV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_configuration_revisions"]
    ) -> ListConfigurationRevisionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_configurations"]
    ) -> ListConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_kafka_versions"]
    ) -> ListKafkaVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_nodes"]
    ) -> ListNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_replicators"]
    ) -> ListReplicatorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_scram_secrets"]
    ) -> ListScramSecretsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_vpc_connections"]
    ) -> ListVpcConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/client/)
        """
