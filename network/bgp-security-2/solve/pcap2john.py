#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Combine of all of Dhiru Kholia pcap convert utilities
# into a single program.  The pcap2john.readme lists
# all of the original license statements. This merge was
# done by JimF, Nov 2014, somewhat as a learning experience
# for Python.
#
# The code itself is still a fabrication of Dhiru.


import base64
from binascii import hexlify
import os
import socket
import struct
import sys
import time

import logging
l = logging.getLogger("scapy.runtime")
l.setLevel(49)

try:
    from scapy.all import *
except ImportError:
    sys.stderr.write("Please install 'scapy' package for Python, running 'pip install --user scapy' should work\n")
    sys.exit(1)

try:
    import dpkt
    import dpkt.ethernet as ethernet
    from dpkt import ip as dip
    import dpkt.stp as stp
except ImportError:
    sys.stderr.write("Please install 'dpkt' package for Python, running 'pip install --user dpkt' should work\n")
    sys.exit(1)


def pcap_parser_tcpmd5(fname):

    f = open(fname, "rb")
    pcap = dpkt.pcap.Reader(f)

    for _, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if eth.type == dpkt.ethernet.ETH_TYPE_IP:
            ip = eth.data

            if ip.v != 4:
                continue

            if ip.p != dpkt.ip.IP_PROTO_TCP:
                continue

            tcp = ip.data

            # this packet doesn't have MD5 signature (too small)
            if tcp.off * 4 < 40:
                continue

            raw_ip_data = ip.pack()
            raw_tcp_data = tcp.pack()
            length = len(raw_tcp_data)

            # connection_id = (ip.src, tcp.sport, ip.dst, tcp.dport)

            if len(tcp.opts) < 18:  # MD5 signature "option" is 18 bytes long
                continue

            found = False

            for opt_type, opt_data in dpkt.tcp.parse_opts(tcp.opts):
                # skip over "undesired" option fields
                # TCP_OPT_MD5 = 19 implies TCP MD5 signature, RFC 2385
                if opt_type != 19:
                    continue

                found = True
                break

            if not found:
                continue

            # MD5 signature "option" is 16 bytes long
            if len(opt_data) != 16:
                continue

            # TCP_OPT_MD5 = 19 implies TCP MD5 signature, RFC 2385
            if opt_type == 19:
                header_length = tcp.off * 4
                data_length = length - header_length
                # print length, header_length, data_length

                # TCP pseudo-header + TCP header + TCP segment data
                # salt_length = 12 + 20 + data_length

                # add TCP pseudo-header
                salt = raw_ip_data[12:12 + 8]  # src. and dest. IP
                salt = salt + b"\x00"  # zero padding
                # salt = salt + raw_ip_data[9]  # protocol
                salt = salt + bytes(raw_ip_data[9].to_bytes())
                # salt = salt + "%c" % (length / 256)  # segment length
                salt = salt + bytes([int(length / 256)])
                # salt = salt + "%c" % (length % 256)  # segment length
                salt = salt + bytes([int(length % 256)])

                # add TCP header
                salt = salt + raw_tcp_data[:16]  # TCP header without checksum
                salt = salt + (b"\x00" * 4)  # add zero checksum

                # add segment data
                salt = salt + raw_tcp_data[header_length:header_length + data_length]
                # print len(salt)

                print("$tcpmd5$%s$%s" % (salt.hex(), opt_data.hex()))

    f.close()

############################################################
# original main, but now calls multiple 2john routines, all
# cut from the original independent convert programs.
############################################################
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s [.pcap files]\n" % sys.argv[0])
        sys.exit(1)

    # advertise what is not handled
    sys.stderr.write("Note: This program does not have the functionality of wpapcap2john, SIPdump, eapmd5tojohn, and vncpcap2john programs which are included with JtR Jumbo.\n\n")
    time.sleep(1)

    for i in range(1, len(sys.argv)):
        pcap_parser_tcpmd5(sys.argv[i])
