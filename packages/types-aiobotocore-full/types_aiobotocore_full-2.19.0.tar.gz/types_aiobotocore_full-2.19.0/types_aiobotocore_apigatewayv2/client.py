"""
Type annotations for apigatewayv2 service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apigatewayv2.client import ApiGatewayV2Client

    session = get_session()
    async with session.create_client("apigatewayv2") as client:
        client: ApiGatewayV2Client
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
    GetApisPaginator,
    GetAuthorizersPaginator,
    GetDeploymentsPaginator,
    GetDomainNamesPaginator,
    GetIntegrationResponsesPaginator,
    GetIntegrationsPaginator,
    GetModelsPaginator,
    GetRouteResponsesPaginator,
    GetRoutesPaginator,
    GetStagesPaginator,
)
from .type_defs import (
    CreateApiMappingRequestRequestTypeDef,
    CreateApiMappingResponseTypeDef,
    CreateApiRequestRequestTypeDef,
    CreateApiResponseTypeDef,
    CreateAuthorizerRequestRequestTypeDef,
    CreateAuthorizerResponseTypeDef,
    CreateDeploymentRequestRequestTypeDef,
    CreateDeploymentResponseTypeDef,
    CreateDomainNameRequestRequestTypeDef,
    CreateDomainNameResponseTypeDef,
    CreateIntegrationRequestRequestTypeDef,
    CreateIntegrationResponseRequestRequestTypeDef,
    CreateIntegrationResponseResponseTypeDef,
    CreateIntegrationResultTypeDef,
    CreateModelRequestRequestTypeDef,
    CreateModelResponseTypeDef,
    CreateRouteRequestRequestTypeDef,
    CreateRouteResponseRequestRequestTypeDef,
    CreateRouteResponseResponseTypeDef,
    CreateRouteResultTypeDef,
    CreateStageRequestRequestTypeDef,
    CreateStageResponseTypeDef,
    CreateVpcLinkRequestRequestTypeDef,
    CreateVpcLinkResponseTypeDef,
    DeleteAccessLogSettingsRequestRequestTypeDef,
    DeleteApiMappingRequestRequestTypeDef,
    DeleteApiRequestRequestTypeDef,
    DeleteAuthorizerRequestRequestTypeDef,
    DeleteCorsConfigurationRequestRequestTypeDef,
    DeleteDeploymentRequestRequestTypeDef,
    DeleteDomainNameRequestRequestTypeDef,
    DeleteIntegrationRequestRequestTypeDef,
    DeleteIntegrationResponseRequestRequestTypeDef,
    DeleteModelRequestRequestTypeDef,
    DeleteRouteRequestParameterRequestRequestTypeDef,
    DeleteRouteRequestRequestTypeDef,
    DeleteRouteResponseRequestRequestTypeDef,
    DeleteRouteSettingsRequestRequestTypeDef,
    DeleteStageRequestRequestTypeDef,
    DeleteVpcLinkRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportApiRequestRequestTypeDef,
    ExportApiResponseTypeDef,
    GetApiMappingRequestRequestTypeDef,
    GetApiMappingResponseTypeDef,
    GetApiMappingsRequestRequestTypeDef,
    GetApiMappingsResponseTypeDef,
    GetApiRequestRequestTypeDef,
    GetApiResponseTypeDef,
    GetApisRequestRequestTypeDef,
    GetApisResponseTypeDef,
    GetAuthorizerRequestRequestTypeDef,
    GetAuthorizerResponseTypeDef,
    GetAuthorizersRequestRequestTypeDef,
    GetAuthorizersResponseTypeDef,
    GetDeploymentRequestRequestTypeDef,
    GetDeploymentResponseTypeDef,
    GetDeploymentsRequestRequestTypeDef,
    GetDeploymentsResponseTypeDef,
    GetDomainNameRequestRequestTypeDef,
    GetDomainNameResponseTypeDef,
    GetDomainNamesRequestRequestTypeDef,
    GetDomainNamesResponseTypeDef,
    GetIntegrationRequestRequestTypeDef,
    GetIntegrationResponseRequestRequestTypeDef,
    GetIntegrationResponseResponseTypeDef,
    GetIntegrationResponsesRequestRequestTypeDef,
    GetIntegrationResponsesResponseTypeDef,
    GetIntegrationResultTypeDef,
    GetIntegrationsRequestRequestTypeDef,
    GetIntegrationsResponseTypeDef,
    GetModelRequestRequestTypeDef,
    GetModelResponseTypeDef,
    GetModelsRequestRequestTypeDef,
    GetModelsResponseTypeDef,
    GetModelTemplateRequestRequestTypeDef,
    GetModelTemplateResponseTypeDef,
    GetRouteRequestRequestTypeDef,
    GetRouteResponseRequestRequestTypeDef,
    GetRouteResponseResponseTypeDef,
    GetRouteResponsesRequestRequestTypeDef,
    GetRouteResponsesResponseTypeDef,
    GetRouteResultTypeDef,
    GetRoutesRequestRequestTypeDef,
    GetRoutesResponseTypeDef,
    GetStageRequestRequestTypeDef,
    GetStageResponseTypeDef,
    GetStagesRequestRequestTypeDef,
    GetStagesResponseTypeDef,
    GetTagsRequestRequestTypeDef,
    GetTagsResponseTypeDef,
    GetVpcLinkRequestRequestTypeDef,
    GetVpcLinkResponseTypeDef,
    GetVpcLinksRequestRequestTypeDef,
    GetVpcLinksResponseTypeDef,
    ImportApiRequestRequestTypeDef,
    ImportApiResponseTypeDef,
    ReimportApiRequestRequestTypeDef,
    ReimportApiResponseTypeDef,
    ResetAuthorizersCacheRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateApiMappingRequestRequestTypeDef,
    UpdateApiMappingResponseTypeDef,
    UpdateApiRequestRequestTypeDef,
    UpdateApiResponseTypeDef,
    UpdateAuthorizerRequestRequestTypeDef,
    UpdateAuthorizerResponseTypeDef,
    UpdateDeploymentRequestRequestTypeDef,
    UpdateDeploymentResponseTypeDef,
    UpdateDomainNameRequestRequestTypeDef,
    UpdateDomainNameResponseTypeDef,
    UpdateIntegrationRequestRequestTypeDef,
    UpdateIntegrationResponseRequestRequestTypeDef,
    UpdateIntegrationResponseResponseTypeDef,
    UpdateIntegrationResultTypeDef,
    UpdateModelRequestRequestTypeDef,
    UpdateModelResponseTypeDef,
    UpdateRouteRequestRequestTypeDef,
    UpdateRouteResponseRequestRequestTypeDef,
    UpdateRouteResponseResponseTypeDef,
    UpdateRouteResultTypeDef,
    UpdateStageRequestRequestTypeDef,
    UpdateStageResponseTypeDef,
    UpdateVpcLinkRequestRequestTypeDef,
    UpdateVpcLinkResponseTypeDef,
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


__all__ = ("ApiGatewayV2Client",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class ApiGatewayV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ApiGatewayV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#generate_presigned_url)
        """

    async def create_api(
        self, **kwargs: Unpack[CreateApiRequestRequestTypeDef]
    ) -> CreateApiResponseTypeDef:
        """
        Creates an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_api)
        """

    async def create_api_mapping(
        self, **kwargs: Unpack[CreateApiMappingRequestRequestTypeDef]
    ) -> CreateApiMappingResponseTypeDef:
        """
        Creates an API mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_api_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_api_mapping)
        """

    async def create_authorizer(
        self, **kwargs: Unpack[CreateAuthorizerRequestRequestTypeDef]
    ) -> CreateAuthorizerResponseTypeDef:
        """
        Creates an Authorizer for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_authorizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_authorizer)
        """

    async def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentRequestRequestTypeDef]
    ) -> CreateDeploymentResponseTypeDef:
        """
        Creates a Deployment for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_deployment)
        """

    async def create_domain_name(
        self, **kwargs: Unpack[CreateDomainNameRequestRequestTypeDef]
    ) -> CreateDomainNameResponseTypeDef:
        """
        Creates a domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_domain_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_domain_name)
        """

    async def create_integration(
        self, **kwargs: Unpack[CreateIntegrationRequestRequestTypeDef]
    ) -> CreateIntegrationResultTypeDef:
        """
        Creates an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_integration)
        """

    async def create_integration_response(
        self, **kwargs: Unpack[CreateIntegrationResponseRequestRequestTypeDef]
    ) -> CreateIntegrationResponseResponseTypeDef:
        """
        Creates an IntegrationResponses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_integration_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_integration_response)
        """

    async def create_model(
        self, **kwargs: Unpack[CreateModelRequestRequestTypeDef]
    ) -> CreateModelResponseTypeDef:
        """
        Creates a Model for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_model)
        """

    async def create_route(
        self, **kwargs: Unpack[CreateRouteRequestRequestTypeDef]
    ) -> CreateRouteResultTypeDef:
        """
        Creates a Route for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_route)
        """

    async def create_route_response(
        self, **kwargs: Unpack[CreateRouteResponseRequestRequestTypeDef]
    ) -> CreateRouteResponseResponseTypeDef:
        """
        Creates a RouteResponse for a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_route_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_route_response)
        """

    async def create_stage(
        self, **kwargs: Unpack[CreateStageRequestRequestTypeDef]
    ) -> CreateStageResponseTypeDef:
        """
        Creates a Stage for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_stage)
        """

    async def create_vpc_link(
        self, **kwargs: Unpack[CreateVpcLinkRequestRequestTypeDef]
    ) -> CreateVpcLinkResponseTypeDef:
        """
        Creates a VPC link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/create_vpc_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#create_vpc_link)
        """

    async def delete_access_log_settings(
        self, **kwargs: Unpack[DeleteAccessLogSettingsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the AccessLogSettings for a Stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_access_log_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_access_log_settings)
        """

    async def delete_api(
        self, **kwargs: Unpack[DeleteApiRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_api)
        """

    async def delete_api_mapping(
        self, **kwargs: Unpack[DeleteApiMappingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an API mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_api_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_api_mapping)
        """

    async def delete_authorizer(
        self, **kwargs: Unpack[DeleteAuthorizerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_authorizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_authorizer)
        """

    async def delete_cors_configuration(
        self, **kwargs: Unpack[DeleteCorsConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a CORS configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_cors_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_cors_configuration)
        """

    async def delete_deployment(
        self, **kwargs: Unpack[DeleteDeploymentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_deployment)
        """

    async def delete_domain_name(
        self, **kwargs: Unpack[DeleteDomainNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_domain_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_domain_name)
        """

    async def delete_integration(
        self, **kwargs: Unpack[DeleteIntegrationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_integration)
        """

    async def delete_integration_response(
        self, **kwargs: Unpack[DeleteIntegrationResponseRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an IntegrationResponses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_integration_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_integration_response)
        """

    async def delete_model(
        self, **kwargs: Unpack[DeleteModelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_model)
        """

    async def delete_route(
        self, **kwargs: Unpack[DeleteRouteRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_route)
        """

    async def delete_route_request_parameter(
        self, **kwargs: Unpack[DeleteRouteRequestParameterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a route request parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_route_request_parameter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_route_request_parameter)
        """

    async def delete_route_response(
        self, **kwargs: Unpack[DeleteRouteResponseRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a RouteResponse.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_route_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_route_response)
        """

    async def delete_route_settings(
        self, **kwargs: Unpack[DeleteRouteSettingsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the RouteSettings for a stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_route_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_route_settings)
        """

    async def delete_stage(
        self, **kwargs: Unpack[DeleteStageRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_stage)
        """

    async def delete_vpc_link(
        self, **kwargs: Unpack[DeleteVpcLinkRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a VPC link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/delete_vpc_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#delete_vpc_link)
        """

    async def export_api(
        self, **kwargs: Unpack[ExportApiRequestRequestTypeDef]
    ) -> ExportApiResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/export_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#export_api)
        """

    async def reset_authorizers_cache(
        self, **kwargs: Unpack[ResetAuthorizersCacheRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resets all authorizer cache entries on a stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/reset_authorizers_cache.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#reset_authorizers_cache)
        """

    async def get_api(self, **kwargs: Unpack[GetApiRequestRequestTypeDef]) -> GetApiResponseTypeDef:
        """
        Gets an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_api)
        """

    async def get_api_mapping(
        self, **kwargs: Unpack[GetApiMappingRequestRequestTypeDef]
    ) -> GetApiMappingResponseTypeDef:
        """
        Gets an API mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_api_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_api_mapping)
        """

    async def get_api_mappings(
        self, **kwargs: Unpack[GetApiMappingsRequestRequestTypeDef]
    ) -> GetApiMappingsResponseTypeDef:
        """
        Gets API mappings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_api_mappings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_api_mappings)
        """

    async def get_apis(
        self, **kwargs: Unpack[GetApisRequestRequestTypeDef]
    ) -> GetApisResponseTypeDef:
        """
        Gets a collection of Api resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_apis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_apis)
        """

    async def get_authorizer(
        self, **kwargs: Unpack[GetAuthorizerRequestRequestTypeDef]
    ) -> GetAuthorizerResponseTypeDef:
        """
        Gets an Authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_authorizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_authorizer)
        """

    async def get_authorizers(
        self, **kwargs: Unpack[GetAuthorizersRequestRequestTypeDef]
    ) -> GetAuthorizersResponseTypeDef:
        """
        Gets the Authorizers for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_authorizers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_authorizers)
        """

    async def get_deployment(
        self, **kwargs: Unpack[GetDeploymentRequestRequestTypeDef]
    ) -> GetDeploymentResponseTypeDef:
        """
        Gets a Deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_deployment)
        """

    async def get_deployments(
        self, **kwargs: Unpack[GetDeploymentsRequestRequestTypeDef]
    ) -> GetDeploymentsResponseTypeDef:
        """
        Gets the Deployments for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_deployments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_deployments)
        """

    async def get_domain_name(
        self, **kwargs: Unpack[GetDomainNameRequestRequestTypeDef]
    ) -> GetDomainNameResponseTypeDef:
        """
        Gets a domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_domain_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_domain_name)
        """

    async def get_domain_names(
        self, **kwargs: Unpack[GetDomainNamesRequestRequestTypeDef]
    ) -> GetDomainNamesResponseTypeDef:
        """
        Gets the domain names for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_domain_names.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_domain_names)
        """

    async def get_integration(
        self, **kwargs: Unpack[GetIntegrationRequestRequestTypeDef]
    ) -> GetIntegrationResultTypeDef:
        """
        Gets an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_integration)
        """

    async def get_integration_response(
        self, **kwargs: Unpack[GetIntegrationResponseRequestRequestTypeDef]
    ) -> GetIntegrationResponseResponseTypeDef:
        """
        Gets an IntegrationResponses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_integration_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_integration_response)
        """

    async def get_integration_responses(
        self, **kwargs: Unpack[GetIntegrationResponsesRequestRequestTypeDef]
    ) -> GetIntegrationResponsesResponseTypeDef:
        """
        Gets the IntegrationResponses for an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_integration_responses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_integration_responses)
        """

    async def get_integrations(
        self, **kwargs: Unpack[GetIntegrationsRequestRequestTypeDef]
    ) -> GetIntegrationsResponseTypeDef:
        """
        Gets the Integrations for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_integrations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_integrations)
        """

    async def get_model(
        self, **kwargs: Unpack[GetModelRequestRequestTypeDef]
    ) -> GetModelResponseTypeDef:
        """
        Gets a Model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_model)
        """

    async def get_model_template(
        self, **kwargs: Unpack[GetModelTemplateRequestRequestTypeDef]
    ) -> GetModelTemplateResponseTypeDef:
        """
        Gets a model template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_model_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_model_template)
        """

    async def get_models(
        self, **kwargs: Unpack[GetModelsRequestRequestTypeDef]
    ) -> GetModelsResponseTypeDef:
        """
        Gets the Models for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_models.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_models)
        """

    async def get_route(
        self, **kwargs: Unpack[GetRouteRequestRequestTypeDef]
    ) -> GetRouteResultTypeDef:
        """
        Gets a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_route)
        """

    async def get_route_response(
        self, **kwargs: Unpack[GetRouteResponseRequestRequestTypeDef]
    ) -> GetRouteResponseResponseTypeDef:
        """
        Gets a RouteResponse.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_route_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_route_response)
        """

    async def get_route_responses(
        self, **kwargs: Unpack[GetRouteResponsesRequestRequestTypeDef]
    ) -> GetRouteResponsesResponseTypeDef:
        """
        Gets the RouteResponses for a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_route_responses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_route_responses)
        """

    async def get_routes(
        self, **kwargs: Unpack[GetRoutesRequestRequestTypeDef]
    ) -> GetRoutesResponseTypeDef:
        """
        Gets the Routes for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_routes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_routes)
        """

    async def get_stage(
        self, **kwargs: Unpack[GetStageRequestRequestTypeDef]
    ) -> GetStageResponseTypeDef:
        """
        Gets a Stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_stage)
        """

    async def get_stages(
        self, **kwargs: Unpack[GetStagesRequestRequestTypeDef]
    ) -> GetStagesResponseTypeDef:
        """
        Gets the Stages for an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_stages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_stages)
        """

    async def get_tags(
        self, **kwargs: Unpack[GetTagsRequestRequestTypeDef]
    ) -> GetTagsResponseTypeDef:
        """
        Gets a collection of Tag resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_tags)
        """

    async def get_vpc_link(
        self, **kwargs: Unpack[GetVpcLinkRequestRequestTypeDef]
    ) -> GetVpcLinkResponseTypeDef:
        """
        Gets a VPC link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_vpc_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_vpc_link)
        """

    async def get_vpc_links(
        self, **kwargs: Unpack[GetVpcLinksRequestRequestTypeDef]
    ) -> GetVpcLinksResponseTypeDef:
        """
        Gets a collection of VPC links.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_vpc_links.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_vpc_links)
        """

    async def import_api(
        self, **kwargs: Unpack[ImportApiRequestRequestTypeDef]
    ) -> ImportApiResponseTypeDef:
        """
        Imports an API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/import_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#import_api)
        """

    async def reimport_api(
        self, **kwargs: Unpack[ReimportApiRequestRequestTypeDef]
    ) -> ReimportApiResponseTypeDef:
        """
        Puts an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/reimport_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#reimport_api)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new Tag resource to represent a tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#untag_resource)
        """

    async def update_api(
        self, **kwargs: Unpack[UpdateApiRequestRequestTypeDef]
    ) -> UpdateApiResponseTypeDef:
        """
        Updates an Api resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_api)
        """

    async def update_api_mapping(
        self, **kwargs: Unpack[UpdateApiMappingRequestRequestTypeDef]
    ) -> UpdateApiMappingResponseTypeDef:
        """
        The API mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_api_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_api_mapping)
        """

    async def update_authorizer(
        self, **kwargs: Unpack[UpdateAuthorizerRequestRequestTypeDef]
    ) -> UpdateAuthorizerResponseTypeDef:
        """
        Updates an Authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_authorizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_authorizer)
        """

    async def update_deployment(
        self, **kwargs: Unpack[UpdateDeploymentRequestRequestTypeDef]
    ) -> UpdateDeploymentResponseTypeDef:
        """
        Updates a Deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_deployment)
        """

    async def update_domain_name(
        self, **kwargs: Unpack[UpdateDomainNameRequestRequestTypeDef]
    ) -> UpdateDomainNameResponseTypeDef:
        """
        Updates a domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_domain_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_domain_name)
        """

    async def update_integration(
        self, **kwargs: Unpack[UpdateIntegrationRequestRequestTypeDef]
    ) -> UpdateIntegrationResultTypeDef:
        """
        Updates an Integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_integration)
        """

    async def update_integration_response(
        self, **kwargs: Unpack[UpdateIntegrationResponseRequestRequestTypeDef]
    ) -> UpdateIntegrationResponseResponseTypeDef:
        """
        Updates an IntegrationResponses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_integration_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_integration_response)
        """

    async def update_model(
        self, **kwargs: Unpack[UpdateModelRequestRequestTypeDef]
    ) -> UpdateModelResponseTypeDef:
        """
        Updates a Model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_model)
        """

    async def update_route(
        self, **kwargs: Unpack[UpdateRouteRequestRequestTypeDef]
    ) -> UpdateRouteResultTypeDef:
        """
        Updates a Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_route)
        """

    async def update_route_response(
        self, **kwargs: Unpack[UpdateRouteResponseRequestRequestTypeDef]
    ) -> UpdateRouteResponseResponseTypeDef:
        """
        Updates a RouteResponse.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_route_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_route_response)
        """

    async def update_stage(
        self, **kwargs: Unpack[UpdateStageRequestRequestTypeDef]
    ) -> UpdateStageResponseTypeDef:
        """
        Updates a Stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_stage)
        """

    async def update_vpc_link(
        self, **kwargs: Unpack[UpdateVpcLinkRequestRequestTypeDef]
    ) -> UpdateVpcLinkResponseTypeDef:
        """
        Updates a VPC link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/update_vpc_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#update_vpc_link)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_apis"]
    ) -> GetApisPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_authorizers"]
    ) -> GetAuthorizersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_deployments"]
    ) -> GetDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_domain_names"]
    ) -> GetDomainNamesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_integration_responses"]
    ) -> GetIntegrationResponsesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_integrations"]
    ) -> GetIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_models"]
    ) -> GetModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_route_responses"]
    ) -> GetRouteResponsesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_routes"]
    ) -> GetRoutesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_stages"]
    ) -> GetStagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/client/)
        """
