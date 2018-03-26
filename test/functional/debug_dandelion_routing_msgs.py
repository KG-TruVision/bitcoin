#!/usr/bin/env python3
# Copyright (c) 2018 Bradley Denby
# Distributed under the MIT software license. See the accompanying file COPYING
# or http://www.opensource.org/licenses/mit-license.php
"""Debug Dandelion routing messages

Desired behaviors:
1. Dandelion transaction inventory advertisement (INV) from "pfrom":
   - If pfrom->setDandelionInventoryKnown.insert(inv.hash)
     (i.e. pfrom hasn't sent this INV to this node before)
     - Ask pfrom for this Dandelion transaction (i.e. reply with GETDATA)

2. Dandelion transaction (DANDELIONTX) from "pfrom":
   - If connman->isDandelionInbound(pfrom)
     - If !stempool.exists(inv.hash), then AcceptToStemPool(tx)
     - If stempool.exists(inv.hash)
       - pto = connman->getDandelionDestination(pfrom)
       - If pto->setDandelionInventoryKnown.count(tx.hash)==0
         - pto->vInventoryDandelionTxToSend.push_back(tx.hash)

3. Dandelion transaction created locally:
   - pto = connman->localDandelionOutbound
   - If pto->setDandelionInventoryKnown.count(tx.hash)==0
     - pto->vInventoryDandelionTxToSend.push_back(tx.hash)
"""

from test_framework.mininode import *                          # P2PInterface
from test_framework.test_framework import BitcoinTestFramework # BitcoinTestFramework
from test_framework.util import *                              # other stuff
import time                                                    # sleep

class DebugDandelionRoutingMsgs(BitcoinTestFramework):
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
        # Construct the P2P graph
        self.log.info('Adding connections...')
        for i in range(len(self.nodes)):
            connect_nodes(self.nodes[i],(i+1)%len(self.nodes))
            time.sleep(0.5)
            connect_nodes(self.nodes[i],(i+2)%len(self.nodes))
            time.sleep(0.5)
        self.log.info('Adding connections complete.')
        # Generate spening money
        self.log.info('Generating spending money...')
        for node in self.nodes:
            node.generate(1)
        self.nodes[0].generate(100)
        self.log.info('Generating spending money complete.')
        # Generate and send a Dandelion transaction
        self.log.info('Sending Dandelion transaction...')
        self.nodes[0].sendtoaddress(self.nodes[3].getnewaddress(),1.0)
        self.log.info('Sending Dandelion transaction complete.')

if __name__ == '__main__':
    DebugDandelionRoutingMsgs().main()
