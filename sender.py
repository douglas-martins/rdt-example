from machine_states import FSM
from rdt_packet import RdtPacket
from utils import ones_complement, check_sum, validate_pkt
from typing import List


class SenderClass:

    def __init__(self, data):
        self.state = FSM.STATE_ONE
        self.data = data
        self.last_pkt = RdtPacket
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
        # Envia o pacote para a Thread B
        return self.last_pkt

    def __get_five_characters__(self) -> List[str]:
        payload = self.data[:5]
        self.full_data = self.data[5:]
        return payload

    def finit_machine(self):
        if self.state == FSM.STATE_ONE:
            self.make_pkt()
            self.send_pkt()
            self.state = FSM.STATE_TWO

        elif self.state == FSM.STATE_TWO:
            '''if not validate_pkt() or 'NACK' == 'NACK':
                self.send_pkt()
            else:
                self.state = FSM.STATE_THREE'''

            print(self.state)

        elif self.state == FSM.STATE_THREE:
            # Ainda não sei se não apenas deixar os estados ONE e TWO
            self.last_pkt.set_ack_num(ack_num=1)
            self.send_pkt()
            self.state = FSM.STATE_FOR

        elif self.state == FSM.STATE_FOR:
            '''if not validate_pkt() or 'NACK' == 'NACK':
                self.send_pkt()
            else:
                self.state = FSM.STATE_ONE'''

            print(self.state)


send = SenderClass("Mensage completa da Alice para o Bob")
send.make_pkt()
