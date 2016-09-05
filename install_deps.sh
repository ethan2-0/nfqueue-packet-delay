#!/bin/bash
# The author (Ethan White) of this code dedicates any and all copyright interest
# in this code to the public domain. The author makes this dedication for the
# benefit of the public at large and to the detriment of our heirs and
# successors. The author intends this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this code
# under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

echo "Note: If not on a Debian-based Linux, you're on your own."
echo "Detailed instructions can be found at https://github.com/kti/python-netfilterqueue."
echo ""

if [[ ! $EUID -eq 0 ]]; then
    >&2 echo "Error: This script must be run as root"
    exit 1
fi

apt-get install build-essential python3-dev libnetfilter-queue-dev
pip3 install NetfilterQueue
