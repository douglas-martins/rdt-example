from random import randint

from utils import check_sum
# from rdt_protocol import RdtPacket


payload = ['x', 'x', 't', 'p', 'v']

# def init_process():
#     alice_packet = RdtPacket(
#         sequence_number=randint(1, 99999),
#         ack_num=0,
#         check_sum=0,
#         payload=payload
#     )
#
#
# def send_packet():
#     return ''



print(check_sum(payload))
