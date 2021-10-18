from typing import List
from rdt_packet import RdtPacket


def check_sum(payload: List[str]) -> str:
    all_bytes = [ord(x) for x in payload]
    total = sum(all_bytes)
    binary_sum = bin(total)

    if len(binary_sum) > 8:
        formatted_binary = binary_sum[2:]
        size = len(formatted_binary) - 8
        first_bits = formatted_binary[:size]
        last_bits = formatted_binary[size:]

        result = bin(int(first_bits, 2) + int(last_bits, 2))
        return format(int(result, 2), '08b')
    else:
        return format(int(binary_sum, 2), '08b')


def ones_complement(binary_str: str):
    return binary_str.replace('1', 'x').replace('0', '1').replace('x', '0')


def validate_pkt(pkt_to_validate) -> bool:
    cs = check_sum(pkt_to_validate.get_payload())
    print(cs)
    print(pkt_to_validate.get_check_sum())
    for a in range(0, len(cs)):
        x = int(cs[a])
        y = int(pkt_to_validate.get_check_sum()[a])
        if (x + y) != 1:
            return False
    return True
