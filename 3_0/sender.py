from machine_states import FSM
from rdt_packet import RdtPacket
from utils import ones_complement, check_sum, validate_pkt
from typing import List
from datetime import datetime


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
            payload=list(payload),
            time_stamp=datetime.now()
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

    def time_out(self):
        seconds = (datetime.now() - self.last_pkt.get_time_stamp()).seconds
        return seconds > 5

    def finite_machine(self):
        if self.state == FSM.STATE_ONE:
            print('---- ack 0 ----')
            self.make_pkt()
            self.state = FSM.STATE_TWO
            return self.send_pkt()

        elif self.state == FSM.STATE_TWO:
            is_corrupted = not validate_pkt(self.rcv_pkt)

            if self.time_out():
                print("---- TIME OUT ----")
                print('Time Stamp Pacote: ' + str(self.last_pkt.get_time_stamp()))
                print('Agora: ' + str(datetime.now()))
                self.last_pkt.set_time_stamp(datetime.now())
                return self.send_pkt()

            if is_corrupted or self.validate_ack(1):
                return self.send_pkt()
            elif not is_corrupted and self.validate_ack(0):
                self.state = FSM.STATE_THREE

            return self.last_pkt

        elif self.state == FSM.STATE_THREE:
            print('---- ack 1 ----')
            self.last_pkt.set_ack_num(ack_num=1)
            self.last_pkt.set_time_stamp(datetime.now())
            self.state = FSM.STATE_FOR
            return self.send_pkt()

        elif self.state == FSM.STATE_FOR:
            is_corrupted = not validate_pkt(self.rcv_pkt)

            if self.time_out():
                self.last_pkt.set_time_stamp(datetime.now())
                return self.send_pkt()

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
