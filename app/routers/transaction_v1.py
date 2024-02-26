from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from sharingiscaring.tooter import Tooter, TooterType, TooterChannel  # noqa
from sharingiscaring.mongodb import (
    MongoDB,
    Collections,
)
from sharingiscaring.GRPCClient.CCD_Types import CCD_BlockItemSummary
from app.state.state import get_mongo_db

router = APIRouter()


@router.get("/{net}/transaction/{tx_hash}", response_class=JSONResponse)
async def get_transaction(
    request: Request,
    net: str,
    tx_hash: str,
    mongodb: MongoDB = Depends(get_mongo_db),
):
    """
    Endpoint to get a transaction as stored in MongoDB collection `transactions`.


    """
    db_to_use = mongodb.testnet if net == "testnet" else mongodb.mainnet
    result = db_to_use[Collections.transactions].find_one(tx_hash)
    if result:
        result = CCD_BlockItemSummary(**result)
        return result.model_dump_json(exclude_none=True)
    else:
        return {"request": tx_hash, "response": 404}
