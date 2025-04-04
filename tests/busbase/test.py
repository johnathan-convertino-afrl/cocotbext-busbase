#!/usr/bin/env python
#******************************************************************************
# file:    test.py
#
# author:  JAY CONVERTINO
#
# date:    2025/03/17
#
# about:   Brief
# Cocotb test bench for analog devices uP
#
# license: License MIT
# Copyright 2025 Jay Convertino
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
#******************************************************************************
# """
#
# Copyright (c) 2020 Alex Forencich
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# """

import itertools
import logging
import os
import random

import cocotb_test.simulator

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, NextTimeStep, Edge, FallingEdge
from cocotb.regression import TestFactory

try:
    from cocotbext.busbase import *
except ImportError as e:
    import sys
    sys.path.append("../../")
    from cocotbext.busbase import *


# Class: basictrans
# create an object that associates a data member and address for operation.
class basictrans(transaction):
    def __init__(self, address, data=None):
        self.address = address
        self.data = data

# Class: basicMaster
# basic bus master
class basicMaster(busbase):
  # Variable: _signals
  # List of signals that are required
  _signals = ["addr", "we", "cs", "data"]

  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, reset, *args, **kwargs):
    super().__init__(entity, name, clock, *args, **kwargs)

    self.log.info("BASIC Master")
    self.log.info("Copyright (c) 2025 Jay Convertino")
    self.log.info("https://github.com/johnathan-convertino-afrl/cocotbext-busbase")

    self._reset = reset

    self.bus.addr.setimmediatevalue(0)
    self.bus.data.setimmediatevalue(0)

  # Function: read
  # Read from a address and return data
  async def read(self, address):
    trans = None
    if(isinstance(address, list)):
      temp = []
      for a in address:
        temp.append(basictrans(a))
      temp = await self.read_trans(temp)
      #need a return with the data list only. This is only a guess at this point
      return [temp[i].data for i in range(len(temp))]
    else:
      trans = await self.read_trans(basictrans(address))
      return trans.data

  # Function: write
  # Write to a address some data
  async def write(self, address, data):
    if(isinstance(address, list) or isinstance(data, list)):
      if(len(address) != len(data)):
        self.log.error(f'Address and data vector must be the same length')
      temp = []
      for i in range(len(address)):
        temp.append(basictrans(address[i], data[i]))
      await self.write_trans(temp)
    else:
      await self.write_trans(basictrans(address, data))

  # Function: _check_type
  # Check and make sure we are only sending 2 bytes at a time and that it is a bytes/bytearray
  def _check_type(self, trans):
      if(not isinstance(trans, basictrans)):
          self.log.error(f'Transaction must be of type: {type(basictrans)}')
          return False

      return True

  # Method: _run
  # _run thread that deals with read and write.
  async def _run(self):
    self.active = False

    trans = None

    while True:

      if self._reset.value:
        self.bus.we.setimmediatevalue(0)
        self.bus.cs.setimmediatevalue(0)
        await RisingEdge(self.clock)
        continue

      if not self.wqueue.empty():
        self.active = True
        while self.active:
          trans = await self.wqueue.get()
          self.bus.we.setimmediatevalue(1)
          self.bus.cs.setimmediatevalue(1)
          self.bus.addr.setimmediatevalue(trans.address)
          self.bus.data.setimmediatevalue(trans.data)
          self._idle_write.set()
          await RisingEdge(self.clock)

          self.active = not self.wqueue.empty()
      elif not self.qqueue.empty():
        self.active = True
        while self.active:
          trans = await self.qqueue.get()
          self.bus.we.setimmediatevalue(0)
          self.bus.cs.setimmediatevalue(1)
          self.bus.addr.setimmediatevalue(trans.address)
          trans.data = self.bus.data.value
          await self.rqueue.put(trans)
          self._idle_read.set()
          await RisingEdge(self.clock)

          self.active = not self.qqueue.empty()
      else:
        self.active = False
        self.bus.we.setimmediatevalue(0)
        self.bus.cs.setimmediatevalue(0)
        await RisingEdge(self.clock)

# Class: basicEchoSlave
# Respond to master reads and write by returning data, simple echo core.
class basicpEchoSlave(busbase):
  # Variable: _signals
  # List of signals that are required
  _signals = ["addr", "we", "cs", "data"]

  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, reset, numreg=256, *args, **kwargs):
    super().__init__(entity, name, clock, *args, **kwargs)

    self.log.info("BASIC Slave")
    self.log.info("Copyright (c) 2025 Jay Convertino")
    self.log.info("https://github.com/johnathan-convertino-afrl/cocotbext-busbase")

    self._reset = reset

    self._registers = {}

    for i in range(numreg):
      self._registers[i] = 0

  # Function: _check_type
  # Check and make sure we are only sending 2 bytes at a time and that it is a bytes/bytearray
  def _check_type(self, trans):
      if(not isinstance(trans, basictrans)):
          self.log.error(f'Transaction must be of type: {type(basictrans)}')
          return False

      return True

  # Method: _run
  # _run thread that deals with read and write.
  async def _run(self):
    self.active = False

    trans = None

    while True:

      await Edge(self.bus.we)

      if self._reset.value:
        continue

      if self.bus.cs.value:
        if self.bus.we.value:
          await FallingEdge(self.clock)
          self._registers[self.bus.addr.value.integer] = self.bus.data.value.integer
        else:
          self.bus.data.value = self._registers[self.bus.addr.value.integer]

        self.acitve = True
      else:
        self.active = False


# Class: TB
# Create the device under test which is the master/slave.
class TB:
    def __init__(self, dut):
        self.dut = dut

        self.log = logging.getLogger("cocotb.tb")
        self.log.setLevel(logging.DEBUG)

        cocotb.start_soon(Clock(dut.clk, 2, units="ns").start())

        self.master  = basicMaster(dut, "b", dut.clk, dut.rst)
        self.slave = basicpEchoSlave(dut, "b", dut.clk, dut.rst)

    async def reset(self):
        self.dut.rst.setimmediatevalue(1)
        await Timer(20, units="ns")
        self.dut.rst.value = 0

# Function: run_test
# Tests the source/sink for valid transmission of data.
async def run_test(dut, payload_data=None):

    tb = TB(dut)

    await tb.reset()

    for test_data in payload_data():

        tb.log.info(f'TEST VALUE : {test_data, test_data}')

        await tb.master.write(test_data, test_data)

        rx_data = await tb.master.read(test_data)

        assert test_data == rx_data, "RECEIVED DATA DOES NOT MATCH"

# Function: incrementing_payload
# Generate a list of ints that increment from 0 to 2^8
def incrementing_payload():
    return list(range(2**8))

# # Function: random_payload
# # Generate a list of random ints 2^16 in the range of 0 to 2^16
# def random_payload():
#     return random.sample(range(2**16), 2**16)


# If its a sim... create the test factory with these options.
if cocotb.SIM_NAME:

    factory = TestFactory(run_test)
    factory.add_option("payload_data", [incrementing_payload])
    factory.generate_tests()


# cocotb-test
tests_dir = os.path.dirname(__file__)

# Function: test
# Main cocotb function that specifies how to put the test together.
def test(request):
    dut = "test"
    module = os.path.splitext(os.path.basename(__file__))[0]
    toplevel = dut

    verilog_sources = [
        os.path.join(tests_dir, f"{dut}.v"),
    ]

    parameters = {}

    extra_env = {f'PARAM_{k}': str(v) for k, v in parameters.items()}

    sim_build = os.path.join(tests_dir, "sim_build",
        request.node.name.replace('[', '-').replace(']', ''))

    cocotb_test.simulator.run(
        python_search=[tests_dir],
        verilog_sources=verilog_sources,
        toplevel=toplevel,
        module=module,
        parameters=parameters,
        sim_build=sim_build,
        extra_env=extra_env,
    )
