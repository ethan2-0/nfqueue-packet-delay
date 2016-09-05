#!/bin/bash
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

source build_package.conf

mkdir pkg-debian
mkdir pkg-debian/DEBIAN
mkdir -p pkg-debian/usr/bin

cp main.py pkg-debian/usr/bin/nfqueue-packet-delay
chmod +x pkg-debian/usr/bin/nfqueue-packet-delay

du_total=$(du -d 0 pkg-debian/usr | cut -f1)

cat > pkg-debian/DEBIAN/control << EOF
Package: nfqueue-packet-delay
Version: $package_version
Architecture: all
Essential: no
Section: web
Priority: optional
Depends: python3 (>=3.3), python3-netfilterqueue (>= 0.7)
Maintainer: Ethan L. White
Installed-Size: $du_total
Description: A Python 3 libnetfilter_queue handler intended to mitigate CPU\
load induced network latency covert channels and other timing attacks
 This package provides a Python 3 libnetfilter_queue handler that delays
 packets using specific patterns designed to make all timing attacks, and in
 particular CPU load induced network latency covert channels.
X-Python3-Version: >=3.3
EOF

dpkg -b pkg-debian/ nfqueue-packet-delay_${package_version}_any.deb
