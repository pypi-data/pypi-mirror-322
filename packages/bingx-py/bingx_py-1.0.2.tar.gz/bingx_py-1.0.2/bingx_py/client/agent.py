from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.agent import (
    CommissionBizType,
    DailyCommissionQueryResponse,
    PaginationParams,
    QueryAgentUserInformationResponse,
    QueryApiTransactionCommissionNonInvitationResponse,
    QueryDepositDetailsOfInvitedUsersResponse,
    QueryInvitedUsersResponse,
    QueryPartnerInformationResponse,
)

if TYPE_CHECKING:
    from bingx_py.client import BingXHttpClient


class AgentAPI:
    """API for managing agent on BingX.

    This class provides methods to manage agent, including query agent user information,
    query partner information, query invited users, query deposit details of invited users,
    query api transaction commission, and query daily commission.
    """

    def __init__(self, client: "BingXHttpClient") -> None:
        """Initialize the AgentAPI.

        Args:
            client (BingXHttpClient): The HTTP client used to interact with the BingX API.

        Returns:
            None

        """
        self.client = client

    def query_invited_users(
        self,
        pagination: PaginationParams,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        last_uid: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> QueryInvitedUsersResponse:
        """Query Invited Users.

        Args:
            pagination (PaginationParams): Page number and size for pagination.
            start_time (Optional[int]): Start timestamp (millisecond). The maximum query window is 30 days.
            If querying for all data, startTime and endTime can be left blank. Defaults to None.
            end_time (Optional[int]): End timestamp (millisecond). The maximum query window is 30 days.
            If querying for all data, startTime and endTime can be left blank. Defaults to None.
            last_uid (Optional[int]): User UID, must be transmitted when the queried data exceeds 10,000.
            The first request does not need to be passed, and the last uid of the current page is passed each time afterwards.
            Defaults to None.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Default is 5 seconds if not provided.
            Defaults to None.

        Returns:
            QueryInvitedUsersResponse: The response data.

        """
        params: dict[str, Any] = {**pagination.model_dump(by_alias=True)}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if last_uid is not None:
            params["lastUid"] = last_uid
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get(
                "/openApi/agent/v1/account/inviteAccountList",
                params=params,
            ),
            QueryInvitedUsersResponse,
        )

    def daily_commission_query(
        self,
        start_time: str,
        end_time: str,
        pagination: PaginationParams,
        uid: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> DailyCommissionQueryResponse:
        """Daily Commission Query (invitation relationship).

        Args:
            start_time (str): Start timestamp, in days, with a maximum query window of 30 days and a sliding range of the last 365 days.
            end_time (str): End timestamp, in days, with a maximum query window of 30 days and a sliding range of the last 365 days.
            pagination (PaginationParams): Page number for pagination, must be greater than 0 and page size for pagination, must be greater than 0 with a maximum value of 100.
            uid (Optional[int]): Invited User UID. Defaults to None.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Default is 5 seconds if not provided. Defaults to None.

        Returns:
            DailyCommissionQueryResponse: The response data.

        """
        params: dict[str, Any] = {
            "startTime": start_time,
            "endTime": end_time,
            **pagination.model_dump(by_alias=True),
        }
        if uid is not None:
            params["uid"] = uid
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get(
                "/openApi/agent/v1/reward/commissionDataList",
                params=params,
            ),
            DailyCommissionQueryResponse,
        )

    def query_agent_user_information(
        self,
        uid: int,
    ) -> QueryAgentUserInformationResponse:
        """Query agent user information.

        Args:
            uid (int): Invited User UID.

        Returns:
            QueryAgentUserInformationResponse: The response data.

        """
        params: dict[str, Any] = {
            "uid": uid,
        }

        return self.client.save_convert(
            self.client.get(
                "/openApi/agent/v1/account/inviteRelationCheck",
                params=params,
            ),
            QueryAgentUserInformationResponse,
        )

    def query_deposit_details_of_invited_users(
        self,
        uid: int,
        biz_type: int,
        start_time: int,
        end_time: int,
        pagination: PaginationParams,
        recv_window: Optional[int] = None,
    ) -> QueryDepositDetailsOfInvitedUsersResponse:
        """Query the deposit details of invited users.

        Args:
            uid (int): Inviting user UID, must be the parent user UID.
            biz_type (int): 1: Deposit.
            start_time (int): Start timestamp (days), only supports querying the last 90 days of data.
            end_time (int): End timestamp (days). Only the last 90 days of data can be queried.
            pagination (PaginationParams): Page number and size for pagination.
            recv_window (Optional[int]): Request valid time window value, unit: milliseconds. If not filled, the default is 5 seconds. Defaults to None.

        Returns:
            QueryDepositDetailsOfInvitedUsersResponse: The response data.

        """
        params: dict[str, Any] = {
            "uid": uid,
            "bizType": biz_type,
            "startTime": start_time,
            "endTime": end_time,
            **pagination.model_dump(by_alias=True),
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get(
                "/openApi/agent/v1/account/inviteRelationCheck",
                params=params,
            ),
            QueryDepositDetailsOfInvitedUsersResponse,
        )

    def query_api_transaction_commission_non_invitation(
        self,
        commission_biz_type: CommissionBizType,
        start_time: str,
        end_time: str,
        pagination: PaginationParams,
        uid: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> QueryApiTransactionCommissionNonInvitationResponse:
        """Query API transaction commission (non-invitation relationship).

        Args:
            commission_biz_type (CommissionBizType): Commission business type.
            start_time (str): Start timestamp (days), only supports querying data after December 1, 2023.
            end_time (str): End timestamp (days), only supports querying data after December 1, 2023.
            pagination (PaginationParams): Page number for pagination, must be greater than 0 and page size for pagination, must be greater than 0 with a maximum value of 100.
            uid (Optional[int]): UID of the trading user (non-invitation relationship user). Defaults to None.
            recv_window (Optional[int]): Request valid time window value, unit: milliseconds. If not filled, the default is 5 seconds. Defaults to None.

        Returns:
            QueryApiTransactionCommissionNonInvitationResponse: The response data.

        """
        params: dict[str, Any] = {
            "commissionBizType": commission_biz_type.value,
            "startTime": start_time,
            "endTime": end_time,
            **pagination.model_dump(by_alias=True),
        }
        if uid is not None:
            params["uid"] = uid
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get(
                "/openApi/agent/v1/reward/third/commissionDataList",
                params=params,
            ),
            QueryApiTransactionCommissionNonInvitationResponse,
        )

    def query_partner_information(
        self,
        start_time: int,
        end_time: int,
        pagination: PaginationParams,
        uid: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> QueryPartnerInformationResponse:
        """Query partner information.

        Args:
            start_time (int): Start time, unit: day, only supports querying the latest 3 months.
            end_time (int): End time, unit: day, only supports querying the latest 3 months.
            pagination (PaginationParams): Page number for pagination, must be greater than 0 and page size for pagination, must be greater than 0 with a maximum value of 200.
            uid (Optional[int]): Partner UID. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, unit: milliseconds. If not filled, the default is 5 seconds. Defaults to None.

        Returns:
            QueryPartnerInformationResponse: The response data.

        """
        params: dict[str, Any] = {
            "startTime": start_time,
            "endTime": end_time,
            **pagination.model_dump(by_alias=True),
        }
        if uid is not None:
            params["uid"] = uid
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/agent/v1/asset/partnerData", params=params),
            QueryPartnerInformationResponse,
        )
