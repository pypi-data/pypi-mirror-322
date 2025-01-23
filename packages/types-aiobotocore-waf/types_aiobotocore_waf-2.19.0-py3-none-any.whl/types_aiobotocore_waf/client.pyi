"""
Type annotations for waf service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_waf.client import WAFClient

    session = get_session()
    async with session.create_client("waf") as client:
        client: WAFClient
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
    GetRateBasedRuleManagedKeysPaginator,
    ListActivatedRulesInRuleGroupPaginator,
    ListByteMatchSetsPaginator,
    ListGeoMatchSetsPaginator,
    ListIPSetsPaginator,
    ListLoggingConfigurationsPaginator,
    ListRateBasedRulesPaginator,
    ListRegexMatchSetsPaginator,
    ListRegexPatternSetsPaginator,
    ListRuleGroupsPaginator,
    ListRulesPaginator,
    ListSizeConstraintSetsPaginator,
    ListSqlInjectionMatchSetsPaginator,
    ListSubscribedRuleGroupsPaginator,
    ListWebACLsPaginator,
    ListXssMatchSetsPaginator,
)
from .type_defs import (
    CreateByteMatchSetRequestRequestTypeDef,
    CreateByteMatchSetResponseTypeDef,
    CreateGeoMatchSetRequestRequestTypeDef,
    CreateGeoMatchSetResponseTypeDef,
    CreateIPSetRequestRequestTypeDef,
    CreateIPSetResponseTypeDef,
    CreateRateBasedRuleRequestRequestTypeDef,
    CreateRateBasedRuleResponseTypeDef,
    CreateRegexMatchSetRequestRequestTypeDef,
    CreateRegexMatchSetResponseTypeDef,
    CreateRegexPatternSetRequestRequestTypeDef,
    CreateRegexPatternSetResponseTypeDef,
    CreateRuleGroupRequestRequestTypeDef,
    CreateRuleGroupResponseTypeDef,
    CreateRuleRequestRequestTypeDef,
    CreateRuleResponseTypeDef,
    CreateSizeConstraintSetRequestRequestTypeDef,
    CreateSizeConstraintSetResponseTypeDef,
    CreateSqlInjectionMatchSetRequestRequestTypeDef,
    CreateSqlInjectionMatchSetResponseTypeDef,
    CreateWebACLMigrationStackRequestRequestTypeDef,
    CreateWebACLMigrationStackResponseTypeDef,
    CreateWebACLRequestRequestTypeDef,
    CreateWebACLResponseTypeDef,
    CreateXssMatchSetRequestRequestTypeDef,
    CreateXssMatchSetResponseTypeDef,
    DeleteByteMatchSetRequestRequestTypeDef,
    DeleteByteMatchSetResponseTypeDef,
    DeleteGeoMatchSetRequestRequestTypeDef,
    DeleteGeoMatchSetResponseTypeDef,
    DeleteIPSetRequestRequestTypeDef,
    DeleteIPSetResponseTypeDef,
    DeleteLoggingConfigurationRequestRequestTypeDef,
    DeletePermissionPolicyRequestRequestTypeDef,
    DeleteRateBasedRuleRequestRequestTypeDef,
    DeleteRateBasedRuleResponseTypeDef,
    DeleteRegexMatchSetRequestRequestTypeDef,
    DeleteRegexMatchSetResponseTypeDef,
    DeleteRegexPatternSetRequestRequestTypeDef,
    DeleteRegexPatternSetResponseTypeDef,
    DeleteRuleGroupRequestRequestTypeDef,
    DeleteRuleGroupResponseTypeDef,
    DeleteRuleRequestRequestTypeDef,
    DeleteRuleResponseTypeDef,
    DeleteSizeConstraintSetRequestRequestTypeDef,
    DeleteSizeConstraintSetResponseTypeDef,
    DeleteSqlInjectionMatchSetRequestRequestTypeDef,
    DeleteSqlInjectionMatchSetResponseTypeDef,
    DeleteWebACLRequestRequestTypeDef,
    DeleteWebACLResponseTypeDef,
    DeleteXssMatchSetRequestRequestTypeDef,
    DeleteXssMatchSetResponseTypeDef,
    GetByteMatchSetRequestRequestTypeDef,
    GetByteMatchSetResponseTypeDef,
    GetChangeTokenResponseTypeDef,
    GetChangeTokenStatusRequestRequestTypeDef,
    GetChangeTokenStatusResponseTypeDef,
    GetGeoMatchSetRequestRequestTypeDef,
    GetGeoMatchSetResponseTypeDef,
    GetIPSetRequestRequestTypeDef,
    GetIPSetResponseTypeDef,
    GetLoggingConfigurationRequestRequestTypeDef,
    GetLoggingConfigurationResponseTypeDef,
    GetPermissionPolicyRequestRequestTypeDef,
    GetPermissionPolicyResponseTypeDef,
    GetRateBasedRuleManagedKeysRequestRequestTypeDef,
    GetRateBasedRuleManagedKeysResponseTypeDef,
    GetRateBasedRuleRequestRequestTypeDef,
    GetRateBasedRuleResponseTypeDef,
    GetRegexMatchSetRequestRequestTypeDef,
    GetRegexMatchSetResponseTypeDef,
    GetRegexPatternSetRequestRequestTypeDef,
    GetRegexPatternSetResponseTypeDef,
    GetRuleGroupRequestRequestTypeDef,
    GetRuleGroupResponseTypeDef,
    GetRuleRequestRequestTypeDef,
    GetRuleResponseTypeDef,
    GetSampledRequestsRequestRequestTypeDef,
    GetSampledRequestsResponseTypeDef,
    GetSizeConstraintSetRequestRequestTypeDef,
    GetSizeConstraintSetResponseTypeDef,
    GetSqlInjectionMatchSetRequestRequestTypeDef,
    GetSqlInjectionMatchSetResponseTypeDef,
    GetWebACLRequestRequestTypeDef,
    GetWebACLResponseTypeDef,
    GetXssMatchSetRequestRequestTypeDef,
    GetXssMatchSetResponseTypeDef,
    ListActivatedRulesInRuleGroupRequestRequestTypeDef,
    ListActivatedRulesInRuleGroupResponseTypeDef,
    ListByteMatchSetsRequestRequestTypeDef,
    ListByteMatchSetsResponseTypeDef,
    ListGeoMatchSetsRequestRequestTypeDef,
    ListGeoMatchSetsResponseTypeDef,
    ListIPSetsRequestRequestTypeDef,
    ListIPSetsResponseTypeDef,
    ListLoggingConfigurationsRequestRequestTypeDef,
    ListLoggingConfigurationsResponseTypeDef,
    ListRateBasedRulesRequestRequestTypeDef,
    ListRateBasedRulesResponseTypeDef,
    ListRegexMatchSetsRequestRequestTypeDef,
    ListRegexMatchSetsResponseTypeDef,
    ListRegexPatternSetsRequestRequestTypeDef,
    ListRegexPatternSetsResponseTypeDef,
    ListRuleGroupsRequestRequestTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListRulesRequestRequestTypeDef,
    ListRulesResponseTypeDef,
    ListSizeConstraintSetsRequestRequestTypeDef,
    ListSizeConstraintSetsResponseTypeDef,
    ListSqlInjectionMatchSetsRequestRequestTypeDef,
    ListSqlInjectionMatchSetsResponseTypeDef,
    ListSubscribedRuleGroupsRequestRequestTypeDef,
    ListSubscribedRuleGroupsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebACLsRequestRequestTypeDef,
    ListWebACLsResponseTypeDef,
    ListXssMatchSetsRequestRequestTypeDef,
    ListXssMatchSetsResponseTypeDef,
    PutLoggingConfigurationRequestRequestTypeDef,
    PutLoggingConfigurationResponseTypeDef,
    PutPermissionPolicyRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateByteMatchSetRequestRequestTypeDef,
    UpdateByteMatchSetResponseTypeDef,
    UpdateGeoMatchSetRequestRequestTypeDef,
    UpdateGeoMatchSetResponseTypeDef,
    UpdateIPSetRequestRequestTypeDef,
    UpdateIPSetResponseTypeDef,
    UpdateRateBasedRuleRequestRequestTypeDef,
    UpdateRateBasedRuleResponseTypeDef,
    UpdateRegexMatchSetRequestRequestTypeDef,
    UpdateRegexMatchSetResponseTypeDef,
    UpdateRegexPatternSetRequestRequestTypeDef,
    UpdateRegexPatternSetResponseTypeDef,
    UpdateRuleGroupRequestRequestTypeDef,
    UpdateRuleGroupResponseTypeDef,
    UpdateRuleRequestRequestTypeDef,
    UpdateRuleResponseTypeDef,
    UpdateSizeConstraintSetRequestRequestTypeDef,
    UpdateSizeConstraintSetResponseTypeDef,
    UpdateSqlInjectionMatchSetRequestRequestTypeDef,
    UpdateSqlInjectionMatchSetResponseTypeDef,
    UpdateWebACLRequestRequestTypeDef,
    UpdateWebACLResponseTypeDef,
    UpdateXssMatchSetRequestRequestTypeDef,
    UpdateXssMatchSetResponseTypeDef,
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

__all__ = ("WAFClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    WAFBadRequestException: Type[BotocoreClientError]
    WAFDisallowedNameException: Type[BotocoreClientError]
    WAFEntityMigrationException: Type[BotocoreClientError]
    WAFInternalErrorException: Type[BotocoreClientError]
    WAFInvalidAccountException: Type[BotocoreClientError]
    WAFInvalidOperationException: Type[BotocoreClientError]
    WAFInvalidParameterException: Type[BotocoreClientError]
    WAFInvalidPermissionPolicyException: Type[BotocoreClientError]
    WAFInvalidRegexPatternException: Type[BotocoreClientError]
    WAFLimitsExceededException: Type[BotocoreClientError]
    WAFNonEmptyEntityException: Type[BotocoreClientError]
    WAFNonexistentContainerException: Type[BotocoreClientError]
    WAFNonexistentItemException: Type[BotocoreClientError]
    WAFReferencedItemException: Type[BotocoreClientError]
    WAFServiceLinkedRoleErrorException: Type[BotocoreClientError]
    WAFStaleDataException: Type[BotocoreClientError]
    WAFSubscriptionNotFoundException: Type[BotocoreClientError]
    WAFTagOperationException: Type[BotocoreClientError]
    WAFTagOperationInternalErrorException: Type[BotocoreClientError]

class WAFClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WAFClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#generate_presigned_url)
        """

    async def create_byte_match_set(
        self, **kwargs: Unpack[CreateByteMatchSetRequestRequestTypeDef]
    ) -> CreateByteMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_byte_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_byte_match_set)
        """

    async def create_geo_match_set(
        self, **kwargs: Unpack[CreateGeoMatchSetRequestRequestTypeDef]
    ) -> CreateGeoMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_geo_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_geo_match_set)
        """

    async def create_ip_set(
        self, **kwargs: Unpack[CreateIPSetRequestRequestTypeDef]
    ) -> CreateIPSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_ip_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_ip_set)
        """

    async def create_rate_based_rule(
        self, **kwargs: Unpack[CreateRateBasedRuleRequestRequestTypeDef]
    ) -> CreateRateBasedRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_rate_based_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_rate_based_rule)
        """

    async def create_regex_match_set(
        self, **kwargs: Unpack[CreateRegexMatchSetRequestRequestTypeDef]
    ) -> CreateRegexMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_regex_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_regex_match_set)
        """

    async def create_regex_pattern_set(
        self, **kwargs: Unpack[CreateRegexPatternSetRequestRequestTypeDef]
    ) -> CreateRegexPatternSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_regex_pattern_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_regex_pattern_set)
        """

    async def create_rule(
        self, **kwargs: Unpack[CreateRuleRequestRequestTypeDef]
    ) -> CreateRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_rule)
        """

    async def create_rule_group(
        self, **kwargs: Unpack[CreateRuleGroupRequestRequestTypeDef]
    ) -> CreateRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_rule_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_rule_group)
        """

    async def create_size_constraint_set(
        self, **kwargs: Unpack[CreateSizeConstraintSetRequestRequestTypeDef]
    ) -> CreateSizeConstraintSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_size_constraint_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_size_constraint_set)
        """

    async def create_sql_injection_match_set(
        self, **kwargs: Unpack[CreateSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> CreateSqlInjectionMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_sql_injection_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_sql_injection_match_set)
        """

    async def create_web_acl(
        self, **kwargs: Unpack[CreateWebACLRequestRequestTypeDef]
    ) -> CreateWebACLResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_web_acl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_web_acl)
        """

    async def create_web_acl_migration_stack(
        self, **kwargs: Unpack[CreateWebACLMigrationStackRequestRequestTypeDef]
    ) -> CreateWebACLMigrationStackResponseTypeDef:
        """
        Creates an AWS CloudFormation WAFV2 template for the specified web ACL in the
        specified Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_web_acl_migration_stack.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_web_acl_migration_stack)
        """

    async def create_xss_match_set(
        self, **kwargs: Unpack[CreateXssMatchSetRequestRequestTypeDef]
    ) -> CreateXssMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/create_xss_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#create_xss_match_set)
        """

    async def delete_byte_match_set(
        self, **kwargs: Unpack[DeleteByteMatchSetRequestRequestTypeDef]
    ) -> DeleteByteMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_byte_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_byte_match_set)
        """

    async def delete_geo_match_set(
        self, **kwargs: Unpack[DeleteGeoMatchSetRequestRequestTypeDef]
    ) -> DeleteGeoMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_geo_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_geo_match_set)
        """

    async def delete_ip_set(
        self, **kwargs: Unpack[DeleteIPSetRequestRequestTypeDef]
    ) -> DeleteIPSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_ip_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_ip_set)
        """

    async def delete_logging_configuration(
        self, **kwargs: Unpack[DeleteLoggingConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_logging_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_logging_configuration)
        """

    async def delete_permission_policy(
        self, **kwargs: Unpack[DeletePermissionPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_permission_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_permission_policy)
        """

    async def delete_rate_based_rule(
        self, **kwargs: Unpack[DeleteRateBasedRuleRequestRequestTypeDef]
    ) -> DeleteRateBasedRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_rate_based_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_rate_based_rule)
        """

    async def delete_regex_match_set(
        self, **kwargs: Unpack[DeleteRegexMatchSetRequestRequestTypeDef]
    ) -> DeleteRegexMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_regex_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_regex_match_set)
        """

    async def delete_regex_pattern_set(
        self, **kwargs: Unpack[DeleteRegexPatternSetRequestRequestTypeDef]
    ) -> DeleteRegexPatternSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_regex_pattern_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_regex_pattern_set)
        """

    async def delete_rule(
        self, **kwargs: Unpack[DeleteRuleRequestRequestTypeDef]
    ) -> DeleteRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_rule)
        """

    async def delete_rule_group(
        self, **kwargs: Unpack[DeleteRuleGroupRequestRequestTypeDef]
    ) -> DeleteRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_rule_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_rule_group)
        """

    async def delete_size_constraint_set(
        self, **kwargs: Unpack[DeleteSizeConstraintSetRequestRequestTypeDef]
    ) -> DeleteSizeConstraintSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_size_constraint_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_size_constraint_set)
        """

    async def delete_sql_injection_match_set(
        self, **kwargs: Unpack[DeleteSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> DeleteSqlInjectionMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_sql_injection_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_sql_injection_match_set)
        """

    async def delete_web_acl(
        self, **kwargs: Unpack[DeleteWebACLRequestRequestTypeDef]
    ) -> DeleteWebACLResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_web_acl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_web_acl)
        """

    async def delete_xss_match_set(
        self, **kwargs: Unpack[DeleteXssMatchSetRequestRequestTypeDef]
    ) -> DeleteXssMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/delete_xss_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#delete_xss_match_set)
        """

    async def get_byte_match_set(
        self, **kwargs: Unpack[GetByteMatchSetRequestRequestTypeDef]
    ) -> GetByteMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_byte_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_byte_match_set)
        """

    async def get_change_token(self) -> GetChangeTokenResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_change_token.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_change_token)
        """

    async def get_change_token_status(
        self, **kwargs: Unpack[GetChangeTokenStatusRequestRequestTypeDef]
    ) -> GetChangeTokenStatusResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_change_token_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_change_token_status)
        """

    async def get_geo_match_set(
        self, **kwargs: Unpack[GetGeoMatchSetRequestRequestTypeDef]
    ) -> GetGeoMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_geo_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_geo_match_set)
        """

    async def get_ip_set(
        self, **kwargs: Unpack[GetIPSetRequestRequestTypeDef]
    ) -> GetIPSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_ip_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_ip_set)
        """

    async def get_logging_configuration(
        self, **kwargs: Unpack[GetLoggingConfigurationRequestRequestTypeDef]
    ) -> GetLoggingConfigurationResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_logging_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_logging_configuration)
        """

    async def get_permission_policy(
        self, **kwargs: Unpack[GetPermissionPolicyRequestRequestTypeDef]
    ) -> GetPermissionPolicyResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_permission_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_permission_policy)
        """

    async def get_rate_based_rule(
        self, **kwargs: Unpack[GetRateBasedRuleRequestRequestTypeDef]
    ) -> GetRateBasedRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_rate_based_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_rate_based_rule)
        """

    async def get_rate_based_rule_managed_keys(
        self, **kwargs: Unpack[GetRateBasedRuleManagedKeysRequestRequestTypeDef]
    ) -> GetRateBasedRuleManagedKeysResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_rate_based_rule_managed_keys.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_rate_based_rule_managed_keys)
        """

    async def get_regex_match_set(
        self, **kwargs: Unpack[GetRegexMatchSetRequestRequestTypeDef]
    ) -> GetRegexMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_regex_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_regex_match_set)
        """

    async def get_regex_pattern_set(
        self, **kwargs: Unpack[GetRegexPatternSetRequestRequestTypeDef]
    ) -> GetRegexPatternSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_regex_pattern_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_regex_pattern_set)
        """

    async def get_rule(
        self, **kwargs: Unpack[GetRuleRequestRequestTypeDef]
    ) -> GetRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_rule)
        """

    async def get_rule_group(
        self, **kwargs: Unpack[GetRuleGroupRequestRequestTypeDef]
    ) -> GetRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_rule_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_rule_group)
        """

    async def get_sampled_requests(
        self, **kwargs: Unpack[GetSampledRequestsRequestRequestTypeDef]
    ) -> GetSampledRequestsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_sampled_requests.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_sampled_requests)
        """

    async def get_size_constraint_set(
        self, **kwargs: Unpack[GetSizeConstraintSetRequestRequestTypeDef]
    ) -> GetSizeConstraintSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_size_constraint_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_size_constraint_set)
        """

    async def get_sql_injection_match_set(
        self, **kwargs: Unpack[GetSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> GetSqlInjectionMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_sql_injection_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_sql_injection_match_set)
        """

    async def get_web_acl(
        self, **kwargs: Unpack[GetWebACLRequestRequestTypeDef]
    ) -> GetWebACLResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_web_acl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_web_acl)
        """

    async def get_xss_match_set(
        self, **kwargs: Unpack[GetXssMatchSetRequestRequestTypeDef]
    ) -> GetXssMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_xss_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_xss_match_set)
        """

    async def list_activated_rules_in_rule_group(
        self, **kwargs: Unpack[ListActivatedRulesInRuleGroupRequestRequestTypeDef]
    ) -> ListActivatedRulesInRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_activated_rules_in_rule_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_activated_rules_in_rule_group)
        """

    async def list_byte_match_sets(
        self, **kwargs: Unpack[ListByteMatchSetsRequestRequestTypeDef]
    ) -> ListByteMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_byte_match_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_byte_match_sets)
        """

    async def list_geo_match_sets(
        self, **kwargs: Unpack[ListGeoMatchSetsRequestRequestTypeDef]
    ) -> ListGeoMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_geo_match_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_geo_match_sets)
        """

    async def list_ip_sets(
        self, **kwargs: Unpack[ListIPSetsRequestRequestTypeDef]
    ) -> ListIPSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_ip_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_ip_sets)
        """

    async def list_logging_configurations(
        self, **kwargs: Unpack[ListLoggingConfigurationsRequestRequestTypeDef]
    ) -> ListLoggingConfigurationsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_logging_configurations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_logging_configurations)
        """

    async def list_rate_based_rules(
        self, **kwargs: Unpack[ListRateBasedRulesRequestRequestTypeDef]
    ) -> ListRateBasedRulesResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_rate_based_rules.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_rate_based_rules)
        """

    async def list_regex_match_sets(
        self, **kwargs: Unpack[ListRegexMatchSetsRequestRequestTypeDef]
    ) -> ListRegexMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_regex_match_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_regex_match_sets)
        """

    async def list_regex_pattern_sets(
        self, **kwargs: Unpack[ListRegexPatternSetsRequestRequestTypeDef]
    ) -> ListRegexPatternSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_regex_pattern_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_regex_pattern_sets)
        """

    async def list_rule_groups(
        self, **kwargs: Unpack[ListRuleGroupsRequestRequestTypeDef]
    ) -> ListRuleGroupsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_rule_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_rule_groups)
        """

    async def list_rules(
        self, **kwargs: Unpack[ListRulesRequestRequestTypeDef]
    ) -> ListRulesResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_rules.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_rules)
        """

    async def list_size_constraint_sets(
        self, **kwargs: Unpack[ListSizeConstraintSetsRequestRequestTypeDef]
    ) -> ListSizeConstraintSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_size_constraint_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_size_constraint_sets)
        """

    async def list_sql_injection_match_sets(
        self, **kwargs: Unpack[ListSqlInjectionMatchSetsRequestRequestTypeDef]
    ) -> ListSqlInjectionMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_sql_injection_match_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_sql_injection_match_sets)
        """

    async def list_subscribed_rule_groups(
        self, **kwargs: Unpack[ListSubscribedRuleGroupsRequestRequestTypeDef]
    ) -> ListSubscribedRuleGroupsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_subscribed_rule_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_subscribed_rule_groups)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_tags_for_resource)
        """

    async def list_web_acls(
        self, **kwargs: Unpack[ListWebACLsRequestRequestTypeDef]
    ) -> ListWebACLsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_web_acls.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_web_acls)
        """

    async def list_xss_match_sets(
        self, **kwargs: Unpack[ListXssMatchSetsRequestRequestTypeDef]
    ) -> ListXssMatchSetsResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/list_xss_match_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#list_xss_match_sets)
        """

    async def put_logging_configuration(
        self, **kwargs: Unpack[PutLoggingConfigurationRequestRequestTypeDef]
    ) -> PutLoggingConfigurationResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/put_logging_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#put_logging_configuration)
        """

    async def put_permission_policy(
        self, **kwargs: Unpack[PutPermissionPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/put_permission_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#put_permission_policy)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#untag_resource)
        """

    async def update_byte_match_set(
        self, **kwargs: Unpack[UpdateByteMatchSetRequestRequestTypeDef]
    ) -> UpdateByteMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_byte_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_byte_match_set)
        """

    async def update_geo_match_set(
        self, **kwargs: Unpack[UpdateGeoMatchSetRequestRequestTypeDef]
    ) -> UpdateGeoMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_geo_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_geo_match_set)
        """

    async def update_ip_set(
        self, **kwargs: Unpack[UpdateIPSetRequestRequestTypeDef]
    ) -> UpdateIPSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_ip_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_ip_set)
        """

    async def update_rate_based_rule(
        self, **kwargs: Unpack[UpdateRateBasedRuleRequestRequestTypeDef]
    ) -> UpdateRateBasedRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_rate_based_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_rate_based_rule)
        """

    async def update_regex_match_set(
        self, **kwargs: Unpack[UpdateRegexMatchSetRequestRequestTypeDef]
    ) -> UpdateRegexMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_regex_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_regex_match_set)
        """

    async def update_regex_pattern_set(
        self, **kwargs: Unpack[UpdateRegexPatternSetRequestRequestTypeDef]
    ) -> UpdateRegexPatternSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_regex_pattern_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_regex_pattern_set)
        """

    async def update_rule(
        self, **kwargs: Unpack[UpdateRuleRequestRequestTypeDef]
    ) -> UpdateRuleResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_rule)
        """

    async def update_rule_group(
        self, **kwargs: Unpack[UpdateRuleGroupRequestRequestTypeDef]
    ) -> UpdateRuleGroupResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_rule_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_rule_group)
        """

    async def update_size_constraint_set(
        self, **kwargs: Unpack[UpdateSizeConstraintSetRequestRequestTypeDef]
    ) -> UpdateSizeConstraintSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_size_constraint_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_size_constraint_set)
        """

    async def update_sql_injection_match_set(
        self, **kwargs: Unpack[UpdateSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> UpdateSqlInjectionMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_sql_injection_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_sql_injection_match_set)
        """

    async def update_web_acl(
        self, **kwargs: Unpack[UpdateWebACLRequestRequestTypeDef]
    ) -> UpdateWebACLResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_web_acl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_web_acl)
        """

    async def update_xss_match_set(
        self, **kwargs: Unpack[UpdateXssMatchSetRequestRequestTypeDef]
    ) -> UpdateXssMatchSetResponseTypeDef:
        """
        This is <b>AWS WAF Classic</b> documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/update_xss_match_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#update_xss_match_set)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_rate_based_rule_managed_keys"]
    ) -> GetRateBasedRuleManagedKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_activated_rules_in_rule_group"]
    ) -> ListActivatedRulesInRuleGroupPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_byte_match_sets"]
    ) -> ListByteMatchSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_geo_match_sets"]
    ) -> ListGeoMatchSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ip_sets"]
    ) -> ListIPSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_logging_configurations"]
    ) -> ListLoggingConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_rate_based_rules"]
    ) -> ListRateBasedRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_regex_match_sets"]
    ) -> ListRegexMatchSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_regex_pattern_sets"]
    ) -> ListRegexPatternSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_rule_groups"]
    ) -> ListRuleGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_rules"]
    ) -> ListRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_size_constraint_sets"]
    ) -> ListSizeConstraintSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sql_injection_match_sets"]
    ) -> ListSqlInjectionMatchSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_subscribed_rule_groups"]
    ) -> ListSubscribedRuleGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_web_acls"]
    ) -> ListWebACLsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_xss_match_sets"]
    ) -> ListXssMatchSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/client/)
        """
