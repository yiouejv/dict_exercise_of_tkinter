import tkinter as tk
import tkinter.messagebox as tb
import random

dict_words = {}  # 空的单词字典库
var_exer_word = ''
var_exer_parse = ''
random_count = 0  # 统计抽取的个数
font_size = 14  # 默认字体大
filename = 'words.csv'

def to_csv(var_word, var_parse):
    if var_word in ('', '\n') or var_parse in ('', '\n'):
        tb.showinfo('提示', '单词或释义不能为空')
        return
    dict_words = load_csv()
    for word in dict_words:  # 判断是否重复添加
        if word == var_word:
            tb.showinfo('提示', '%s单词已存在文件中' % var_word)
            return
    with open(filename, 'at', encoding='utf-8') as wf:
        wf.write(var_word + '|' + var_parse + '\n')
    tb.showinfo('提示', '已成功添加单词：%s, 释义：%s' % (var_word, var_parse))


def load_csv():
    '''读取单词文件，返回单词字典'''
    with open(filename, 'rt', encoding='utf-8') as rf:
        s = rf.read()
    words = s.split('\n')[:-1]
    dict_words = {}  # 单词存入字典，英文为键， 中文为值
    for word in words:
        key = word.split('|')[0]
        value = word.split('|')[1]
        dict_words[key] = value
    return dict_words


def random_words_parse():
    '''返回单词和解释'''
    global dict_words, var_exer_word, var_exer_parse, flag, random_count
    keys = []
    for key in dict_words.keys():
        keys.append(key)  # 把所有的英文单词放入列表
    try:
        word = random.choice(keys)
        print('英文：', word)
        var_exer_word = word
        var_exer_parse = dict_words[word]
        print('中文：', dict_words[word])
        random_count += 1
        del dict_words[word]
        if len(dict_words) == 1:  # 抽完了
            return False
        return True
    except:
        pass


def get_e_word(e_word, e_parse):
    var_word = e_word.get().strip()
    var_parse = e_parse.get()
    to_csv(var_word, var_parse)
    # print('get_e_word', var_word)
    # print('get_e_word', var_parse)


def cilck_random_word(var_screen):
    if random_words_parse():
        var_screen.set('抽取好了哦! 这是第%d个' % random_count)
    else:
        var_screen.set('全都看过啦, 没单词啦!!!')


def select_word_parse(e_select, var_screen):
    dict_wds = load_csv()
    for key in dict_wds:  # 判断是否是英文
        var = e_select.get()
        if var == key:
            count = 0  # 统计中文字符的个数
            for ch in var:
                if ord(ch) > 128:
                    count += 1
            if len(dict_wds[key]) > 25:
                var_screen.set(dict_wds[key][:25+count*2] + '\n' + dict_wds[key][25+count*2:])
            else:
                var_screen.set(dict_wds[key])
            return

    for value in dict_wds.values():  # 如果输入的时中文
        if e_select.get() == value:
            for k in dict_wds.keys():  # 判断是否存在对应的
                if dict_words[k] == value:
                    count = 0  # 统计中文字符的个数
                    for ch in value:
                        if ord(ch) > 128:
                            count += 1
                    if len(e_select.get()) > 25:
                        var_screen.set(k[:25+count*2] + '\n' + k[25+count*2:])
                    else:
                        var_screen.set(k)
                    return
    else:
        var_screen.set('库中无释义对应的英文')
        return

def var_screen_set(var_screen, var_exer):
    if len(var_exer) > 25:
        var_screen.set(var_exer[:25] + '\n' + var_exer[25:])
    else:
        var_screen.set(var_exer)


def ui():
    global font_size
    window = tk.Tk()
    window.title('单词训练程序 by 杨文俊')
    window.geometry('500x400+500+300')
    lbl_word = tk.Label(window, text='英文单词', width=10, height=3)
    lbl_word.place(x = 5, y = 250)
    var_word = tk.StringVar()
    var_screen = tk.StringVar()
    var_parse = tk.StringVar()
    var_select = tk.StringVar()
    e_word = tk.Entry(window, textvariable=var_word, width=45)
    e_word.place(x = 90, y = 268)
    btn_word_reset = tk.Button(window, text='重置', width=3, height=1,
                        command=lambda: var_word.set(''))
    btn_word_reset.place(x = 430, y = 268)
    tk.Label(window, text='中文释义', width=10, height=3).place(x = 5, y = 290)
    e_parse = tk.Entry(window, textvariable=var_parse, width=45)
    e_parse.place(x = 90, y = 310)
    tk.Button(window, text='重置',width=3, height=1,
                        command=lambda : var_parse.set('')).place(x = 430, y = 305)
    tk.Button(window, text = '随机抽取单词', width=10, height=1,
                        command=lambda :cilck_random_word(var_screen)).place(x = 50, y = 120)
    btn_add = tk.Button(window, text='添加单词', width=10, height=1,
                        command=lambda :get_e_word(e_word, e_parse))
    btn_add.place(x = 300, y = 350)
    tk.Label(window, textvariable=var_screen, width=100, height=3, font=('黑体', font_size),
                          background='green').pack(side='top')
    tk.Button(window, text='英文', width=8, height=1,
              command=lambda : var_screen_set(var_screen, var_exer_word)).place(x=200, y=120)
    tk.Button(window, text='释义', width=8, height=1,
              command=lambda : var_screen_set(var_screen, var_exer_parse)).place(x=350, y=120)
    e_select = tk.Entry(window, textvariable=var_select, width=20)
    e_select.place(x=120, y=180)
    tk.Button(window, width=8, height=1, text='查询',
              command=lambda : select_word_parse(e_select, var_screen)).place(x=300, y=175)
    window.update_idletasks()
    return window


def main():
    global dict_words
    dict_words = load_csv()
    window = ui()
    window.mainloop()


if __name__ == '__main__':
    main()