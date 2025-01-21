from enum import Enum

from pydantic import BaseModel, Field

# Enums


class ReferralType(Enum):
    """Enum for referral types.

    Args:
        DIRECT (int): Direct referral.
        INDIRECT (int): Indirect referral.

    """

    DIRECT = 1
    INDIRECT = 2


class CommissionBizType(Enum):
    """Enum for commission business types.

    Args:
        PERPETUAL_CONTRACT (int): Perpetual contract commission.
        SPOT (int): Spot trading commission.

    """

    PERPETUAL_CONTRACT = 81
    SPOT = 82


# Helper model
class PaginationParams(BaseModel):
    """Model for pagination parameters.

    Args:
        page_index (int): Page number for pagination, must be greater than 0.
        page_size (int): The number of pages must be greater than 0 and the maximum value is 200.

    """

    page_index: int = Field(
        ...,
        description="Page number for pagination, must be greater than 0",
        alias="pageIndex",
    )
    page_size: int = Field(
        ...,
        description="The number of pages must be greater than 0 and the maximum value is 200",
        alias="pageSize",
    )


class InvitedUser(BaseModel):
    """Model for an invited user.

    Args:
        uid (str): Invited User UID.
        own_invite_code (str): Invitation code for Invited User.
        inviter_sid (int): Superiors Uid.
        invitation_code (str): Invitation code for superiors.
        register_time (int): Registration timestamp, unit: milliseconds.
        direct_invitation (bool): True: Direct invitation, False: Indirect invitation.
        kyc_result (str): True: KYC, False: No KYC.
        deposit (bool): True: Deposited, False: Not deposited.
        balance_volume (str): Net assets (USDT).
        trade (bool): True: Traded, False: Not traded, excluding trades made with trial funds or additional funds.
        user_level (int): Customer level.
        commission_ratio (int): Commission percentage, unit: %.
        current_benefit (int): Current welfare method: 0 - No welfare, 1 - Fee cashback, 2 - Perpetual fee discount.
        benefit_ratio (int): Transaction fee reduction percentage, unit: %.
        benefit_expiration (int): Welfare expiration timestamp, unit: milliseconds.

    """

    uid: str = Field(..., description="Invited User UID")
    own_invite_code: str = Field(
        ...,
        description="Invitation code for Invited User",
        alias="ownInviteCode",
    )
    inviter_sid: int = Field(..., description="Superiors Uid", alias="inviterSid")
    invitation_code: str = Field(
        ...,
        description="Invitation code for superiors",
        alias="InvitationCode",
    )
    register_time: int = Field(
        ...,
        description="Registration timestamp, unit: milliseconds",
        alias="registerTime",
    )
    direct_invitation: bool = Field(
        ...,
        description="True: Direct invitation, False: Indirect invitation",
        alias="directInvitation",
    )
    kyc_result: str = Field(
        ...,
        description="True: KYC, False: No KYC",
        alias="kycResult",
    )
    deposit: bool = Field(..., description="True: Deposited, False: Not deposited")
    balance_volume: str = Field(
        ...,
        description="Net assets (USDT)",
        alias="balanceVolume",
    )
    trade: bool = Field(
        ...,
        description="True: Traded, False: Not traded, excluding trades made with trial funds or additional funds",
    )
    user_level: int = Field(
        ...,
        description="Customer level",
        alias="userLevel",
    )
    commission_ratio: int = Field(
        ...,
        description="Commission percentage, unit: %",
        alias="commissionRatio",
    )
    current_benefit: int = Field(
        ...,
        description="Current welfare method: 0 - No welfare, 1 - Fee cashback, 2 - Perpetual fee discount",
        alias="currentBenefit",
    )
    benefit_ratio: int = Field(
        ...,
        description="Transaction fee reduction percentage, unit: %",
        alias="benefitRatio",
    )
    benefit_expiration: int = Field(
        ...,
        description="Welfare expiration timestamp, unit: milliseconds",
        alias="benefitExpiration",
    )


class QueryInvitedUsersResponseData(BaseModel):
    """Model for the data field in QueryInvitedUsersResponse.

    Args:
        data (List[InvitedUser]): List of invited users.
        total (int): Total number of invited users.
        current_agent_uid (int): Current agent UID.

    """

    data: list[InvitedUser] = Field(
        ...,
        description="List of invited users",
        alias="list",
    )
    total: int = Field(..., description="Total number of invited users")
    current_agent_uid: int = Field(
        ...,
        description="Current agent UID",
        alias="currentAgentUid",
    )


class QueryInvitedUsersResponse(BaseModel):
    """Model for the response of Query Invited Users.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (QueryInvitedUsersResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: QueryInvitedUsersResponseData = Field(..., description="Response data")


class CommissionData(BaseModel):
    """Model for commission data.

    Args:
        uid (int): Invited User UID.
        commission_time (int): Commission timestamp, date.
        trading_volume (str): Total trading volume in USDT for Spot, Standard Contract, Perpetual Contract, Copy Trading, and MT5 business lines combined.
        commission_volume (str): Commission amount in USDT.
        spot_trading_volume (str): Spot transaction amount, discounted to USDT.
        swap_trading_volume (str): Perpetual contract trading volume, converted into USDT.
        std_trading_volume (str): Standard contract transaction amount, discounted in USDT.
        ext_copy_trading_volume (str): Copy transaction amount, discounted in USDT.
        mt5_trading_volume (str): MT5 transaction volume, discount USDT.
        spot_commission_volume (str): Spot commission rebate amount, discounted in USDT.
        swap_commission_volume (str): Perpetual contract rebate commission amount, converted into USDT.
        std_commission_volume (str): Standard contract rebate amount, discounted in USDT.
        ext_copy_commission_volume (str): The commission amount for following orders is discounted in USDT.
        mt5_commission_volume (str): MT5 rebate commission amount, discount USDT.

    """

    uid: int = Field(..., description="Invited User UID")
    commission_time: int = Field(
        ...,
        description="Commission timestamp, date",
        alias="commissionTime",
    )
    trading_volume: str = Field(
        ...,
        description="Total trading volume in USDT for Spot, Standard Contract, Perpetual Contract, Copy Trading, and MT5 business lines combined",
        alias="tradingVolume",
    )
    commission_volume: str = Field(
        ...,
        description="Commission amount in USDT",
        alias="commissionVolume",
    )
    spot_trading_volume: str = Field(
        ...,
        description="Spot transaction amount, discounted to USDT",
        alias="spotTradingVolume",
    )
    swap_trading_volume: str = Field(
        ...,
        description="Perpetual contract trading volume, converted into USDT",
        alias="swapTradingVolume",
    )
    std_trading_volume: str = Field(
        ...,
        description="Standard contract transaction amount, discounted in USDT",
        alias="stdTradingVolume",
    )
    ext_copy_trading_volume: str = Field(
        ...,
        description="Copy transaction amount, discounted in USDT",
        alias="extCopyTradingVolume",
    )
    mt5_trading_volume: str = Field(
        ...,
        description="MT5 transaction volume, discount USDT",
        alias="mt5TradingVolume",
    )
    spot_commission_volume: str = Field(
        ...,
        description="Spot commission rebate amount, discounted in USDT",
        alias="spotCommissionVolume",
    )
    swap_commission_volume: str = Field(
        ...,
        description="Perpetual contract rebate commission amount, converted into USDT",
        alias="swapCommissionVolume",
    )
    std_commission_volume: str = Field(
        ...,
        description="Standard contract rebate amount, discounted in USDT",
        alias="stdCommissionVolume",
    )
    ext_copy_commission_volume: str = Field(
        ...,
        description="The commission amount for following orders is discounted in USDT",
        alias="extCopyCommissionVolume",
    )
    mt5_commission_volume: str = Field(
        ...,
        description="MT5 rebate commission amount, discount USDT",
        alias="mt5CommissionVolume",
    )


class DailyCommissionQueryResponseData(BaseModel):
    """Model for the data field in DailyCommissionQueryResponse.

    Args:
        data (List[CommissionData]): List of commission data.
        total (int): Total number of records.
        current_agent_uid (int): Current agent UID.

    """

    data: list[CommissionData] = Field(
        ...,
        description="List of commission data",
        alias="list",
    )
    total: int = Field(..., description="Total number of records")
    current_agent_uid: int = Field(
        ...,
        description="Current agent UID",
        alias="currentAgentUid",
    )


class DailyCommissionQueryResponse(BaseModel):
    """Model for the response of Daily Commission Query.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (DailyCommissionQueryResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: DailyCommissionQueryResponseData = Field(..., description="Response data")


class AgentUserInformationData(BaseModel):
    """Model for the data field in QueryAgentUserInformationResponse.

    Args:
        uid (int): Invited User UID.
        exist_inviter (str): True: There is an inviter, False: There is no inviter.
        invite_result (bool): True: Invitation relationship, False: Non-invitation relationship.
        direct_invitation (bool): True: Direct invitation, False: Indirect invitation.
        inviter_sid (int): Superiors Uid.
        register_time (int): Registration timestamp, unit: milliseconds.
        deposit (bool): True: Deposited, False: Not deposited.
        kyc_result (str): True: KYC, False: No KYC.
        balance_volume (str): Net assets (USDT).
        trade (bool): True: Traded, False: Not traded, excluding trades made with trial funds or additional funds.
        user_level (int): Customer level.
        commission_ratio (int): Commission percentage, unit: %.
        current_benefit (int): Current welfare method: 0 - No welfare, 1 - Fee cashback, 2 - Perpetual fee discount.
        benefit_ratio (int): Transaction fee reduction percentage, unit: %.
        benefit_expiration (int): Welfare expiration timestamp, unit: milliseconds.

    """

    uid: int = Field(..., description="Invited User UID")
    exist_inviter: str = Field(
        ...,
        description="True: There is an inviter, False: There is no inviter",
        alias="existInviter",
    )
    invite_result: bool = Field(
        ...,
        description="True: Invitation relationship, False: Non-invitation relationship",
        alias="inviteResult",
    )
    direct_invitation: bool = Field(
        ...,
        description="True: Direct invitation, False: Indirect invitation",
        alias="directInvitation",
    )
    inviter_sid: int = Field(..., description="Superiors Uid", alias="inviterSid")
    register_time: int = Field(
        ...,
        description="Registration timestamp, unit: milliseconds",
        alias="registerDateTime",
    )
    deposit: bool = Field(..., description="True: Deposited, False: Not deposited")
    kyc_result: str = Field(
        ...,
        description="True: KYC, False: No KYC",
        alias="kycResult",
    )
    balance_volume: str = Field(
        ...,
        description="Net assets (USDT)",
        alias="balanceVolume",
    )
    trade: bool = Field(
        ...,
        description="True: Traded, False: Not traded, excluding trades made with trial funds or additional funds",
    )
    user_level: int = Field(..., description="Customer level", alias="userLevel")
    commission_ratio: int = Field(
        ...,
        description="Commission percentage, unit: %",
        alias="commissionRatio",
    )
    current_benefit: int = Field(
        ...,
        description="Current welfare method: 0 - No welfare, 1 - Fee cashback, 2 - Perpetual fee discount",
        alias="currentBenefit",
    )
    benefit_ratio: int = Field(
        ...,
        description="Transaction fee reduction percentage, unit: %",
        alias="benefitRatio",
    )
    benefit_expiration: int = Field(
        ...,
        description="Welfare expiration timestamp, unit: milliseconds",
        alias="benefitExpiration",
    )


class QueryAgentUserInformationResponse(BaseModel):
    """Model for the response of Query Agent User Information.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        msg (str): Error Details Description.
        timestamp (int): Response timestamp.
        data (AgentUserInformationData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    timestamp: int = Field(..., description="Response timestamp")
    data: AgentUserInformationData = Field(..., description="Response data")


class DepositDetail(BaseModel):
    """Model for deposit details.

    Args:
        uid (int): Invited User UID.
        invite_result (bool): True: Invitation relationship, False: Non-invitation relationship.
        direct_invitation (bool): True: Direct invitation, False: Indirect invitation.
        biz_type (int): 1: Deposit.
        biz_time (int): Event time.
        asset_type (int): Operation type breakdown.
        asset_type_name (str): Operation type subdivision name.
        currency_name (str): Currency.
        currency_amount_volume (str): Amount.

    """

    uid: int = Field(..., description="Invited User UID")
    invite_result: bool = Field(
        ...,
        description="True: Invitation relationship, False: Non-invitation relationship",
        alias="inviteResult",
    )
    direct_invitation: bool = Field(
        ...,
        description="True: Direct invitation, False: Indirect invitation",
        alias="directInvitation",
    )
    biz_type: int = Field(..., description="1: Deposit", alias="bizType")
    biz_time: int = Field(..., description="Event time", alias="bizTime")
    asset_type: int = Field(
        ...,
        description="Operation type breakdown",
        alias="assetType",
    )
    asset_type_name: str = Field(
        ...,
        description="Operation type subdivision name",
        alias="assetTypeName",
    )
    currency_name: str = Field(..., description="Currency", alias="currencyName")
    currency_amount_volume: str = Field(
        ...,
        description="Amount",
        alias="currencyAmountVolume",
    )


class QueryDepositDetailsOfInvitedUsersResponseData(BaseModel):
    """Model for the data field in QueryDepositDetailsOfInvitedUsersResponse.

    Args:
        data (List[DepositDetail]): List of deposit details.
        total (int): Total number of records.

    """

    data: list[DepositDetail] = Field(
        ...,
        description="List of deposit details",
        alias="list",
    )
    total: int = Field(..., description="Total number of records")


class QueryDepositDetailsOfInvitedUsersResponse(BaseModel):
    """Model for the response of Query the deposit details of invited users.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        msg (str): Error Details Description.
        timestamp (int): Response timestamp.
        data (QueryDepositDetailsOfInvitedUsersResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    timestamp: int = Field(..., description="Response timestamp")
    data: QueryDepositDetailsOfInvitedUsersResponseData = Field(
        ...,
        description="Response data",
    )


class ApiTransactionCommissionNonInvitationData(BaseModel):
    """Model for API transaction commission data (non-invitation relationship).

    Args:
        uid (int): UID of the trading user (non-invitation relationship user).
        commission_time (int): Commission timestamp, date.
        trade_volume (str): API order amount is discounted in USDT.
        commission_volume (str): Rebate commission amount in USDT.
        commission_biz_type (int): 81: Perpetual contract trading API commission, 82: Spot trading API commission.

    """

    uid: int = Field(
        ...,
        description="UID of the trading user (non-invitation relationship user)",
    )
    commission_time: int = Field(
        ...,
        description="Commission timestamp, date",
        alias="commissionTime",
    )
    trade_volume: str = Field(
        ...,
        description="API order amount is discounted in USDT",
        alias="tradeVolume",
    )
    commission_volume: str = Field(
        ...,
        description="Rebate commission amount in USDT",
        alias="commissionVolume",
    )
    commission_biz_type: int = Field(
        ...,
        description="81: Perpetual contract trading API commission, 82: Spot trading API commission",
        alias="commissionBizType",
    )


class QueryApiTransactionCommissionNonInvitationResponseData(BaseModel):
    """Model for the data field in QueryApiTransactionCommissionNonInvitationResponse.

    Args:
        data (List[ApiTransactionCommissionNonInvitationData]): List of API transaction commission data.
        total (int): Total number of records.

    """

    data: list[ApiTransactionCommissionNonInvitationData] = Field(
        ...,
        description="List of API transaction commission data",
        alias="list",
    )
    total: int = Field(..., description="Total number of records")


class QueryApiTransactionCommissionNonInvitationResponse(BaseModel):
    """Model for the response of Query API transaction commission (non-invitation relationship).

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        msg (str): Error Details Description.
        timestamp (int): Response timestamp.
        data (QueryApiTransactionCommissionNonInvitationResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    timestamp: int = Field(..., description="Response timestamp")
    data: QueryApiTransactionCommissionNonInvitationResponseData = Field(
        ...,
        description="Response data",
    )


class PartnerInformationData(BaseModel):
    """Model for partner information data.

    Args:
        uid (int): Partner UID.
        email (str): Partner mailbox, encrypted status.
        phone (str): Partner's mobile phone number, encrypted.
        referral_type (ReferralType): Invitation type: 1: direct invitation, 2: indirect invitation.
        remarks (str): Remarks.
        referrer_uid (int): Superior Uid.
        language (str): Language.
        new_referees (str): The number of new invitees during the query period.
        first_trade (str): Number of people who made their first transaction during the query period.
        branch_deposits (str): The amount of channel recharge during the query period.
        branch_trading (str): Number of channel transactions during query time.
        branch_trading_vol (str): The transaction amount of the channel during the query period.
        level (str): Level.
        commission_ratio (str): Rebate ratio.

    """

    uid: int = Field(..., description="Partner UID")
    email: str = Field(..., description="Partner mailbox, encrypted status")
    phone: str = Field(
        ...,
        description="Partner's mobile phone number, encrypted",
        alias="Phone",
    )
    referral_type: ReferralType = Field(
        ...,
        description="Invitation type: 1: direct invitation, 2: indirect invitation",
        alias="referralType",
    )
    remarks: str = Field(..., description="Remarks")
    referrer_uid: int = Field(..., description="Superior Uid", alias="referrerUid")
    language: str = Field(..., description="Language")
    new_referees: str = Field(
        ...,
        description="The number of new invitees during the query period",
        alias="newReferees",
    )
    first_trade: str = Field(
        ...,
        description="Number of people who made their first transaction during the query period",
        alias="firstTrade",
    )
    branch_deposits: str = Field(
        ...,
        description="The amount of channel recharge during the query period",
        alias="branchDeposits",
    )
    branch_trading: str = Field(
        ...,
        description="Number of channel transactions during query time",
        alias="branchTrading",
    )
    branch_trading_vol: str = Field(
        ...,
        description="The transaction amount of the channel during the query period",
        alias="branchTradingVol",
    )
    level: str = Field(..., description="Level")
    commission_ratio: str = Field(
        ...,
        description="Rebate ratio",
        alias="commissionRatio",
    )


class QueryPartnerInformationResponseData(BaseModel):
    """Model for the data field in QueryPartnerInformationResponse.

    Args:
        data (List[PartnerInformationData]): List of partner information data.
        total (int): Total number of records.

    """

    data: list[PartnerInformationData] = Field(
        ...,
        description="List of partner information data",
        alias="list",
    )
    total: int = Field(..., description="Total number of records")


class QueryPartnerInformationResponse(BaseModel):
    """Model for the response of Query partner information.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (QueryPartnerInformationResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: QueryPartnerInformationResponseData = Field(..., description="Response data")
