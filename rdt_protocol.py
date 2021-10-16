import dataclasses
from typing import List


@dataclasses
class RdtPacket:
    sequence_number: int
    ack_num: int
    check_sum: int
    payload: List[str]

    def __init__(self, sequence_number: int, ack_num: int, check_sum: int, payload: List[str]):
        self.sequence_number = sequence_number
        self.ack_num = ack_num
        self.check_sum = check_sum
        self.payload = payload
