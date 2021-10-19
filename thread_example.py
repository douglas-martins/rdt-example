import threading
from threading import Thread
import time

from rdt_packet import RdtPacket
from sender import SenderClass
from receiver import ReceiverClass

check = threading.Condition()
packet: RdtPacket
bob_rcv: RdtPacket
message = "Mensagem para "
sender = SenderClass(message)
receiver: ReceiverClass


def default_sender():
    global sender
    global packet
    global bob_rcv

    sender.set_rcv_pkt(bob_rcv)
    packet = sender.finite_machine()
    packet = sender.finite_machine()

    check.notify()
    check.release()
    check.acquire()
    check.wait()


def default_receiver():
    global packet
    global bob_rcv
    global receiver

    check.acquire()
    check.wait()

    receiver = ReceiverClass(packet)
    receiver.finite_machine()
    bob_rcv = receiver.send_ack()

    check.notify()
    check.release()


def alice_routine():
    global packet
    global bob_rcv

    print("Alice will send a packet")
    packet = sender.finite_machine()

    check.acquire()
    check.wait()

    default_sender()

    default_sender()

    default_sender()

    default_sender()

    default_sender()


def bob_routine():
    global packet
    global bob_rcv
    global receiver

    check.acquire()

    receiver = ReceiverClass(packet)
    receiver.finite_machine()
    bob_rcv = receiver.send_ack()

    check.notify()
    check.release()

    default_receiver()
    default_receiver()
    default_receiver()
    default_receiver()
    default_receiver()


Thread(target=alice_routine).start()
Thread(target=bob_routine).start()
