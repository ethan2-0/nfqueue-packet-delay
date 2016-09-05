# nfqueue-packet-delay
This is a libnetfilter_queue handler intended to mitigate various timing
attacks. It was created in particular to mitigate a covert channel based on the
observation that ping latency is dependant on CPU usage.

# Mechanism

This handler queues up all packets across a variable-length window; each window
has its length chosen randomly from an interval specified as a command-line
argument, with a default interval of [0.075s, 0.2s). This should make it very
difficult to observe timing differences even up the order of 100 microseconds;
for larger timing differences, the default interval isn't adequate, and should be
increased in both magnitude and range.

This mechanism could certainly be improved, but what we have now seems adequate.
I did consider just adding a random delay to each packet, but that would
be more complex (requiring state per packet), and I don't think it would
really have any substantiative benifits.

# Usage

~~~
usage: nfqueue-packet-delay [-h] [--delay-min DELAY_MIN]
                            [--delay-max DELAY_MAX] [--queue QUEUE]
                            [--print-delay] [--print-bandwidth]

Attempt to mitigate timing attacks by delaying packets using specific patterns

optional arguments:
  -h, --help            show this help message and exit
  --delay-min DELAY_MIN, -m DELAY_MIN
                        set the minimum window length in seconds
  --delay-max DELAY_MAX, -M DELAY_MAX
                        set the maximum window length in seconds
  --queue QUEUE, -q QUEUE
                        the queue number
  --print-delay, -d     print the duration of each window
  --print-bandwidth, -b
                        print the bandwidth observed in each window, in
                        kilobits per second
~~~

# License

SQLLite public-domain dedication + MIT license warranty disclaimer. See
the `LICENSE` file for details.

# Debian packaging

Run `build_package.sh` to build a Debian package. Note that this has only been
tested on Debian 8 and Ubuntu 16.04 on x64. Your mileage may vary. Note that
there are no facilities for creating a Python wheel or any other formats.
