import unittest
import moduleParser

class TestModuleParser(unittest.TestCase):
    def setUp(self):
        self.stringPattern1 = \
        '''module Y8 (
  output 	      i_CLK_13m5,    	//  serial clock
  input 	      i_RST,          	//  hight for reset
  input           i_EN,             //  system i_ENable
  //  module Y8
  input  [7:0] i_Y_data,         //  data in

  output [ 9 : 0] PIX_CNT_o,   //  pix count.
  output [ 9 : 0] LINE_CNT_o,       //  Line count,
  output          VSYNC_o,          //  vertical synchronization
  output          HSYNC_o,          //  horizontal synchronization
  inout          DATA_RQ_o,        //  active area

  output [ 7 : 0] Y_data_o          //  parallel output
);

reg simpleREG;
wire [0:600] someWire; // comment
//block comment

/* input reg commetnReg;
// comment
assign ww = PIX_CNT_o ^ LINE_CNT_o;
*/

endmodule
        '''
        self.StringResultPattern1 = \
            '''module Y8_0 (
.i_CLK_13m5 (  ),
.i_RST      (  ),
.i_EN       (  ),
.i_Y_data   (  ),
.PIX_CNT_o  (  ),
.LINE_CNT_o (  ),
.VSYNC_o    (  ),
.HSYNC_o    (  ),
.DATA_RQ_o  (  ),
.Y_data_o   (  )
);'''

        self.stringPattern2 = \
'''module Y8 (i_CLK_13m5, i_RST, 
  HSYNC_o,          //  horizontal synchronization
  DATA_RQ_o);
output 	       i_CLK_13m5;
input 	       i_RST;
output         HSYNC_o;
inout          DATA_RQ_o;
'''

        self.StringResultPattern2 = \
'''module Y8_0 (
.i_CLK_13m5 (  ),
.i_RST      (  ),
.HSYNC_o    (  ),
.DATA_RQ_o  (  )
);'''
    def test_zeroString(self):
        self.assertEqual(moduleParser.getInstance(''), 'Введена пустая строка')

    def test_String_pattern1(self):
        self.assertEqual(moduleParser.getInstance(self.stringPattern1), self.StringResultPattern1)
    def test_String_pattern2(self):
        self.assertEqual(moduleParser.getInstance(self.stringPattern2), self.StringResultPattern2)



if __name__ == "__main__":
    unittest.main()