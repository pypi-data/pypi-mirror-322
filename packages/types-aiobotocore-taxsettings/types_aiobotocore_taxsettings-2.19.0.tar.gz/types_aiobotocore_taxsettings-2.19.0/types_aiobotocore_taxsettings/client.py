"""
Type annotations for taxsettings service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_taxsettings.client import TaxSettingsClient

    session = get_session()
    async with session.create_client("taxsettings") as client:
        client: TaxSettingsClient
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
    ListSupplementalTaxRegistrationsPaginator,
    ListTaxExemptionsPaginator,
    ListTaxRegistrationsPaginator,
)
from .type_defs import (
    BatchDeleteTaxRegistrationRequestRequestTypeDef,
    BatchDeleteTaxRegistrationResponseTypeDef,
    BatchGetTaxExemptionsRequestRequestTypeDef,
    BatchGetTaxExemptionsResponseTypeDef,
    BatchPutTaxRegistrationRequestRequestTypeDef,
    BatchPutTaxRegistrationResponseTypeDef,
    DeleteSupplementalTaxRegistrationRequestRequestTypeDef,
    DeleteTaxRegistrationRequestRequestTypeDef,
    GetTaxExemptionTypesResponseTypeDef,
    GetTaxInheritanceResponseTypeDef,
    GetTaxRegistrationDocumentRequestRequestTypeDef,
    GetTaxRegistrationDocumentResponseTypeDef,
    GetTaxRegistrationRequestRequestTypeDef,
    GetTaxRegistrationResponseTypeDef,
    ListSupplementalTaxRegistrationsRequestRequestTypeDef,
    ListSupplementalTaxRegistrationsResponseTypeDef,
    ListTaxExemptionsRequestRequestTypeDef,
    ListTaxExemptionsResponseTypeDef,
    ListTaxRegistrationsRequestRequestTypeDef,
    ListTaxRegistrationsResponseTypeDef,
    PutSupplementalTaxRegistrationRequestRequestTypeDef,
    PutSupplementalTaxRegistrationResponseTypeDef,
    PutTaxExemptionRequestRequestTypeDef,
    PutTaxExemptionResponseTypeDef,
    PutTaxInheritanceRequestRequestTypeDef,
    PutTaxRegistrationRequestRequestTypeDef,
    PutTaxRegistrationResponseTypeDef,
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


__all__ = ("TaxSettingsClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    AttachmentUploadException: Type[BotocoreClientError]
    CaseCreationLimitExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class TaxSettingsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings.html#TaxSettings.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TaxSettingsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings.html#TaxSettings.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#generate_presigned_url)
        """

    async def batch_delete_tax_registration(
        self, **kwargs: Unpack[BatchDeleteTaxRegistrationRequestRequestTypeDef]
    ) -> BatchDeleteTaxRegistrationResponseTypeDef:
        """
        Deletes tax registration for multiple accounts in batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/batch_delete_tax_registration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#batch_delete_tax_registration)
        """

    async def batch_get_tax_exemptions(
        self, **kwargs: Unpack[BatchGetTaxExemptionsRequestRequestTypeDef]
    ) -> BatchGetTaxExemptionsResponseTypeDef:
        """
        Get the active tax exemptions for a given list of accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/batch_get_tax_exemptions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#batch_get_tax_exemptions)
        """

    async def batch_put_tax_registration(
        self, **kwargs: Unpack[BatchPutTaxRegistrationRequestRequestTypeDef]
    ) -> BatchPutTaxRegistrationResponseTypeDef:
        """
        Adds or updates tax registration for multiple accounts in batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/batch_put_tax_registration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#batch_put_tax_registration)
        """

    async def delete_supplemental_tax_registration(
        self, **kwargs: Unpack[DeleteSupplementalTaxRegistrationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a supplemental tax registration for a single account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/delete_supplemental_tax_registration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#delete_supplemental_tax_registration)
        """

    async def delete_tax_registration(
        self, **kwargs: Unpack[DeleteTaxRegistrationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes tax registration for a single account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/delete_tax_registration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#delete_tax_registration)
        """

    async def get_tax_exemption_types(self) -> GetTaxExemptionTypesResponseTypeDef:
        """
        Get supported tax exemption types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/get_tax_exemption_types.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#get_tax_exemption_types)
        """

    async def get_tax_inheritance(self) -> GetTaxInheritanceResponseTypeDef:
        """
        The get account tax inheritance status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/get_tax_inheritance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#get_tax_inheritance)
        """

    async def get_tax_registration(
        self, **kwargs: Unpack[GetTaxRegistrationRequestRequestTypeDef]
    ) -> GetTaxRegistrationResponseTypeDef:
        """
        Retrieves tax registration for a single account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/get_tax_registration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#get_tax_registration)
        """

    async def get_tax_registration_document(
        self, **kwargs: Unpack[GetTaxRegistrationDocumentRequestRequestTypeDef]
    ) -> GetTaxRegistrationDocumentResponseTypeDef:
        """
        Downloads your tax documents to the Amazon S3 bucket that you specify in your
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/get_tax_registration_document.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#get_tax_registration_document)
        """

    async def list_supplemental_tax_registrations(
        self, **kwargs: Unpack[ListSupplementalTaxRegistrationsRequestRequestTypeDef]
    ) -> ListSupplementalTaxRegistrationsResponseTypeDef:
        """
        Retrieves supplemental tax registrations for a single account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/list_supplemental_tax_registrations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#list_supplemental_tax_registrations)
        """

    async def list_tax_exemptions(
        self, **kwargs: Unpack[ListTaxExemptionsRequestRequestTypeDef]
    ) -> ListTaxExemptionsResponseTypeDef:
        """
        Retrieves the tax exemption of accounts listed in a consolidated billing family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/list_tax_exemptions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#list_tax_exemptions)
        """

    async def list_tax_registrations(
        self, **kwargs: Unpack[ListTaxRegistrationsRequestRequestTypeDef]
    ) -> ListTaxRegistrationsResponseTypeDef:
        """
        Retrieves the tax registration of accounts listed in a consolidated billing
        family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/list_tax_registrations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#list_tax_registrations)
        """

    async def put_supplemental_tax_registration(
        self, **kwargs: Unpack[PutSupplementalTaxRegistrationRequestRequestTypeDef]
    ) -> PutSupplementalTaxRegistrationResponseTypeDef:
        """
        Stores supplemental tax registration for a single account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/put_supplemental_tax_registration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#put_supplemental_tax_registration)
        """

    async def put_tax_exemption(
        self, **kwargs: Unpack[PutTaxExemptionRequestRequestTypeDef]
    ) -> PutTaxExemptionResponseTypeDef:
        """
        Adds the tax exemption for a single account or all accounts listed in a
        consolidated billing family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/put_tax_exemption.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#put_tax_exemption)
        """

    async def put_tax_inheritance(
        self, **kwargs: Unpack[PutTaxInheritanceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The updated tax inheritance status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/put_tax_inheritance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#put_tax_inheritance)
        """

    async def put_tax_registration(
        self, **kwargs: Unpack[PutTaxRegistrationRequestRequestTypeDef]
    ) -> PutTaxRegistrationResponseTypeDef:
        """
        Adds or updates tax registration for a single account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/put_tax_registration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#put_tax_registration)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_supplemental_tax_registrations"]
    ) -> ListSupplementalTaxRegistrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tax_exemptions"]
    ) -> ListTaxExemptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tax_registrations"]
    ) -> ListTaxRegistrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings.html#TaxSettings.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings.html#TaxSettings.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/client/)
        """
