#!/usr/bin/env python3
# Copyright (c) 2018 Bradley Denby
# Distributed under the MIT software license. See the accompanying file COPYING
# or http://www.opensource.org/licenses/mit-license.php
"""Debug Dandelion routing data structures

Desired behaviors:
1. New inbound connection "pfrom":
   - Append pfrom to vDandelionInbound vector
   - If vDandelionOutbound vector is not empty:
     - Each outbound connection forwards Dandelion transactions from a number
       n\in[0,len(vDandelionInbound)] of inbound connections. Collect the set S
       of outbound connections with the smallest such n.
     - Select an outbound connection "pto" uniformly at random from S
     - Add (pfrom, pto) to mDandelionRouting map

2. New outbound connection "pto":
   - Append pto to vDandelionOutbound vector
   - If vDandelionOutbound vector has length 1:
     - Trigger periodic Dandelion routing shuffle

3. Closed inbound connection "pfrom":
   - Remove pfrom from vDandelionInbound vector
   - Remove all pairs (pfrom, *) from mDandelionRouting map

4. Closed outbound connection "pto":
   - Remove pto from vDandelionOutbound vector
   - If vDandelionOutbound vector is not empty:
     - Each remaining outbound connection forwards Dandelion transactions from a
       number n\in[0,len(vDandelionInbound)] of inbound connections. Collect the
       set S of outbound connections with the smallest such n.
     - Select an outbound connection "new pto" uniformly at random from S
     - Replace all mDandelionRouting map pairs (*, pto) with (*, new pto)
     - Replace all mDandelionTxDestination map pairs (*, pto) with (*, new pto)
"""

from test_framework.mininode import *                          # P2PInterface
from test_framework.test_framework import BitcoinTestFramework # BitcoinTestFramework
from test_framework.util import *                              # other stuff
import time                                                    # sleep

class DebugDandelionRoutingData(BitcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 6
        self.extra_args = []
        for i in range(self.num_nodes):
            self.extra_args.append(["-debug=dandelion"])

    def setup_network(self):
        self.setup_nodes()

    def run_test(self):
        network_thread_start()
        self.log.info('Adding connections...')
        for i in range(len(self.nodes)):
            connect_nodes(self.nodes[i],(i+1)%len(self.nodes))
            time.sleep(0.5)
            connect_nodes(self.nodes[i],(i+2)%len(self.nodes))
            time.sleep(0.5)
        self.log.info('Adding connections complete.')
        self.log.info('Removing connections...')
        for i in range(len(self.nodes)):
            j = (i+2)%len(self.nodes)
            disconnect_nodes(self.nodes[j],(j+1)%len(self.nodes))
            time.sleep(0.5)
            disconnect_nodes(self.nodes[j],(j+2)%len(self.nodes))
            time.sleep(0.5)
        self.log.info('Removing connections complete.')

if __name__ == '__main__':
    DebugDandelionRoutingData().main()
