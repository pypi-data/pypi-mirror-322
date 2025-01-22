import typing as t
from tons.tonsdk.boc import Cell
from tons.tonsdk.contract.wallet import WalletContract


class WalletV1ContractBase(WalletContract):
    def create_signing_message(self, seqno=None, valid_until: t.Optional[int] = None):
        seqno = seqno or 0
        cell = Cell()
        cell.bits.write_uint(seqno, 32)
        return cell

class WalletV1ContractR3(WalletV1ContractBase):
    def __init__(self, **kwargs) -> None:
        self.code = "B5EE9C7241010101005F0000BAFF0020DD2082014C97BA218201339CBAB19C71B0ED44D0D31FD70BFFE304E0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54B5B86E42"
        kwargs["code"] = Cell.one_from_boc(self.code)
        super().__init__(**kwargs)