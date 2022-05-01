# Парсинг
import re


s =''
'''
module Y8 (
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

def getInstance(s, postfix ='_0'):
    # пустая строка
    if s == '':
        return f'Введена пустая строка'
    # оставим только содержимое модуля
    ModuleString = s[s.find('module') : s.find(');')+2]
    #print('Содержимое модуля: ', ModuleString)
    # добавим пробелы после символов (),
    #s=''.join((' {} '.format(el) if el in '(),' else el for el in ModuleString))
    # преобразуем в список, чтобы далее разбить на слова

    # запомним имя модуля
    ModuleName = ModuleString[ ModuleString.find('module') + 7: ModuleString.find('(') - 1 ].strip()
    # если не нашлось модуля
    if ModuleName == '':
        ModuleName = 'ModuleName' #Не смог найти имя модуля, может быть так и зажумано'

    print('имя модуля: ', ModuleName)

    remove_list = ['input','output', 'reg', 'wire', 'int', 'bit', 'logic', 'packet_t', ',']
    ports = []
    # разбиваем на строки по запятой и делим на строки
    d = ModuleString.replace(",", ",\n")
    lines = d.split('\n')

    InputCount, OutputCount = 0, 0

    for line in lines:
        result1 = re.match(r'(.+)[input|output] (.+),', line)
        result2 = re.match(r'(.+)[input|output] (.+)', line)
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
    print('inputs:', ports)

    # имя
    out = ModuleName + ' ' + ModuleName + postfix+' (\n'
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
    #print(out)
    return out


if __name__ == "__main__":
    getInstance(s)