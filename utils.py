from typing import List


def check_sum(payload: List[str]) -> str:
    first_byte, second_byte, third_byte, four_byte, fifth_byte = [ord(x) for x in payload]

    binary_sum = bin(first_byte + second_byte + third_byte + four_byte + fifth_byte)

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

