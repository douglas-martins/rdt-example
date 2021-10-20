from machine_states import FSM
from rdt_packet import RdtPacket
from utils import ones_complement, check_sum, validate_pkt
import copy


class ReceiverClass:

    def __init__(self, rcv_pkt: RdtPacket):
        self.state = FSM.STATE_ONE
        self.seq_num = 0
        self.pkt = copy.copy(rcv_pkt)
        self.pkt_to_send = RdtPacket

    def make_pkt(self, is_ack: str):
        self.pkt_to_send = RdtPacket(
            sequence_number=self.seq_num,
            ack_num=0,
            check_sum=ones_complement(check_sum(list(is_ack))),
            payload=list(is_ack)
        )

    def send_ack(self):
        return self.pkt_to_send

    def set_pkt(self, pkt):
        self.pkt = pkt

    def finite_machine(self):
        if self.state == FSM.STATE_ONE:
            if validate_pkt(self.pkt):
                print('---- ACK ----')
                is_ack = 'ack'
                if self.pkt.get_ack_num() == 0:
                    self.state = FSM.STATE_TWO
            else:
                print('---- NACK ----')
                print('Pacote recebido: ' + str(self.pkt))
                is_ack = 'nack'

            self.make_pkt(is_ack)
            return self.send_ack()
        elif self.state == FSM.STATE_TWO:
            if validate_pkt(self.pkt):
                print('---- ACK ----')
                is_ack = 'ack'
                if self.pkt.get_ack_num() == 1:
                    self.state = FSM.STATE_ONE
            else:
                print('---- NACK ----')
                print('Pacote recebido: ' + str(self.pkt))
                is_ack = 'nack'

            self.make_pkt(is_ack)
            return self.send_ack()
        else:
            print("RESET")

    def report(self):
        print("---- receiver ----")
        print("Estado atual: " + str(self.state))
        print("Pacote de envio: " + str(self.pkt_to_send))
        print("------------------")

    def force_nack(self, fake_payload):
        self.pkt.set_payload(fake_payload)

