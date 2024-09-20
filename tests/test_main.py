import pytest
import httpx
import asyncio
from schemas import WalletOperation

async def get_wallet_balance(wallet_uuid):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/wallets/{wallet_uuid}")
        response.raise_for_status()
        return response.json()

async def create_wallet():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/wallets")
        response.raise_for_status()
        return response.json()

async def update_wallet(wallet_uuid: str, operation: WalletOperation):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8000/wallets/{wallet_uuid}/operation", json=operation)
        response.raise_for_status()
        return response.json()

@pytest.mark.asyncio
async def test_create_wallet():
    wallet = await create_wallet()
    assert 'uuid' in wallet
    assert wallet['balance'] == 0
    print("Тест создания кошелька")

@pytest.mark.asyncio
async def test_get_wallet_balance():
    wallet = await create_wallet()
    wallet_uuid = wallet['uuid']
    balance = await get_wallet_balance(wallet_uuid)
    assert balance['uuid'] == wallet_uuid
    assert balance['balance'] == 0
    print("Тест получения баланса кошелька")

@pytest.mark.asyncio
async def test_update_wallet_deposit():
    wallet = await create_wallet()
    wallet_uuid = wallet['uuid']
    operation = {"operation": "DEPOSIT", "amount": 100}
    updated_balance = await update_wallet(wallet_uuid, operation)
    assert updated_balance['balance'] == 100
    print("Тест пополнения кошелька")

@pytest.mark.asyncio
async def test_update_wallet_withdraw():
    wallet = await create_wallet()
    wallet_uuid = wallet['uuid']
    await update_wallet(wallet_uuid, {"operation": "DEPOSIT", "amount": 100})
    operation = {"operation": "WITHDRAW", "amount": 50}
    updated_balance = await update_wallet(wallet_uuid, operation)
    assert updated_balance['balance'] == 50
    print("Тест снятия средств с кошелька")

@pytest.mark.asyncio
async def test_update_wallet_withdraw_insufficient_funds():
    wallet = await create_wallet()
    wallet_uuid = wallet['uuid']
    operation = {"operation": "WITHDRAW", "amount": 50}
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await update_wallet(wallet_uuid, operation)
    assert exc_info.value.response.status_code == 400
    print("Тест снятия средств при недостатке средств")

async def load_test(total_requests):
    wallets = await asyncio.gather(*(create_wallet() for _ in range(total_requests)))
    for wallet in wallets:
        wallet_uuid = wallet['uuid']
        await update_wallet(wallet_uuid, {"operation": "DEPOSIT", "amount": 100})
        await update_wallet(wallet_uuid, {"operation": "WITHDRAW", "amount": 50})

@pytest.mark.asyncio
async def test_load():
    total_requests = 1000
    await load_test(total_requests)
    print(f"Нагрузочный тест на {total_requests} запросов")