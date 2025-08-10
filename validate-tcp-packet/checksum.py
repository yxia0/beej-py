def construct_ip_header(id: int):
    with open(f"tcp_data/tcp_addrs_{id}.txt", "r") as f:
        source_addr, target_addr = f.readline().split(" ")

    with open(f"tcp_data/tcp_data_{id}.dat", "rb") as f:
        content_bytes = f.read()
        tcp_data_len_in_bytes = len(content_bytes).to_bytes(2, "big")

    source_bytes = b"".join(
        [int(num).to_bytes(1, "big") for num in source_addr.split(".")]
    )
    target_bytes = b"".join(
        [int(num).to_bytes(1, "big") for num in target_addr.split(".")]
    )

    header_bytes = b"".join(
        [
            source_bytes,
            target_bytes,
            b"\x00",
            b"\x06",
            tcp_data_len_in_bytes,
        ]
    )

    return header_bytes


def extract_checksum(id: int) -> tuple[int, bytes]:
    with open(f"tcp_data/tcp_data_{id}.dat", "rb") as f:
        content_bytes = f.read()

    checksum_int = int.from_bytes(content_bytes[16:18], "big")

    # generate zero checksum header
    tcp_zero_cksum = content_bytes[:16] + b"\x00\x00" + content_bytes[18:]
    if len(content_bytes) % 2 == 1:
        tcp_zero_cksum += b"\x00"

    return checksum_int, tcp_zero_cksum


def calculate_checksum(
    header_bytes: bytes, tcp_zero_cksum: bytes, checksum: int
) -> bool:
    data = header_bytes + tcp_zero_cksum
    offset = 0
    total = 0
    while offset <= len(data) - 2:
        word = int.from_bytes(data[offset : offset + 2], "big")
        total += word
        total = (total & 0xFFFF) + (total >> 16)
        offset += 2

    calculated_cksum = (~total) & 0xFFFF
    return calculated_cksum == checksum


if __name__ == "__main__":
    for i in range(10):
        header = construct_ip_header(i)
        checksum, tcp_zero_cksum = extract_checksum(i)
        print(calculate_checksum(header, tcp_zero_cksum, checksum))
