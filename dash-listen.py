# The following script is forked from zippocage/dash_hack:
#   https://github.com/zippocage/dash_hack
# which is an adjusted version of Aaron Bell's script:
#   http://www.aaronbell.com/how-to-hack-amazons-wifi-button/
# If you want to run this script as an ubuntu service, check out:
#   http://askubuntu.com/questions/175751/how-do-i-run-a-python-script-in-the-background-and-restart-it-after-a-crash
#
# How to use:
#   1. Setup an account in If This Then That (IFTTT): http://www.ifttt.com/
#   2. Create a new recipe using the Maker Channel for the IF command:
#       a. https://ifttt.com/maker
#   3. Update the MAKER_KEY variable below.
#   4. Connect your Amazon Dash Button to your network but skip the last step of the setup where they ask you which
#      product you want the button to purchase.
#   5. Run this program via `python dash-listen.py`.
#   6. Push the Amazon Dash Button and take note of its Mac Address.
#   7. Overwrite the sample Mac Addresses with your Amazon Dash Button(s) Mac Address(es).
#   8. Re-run `python dash-listen.py`.
#   9. Now you can configure IFTTT to do anything you want when you push the button.
#

import socket
import struct
import binascii
import time
import json
import urllib2
import datetime

# Use your own IFTTT key, not this fake one
MAKER_KEY = 'dzwVhf04I_s2aL0VhD9Vj'

# Replace these fake MAC addresses on the left and the names on the right with your own.
# The name of the dash buttons are what will be used when triggering the Maker event like so:
#   https://maker.ifttt.com/trigger/<DASH_BUTTON_NICKNAME>/with/key/<MAKER_KEY>
MAC_ADDRESSES = {
    '747500000001' : 'DASH_BUTTON_NICKNAME',
    '747500000002' : 'dash_elements1',
    '747500000003' : 'dash_elements2',
    '747500000004' : 'dash_cottonelle',
    '747500000005' : 'dash_huggies'
}

# How many seconds should we wait before another button push triggers the event?
trigger_timeout = 5

# Records the last time the event was triggered
trigger_time = {}

# Trigger an IFTTT URL where the event is the same as the strings in MAC_ADDRESSES
# Body includes JSON with timestamp values.
def trigger_url(trigger):
    data = '{ "value1" : "' + time.strftime("%Y-%m-%d") + '", "value2" : "' + time.strftime("%H:%M") + '" }'
    req = urllib2.Request( 'https://maker.ifttt.com/trigger/'+trigger+'/with/key/'+MAKER_KEY , data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return response

def record_trigger(trigger):
    print 'Triggering '+ trigger +' event, response: ' + trigger_url(trigger)

def is_within_secs(last_time, diff):
    return (datetime.datetime.now() - last_time).total_seconds() < (diff +1)

# Check if the event has triggered within the timeout already
def has_already_triggered(trigger):
    global trigger_time
    
    if trigger in trigger_time:
        if (is_within_secs(trigger_time[trigger], trigger_timeout)):
            return True

    trigger_time[trigger] = datetime.datetime.now()
    return False

rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

while True:
    packet = rawSocket.recvfrom(2048)
    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
    # skip non-ARP packets
    ethertype = ethernet_detailed[2]
    if ethertype != '\x08\x06':
        continue
    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
    source_mac = binascii.hexlify(arp_detailed[5])
    source_ip = socket.inet_ntoa(arp_detailed[6])
    dest_ip = socket.inet_ntoa(arp_detailed[8])
    if source_mac in MAC_ADDRESSES:

        if has_already_triggered(MAC_ADDRESSES[source_mac]):
            print "Culled duplicate trigger " + MAC_ADDRESSES[source_mac]
        else:
            record_trigger(MAC_ADDRESSES[source_mac])

    elif source_ip == '0.0.0.0':
        print "Dash button detected with MAC ADDRESS " + source_mac
