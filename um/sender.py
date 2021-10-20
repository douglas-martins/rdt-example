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
        print("## Enviando pacote ##")
        print(self.last_pkt)
        print("#####################")
        return self.last_pkt

    def __get_five_characters__(self) -> List[str]:
        payload = self.data[:5]
        self.data = self.data[5:]
        return payload

    def finite_machine(self):
        if self.state == FSM.STATE_ONE:
            self.make_pkt()
            self.state = FSM.STATE_TWO
            return self.send_pkt()

        elif self.state == FSM.STATE_TWO:
            if not validate_pkt(self.rcv_pkt) or ''.join(self.rcv_pkt.get_payload()) == 'nack':
                return self.send_pkt()
            else:
                self.state = FSM.STATE_THREE

            return None

        elif self.state == FSM.STATE_THREE:
            self.last_pkt.set_ack_num(ack_num=1)
            self.state = FSM.STATE_FOR
            return self.send_pkt()

        elif self.state == FSM.STATE_FOR:
            if not validate_pkt(self.rcv_pkt) or ''.join(self.rcv_pkt.get_payload()) == 'nack':
                return self.send_pkt()
            else:
                self.state = FSM.STATE_ONE
            return None

    def set_rcv_pkt(self, rcv_pkt: RdtPacket):
        self.rcv_pkt = rcv_pkt
