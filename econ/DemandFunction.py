# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

# Conveience functions

def getLinearDemandFunction(constant, slope):
    def df(price):
        return max(0.0, constant + slope * price)
    return df