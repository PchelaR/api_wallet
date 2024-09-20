from fastapi import APIRouter
from handlers import create_wallet, get_wallet_balance, update_wallet

router = APIRouter()

router.add_api_route("/wallets", create_wallet, methods=["POST"])
router.add_api_route("/wallets/{wallet_uuid}", get_wallet_balance, methods=["GET"])
router.add_api_route("/wallets/{wallet_uuid}/operation", update_wallet, methods=["POST"])
