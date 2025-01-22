"""
Python client for the Solscan API.

This module provides a client for interacting with both the public and pro Solscan APIs.
It handles authentication, rate limiting, and provides typed responses for API endpoints.

Example:
    client = Client(auth_token_file_path="path/to/token")
    chain_info = await client.chain_info()

Rate Limits:
    - V2 API: 1000 requests per minute
    - V3 API: 2000 requests per minute

Classes:
    Client: Main client class for making API requests
    Flow: Enum for specifying transaction flow direction
    TinyPageSize: Enum for pagination sizes (12, 24, 36)
    SmallPageSize: Enum for pagination sizes (50, 100)
"""


import asyncio
import base64
from enum import Enum
import math
import statistics
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import getpass
from typing import Any, Awaitable, Callable, TypeVar, TypedDict, List
from pyrate_limiter import Duration, Limiter, Rate
from loguru import logger
import requests


public_base_url = "https://public-api.solscan.io"
pro_base_url = "https://pro-api.solscan.io/v2.0"

v2_max_requests_per_minute = 1000
v3_max_requests_per_minute = 2000

D = TypeVar("D")

RespData = TypedDict("RespData",{"success": bool,"data": D})

Errors = TypedDict("Errors",{"code": int,"message": str})

RespError = TypedDict("RespError",{"success": bool,"errors": Errors})

ChainInfo = TypedDict("ChainInfo", {
    "blockHeight": int,
    "currentEpoch": int,
    "absoluteSlot": int,
    "transactionCount": int
})

class Flow(Enum):
    # Account Activity
    IN = "in"
    OUT = "out"
    # Token Activity
    EMPTY = ""
    
class TinyPageSize(Enum):
    PAGE_SIZE_12 = 12
    PAGE_SIZE_24 = 24
    PAGE_SIZE_36 = 36

class SmallPageSize(Enum):
    PAGE_SIZE_10 = 10
    PAGE_SIZE_20 = 20
    PAGE_SIZE_30 = 30
    PAGE_SIZE_40 = 40
    
class LargePageSize(Enum):
    PAGE_SIZE_10 = 10
    PAGE_SIZE_20 = 20
    PAGE_SIZE_30 = 30
    PAGE_SIZE_40 = 40
    PAGE_SIZE_60 = 60
    PAGE_SIZE_100 = 100
    
class SortBy(Enum):
    BLOCK_TIME = "block_time"
    
class MarketSortBy(Enum):
    VOLUME = "volume"
    TRADE = "trade"
    
class TokenSortBy(Enum):
    PRICE = "price"
    HOLDER = "holder"
    MARKET_CAP = "market_cap" 
    CREATED_TIME = "created_time"
    
class NFTCollectionSortBy(Enum):
    ITEMS = "items"
    FLOOR_PRICE = "floor_price"
    VOLUMES = "volumes"
    
class NFTCollectionItemSortBy(Enum):
    LAST_TRADE = "last_trade"
    LISTING_PRICE = "listing_price"

class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"
    
class AccountActivityType(Enum):
    TRANSFER = "ACTIVITY_SPL_TRANSFER"
    BURN = "ACTIVITY_SPL_BURN"
    MINT = "ACTIVITY_SPL_MINT"
    CREATE_ACCOUNT = "ACTIVITY_SPL_CREATE_ACCOUNT"
    
class TokenType(Enum):
    TOKEN = "token"
    NFT = "nft"
    
class ActivityType(Enum):
    # Account Activity
    ACCOUNT_ACTIVITY_SWAP = "ACTIVITY_TOKEN_SWAP"
    ACCOUNT_ACTIVITY_AGG_SWAP = "ACTIVITY_AGG_TOKEN_SWAP"
    ACCOUNT_ACTIVITY_ADD_LIQUIDITY = "ACTIVITY_TOKEN_ADD_LIQ"
    ACCOUNT_ACTIVITY_REMOVE_LIQUIDITY = "ACTIVITY_TOKEN_REMOVE_LIQ"
    ACCOUNT_ACTIVITY_STAKE = "ACTIVITY_SPL_TOKEN_STAKE"
    ACCOUNT_ACTIVITY_UNSTAKE = "ACTIVITY_SPL_TOKEN_UNSTAKE"
    ACCOUNT_ACTIVITY_WITHDRAW_STAKE = "ACTIVITY_SPL_TOKEN_WITHDRAW_STAKE"
    ACCOUNT_ACTIVITY_MINT = "ACTIVITY_SPL_MINT"
    ACCOUNT_ACTIVITY_INIT_MINT = "ACTIVITY_SPL_INIT_MINT"
    # Token Activity
    TOKEN_ACTIVITY_TRANSFER = "ACTIVITY_SPL_TRANSFER"
    TOKEN_ACTIVITY_BURN = "ACTIVITY_SPL_BURN" 
    TOKEN_ACTIVITY_MINT = "ACTIVITY_SPL_MINT"
    TOKEN_ACTIVITY_CREATE_ACCOUNT = "ACTIVITY_SPL_CREATE_ACCOUNT"
    
class NFTActivityType(Enum):
    SOLD = "ACTIVITY_NFT_SOLD"
    LISTING = "ACTIVITY_NFT_LISTING"
    BIDDING = "ACTIVITY_NFT_BIDDING"
    CANCEL_BID = "ACTIVITY_NFT_CANCEL_BID"
    CANCEL_LIST = "ACTIVITY_NFT_CANCEL_LIST"
    REJECT_BID = "ACTIVITY_NFT_REJECT_BID"
    UPDATE_PRICE = "ACTIVITY_NFT_UPDATE_PRICE"
    LIST_AUCTION = "ACTIVITY_NFT_LIST_AUCTION"

class BalanceChangeType(Enum):
    INC = "inc"
    DEC = "dec"
    
class TxStatus(Enum):
    SUCCESS = "Success"
    FAIL = "Fail"

class StakeRole(Enum):
    STAKER = "staker"
    WITHDRAWER = "withdrawer"
    
class StakeAccountStatus(Enum):
    ACTIVE = "active"
    
class StakeAccountType(Enum):
    ACTIVE = "active"
    
class AccountType(Enum):
    SYSTEM_ACCOUNT = "system_account"
    
class TxFilter(Enum):
    EXCEPT_VOTE = "exceptVote"
    ALL = "all"

Transfer = TypedDict("AccountTransfer", {
    "block_id": int,
    "trans_id": str,
    "block_time": int,
    "time": str,
    "activity_type": ActivityType,
    "from_address": str,
    "to_address": str,
    "token_address": str,
    "token_decimals": int,
    "amount": int,
    "flow": Flow
})

TokenAccount = TypedDict("TokenAccount", {
    "token_account": str,
    "token_address": str, 
    "amount": int,
    "token_decimals": int,
    "owner": str
})

ChildRouter = TypedDict("ChildRouter", {
    "token1": str,
    "token1_decimals": int,
    "amount1": str,
    "token2": str, 
    "token2_decimals": int,
    "amount2": str,
})

Router = TypedDict("Router", {
    "token1": str,
    "token1_decimals": int,
    "amount1": str,
    "token2": str, 
    "token2_decimals": int,
    "amount2": str,
    "child_routers": List[ChildRouter]
})

AmountInfo = TypedDict("AmountInfo", {
    "token1": str,
    "token1_decimals": int,
    "amount1": int,
    "token2": str,
    "token2_decimals": int, 
    "amount2": int,
    "routers": List[Router]
})

DefiActivity = TypedDict("DefiActivity", {
    "block_id": int,
    "trans_id": str,
    "block_time": int,
    "time": str,
    "activity_type": ActivityType,
    "from_address": str,
    "to_address": str,
    "sources": List[str],
    "platform": str,
    # "amount_info": AmountInfo,
    "routers": List[Router]
})

AccountChangeActivity = TypedDict("AccountChangeActivity", {
    "block_id": int,
    "block_time": int,
    "time": str,
    "trans_id": str,
    "address": str,
    "token_address": str,
    "token_account": str,
    "token_decimals": int,
    "amount": int,
    "pre_balance": int,
    "post_balance": int,
    "change_type": BalanceChangeType,
    "fee": int
})

ParsedCancelAllAndPlaceOrders = TypedDict("ParsedCancelAllAndPlaceOrders", {
    "type": str,
    "program": str,
    "program_id": str
})

Transaction = TypedDict("Transaction", {
    "slot": int,
    "fee": int,
    "status": TxStatus,
    "signer": List[str],
    "block_time": int,
    "tx_hash": str,
    "parsed_instructions": List[ParsedCancelAllAndPlaceOrders],
    "program_ids": List[str],
    "time": str
})

AccountStake = TypedDict("AccountStake", {
    "amount": int,
    "role": List[StakeRole],
    "status": StakeAccountStatus,
    "type": StakeAccountType,
    "voter": str,
    "active_stake_amount": int,
    "delegated_stake_amount": int,
    "sol_balance": int,
    "total_reward": str,
    "stake_account": str,
    "activation_epoch": int,
    "stake_type": int
})

AccountDetail = TypedDict("AccountDetail", {
    "account": str,
    "lamports": int,
    "type": AccountType,
    "executable": bool,
    "owner_program": str,
    "rent_epoch": int,
    "is_oncurve": bool
})

Market = TypedDict("Market", {
    "pool_id": str,
    "program_id": str,
    "token_1": str,
    "token_2": str,
    "token_account_1": str,
    "token_account_2": str,
    "total_trades_24h": int,
    "total_trades_prev_24h": int,
    "total_volume_24h": float,
    "total_volume_prev_24h": float
})

Token = TypedDict("Token", {
    "address": str,
    "decimals": int,
    "name": str,
    "symbol": str,
    "market_cap": float,
    "price": float,
    "price_24h_change": float,
    "created_time": int
})

TokenPrice = TypedDict("TokenPrice", {
    "date": int, # yyyymmdd
    "price": float
})

TokenHolder = TypedDict("TokenHolder", {
    "address": str,
    "amount": int,
    "decimals": int,
    "owner": str,
    "rank": int
})

TokenMeta = TypedDict("TokenMeta", {
    "supply": str,
    "address": str,
    "name": str,
    "symbol": str,
    "icon": str,
    "decimals": int,
    "holder": int,
    "creator": str,
    "create_tx": str,
    "created_time": int,
    "first_mint_tx": str,
    "first_mint_time": int,
    "price": float,
    "volume_24h": float,
    "market_cap": float,
    "market_cap_rank": int,
    "price_change_24h": float
})

TokenTop = TypedDict("TokenTop", {
    "address": str,
    "decimals": int,
    "name": str,
    "symbol": str,
    "market_cap": float,
    "price": float,
    "price_24h_change": float,
    "created_time": int
})

AccountKey = TypedDict("AccountKey", {
    "pubkey": str,
    "signer": bool,
    "source": str,
    "writable": bool
})

TransferInfo = TypedDict("TransferInfo", {
    "source_owner": str,
    "source": str,
    "destination": str,
    "destination_owner": str,
    "transfer_type": str,
    "token_address": str,
    "decimals": int,
    "amount_str": str,
    "amount": int,
    "program_id": str,
    "outer_program_id": str,
    "ins_index": int,
    "outer_ins_index": int,
    "event": str,
    "fee": dict
})

InstructionData = TypedDict("InstructionData", {
    "ins_index": int,
    "parsed_type": str,
    "type": str,
    "program_id": str,
    "program": str,
    "outer_program_id": str | None,
    "outer_ins_index": int,
    "data_raw": str | dict,
    "accounts": List[str],
    "activities": List[dict],
    "transfers": List[TransferInfo],
    "program_invoke_level": int
})

BalanceChange = TypedDict("BalanceChange", {
    "address": str,
    "pre_balance": str,
    "post_balance": str,
    "change_amount": str
})

TokenBalanceChange = TypedDict("TokenBalanceChange", {
    "address": str,
    "change_type": str,
    "change_amount": str,
    "decimals": int,
    "post_balance": str,
    "pre_balance": str,
    "token_address": str,
    "owner": str,
    "post_owner": str,
    "pre_owner": str
})

TransactionDetail = TypedDict("TransactionDetail", {
    "block_id": int,
    "fee": int,
    "reward": List[Any],
    "sol_bal_change": List[BalanceChange],
    "token_bal_change": List[TokenBalanceChange],
    "tokens_involved": List[str],
    "parsed_instructions": List[InstructionData],
    "programs_involved": List[str],
    "signer": List[str],
    "status": int,
    "account_keys": List[AccountKey],
    "compute_units_consumed": int,
    "confirmations": int | None,
    "version": str,
    "tx_hash": str,
    "block_time": int,
    "log_message": List[str],
    "recent_block_hash": str,
    "tx_status": str
})

TxActionData = TypedDict("TxActionData", {
    "amm_id": str,
    "amm_authority": str | None,
    "account": str,
    "token_1": str,
    "token_2": str,
    "amount_1": int,
    "amount_1_str": str,
    "amount_2": int,
    "amount_2_str": str,
    "token_decimal_1": int,
    "token_decimal_2": int,
    "token_account_1_1": str,
    "token_account_1_2": str,
    "token_account_2_1": str,
    "token_account_2_2": str,
    "owner_1": str,
    "owner_2": str
})

TxAction = TypedDict("TxAction", {
    "name": str,
    "activity_type": str,
    "program_id": str,
    "data": TxActionData,
    "ins_index": int,
    "outer_ins_index": int,
    "outer_program_id": str | None
})

TxActionTransfer = TypedDict("TxActionTransfer", {
    "source_owner": str,
    "source": str,
    "destination": str,
    "destination_owner": str,
    "transfer_type": str,
    "token_address": str,
    "decimals": int,
    "amount_str": str,
    "amount": int,
    "program_id": str,
    "outer_program_id": str,
    "ins_index": int,
    "outer_ins_index": int
})

# Update TransactionAction to match the actual response
TransactionAction = TypedDict("TransactionAction", {
    "tx_hash": str,
    "block_id": int,
    "block_time": int,
    "time": str,
    "fee": int,
    "transfers": List[TxActionTransfer],
    "activities": List[TxAction]
})

BlockDetail = TypedDict("BlockDetail", {
    "fee_rewards": int,
    "transactions_count": int,
    "current_slot": int,
    "block_height": int,
    "block_time": int,
    "time": str,
    "block_hash": str,
    "parent_slot": int,
    "previous_block_hash": str
})

PoolMarket = TypedDict("PoolMarket", {
    "pool_address": str,
    "program_id": str,
    "token1": str,
    "token1_account": str, 
    "token2": str,
    "token2_account": str,
    "total_volume_24h": int,
    "total_trade_24h": int,
    "created_time": int
})

PoolMarketInfo = TypedDict("PoolMarketInfo", {
    "pool_address": str,
    "program_id": str,
    "token1": str,
    "token2": str,
    "token1_account": str,
    "token2_account": str,
    "token1_amount": float,
    "token2_amount": float
})

PoolMarketDayVolume = TypedDict("PoolMarketDayVolume", {
    "day": int, # yyyymmdd
    "volume": float,
})

PoolMarketVolume = TypedDict("PoolMarketVolume", {
    "pool_address": str,
    "program_id": str,
    "total_volume_24h": int,
    "total_volume_change_24h": float,
    "total_trades_24h": int, 
    "total_trades_change_24h": float,
    "days": List[PoolMarketDayVolume]
})

APIUsage = TypedDict("APIUsage", {
    "remaining_cus": int,
    "usage_cus": int, 
    "total_requests_24h": int,
    "success_rate_24h": float,
    "total_cu_24h": int
})

NFTCreator = TypedDict("NFTCreator", {
    "address": str,
    "verified": int,
    "share": int
})

NFTFile = TypedDict("NFTFile", {
    "uri": str,
    "type": str
})

NFTProperties = TypedDict("NFTProperties", {
    "files": List[NFTFile],
    "category": str
})

NFTAttribute = TypedDict("NFTAttribute", {
    "trait_type": str,
    "value": str
})

NFTMetadata = TypedDict("NFTMetadata", {
    "image": str,
    "tokenId": int,
    "name": str,
    "symbol": str,
    "description": str,
    "seller_fee_basis_points": int,
    "edition": int,
    "attributes": List[NFTAttribute],
    "properties": NFTProperties,
    "retried": int
})

NFTData = TypedDict("NFTData", {
    "name": str,
    "symbol": str,
    "uri": str,
    "sellerFeeBasisPoints": int,
    "creators": List[NFTCreator],
    "id": int
})

NFTInfo = TypedDict("NFTInfo", {
    "address": str,
    "collection": str,
    "collectionId": str,
    "collectionKey": str,
    "createdTime": int,
    "data": NFTData,
    "meta": NFTMetadata,
    "mintTx": str
})

NFTActivity = TypedDict("NFTActivity", {
    "block_id": int,
    "trans_id": str, 
    "block_time": int,
    "time": str,
    "activity_type": NFTActivityType,
    "from_address": str,
    "to_address": str,
    "token_address": str,
    "marketplace_address": str,
    "collection_address": str,
    "amount": int,
    "price": int,
    "currency_token": str,
    "currency_decimals": int
})

NFTCollection = TypedDict("NFTCollection", {
    "collection_id": str,
    "name": str,
    "symbol": str,
    "floor_price": float,
    "items": int,
    "marketplaces": List[str],
    "volumes": float,
    "total_vol_prev_24h": float
})

NFTTradeInfo = TypedDict("NFTTradeInfo", {
    "trade_time": int,
    "signature": str,
    "market_id": str,
    "type": str,
    "price": str,
    "currency_token": str,
    "currency_decimals": int,
    "seller": str,
    "buyer": str
})

NFTCollectionMeta = TypedDict("NFTCollectionMeta", {
    "name": str,
    "family": str
})

NFTMetaProperties = TypedDict("NFTMetaProperties", {
    "files": List[NFTFile],
    "category": str,
    "creators": List[NFTCreator]
})

NFTItemMetadata = TypedDict("NFTItemMetadata", {
    "name": str,
    "symbol": str,
    "description": str,
    "seller_fee_basis_points": int,
    "image": str,
    "external_url": str,
    "collection": NFTCollectionMeta,
    "attributes": List[NFTAttribute],
    "properties": NFTMetaProperties
})

NFTItemData = TypedDict("NFTItemData", {
    "name": str,
    "symbol": str,
    "uri": str,
    "sellerFeeBasisPoints": int,
    "creators": List[NFTCreator],
    "id": int
})

NFTItemInfo = TypedDict("NFTItemInfo", {
    "address": str,
    "token_name": str,
    "token_symbol": str,
    "collection_id": str,
    "data": NFTItemData,
    "meta": NFTItemMetadata,
    "mint_tx": str,
    "created_time": int
})

NFTCollectionItem = TypedDict("NFTCollectionItem", {
    "tradeInfo": NFTTradeInfo,
    "info": NFTItemInfo
})

class Client:
    """A client for interacting with the Solscan API.

    The client handles authentication, rate limiting, and provides methods for accessing
    various Solscan API endpoints. It supports both encrypted and unencrypted auth tokens.

    Attributes:
        _headers (dict): HTTP headers including auth token
        _max_requests_per_minute (int): Maximum allowed API requests per minute
        _limiter (Limiter): Rate limiter to enforce request limits

    Example:
        client = Client(auth_token="your_token_here")
        # Or with a token file:
        client = Client(auth_token_file_path="path/to/token.txt")

        # Make API calls:
        account_info = await client.account_info("wallet_address")
    """
    
    def __init__(self, *, auth_token: str=None, auth_token_file_path: str=None, aes_256_hex_password: str=None, max_requests_per_minute: int=v2_max_requests_per_minute):
        """Initialize a new Solscan API client.

        Args:
            auth_token (str, optional): The authentication token string. Either this or auth_token_file_path must be provided.
            auth_token_file_path (str, optional): Path to file containing the auth token. Either this or auth_token must be provided.
            aes_256_hex_password (str, optional): 64-character hex password for decrypting an encrypted auth token. If not provided but token is encrypted, will prompt for password.
            max_requests_per_minute (int, optional): Maximum API requests allowed per minute. Defaults to v2_max_requests_per_minute.

        Raises:
            Exception: If neither auth_token nor auth_token_file_path is provided
            Exception: If aes_256_hex_password is provided but not 64 characters long
            Exception: If auth token decryption fails
        """

        if not auth_token and not auth_token_file_path:
            raise Exception("Must provide either auth_token or auth_token_file")
        if auth_token_file_path:
            with open(auth_token_file_path, "r") as f:
                auth_token = f.read()
                auth_token = auth_token.strip("\n\r\t ")
        if not aes_256_hex_password:
            aes_256_hex_password = getpass.getpass("Enter solscan auth token decryption password(if have not, just press enter): ")
        if aes_256_hex_password:
            if len(aes_256_hex_password) != 64:
                raise Exception("Hex Password must be 64 characters long")
            encrypted_bytes = base64.b64decode(auth_token.encode('utf-8'))
            iv = encrypted_bytes[:AES.block_size]
            ciphertext = encrypted_bytes[AES.block_size:]
            cipher = AES.new(bytes.fromhex(aes_256_hex_password), AES.MODE_CBC, iv)
            decrypted_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
            auth_token = decrypted_bytes.decode('utf-8')
        self._headers = {"content-type": "application/json", "token": auth_token}
        self._max_requests_per_minute = max(1, max_requests_per_minute-10)
        # self._max_requests_per_second = self._max_requests_per_minute / 60
        self._limiter = Limiter(Rate(self._max_requests_per_minute, Duration.MINUTE))

    async def get(self, base_url: str, path: str, kwargs: dict[str, Any]={}, *, export: bool = False) -> D:
        """Makes a GET request to the Solscan API.

        Args:
            base_url (str): The base URL for the API (public or pro)
            path (str): The API endpoint path
            kwargs (dict[str, Any], optional): Query parameters to include. Defaults to None.
            export (bool, optional): Whether to return raw response content. Defaults to False.

        Returns:
            D: The response data, typed according to the endpoint's return type.
            If export=True, returns the raw response content instead.

        Raises:
            Exception: If the API request fails, with status code and error message.
            - 401: Unauthorized - Invalid or missing auth token
            - 403: Forbidden - Account lacks permission 
            - 404: Not Found - Invalid endpoint or resource not found
            - 429: Too Many Requests - Rate limit exceeded
            - 500: Internal Server Error - Server-side error
        """
        url = f"{base_url}/{path.lstrip('/')}"
        kvs = []
        for key, value in kwargs.items():
            if value is None or key == "self" or key == "_must":
                continue
            elif isinstance(value, list):
                for v in value:
                    kvs.append(f"{key}[]={v}")
            elif isinstance(value, bool):
                kvs.append(f"{key}={str(value).lower()}")
            elif isinstance(value, Enum):
                kvs.append(f"{key}={value.value}")
            else:
                kvs.append(f"{key}={value}")
        if kvs:
            query_params = "&".join(kvs)
            url = f"{url}?{query_params}"
        must = kwargs.get("_must", False)
        i = 0
        while True:
            i += 1
            try:
                self._limiter.try_acquire("get")
                break
            except Exception as e:
                logger.error(f"Solscan client limiter waited {i} times: {e}")
                await asyncio.sleep(1)
        i = 0
        while True:
            i += 1
            try:
                resp = await asyncio.to_thread(requests.get, url, headers=self._headers)
                break
            except Exception as e:
                if not must:
                    raise e
                logger.error(f"Solscan client retry {i} times: {e}")
                await asyncio.sleep(1)
                if i == 60:
                    return await self.get(base_url, path, kwargs, export=export)
        if resp.status_code == 200:
            if export:
                return resp.content
            else:
                return resp.json()["data"]
        elif resp.status_code == 401:
            raise Exception("401: Unauthorized")
        elif resp.status_code == 403:
            raise Exception("403: Forbidden")
        elif resp.status_code == 404:
            raise Exception("404: Not Found")
        elif resp.status_code == 429:
            raise Exception("429: Too Many Requests")
        elif resp.status_code == 500:
            raise Exception("500: Internal Server Error")
        else:
            raise Exception(f"{resp.status_code}: {resp.text}")
        
    async def massive_get(self, tasker: Callable[[], Awaitable[D]], kwargs: dict[str, Any]) -> D:
        del kwargs["self"]
        total_size = kwargs.pop("total_size")
        page_size = kwargs["page_size"].value
        page_num = math.ceil(total_size / page_size)
        group_size = self._max_requests_per_minute
        group_num = math.ceil(page_num / group_size)
        logger.info(f"Massive getting {total_size} items, {page_size} per page, {page_num} pages, {group_size} per group, {group_num} groups, tasker: {tasker.__name__}")
        all_data = []
        for group in range(group_num):
            start_page = group * group_size + 1
            end_page = min((group + 1) * group_size, page_num)
            tasks = []
            logger.info(f"Getting group {group} from {start_page} to {end_page}")
            for page in range(start_page, end_page+1):
                tasks.append(tasker(**kwargs, page=page))
            start_time = time.time()
            results = await asyncio.gather(*tasks)
            end_time = time.time()
            duration = end_time - start_time
            has_no_more_data = False
            num_of_data = 0
            for result in results:
                if isinstance(result, tuple):
                    all_data.append(result)
                else:
                    if len(result) == 0:
                        has_no_more_data = True
                    else:
                        all_data.extend(result)
                        num_of_data += len(result)
            logger.info(f"Group {group} got {num_of_data} data")
            if group < group_num-1 and not has_no_more_data:
                logger.info(f"Sleeping {max(0.1, 60 - duration+0.1)} seconds")
                time.sleep(max(0.1, 60 - duration+0.1))
            if has_no_more_data:
                break
        return all_data[:total_size]
    
    async def test_speed(self):
        times = 10
        durations = []
        for i in range(times):
            start_time = time.time()
            await self.account_transfers("FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT")
            end_time = time.time()
            duration = end_time - start_time
            durations.append(duration)
        logger.info(f"Test speed: {sum(durations)/times} seconds, max: {max(durations)}, min: {min(durations)}, std: {statistics.stdev(durations)}")

    async def chain_info(self) -> RespData[ChainInfo]:
        return await self.get(public_base_url, "chaininfo")
    
    async def account_transfers(self,
                           address: str,
                           *,
                           activity_type: AccountActivityType = None,
                           token_account: str = None,
                           from_address: str = None,
                           to_address: str = None,
                           token: str = None,
                           amount_range: List[int] = None,
                           block_time_range: List[int] = None,
                           exclude_amount_zero: bool = False,
                           flow: Flow = None,
                           page: int = 1,
                           page_size: LargePageSize = LargePageSize.PAGE_SIZE_100,
                           sort_order: SortOrder = SortOrder.DESC,
                           _must: bool = False) -> List[Transfer]:
        """Get account transfer history.
        
        Args:
            address (str): Account address
            activity_type (AccountActivityType, optional): Filter by activity type. Defaults to None.
            token_account (str, optional): Filter by token account. Defaults to None.
            from_address (str, optional): Filter by from address. Defaults to None.
            to_address (str, optional): Filter by to address. Defaults to None.
            token (str, optional): Filter by token address. Defaults to None.
            amount_range (List[int], optional): Filter by amount range [min, max]. Defaults to None.
            block_time_range (List[int], optional): Filter by block time range [start, end]. Defaults to None.
            exclude_amount_zero (bool, optional): Whether to exclude zero amount transfers. Defaults to False.
            flow (Flow, optional): Filter by transfer direction (in/out). Defaults to None.
            page (int, optional): Page number. Defaults to 1.
            page_size (LargePageSize, optional): Number of items per page. Defaults to 10.
            sort_order (SortOrder, optional): Sort order. Defaults to DESC.

        Returns:
            List[Transfer]: List of transfers

        Example:
            >>> # Get all transfers for an account
            >>> client.account_transfers("FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT")

            >>> # Get only incoming transfers
            >>> client.account_transfers("FG4Y4yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT",
            ...                         flow=Flow.IN)

            >>> # Get transfers within a time range
            >>> client.account_transfers("FG4Y4yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT", 
            ...                         block_time_range=[1640995200, 1641081600])
        """
        args = locals()
        args["from"] = args.pop("from_address")
        args["to"] = args.pop("to_address")
        args["amount"] = args.pop("amount_range")
        args["block_time"] = args.pop("block_time_range")
        return await self.get(pro_base_url, "/account/transfer", args)

    async def massive_account_transfers(self,
                           address: str,
                           *,
                           total_size: int = LargePageSize.PAGE_SIZE_100.value,
                           activity_type: AccountActivityType = None,
                           token_account: str = None,
                           from_address: str = None,
                           to_address: str = None,
                           token: str = None,
                           amount_range: List[int] = None,
                           block_time_range: List[int] = None,
                           exclude_amount_zero: bool = False,
                           flow: Flow = None,
                           page_size: LargePageSize = LargePageSize.PAGE_SIZE_100,
                           sort_order: SortOrder = SortOrder.DESC,
                           _must: bool = True) -> List[Transfer]:
        return await self.massive_get(self.account_transfers, locals())
    
    async def account_token_accounts(self,
                       address: str,
                           *,
                       type: TokenType = TokenType.TOKEN,
                       page: int = 1,
                       page_size: SmallPageSize = SmallPageSize.PAGE_SIZE_40,
                       hide_zero: bool = False,
                       _must: bool = False) -> List[TokenAccount]:
        return await self.get(pro_base_url, "/account/token-accounts", locals())

    async def massive_account_token_accounts(self,
                       address: str,
                           *,
                       total_size: int = SmallPageSize.PAGE_SIZE_40.value,
                       type: TokenType = TokenType.TOKEN,
                       page_size: SmallPageSize = SmallPageSize.PAGE_SIZE_40,
                       hide_zero: bool = False,
                       _must: bool = True) -> List[TokenAccount]:
        return await self.massive_get(self.account_token_accounts, locals())
    
    async def account_defi_activities(self,
                        address: str,
                           *,
                        activity_type: ActivityType = None,
                        from_address: str = None,
                        platform: List[str] = None,
                        source: List[str] = None,
                        token: str = None,
                        block_time_range: List[int] = None,
                        page: int = 1,
                        page_size: SmallPageSize = SmallPageSize.PAGE_SIZE_40,
                        sort_by: SortBy = SortBy.BLOCK_TIME,
                        sort_order: SortOrder = SortOrder.DESC,
                        _must: bool = False) -> List[DefiActivity]:
        """Get DeFi activities for an account.

        Args:
            address (str): Account address
            activity_type (ActivityType, optional): Filter by activity type. Defaults to None.
            from_address (str, optional): Filter by from address. Defaults to None.
            platform (List[str], optional): Filter by platform names. Defaults to None.
            source (List[str], optional): Filter by source names. Defaults to None.
            token (str, optional): Filter by token address. Defaults to None.
            block_time_range (List[int], optional): Filter by block time range [start, end]. Defaults to None.
            page (int, optional): Page number. Defaults to 1.
            page_size (SmallPageSize, optional): Number of items per page. Defaults to 10.
            sort_by (SortBy, optional): Sort field. Defaults to block_time.
            sort_order (SortOrder, optional): Sort order. Defaults to DESC.

        Returns:
            List[DefiActivity]: List of DeFi activities

        Example:
            >>> # Get all DeFi activities for an account
            >>> client.account_defi_activities("FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT")

            >>> # Get swap activities only
            >>> client.account_defi_activities("FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT",
            ...                               activity_type=ActivityType.ACCOUNT_ACTIVITY_SWAP)

            >>> # Get activities within a time range
            >>> client.account_defi_activities("FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT",
            ...                               block_time_range=[1640995200, 1641081600])
        """
        args = locals()
        args["from"] = args.pop("from_address")
        args["block_time"] = args.pop("block_time_range")
        return await self.get(pro_base_url, "/account/defi/activities", args)

    async def massive_account_defi_activities(self,
                        address: str,
                           *,
                        total_size: int = SmallPageSize.PAGE_SIZE_40.value,
                        activity_type: ActivityType = None,
                        from_address: str = None,
                        platform: List[str] = None,
                        source: List[str] = None,
                        token: str = None,
                        block_time_range: List[int] = None,
                        page_size: SmallPageSize = SmallPageSize.PAGE_SIZE_40,
                        sort_by: SortBy = SortBy.BLOCK_TIME,
                        sort_order: SortOrder = SortOrder.DESC,
                        _must: bool = True) -> List[DefiActivity]:
        return await self.massive_get(self.account_defi_activities, locals())
    
    async def account_balance_changes(self,
                        address: str,
                           *,
                        token: str = None,
                        amount_range: List[int] = None,
                        block_time_range: List[int] = None,
                        page: int = 1,
                        page_size: LargePageSize = LargePageSize.PAGE_SIZE_100,
                        remove_spam: bool = True,
                        flow: Flow = None,
                        sort_by: SortBy = SortBy.BLOCK_TIME,
                        sort_order: SortOrder = SortOrder.DESC,
                        _must: bool = False) -> List[AccountChangeActivity]:
        """Get balance change activities for an account.

        Args:
            address (str): Account address
            token (str, optional): Filter by token address. Defaults to None.
            amount_range (List[int], optional): Filter by amount range [min, max]. Defaults to None.
            block_time_range (List[int], optional): Filter by block time range [start, end]. Defaults to None.
            page (int, optional): Page number. Defaults to 1.
            page_size (LargePageSize, optional): Number of items per page. Defaults to 10.
            remove_spam (bool, optional): Whether to remove spam transactions. Defaults to True.
            flow (Flow, optional): Filter by flow direction (in/out). Defaults to None.
            sort_by (SortBy, optional): Sort field. Defaults to block_time.
            sort_order (SortOrder, optional): Sort order. Defaults to DESC.

        Returns:
            List[AccountChangeActivity]: List of balance change activities

        Example:
            >>> # Get all balance changes for an account
            >>> client.account_balance_changes("FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT")

            >>> # Get changes for a specific token
            >>> client.account_balance_changes("FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT",
            ...                               token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")

            >>> # Get changes within an amount range
            >>> client.account_balance_changes("FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT",
            ...                               amount_range=[1000000, 10000000])
        """
        args = locals()
        args["amount"] = args.pop("amount_range")
        args["block_time"] = args.pop("block_time_range")
        return await self.get(pro_base_url, "/account/balance_change", args)

    async def massive_account_balance_changes(self,
                        address: str,
                           *,
                        total_size: int = LargePageSize.PAGE_SIZE_100.value,
                        token: str = None,
                        amount_range: List[int] = None,
                        block_time_range: List[int] = None,
                        page_size: LargePageSize = LargePageSize.PAGE_SIZE_100,
                        remove_spam: bool = True,
                        flow: Flow = None,
                        sort_by: SortBy = SortBy.BLOCK_TIME,
                        sort_order: SortOrder = SortOrder.DESC,
                        _must: bool = True) -> List[AccountChangeActivity]:
        return await self.massive_get(self.account_balance_changes, locals())
    
    async def account_transactions(self, address: str, *,before: str = None, limit: SmallPageSize=SmallPageSize.PAGE_SIZE_40, _must: bool = False) -> List[Transaction]:
        return await self.get(pro_base_url, "/account/transactions", locals())
    
    async def massive_account_transactions(self, address: str, *, total_size: int = SmallPageSize.PAGE_SIZE_40.value, before: str = None, limit: SmallPageSize=SmallPageSize.PAGE_SIZE_40, _must: bool = True) -> List[Transaction]:
        trans = []
        page_num = math.ceil(total_size / limit.value)
        for i in range(page_num):
            new_trans = await self.account_transactions(address, before=before, limit=limit, _must=_must)
            if not new_trans:
                break
            trans.extend(new_trans)
            before = new_trans[-1]["tx_hash"]
        return trans[:total_size]
    
    async def account_stakes(self, address: str, *, page: int = 1, page_size: SmallPageSize = SmallPageSize.PAGE_SIZE_40) -> List[AccountStake]:
        return await self.get(pro_base_url, "/account/stake", locals())
    
    async def account_detail(self, address: str) -> AccountDetail:
        return await self.get(pro_base_url, "/account/detail", locals())
    
    async def account_rewards_export(self, address:str, *, time_from:int, time_to:int) -> bytes:
        return await self.get(pro_base_url, "/account/reward/export", locals(), export=True)
                             
    async def account_transfer_export(self, 
                                address:str,
                                *,
                                activity_type:AccountActivityType = None,
                                token_account:str = None,
                                from_address:str = None,
                                to_address:str = None,
                                token:str = None,
                                amount_range:List[int] = None,
                                block_time_range:List[int] = None,
                                exclude_amount_zero:bool=False,
                                flow: Flow = None) -> bytes:
        """Export account transfer history to CSV.
        
        Args:
            address (str): Account address to get transfers for
            activity_type (AccountActivityType, optional): Filter by activity type. Defaults to None.
            token_account (str, optional): Filter by token account. Defaults to None.
            from_address (str, optional): Filter by sender address. Defaults to None.
            to_address (str, optional): Filter by recipient address. Defaults to None.
            token (str, optional): Filter by token mint address. Defaults to None.
            amount_range (List[int], optional): Filter by amount range [min, max]. Defaults to None.
            block_time_range (List[int], optional): Filter by block time range [start, end]. Defaults to None.
            exclude_amount_zero (bool, optional): Whether to exclude zero amount transfers. Defaults to False.
            flow (Flow, optional): Filter by flow direction (in/out). Defaults to None.

        Returns:
            bytes: CSV file content as bytes

        Example:
            >>> # Export all transfers for an account
            >>> csv_data = client.account_transfer_export("FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT")
            >>> with open("transfers.csv", "wb") as f:
            ...     f.write(csv_data)

            >>> # Export filtered transfers
            >>> csv_data = client.account_transfer_export(
            ...     "FG4Y3yX4AAchp1HvNZ7LfzFTewF2f6nDoMDCohTFrdpT",
            ...     activity_type=AccountActivityType.TRANSFER,
            ...     token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            ...     amount_range=[1000000, 10000000]
            ... )
        """
        args = locals()
        args["amount"] = args.pop("amount_range")
        args["block_time"] = args.pop("block_time_range")
        return await self.get(pro_base_url, "/account/transfer/export", args, export=True)
    
    async def token_transfers(self,
                       address:str,
                              *,
                       activity_type:ActivityType = None,
                       from_address:str = None,
                       to_address:str = None,
                       amount_range:List[int] = None,
                       block_time_range:List[int] = None,
                       exclude_amount_zero:bool=False,
                       page:int = 1,
                       page_size:LargePageSize = LargePageSize.PAGE_SIZE_100,
                       sort_by:SortBy = SortBy.BLOCK_TIME,
                       sort_order:SortOrder = SortOrder.DESC,
                       _must: bool=False) -> List[Transfer]:
        """Get token transfer history.
        If want to get massive data, use massive_token_transfers instead.
        
        Args:
            address (str): Token address to get transfers for
            activity_type (ActivityType, optional): Filter by activity type. Defaults to None.
            from_address (str, optional): Filter by sender address. Defaults to None.
            to_address (str, optional): Filter by recipient address. Defaults to None.
            amount_range (List[int], optional): Filter by amount range [min, max]. Defaults to None.
            block_time_range (List[int], optional): Filter by block time range [start, end]. Defaults to None.
            exclude_amount_zero (bool, optional): Whether to exclude zero amount transfers. Defaults to False.
            page (int, optional): Page number. Defaults to 1.
            page_size (LargePageSize, optional): Number of results per page. Defaults to 10.
            sort_by (SortBy, optional): Field to sort by. Defaults to block_time.
            sort_order (SortOrder, optional): Sort order (asc/desc). Defaults to DESC.
            _must (bool, optional): Whether to use must_get. Defaults to False.

        Returns:
            List[Transfer]: List of token transfers

        Example:
            >>> # Get all transfers for a token
            >>> transfers = client.token_trasfers("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
            >>> for transfer in transfers:
            ...     print(f"{transfer['from_address']} -> {transfer['to_address']}: {transfer['amount']}")

            >>> # Get filtered transfers
            >>> transfers = client.token_trasfers(
            ...     "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            ...     activity_type=ActivityType.TOKEN_ACTIVITY_TRANSFER,
            ...     amount_range=[1000000, 10000000],
            ...     page_size=LargePageSize.PAGE_SIZE_100
            ... )
        """
        args = locals()
        args["from"] = args.pop("from_address")
        args["to"] = args.pop("to_address")
        args["amount"] = args.pop("amount_range")
        args["block_time"] = args.pop("block_time_range")
        return await self.get(pro_base_url, "/token/transfer", args)
    
    async def massive_token_transfers(self,
                       address:str,
                       *,
                       total_size: int = LargePageSize.PAGE_SIZE_100.value,
                       activity_type:ActivityType = None,
                       from_address:str = None,
                       to_address:str = None,
                       amount_range:List[int] = None,
                       block_time_range:List[int] = None,
                       exclude_amount_zero:bool=False,
                       page_size:LargePageSize = LargePageSize.PAGE_SIZE_100,
                       sort_by:SortBy = SortBy.BLOCK_TIME,
                       sort_order:SortOrder = SortOrder.DESC,
                       _must: bool=True) -> List[Transfer]:
        return await self.massive_get(self.token_transfers, locals())  

    async def token_defi_activities(self,
                             address:str,
                                    *,
                             from_address:str = None,
                             platform:List[str] = None,
                             source:List[str] = None,
                             activity_type:ActivityType = None,
                             token:str = None,
                             block_time_range:List[int] = None,
                             page:int = 1,
                             page_size:LargePageSize = LargePageSize.PAGE_SIZE_100,
                             sort_by:SortBy = SortBy.BLOCK_TIME,
                             sort_order:SortOrder = SortOrder.DESC,
                             _must: bool=False) -> List[DefiActivity]:
        """Get DeFi activities for a token.
        
        If want to get massive data, use massive_token_defi_activities instead.

        Args:
            address (str): Token address to get activities for
            from_address (str, optional): Filter by sender address. Defaults to None.
            platform (List[str], optional): Filter by platform names. Defaults to None.
            source (List[str], optional): Filter by source names. Defaults to None.
            activity_type (ActivityType, optional): Filter by activity type. Defaults to None.
            token (str, optional): Filter by token address. Defaults to None.
            block_time_range (List[int], optional): Filter by block time range [start, end]. Defaults to None.
            page (int, optional): Page number. Defaults to 1.
            page_size (LargePageSize, optional): Number of results per page. Defaults to 10.
            sort_by (SortBy, optional): Field to sort by. Defaults to block_time.
            sort_order (SortOrder, optional): Sort order (asc/desc). Defaults to DESC.
            _must (bool, optional): Whether to use must_get. Defaults to False.

        Returns:
            List[DefiActivity]: List of DeFi activities

        Example:
            >>> # Get all DeFi activities for a token
            >>> activities = client.token_defi_activities("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
            >>> for activity in activities:
            ...     print(f"{activity['activity_type']}: {activity['amount_info']}")

            >>> # Get filtered activities
            >>> activities = client.token_defi_activities(
            ...     "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            ...     platform=["Raydium"],
            ...     activity_type=ActivityType.ACCOUNT_ACTIVITY_SWAP,
            ...     page_size=LargePageSize.PAGE_SIZE_100
            ... )
        """
        args = locals()
        args["from"] = args.pop("from_address")
        args["block_time"] = args.pop("block_time_range")
        return await self.get(pro_base_url, "/token/defi/activities", args)
    
    async def massive_token_defi_activities(self,
                             address:str,
                             *,
                             total_size: int = LargePageSize.PAGE_SIZE_100.value,
                             from_address:str = None,
                             platform:List[str] = None,
                             source:List[str] = None,
                             activity_type:ActivityType = None,
                             token:str = None,
                             block_time_range:List[int] = None,
                             page_size:LargePageSize = LargePageSize.PAGE_SIZE_100,
                             sort_by:SortBy = SortBy.BLOCK_TIME,
                             sort_order:SortOrder = SortOrder.DESC,
                             _must: bool=True) -> List[DefiActivity]:
        return await self.massive_get(self.token_defi_activities, locals())
    
    async def token_markets(self,
                      token_pair:List[str],
                      *,
                      sort_by:MarketSortBy = MarketSortBy.VOLUME,
                      program:str = None,
                      page:int = 1,
                      page_size:LargePageSize = LargePageSize.PAGE_SIZE_100) -> List[Market]:
        args = locals()
        args["token"] = args.pop("token_pair")
        return await self.get(pro_base_url, "/token/markets", args)

    async def token_list(self,
                   *,
                   sort_by:TokenSortBy = TokenSortBy.PRICE,
                   sort_order:SortOrder = SortOrder.DESC,
                   page:int = 1,
                   page_size:LargePageSize = LargePageSize.PAGE_SIZE_100,
                   _must: bool=False) -> List[Token]:
        return await self.get(pro_base_url, "/token/list", locals())
    
    async def massive_token_list(self, *, total_size: int = LargePageSize.PAGE_SIZE_100.value, sort_by:TokenSortBy = TokenSortBy.PRICE, 
                                 sort_order:SortOrder = SortOrder.DESC, page_size:LargePageSize = LargePageSize.PAGE_SIZE_100, _must: bool=True) -> List[Token]:
        return await self.massive_get(self.token_list, locals())
    
    async def token_trending(self, *, limit:int = 10) -> List[Token]:
        return await self.get(pro_base_url, "/token/trending", locals())

    async def token_price(self, address: str, *, time_range: List[int] = None) -> List[TokenPrice]:
        """Get token price history.
        
        Args:
            address (str): Token address
            time_range (List[int], optional): Time range in yyyymmdd. Defaults to None.
                If provided, must be a list of 2 yyyymmdd [start_time, end_time].
                
        Returns:
            List[TokenPrice]: List of token prices with dates
            
        Example:
            >>> client.token_price("HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC")
            return real-time price

            >>> # Get prices between Jan 1 2022 and Jan 7 2022
            >>> client.token_price("HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC", 
            ...                   [20250101, 20250102])
            [{'date': 20250101, 'price': 2.1796472}, {'date': 20250102, 'price': 2.34}]
        """
        args = locals()
        args["time"] = args.pop("time_range")
        return await self.get(pro_base_url, "/token/price", args)
    
    async def token_holders(self,
                        address: str,
                        *,
                        page: int = 1,
                        page_size: SmallPageSize = SmallPageSize.PAGE_SIZE_40,
                        from_amount: str=None,
                        to_amount: str=None,
                        _must: bool=False) -> tuple[int, List[TokenHolder]]:
        data = await self.get(pro_base_url, "/token/holders", locals())
        return data["total"], data["items"]
    
    async def massive_token_holders(self,
                             address: str,
                             *,
                             total_size: int = SmallPageSize.PAGE_SIZE_40.value,
                             from_amount: str=None,
                             to_amount: str=None,
                             page_size:SmallPageSize = SmallPageSize.PAGE_SIZE_40,
                             _must: bool=True) -> tuple[int, List[TokenHolder]]:
        args = locals()
        num = 0
        holders = []
        for h in await self.massive_get(self.token_holders, args):
            holders.extend(h[1])
            num = h[0]
        return num, holders[:total_size]
    
    async def token_meta(self, address: str) -> TokenMeta:
        return await self.get(pro_base_url, "/token/meta", locals())
    
    async def token_top(self, *, limit:int = 10) -> List[TokenTop]:
        return await self.get(pro_base_url, "/token/top", locals())
    
    async def tx_last(self, *, limit: LargePageSize = LargePageSize.PAGE_SIZE_100, filter: TxFilter = TxFilter.ALL) -> List[Transaction]:
        return await self.get(pro_base_url, "/transaction/last", locals())

    async def tx_detail(self, tx: str) -> TransactionDetail:
        return await self.get(pro_base_url, "/transaction/detail", locals())
    
    async def tx_actions(self, tx: str) -> TransactionAction:
        return await self.get(pro_base_url, "/transaction/actions", locals())

    async def block_last(self, *, limit: LargePageSize=LargePageSize.PAGE_SIZE_100) -> BlockDetail:
        return await self.get(pro_base_url, "/block/last", locals())

    async def block_transactions(self, block: int, *, page: int = 1, page_size: LargePageSize = LargePageSize.PAGE_SIZE_100) -> tuple[int, List[Transaction]]:
        data = await self.get(pro_base_url, "/block/transactions", locals())
        return data["total"], data["transactions"]

    async def block_detail(self, block: int) -> BlockDetail:
        return await self.get(pro_base_url, "/block/detail", locals())
    
    async def pool_market_list(self,
                         *,
                         sort_by: str = "created_time",
                         sort_order: SortOrder = SortOrder.DESC,
                         page: int = 1,
                         page_size: LargePageSize = LargePageSize.PAGE_SIZE_100, 
                         program: str = None,
                         ) -> List[PoolMarket]:
        return await self.get(pro_base_url, "/market/list", locals())
    
    async def pool_market_info(self, address: str) -> PoolMarketInfo:
        return await self.get(pro_base_url, "/market/info", locals())
    
    async def pool_market_volume(self, address: str, *, time_range: List[int] = None) -> PoolMarketVolume:
        args = locals()
        args["time"] = args.pop("time_range")
        return await self.get(pro_base_url, "/market/volume", args)

    async def api_usage(self) -> APIUsage:
        return await self.get(pro_base_url, "/monitor/usage", locals())

    async def news_nft(self, *, filter: str = "created_time", page: int = 1, page_size: TinyPageSize = TinyPageSize.PAGE_SIZE_36) -> List[NFTInfo]:
        return await self.get(pro_base_url, "/nft/news", locals())
    
    async def nft_activity(self,
                          *,
                    from_address: str = None,
                    to_address: str = None,
                    source: List[str] = None,
                    activity_type: NFTActivityType = None,
                    token: str = None,
                    collection: str = None,
                    currency_token: str = None,
                    price_range: List[float] = None,
                    block_time_range: List[int] = None,
                    page: int = 1,
                    page_size: LargePageSize = LargePageSize.PAGE_SIZE_100) -> List[NFTActivity]:
        """Get NFT activity history.
        
        Args:
            from_address (str, optional): Filter by sender address. Defaults to None.
            to_address (str, optional): Filter by recipient address. Defaults to None.
            source (List[str], optional): Filter by marketplace source. Defaults to None.
            activity_type (NFTActivityType, optional): Filter by activity type. Defaults to None.
            token (str, optional): Filter by NFT token address. Defaults to None.
            collection (str, optional): Filter by collection address. Defaults to None.
            currency_token (str, optional): Filter by currency token address. Defaults to None.
            price_range (List[float], optional): Filter by price range [min, max]. Defaults to None.
            block_time_range (List[int], optional): Filter by block time range [start, end]. Defaults to None.
            page (int, optional): Page number. Defaults to 1.
            page_size (LargePageSize, optional): Number of results per page. Defaults to 100.

        Returns:
            List[NFTActivity]: List of NFT activities

        Example:
            >>> # Get all NFT activities
            >>> client.nft_activity()

            >>> # Get activities for a specific collection
            >>> client.nft_activity(
            ...     collection="fc8dd31116b25e6690d83f6fb102e67ac6a9364dc2b96285d636aed462c4a983",
            ...     activity_type=NFTActivityType.SOLD
            ... )

            >>> # Get activities within a price range
            >>> client.nft_activity(price_range=[1.5, 10.0])
        """
        args = locals()
        args["from"] = args.pop("from_address")
        args["to"] = args.pop("to_address")
        args["price"] = args.pop("price_range")
        args["block_time"] = args.pop("block_time_range")
        return await self.get(pro_base_url, "/nft/activity", locals())

    async def nft_collection_list(self,
                             *,
                             sort_by: NFTCollectionSortBy = NFTCollectionSortBy.FLOOR_PRICE,
                             sort_order: SortOrder = SortOrder.DESC,
                             page: int = 1,
                             page_size: SmallPageSize = SmallPageSize.PAGE_SIZE_40,
                             collection: str = None,
                             ) -> List[NFTCollection]:
        return await self.get(pro_base_url, "/nft/collection/lists", locals())
    
    async def nft_collection_items(self,
                             collection: str,
                             *,
                             sort_by: NFTCollectionItemSortBy = NFTCollectionItemSortBy.LAST_TRADE,
                             page: int = 1,
                             page_size: TinyPageSize = TinyPageSize.PAGE_SIZE_36,
                             ) -> List[NFTCollectionItem]:
        return await self.get(pro_base_url, "/nft/collection/items", locals())
    

if __name__ == "__main__":
    import os
    import pathlib
    token = "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
    account = "1HBjhkQvVzNpLyp8REVjZTQ5NCR2qtMgiMNa2ViSA98"
    home = str(pathlib.Path.home())
    token_file = os.path.join(home, "test_tokens/solscan_auth_token_unencrypted")
    client = Client(auth_token_file_path=token_file)
    data = asyncio.run(client.test_speed())
