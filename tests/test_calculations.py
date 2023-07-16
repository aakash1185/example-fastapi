import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def regular_bank_account():
    return BankAccount(50)



@pytest.mark.parametrize("num1, num2, expected", [(3,2,5), (7,1,8), (12,4,16)])
def test_add(num1, num2, expected):
    assert add(num1,num2) == expected

def test_subtract():
    assert subtract(5,3) == 2

def test_multiply():
    assert multiply(5,3) == 15

def test_divide():
    assert divide(20,5) == 4

def test_bank_set_initial_amount(regular_bank_account):    
    assert regular_bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw_amount(regular_bank_account):
    regular_bank_account.withdraw(20)
    assert regular_bank_account.balance == 30

def test_bank_deposit_amount(regular_bank_account):
    regular_bank_account.deposit(30)
    assert regular_bank_account.balance == 80

def test_bank_collect_interest(regular_bank_account):
    regular_bank_account.collect_interest()
    assert round(regular_bank_account.balance, 5) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200,100,100),
    (1500,750,750),
    (100,20, 80)
    ])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(regular_bank_account):
    with pytest.raises(InsufficientFunds):
        regular_bank_account.withdraw(200)