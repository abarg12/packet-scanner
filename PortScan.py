import sys
import argparse
import socket


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

    for i in range(65536):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            sock.connect((host, i))
            try:
                service = socket.getservbyport(i, "tcp")
                print(service)
            except:
                print("NA") 
        except:
            num_open -= 1

    print(num_open)



def parse_input():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("hostname")
    return parser.parse_args()


if __name__ == "__main__":
    main()
