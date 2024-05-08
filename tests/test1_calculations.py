    
from app.calculations import add,sub,mul,div,BankAccount,InsufficientFunds
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("a, b, expected",
                         [(3,2,5),
                         (7,1,8),
                         (4,4,8)]
                         )
def test_add(a,b,expected):
    assert add(a,b) == expected


def test_sub():
 
    assert sub(5,3) == 2


def test_mul():
    assert mul(5,3) == 15


def test_div():

    assert div(6,3) == 2



def test_bank_init_amt(bank_account):
    assert bank_account.balance == 50


def test_bank_def_amt(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_withdraw(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect_int(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,3) == 55


@pytest.mark.parametrize("dep, wit, expected",
                         [(200,100,100),
                         (50,10,40),
                         (400,140,260)]
                    
                         )



def test_bank_trans(zero_bank_account,dep,wit,expected):
    zero_bank_account.deposit(dep)
    zero_bank_account.withdraw(wit)
    assert zero_bank_account.balance == expected

 
def test_insuf_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(50)