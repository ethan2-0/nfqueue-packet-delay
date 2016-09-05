#!/usr/bin/python3
# The author (Ethan White) of this code dedicates any and all copyright interest
# in this code to the public domain. The author makes this dedication for the
# benefit of the public at large and to the detriment of the author's heirs and
# successors. The author intends this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this code
# under copyright law.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import netfilterqueue
import sys
import threading
import time
import binascii
import random
import argparse

rand = random.SystemRandom()

last_sleep_end = None

class PacketHandlerThread(threading.Thread):
    def __init__(self, handler, delay_min, delay_max,
            print_bandwidth, print_delay):
        threading.Thread.__init__(self)
        self.handler = handler
        self.stop_requested = False
        self.on_stop = None
        self.print_bandwidth = print_bandwidth
        self.print_delay = print_delay
        self.delay_min = delay_min
        self.delay_max = delay_max

    def run(self):
        while True:
            global last_sleep_end
            t = (self.delay_max - self.delay_min) * rand.random()
            t += self.delay_min
            if last_sleep_end is not None:
                # Subtract off the time it's taken to go through and accept all
                # the packets. This may be unnecessary, but it shouldn't hurt.
                t -= time.time() - last_sleep_end
            if self.print_delay:
                print("Sleeping for %1.2fms" % t)
            time.sleep(t)
            last_sleep_end = time.time()

            size_total = 0
            for packet in self.handler.packets:
                if self.print_bandwidth:
                    size_total += packet.get_payload_len()
                packet.accept()

            if self.print_bandwidth:
                print("Accepted %1.2fKb across a %1.2fs window, for %1.2fKbps."
                    % (size_total / 128, t, size_total / (128 * t)))

            self.handler.packets = []

            if self.stop_requested:
                break

        if self.on_stop is not None:
            self.on_stop()

    def request_stop(self, on_stop):
        self.on_stop = on_stop
        self.stop_requested = True

class PacketHandler:
    def __init__(self, delay, print_bandwidth, print_delay, queue):
        self.packets = []
        self.queue_num = queue
        self.queue = netfilterqueue.NetfilterQueue()
        self.delay_min, self.delay_max = delay
        self.print_bandwidth = print_bandwidth
        self.print_delay = print_delay
        self.handler_thread = PacketHandlerThread(self, self.delay_min,
            self.delay_max, self.print_bandwidth, self.print_delay)

    def run(self):
        self.queue.bind(self.queue_num, handler.handle)
        self.handler_thread.start()
        self.queue.run()

    def handle(self, packet):
        self.packets.append(packet)

    def cleanup(self, on_done):
        self.queue.unbind()
        self.handler_thread.request_stop(on_done)

parser = argparse.ArgumentParser(description="Attempt to mitigate timing "
    + "attacks by delaying packets using specific patterns")
parser.add_argument("--delay-min", "-m", type=float, default=0.075,
    help="set the minimum window length in seconds")
parser.add_argument("--delay-max", "-M", type=float, default=0.2,
    help="set the maximum window length in seconds")
parser.add_argument("--queue", "-q", type=int, default=0,
    help="the queue number")
parser.add_argument("--print-delay", "-d", action="store_true",
    help="print the duration of each window")
parser.add_argument("--print-bandwidth", "-b", action="store_true",
    help="print the bandwidth observed in each window, in kilobits per second")
args = parser.parse_args()

if args.delay_min > args.delay_max:
    sys.stdout.write(("%s: error: minimum delay must be less than or equal to "
        + "maximum delay") % sys.argv[0])
    sys.exit(1)

# Namespace(delay_max=0.2, delay_min=2.0, print_bandwidth=False, print_delay=False, queue=0)

handler = PacketHandler(delay=(args.delay_min, args.delay_max),
    print_bandwidth=args.print_bandwidth, print_delay=args.print_delay,
    queue=args.queue)

try:
    handler.run()
except KeyboardInterrupt:
    sys.stdout.write("Shutting down...")

handler.cleanup(lambda: print("Bye!"))
