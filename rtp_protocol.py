

class RtpProtocol:

    def __int__(self):
        self.version = 2
        self.header_size = 10
        self.message_size = 8

    def __init__(self, version):
        self.version = version
        self.__init__(self)

    def encode(self, msg):
        return msg

    def decode(self, msg):
        return msg

    def checksum(self, message):
        # Dividindo a mensagem em pacotes de bits
        bit_packet_one, bit_packet_two, bit_packet_three, bit_packet_four = self.__get_bits_packets(message)

        # Calculando a soma, em binário, dos pacotes
        binary_sum = bin(
            int(bit_packet_one, 2) + int(bit_packet_two, 2) +
            int(bit_packet_three, 2) + int(bit_packet_four, 2)
        )[2:]

        # Verifica bits de overflow
        if len(binary_sum) > self.message_size:
            x = len(binary_sum) - self.message_size
            binary_sum = bin(int(binary_sum[0:x], 2) + int(binary_sum[x:], 2))[2:]

        if len(binary_sum) < self.message_size:
            binary_sum = '0' * (self.message_size - len(binary_sum)) + binary_sum

        return self.__make_binary_sum(binary_sum)

    def receiver_check_sum(self, message, check_sum):
        # Dividindo a mensagem em pacotes de bits
        bit_packet_one, bit_packet_two, bit_packet_three, bit_packet_four = self.__get_bits_packets(message)

        receiver_sum = bin(
            int(bit_packet_one, 2) + int(bit_packet_two, 2) + int(check_sum, 2) +
            int(bit_packet_three, 2) + int(bit_packet_four, 2) + int(check_sum, 2)
        )[2:]

        if len(receiver_sum) > self.message_size:
            x = len(receiver_sum) - self.message_size
            receiver_sum = bin(int(receiver_sum[0:x], 2) + int(receiver_sum[x:], 2))[2:]

        return self.__make_binary_sum(receiver_sum)

    def __get_bits_packets(self, message):
        return (
            message[0:self.message_size], message[self.message_size:2 * self.message_size],
            message[2 * self.message_size:3 * self.message_size], message[3 * self.message_size:4 * self.message_size]
        )

    def __make_binary_sum(self, message):
        binary_sum = ''
        for i in message:
            binary_sum += '0' if i == '1' else '1'

        return binary_sum
