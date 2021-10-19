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
    bob_rcv = receiver.finite_machine()

    check.notify()
    check.release()


def alice_routine():
    global packet
    global bob_rcv

    print("Alice will send a packet")
    packet = sender.finite_machine()

    check.acquire()
    check.wait()

    default_sender() # Faz o primeiro pacote e envia

    default_sender() # Recebe o pacote de resposta de quem recebeu

    default_sender() # Envia o pacote novamente como ack_num 1

    default_sender() # Recebe o pacote de resposta de quem recebeu

    default_sender() # Faz o segundo pacote e envia


def bob_routine():
    global packet
    global bob_rcv
    global receiver

    check.acquire()

    receiver = ReceiverClass(packet)
    bob_rcv = receiver.finite_machine() # Recebe o pacote (ack 0) e envia um ack ou nack dependendo do que recebeu

    check.notify()
    check.release()

    default_receiver() # Recebe o pacote (ack 1) e envia um ack ou nack dependendo do que recebeu

    default_receiver()

    default_receiver()

    default_receiver()

    default_receiver()


Thread(target=alice_routine).start()
Thread(target=bob_routine).start()
