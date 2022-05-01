import unittest
import moduleParser

class TestModuleParser(unittest.TestCase):
    def setUp(self):
        self.SimpleString = \
        '''
        module module (
          input 	      i_CLK_13m5,    	//  serial clock 
          input 	      i_RST,          	//  hight for reset
          input           i_EN,             //  system i_ENable
          //  Y8                 
          input  [ 7 : 0] i_Y_data,         //  data in
        
          
          output [ 9 : 0] PIX_CNT_o,        //  pix count.
          output [ 9 : 0] LINE_CNT_o,       //  Line count
          output          VSYNC_o,          //  vertical synchronization
          output          HSYNC_o,          //  horizontal synchronization 
          output          DATA_RQ_o,        //  active area 
        
          output [ 7 : 0] Y_data_o          //  parallel output            
        );
        other tings text
        reg dsfasf;
        wire [0:600] dfasf; 
        endmodule
        '''
        self.SimpleStringResult = \
            '''module module_0 (
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
    def test_SimpleString(self):
        self.assertEqual(moduleParser.getInstance(self.SimpleString), self.SimpleStringResult)

    def test_zeroString(self):
        self.assertEqual(moduleParser.getInstance(''), 'Введена пустая строка')


if __name__ == "__main__":
    unittest.main()