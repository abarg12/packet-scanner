import sys
import argparse
import socket
import time


if sys.version_info[0] != 2 or sys.version_info[1] != 7:
    print("This script requires Python version 2.7")
    sys.exit(1)


def main():
    args = parse_input()
    if args.hostname != None:
        connect_to_host(args.hostname)
    else:
        print("Please provide host to connect to")
        exit(0)


def connect_to_host(host):
    num_open = 65535
    f = open("scanner.txt", "w")

    start_time = time.time()

    for i in range(65536):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            sock.connect((host, i))
            try:
                service = socket.getservbyport(i, "tcp")
                string_out = str(i) + " (" + service + ") was open\n"
                f.write(string_out)
            except:
                string_out = str(i) + " (NA) was open\n"
                f.write(string_out)
        except:
            num_open -= 1

    total_time = time.time() - start_time
    f.write(str(total_time) + "s\n")
    f.write(str(total_time / 65535) + "s\n")
    f.close()


def parse_input():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("hostname")
    return parser.parse_args()


if __name__ == "__main__":
    main()

