# Парсинг
import re

# добавим пробелы после символов (),
# s=''.join((' {} '.format(el) if el in '(),' else el for el in ModuleString))
# преобразуем в список, чтобы далее разбить на слова

s ='''module Y8 (
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
def getInstance(s, postfix ='_0'):
    # пустая строка
    if s == '':
        return f'Введена пустая строка'
    s = deleteComments(s)
    # определим язык, verilog vs VHDL
    language = identifyProgLang(s)

    if language == 'verilog':
        # запомним имя модуля
        ModuleName = s[s.find('module') + 7: s.find('(') - 1].strip()
        print(ModuleName)
        # если скобки содержат описания направления портов
        if re.match(r'(.*?)[input|output|inout] (.*?)\);', s, flags=re.S):
            ports = parseVerilogPatternSimple(s)
        else:
            ports = parseVerilogPatternHard(s)

    # формируем результат
    # имя
    out = 'module' + ' ' + ModuleName + postfix+' (\n'
    try:
        # переменные
        maxLen = len( max( ports, key=len ) )
        for i, item in enumerate(ports):
            out += ('.' + item.ljust(maxLen, ' ') + ' (  )')
            if i != len(ports)-1:
                out += ',\n'
        print('\n')
        out += '\n);'
    except:
        out += 'Не нашел ни одного порта);'
    # закрывающая строка
    print(out)
    return out


def deleteComments (s):
    # удалим все комментарии // и /* */
    return re.sub('//.*?\n|/\*.*?\*/', '', s, flags=re.S)


def identifyProgLang (s):
    if re.search(r'module.*?\(', s, flags=re.S):
        return 'verilog'
    elif re.search(r'entity.*?is', s, flags=re.S):
        return 'VHDL'
    else:
        return None


def parseVerilogPatternSimple(s):
    # получим содержание скобок модуля
    ModuleString = s[s.find('module'): s.find(');') + 2]

    remove_list = ['input', 'output', 'inout', 'reg', 'wire', 'int', 'bit', 'logic', 'packet_t', ',']
    ports = []
    # разбиваем на строки по запятой и делим на строки
    d = ModuleString.replace(",", ",\n")
    lines = d.split('\n')

    InputCount, OutputCount = 0, 0

    for line in lines:
        result1 = re.match(r'(.+)[input|output|inout] (.+),', line)
        result2 = re.match(r'(.+)[input|output|inout] (.+)', line)
        if result1 is not None:
            # удалить [*]
            line = [re.sub(r'\[[^\[\]]*\]\ ', '', line)]
            # Удалить из списка
            buf = (''.join([x for x in re.split(r'(\W+)', ' '.join(line)) if x not in remove_list]))
            # удалить запятые
            buf = re.sub(r',', '', buf)
            # убрать пробелы и таб
            buf = buf.split()
            ports.append(buf[0])
        # обработка последней строки
        if result1 == None and result2 != None:
            last = [re.sub(r'\[[^\[\]]*\]\ ', '', line)]
            last = (''.join([x for x in re.split(r'(\W+)', ' '.join(last)) if x not in remove_list]))
            last = re.sub(r',', '', last)
            last = last.split()
    if 'last' in locals():
        ports.append(last[0])
    return ports

def parseVerilogPatternHard(s):

    pass

if __name__ == "__main__":
    getInstance(s)