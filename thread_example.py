import threading
from threading import Thread
import time
from math import ceil

from machine_states import FSM
from rdt_packet import RdtPacket
from sender import SenderClass
from receiver import ReceiverClass

check = threading.Condition()
alice_state = FSM.STATE_ONE
bob_state = FSM.STATE_ONE
packet: RdtPacket
bob_rcv: RdtPacket
message = "Mensagem para bob"


def alice_routine():
    global packet
    global bob_rcv
    global message
    sender = SenderClass(message)
    print("Alice will send a packet")
    packet = sender.finite_machine()

    check.acquire()
    check.wait()

    for a in range(0, ceil(len(message)/5)):
        sender.set_rcv_pkt(bob_rcv)
        packet = sender.finite_machine()
        packet = sender.finite_machine()

        check.notify()
        check.release()
        check.acquire()
        check.wait()


def bob_routine():
    global packet
    global bob_rcv
    check.acquire()

    receiver = ReceiverClass(packet)
    receiver.finite_machine()
    bob_rcv = receiver.send_ack()

    check.notify()
    check.release()
    print(ceil(len(message) / 5))
    for a in range(0, ceil(len(message) / 5)):
        check.acquire()
        check.wait()

        receiver = ReceiverClass(packet)
        receiver.finite_machine()
        bob_rcv = receiver.send_ack()

        check.notify()
        check.release()


Thread(target=alice_routine).start()
Thread(target=bob_routine).start()
