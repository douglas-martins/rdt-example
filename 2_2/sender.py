from machine_states import FSM
from rdt_packet import RdtPacket
from utils import ones_complement, check_sum, validate_pkt
from typing import List


class SenderClass:

    def __init__(self, data):
        self.state = FSM.STATE_ONE
        self.data = data
        self.last_pkt = RdtPacket
        self.rcv_pkt = RdtPacket
        self.seq_num = 0

    def make_pkt(self):
        payload = self.__get_five_characters__()
        self.last_pkt = RdtPacket(
            sequence_number=self.seq_num,
            ack_num=0,
            check_sum=ones_complement(check_sum(payload)),
            payload=list(payload)
        )
        self.seq_num += 1

    def send_pkt(self):
        print("---- ENVIANDO PACOTE ----")
        return self.last_pkt

    def __get_five_characters__(self) -> List[str]:
        payload = self.data[:5]
        self.data = self.data[5:]
        return payload

    def validate_ack(self, ack_num):
        return ''.join(self.rcv_pkt.get_payload()) == 'ack' and self.rcv_pkt.get_ack_num() == ack_num

    def finite_machine(self):
        if self.state == FSM.STATE_ONE:
            self.make_pkt()
            print('---- ack 0 ----')
            self.state = FSM.STATE_TWO
            return self.send_pkt()

        elif self.state == FSM.STATE_TWO:
            is_corrupted = not validate_pkt(self.rcv_pkt)

            if is_corrupted or self.validate_ack(1):
                return self.send_pkt()
            elif not is_corrupted and self.validate_ack(0):
                self.state = FSM.STATE_THREE

            return self.last_pkt

        elif self.state == FSM.STATE_THREE:
            print('---- ack 1 ----')
            self.last_pkt.set_ack_num(ack_num=1)
            self.state = FSM.STATE_FOR
            return self.send_pkt()

        elif self.state == FSM.STATE_FOR:
            is_corrupted = not validate_pkt(self.rcv_pkt)

            if is_corrupted or self.validate_ack(0):
                return self.send_pkt()
            elif not is_corrupted and self.validate_ack(1):
                self.state = FSM.STATE_ONE

            return self.last_pkt

    def report(self):
        print("---- sender ----")
        print("Estado atual: " + str(self.state))
        print("Pacote de envio: " + str(self.last_pkt))
        print("------------------")

    def set_rcv_pkt(self, rcv_pkt: RdtPacket):
        self.rcv_pkt = rcv_pkt
