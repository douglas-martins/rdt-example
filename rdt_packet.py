from typing import List


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

    def get_sequence_number(self):
        return self.sequence_number

    def get_ack_num(self):
        return self.ack_num

    def get_check_sum(self):
        return self.check_sum

    def get_payload(self):
        return self.payload

    def set_sequence_number(self, sequence_number):
        self.sequence_number = sequence_number

    def set_ack_num(self, ack_num):
        self.ack_num = ack_num

    def set_check_sum(self, check_sum):
        self.check_sum = check_sum

    def set_payload(self, payload):
        self.payload = payload

    def __str__(self):
        return f"RdtPacket:[sequence_number:{self.sequence_number}, ack_num:{self.ack_num}, check_sum:{self.check_sum}," \
               f" payload:{self.payload}] "
