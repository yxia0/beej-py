import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2


def usage():
    print("usage: wordclient.py server port", file=sys.stderr)


packet_buffer = b""


def buffer_has_full_packet() -> bool:
    global packet_buffer
    if len(packet_buffer) < 2:
        # does not have full word len info
        return False

    # assume the first two bytes are word len
    word_len = int.from_bytes(packet_buffer[:2], "big")
    if len(packet_buffer[2:]) < word_len:
        return False

    return True


def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    while True:
        if buffer_has_full_packet():
            word_len = int.from_bytes(packet_buffer[:2], "big")
            word_packet = packet_buffer[: 2 + word_len]
            packet_buffer = packet_buffer[2 + word_len :]
            return word_packet
        else:
            more_data = s.recv(30)
            if len(more_data) == 0:
                s.close()
                return None
            else:
                packet_buffer += more_data


def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    word_bytes = word_packet[2:]
    return word_bytes.decode(encoding="utf-8")


# Do not modify:


def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
