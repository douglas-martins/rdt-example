from machine_states import FSM
from rdt_packet import RdtPacket
from utils import ones_complement, check_sum, validate_pkt
from sender import SenderClass


class ReceiverClass:

    def __init__(self, rcv_pkt: RdtPacket):
        self.state = FSM.STATE_ONE
        self.seq_num = 0
        self.pkt = rcv_pkt
        self.send_ack = RdtPacket

    def make_pkt(self, is_ack: str):
        self.send_ack = RdtPacket(
            sequence_number=self.seq_num,
            ack_num=0,
            check_sum=ones_complement(check_sum(list(is_ack))),
            payload=list(is_ack)
        )

    def finite_machine(self):
        if self.state == FSM.STATE_ONE:
            if validate_pkt(self.pkt):
                is_ack = 'ACK'
                if self.pkt.get_ack_num() == 0:
                    self.state = FSM.STATE_TWO
            else:
                is_ack = 'NACK'

            self.make_pkt(is_ack)
            print(self.state)
        elif self.state == FSM.STATE_TWO:
            if validate_pkt(self.pkt):
                is_ack = 'ACK'
                if self.pkt.get_ack_num() == 1:
                    self.state = FSM.STATE_ONE
            else:
                is_ack = 'NACK'

            self.make_pkt(is_ack)
            print(self.state)
        else:
            print("RESET")


send = SenderClass("Mensage completa da Alice para o Bob")
send.make_pkt()
receiver = ReceiverClass(send.last_pkt)
