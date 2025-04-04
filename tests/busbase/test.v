//******************************************************************************
// file:    test.v
//
// author:  JAY CONVERTINO
//
// date:    2025/04/04
//
// about:   Brief
// Test bench for busbase
//
// license: License MIT
// Copyright 2025 Jay Convertino
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to
// deal in the Software without restriction, including without limitation the
// rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
// sell copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
// IN THE SOFTWARE.
//
//******************************************************************************

`timescale 1ns/100ps

/*
 * Module: test
 *
 * Test bench loop busbase example
 *
 * Parameters:
 *
 *   ADDRESS_WIDTH   - Width of the address in bits.
 *   BUS_WIDTH       - Width of the data in bytes.
 *
 * Ports:
 *
 *   clk            - Clock for all devices in the core
 *   rst            - Negative reset
 *   b_addr         - address to read write from
 *   b_we           - write enable 1, read 0
 *   b_cs           - chip select, 1 selected
 *   b_data         - data input/output
 */
module test #(
    parameter ADDRESS_WIDTH = 32,
    parameter BUS_WIDTH = 4
  )
  (
    input                       clk,
    input                       rst,
    inout [ADDRESS_WIDTH-1:0]   b_addr,
    inout                       b_we,
    inout                       b_cs,
    inout [(BUS_WIDTH*8)-1:0]   b_data
  );

  //copy pasta, fst generation
  initial
  begin
    $dumpfile("test.fst");
    $dumpvars(0,test);
  end

endmodule
