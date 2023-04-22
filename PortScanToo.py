import sys
import argparse
import socket
import time


def main():
    args = parse_input()
    if args.hostname != None:
        connect_to_host(args.hostname)
    else:
        print("Please provide host to connect to")
        exit(0)


def connect_to_host(host):
    num_open = 65535
    f = open("scannertoo.txt", "w")

    start_time = time.time()

    new_order_list = [2*i for i in range(32768)]
    new_order_list = new_order_list + [(2*i)+1 for i in range(32768)]

    strings_to_print = []
    order_to_print = []

    for i in new_order_list:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            sock.connect((host, i))
            try:
                service = socket.getservbyport(i, "tcp")
                string_out = str(i) + " (" + service + ") was open\n"
                strings_to_print.append(string_out)
                order_to_print.append(i)
            except:
                string_out = str(i) + " (NA) was open\n"
                strings_to_print.append(string_out)
                order_to_print.append(i)
                
        except:
            num_open -= 1

    total_time = time.time() - start_time

    # idea from geeksforgeeks tutorial: https://www.geeksforgeeks.org/python-returning-index-of-a-sorted-list/
    sort_index = [i for i, x in sorted(enumerate(order_to_print), key=lambda x: x[1])]
    for i in sort_index:
        f.write(strings_to_print[i])

    f.write(str(total_time) + "s\n")
    f.write(str(total_time / 65535) + "s\n")
    f.close()


def parse_input():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("hostname")
    return parser.parse_args()


if __name__ == "__main__":
    main()

