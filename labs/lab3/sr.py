#!/usr/bin/env python3
# SUTD 50.012 Networks Lab 3
# James Raphael Tiovalen (1004555)

import config
import threading
import time
import udt
import util

# Selective Repeat reliable transport protocol.
class SelectiveRepeat:
    # "msg_handler" is used to deliver messages to application layer
    def __init__(self, local_port, remote_port, msg_handler):
        util.log("Starting up `Selective Repeat` protocol ... ")
        self.network_layer = udt.NetworkLayer(local_port, remote_port, self)
        self.msg_handler = msg_handler
        self.sender_base = 0
        self.next_sequence_number = 0
        self.timer_list = [self.set_timer(-1)] * config.WINDOW_SIZE
        self.ack_list = [False] * config.WINDOW_SIZE
        self.sender_buffer = [b""] * config.WINDOW_SIZE
        self.receiver_last_ack = b""
        self.is_receiver = True
        self.receiver_base = 0
        self.rcv_list = [False] * config.WINDOW_SIZE
        self.rcv_buffer = [b""] * config.WINDOW_SIZE
        self.sender_lock = threading.Lock()

    def set_timer(self, seq_num):
        return threading.Timer(
            (config.TIMEOUT_MSEC / 1000.0), self._timeout, {seq_num: seq_num}
        )

    # "send" is called by application. Return true on success, false otherwise.
    def send(self, msg):
        self.is_receiver = False
        if self.next_sequence_number < (self.sender_base + config.WINDOW_SIZE):
            threading.Thread(target=self._send_helper(msg))
            return True
        else:
            util.log("Window is full. App data rejected.")
            time.sleep(1)
            return False

    # Helper fn for thread to send the next packet
    def _send_helper(self, msg):
        self.sender_lock.acquire()
        packet = util.make_packet(msg, config.MSG_TYPE_DATA, self.next_sequence_number)
        packet_data = util.extract_data(packet)
        util.log("Sending data: " + util.pkt_to_string(packet_data))
        self.network_layer.send(packet)
        if self.next_sequence_number < self.sender_base + config.WINDOW_SIZE:
            packet_offset_index = (
                self.next_sequence_number - self.sender_base
            ) % config.WINDOW_SIZE
            self.sender_buffer[packet_offset_index] = packet
            self.ack_list[packet_offset_index] = False
            self.timer_list[packet_offset_index] = self.set_timer(
                self.next_sequence_number
            )
            self.timer_list[packet_offset_index].start()
            self.next_sequence_number += 1
        self.sender_lock.release()
        return

    # "handler" to be called by network layer when packet is ready.
    def handle_arrival_msg(self):
        msg = self.network_layer.recv()
        msg_data = util.extract_data(msg)

        if msg_data.is_corrupt:
            return

        # If ACK message, assume it's for sender
        if msg_data.msg_type == config.MSG_TYPE_ACK:
            self.sender_lock.acquire()
            packet_offset_index = (
                msg_data.seq_num - self.sender_base
            ) % config.WINDOW_SIZE
            self.ack_list[packet_offset_index] = True
            print(
                f"Stopping sender's timer for packet number {msg_data.seq_num} after receiving ACK..."
            )
            util.log(
                "Received ACK with seq #"
                + util.pkt_to_string(msg_data)
                + ". Stopping timer..."
            )
            self.timer_list[packet_offset_index].cancel()
            self.timer_list[packet_offset_index] = self.set_timer(msg_data.seq_num)

            # Check if the packet right after sender_base is ACK'd
            # If yes, we move the send_base
            # We also update the timer_list and ack_list arrays accordingly
            try:
                while self.ack_list[0] == True:
                    self.sender_base += 1
                    util.log(f"Updated send_base to {self.sender_base}.")
                    # Remove first element and add False ACK flag
                    self.ack_list = self.ack_list[1:] + [False]
                    # Remove first element and add an empty timer
                    self.timer_list = self.timer_list[1:] + [self.set_timer(-1)]
                    self.sender_buffer = self.sender_buffer[1:] + [b""]
            except IndexError:
                pass
            self.sender_lock.release()
        # If DATA message, assume it's for receiver
        else:
            assert msg_data.msg_type == config.MSG_TYPE_DATA
            util.log("Received DATA: " + util.pkt_to_string(msg_data))
            ack_pkt = util.make_packet(b"", config.MSG_TYPE_ACK, msg_data.seq_num)
            if msg_data.seq_num in range(
                self.receiver_base, self.receiver_base + config.WINDOW_SIZE
            ):
                self.network_layer.send(ack_pkt)
                util.log("Sent ACK: " + util.pkt_to_string(util.extract_data(ack_pkt)))
                packet_offset_index = (
                    msg_data.seq_num - self.receiver_base
                ) % config.WINDOW_SIZE
                self.rcv_list[packet_offset_index] = True
                # Append the payload
                self.rcv_buffer[packet_offset_index] = msg_data.payload

                if msg_data.seq_num == self.receiver_base:
                    while self.rcv_list[0] == True:
                        self.msg_handler(self.rcv_buffer[0])
                        self.receiver_base += 1
                        self.rcv_list = self.rcv_list[1:] + [False]
                        self.rcv_buffer = self.rcv_buffer[1:] + [b""]
                        util.log(f"Updated rcv_base to {self.receiver_base}.")

            elif msg_data.seq_num < self.receiver_base:
                self.network_layer.send(ack_pkt)
                util.log("Packet received outside the current receiver's window.")
                util.log("Sent ACK: " + util.pkt_to_string(util.extract_data(ack_pkt)))

        return

    # Cleanup resources.
    def shutdown(self):
        if not self.is_receiver:
            self._wait_for_last_ACK()
        for timer in self.timer_list:
            if timer.is_alive():
                timer.cancel()
        util.log("Connection shutting down...")
        self.network_layer.shutdown()

    def _wait_for_last_ACK(self):
        while self.sender_base < self.next_sequence_number - 1:
            util.log(
                "Waiting for last ACK from receiver with sequence # "
                + str(int(self.next_sequence_number - 1))
                + "."
            )
            time.sleep(1)

    def _timeout(self, seq_num):
        util.log(f"Timeout! Resending packet {seq_num}...")
        self.sender_lock.acquire()
        packet_offset_index = (seq_num - self.sender_base) % config.WINDOW_SIZE
        self.timer_list[packet_offset_index].cancel()
        self.timer_list[packet_offset_index] = self.set_timer(seq_num)
        pkt = self.sender_buffer[packet_offset_index]
        self.network_layer.send(pkt)
        util.log("Resending packet: " + util.pkt_to_string(util.extract_data(pkt)))
        self.timer_list[packet_offset_index].start()
        self.sender_lock.release()
        return
