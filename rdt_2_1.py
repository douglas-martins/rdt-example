from random import randint

from utils import check_sum, ones_complement

from rdt_packet import RdtPacket
from machine_states import FSM


payload = ['x', 'x', 't', 'p', 'v']

# void transport_layer_input_A() {
# // pode usar uma para cada host ou uma unica que pode ser chamada que
# // FSM
# enum estado_fsm_t {s1, s2, s3} estados_op;
# while (1){
#   switch (estado){
#       case s1: // cÃ³digo do estado
#       break;
#
#       default:
#       break;
#    }
#   }
# }


def init_process():
    alice_packet = RdtPacket(
        sequence_number=randint(1, 99999),
        ack_num=0,
        check_sum=ones_complement(check_sum(payload)),
        payload=payload
    )




#
#
# def send_packet():
#     return ''

init_process()
print(check_sum(payload))
