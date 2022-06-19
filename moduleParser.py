# Парсинг
import re

# добавим пробелы после символов (),
# s=''.join((' {} '.format(el) if el in '(),' else el for el in ModuleString))
# преобразуем в список, чтобы далее разбить на слова

s =\
'''module equals(
  inout [ `def:0 ] i_a,
  input i_b = 0,
  input i_c= 0,          //  comment
  input i_d =0,
  input i_e=0);
reg        o_z;
'''


def getInstance (s, postfix ='_0'):
    # пустая строка
    if s == '':
        return f'Введена пустая строка'
    s = deleteComments(s)
    # определим язык, verilog vs VHDL
    language = identifyProgLang(s)

    if language == 'verilog':
        # запомним имя модуля
        ModuleName = s[s.find('module') + 7: s.find('(')].strip()
        # если скобки содержат описания направления портов
        if re.match(r'(.*?)[input|output|inout] (.*?)\);', s, flags=re.S):
            ports = parseVerilogPatternRoundBrackets(s)
        else:
            ports = parseVerilogPatternPatternPorts(s)
    elif language == 'VHDL':
        return 'VHDL сейчас не поддерживается'
    else:
        return 'Не удалось найти модуль'
    return createModule(ports, ModuleName, postfix)

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


def parseVerilogPatternRoundBrackets(s):
    # получим содержание скобок модуля
    ModuleString = s[s.find('module'): s.find(');') + 2]

    remove_list = ['input', 'output', 'inout', 'reg', 'wire', 'int', 'bit', 'logic', 'packet_t', ',']
    ports = []
    # разбиваем на строки по запятой и делим на строки
    d = ModuleString.replace(",", ",\n")

    lines = d.split('\n')

    for line in lines:
        result1 = re.match(r'(.+)[input|output|inout] (.+),', line)
        result2 = re.match(r'(.+)[input|output|inout] (.+)', line)
        if result1 is not None:
            # удалить [*]
            line = [re.sub(r'\[[^\[\]]*\]\ ', '', line)]
            # удалить [=*]
            line = [''.join(line).split("=")[0]]
            # Удалить из списка
            buf = (''.join([x for x in re.split(r'(\W+)', ' '.join(line)) if x not in remove_list]))
            # удалить запятые
            buf = re.sub(r',', '', buf)
            # убрать пробелы и таб
            buf = buf.split()
            ports.append(buf[0])
        # обработка последней строки
        if result1 == None and result2 != None:
            # удалить [*]
            last = [re.sub(r'\[[^\[\]]*\]\ ', '', line)]
            # удалить [=*]
            last = [''.join(last).split("=")[0]]
            # Удалить из списка
            last = (''.join([x for x in re.split(r'(\W+)', ' '.join(last)) if x not in remove_list]))
            # удалить запятые
            last = re.sub(r',', '', last)
            last = last.split()
    if 'last' in locals():
        ports.append(last[0])
    return ports


def parseVerilogPatternPatternPorts(s):
    # оставим только то, что в скобках
    res = s[s.find('(')+1: s.find(')')]
    # удалим все пробелы и переносы
    res = ''.join(res.split())
    # получим список портов
    ports = res.split(',')
    return ports


def createModule (ports, ModuleName, postfix):
    # формируем результат
    try:
        # имя
        out = ModuleName + ' ' + ModuleName + postfix + ' (\n'
        # переменные
        maxLen = len(max(ports, key=len))
        for i, item in enumerate(ports):
            out += ('.' + item.ljust(maxLen, ' ') + ' (  )')
            if i != len(ports) - 1:
                out += ',\n'
        print('\n')
        # закрывающая строка
        out += '\n);'
    except:
        out += 'Не нашел ни одного порта);'
    return out

if __name__ == "__main__":
    print(getInstance(s))
