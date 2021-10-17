import threading
from threading import Thread
import time

from machine_states import FSM
from rdt_packet import RdtPacket

check = threading.Condition()
alice_state = FSM.STATE_ONE
bob_state = FSM.STATE_ONE
packet: RdtPacket


def alice_routine():
    global packet
    print("Alice will send a packet")
    packet = RdtPacket(
        sequence_number=0,
        ack_num=0,
        check_sum=0,
        payload=['x', 'x', 't', 'p', 'v']
    )
    print(packet)
    check.acquire()
    check.wait()

    if packet.get_ack_num() == 1:
        print("\nAlice recieved ACK")


def bob_routine():
    global packet
    print("Bob received a alice packet")
    check.acquire()
    time.sleep(2)  # ou faz a lógica para verificar se o pacote está corrupto ou não
    alice_state = FSM.STATE_TWO
    print("Bob modify packet to send (if necessary)")
    packet.set_sequence_number(packet.get_sequence_number() + 1)
    packet.set_ack_num(1)
    print(packet)
    check.notify()
    check.release()
    print("Bob send ACK to Alice")


Thread(target=alice_routine).start()
Thread(target=bob_routine).start()
