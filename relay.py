import requests
import random
import socket
import threading

# what relays do we search
search = ["flag=stable", ""]
search = "&".join(search)

# how much we test test_size*tests_num
test_size = 4
tests_num = 3


def total_number():
    r = requests.get(
        "https://onionoo.torproject.org/summary?" + search + "limit=0")

    return r.json()['relays_truncated']


def check_ip_port(ip_port: str):
    ip, port = ip_port.split(":")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((ip, int(port)))

        print(ip_port)

    except:
        return


def get_rand_relays():
    rand = random.randint(0, total_number() - test_size)

    params = ["offset=" + str(rand),
              "limit=" + str(test_size),
              'fields=or_addresses'
              ""]
    params = "&".join(params)

    r = requests.get(
        "https://onionoo.torproject.org/details?" + search + params)

    relays = r.json()['relays']

    ips = []
    for relay in relays:
        ips.append(relay['or_addresses'][0])

    return ips


for _ in range(tests_num):
    for ip_port in get_rand_relays():
        threading.Thread(target=check_ip_port, args=(ip_port, )).start()
