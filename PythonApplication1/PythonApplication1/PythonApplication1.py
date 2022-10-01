import numpy as np
import re
import random
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext


####################################
# Завантаження тесту та його парсинг
####################################

window = tk.Tk()

# Користувач вказує шлях до txt файлу
text_path = filedialog.askopenfilename(title='Choose the test, please')

window.destroy()

# зчитуємо вміст файлу та видаляємо табуляцію
with open(text_path, 'r', encoding='utf-8') as file:
    Text = file.read()
    Text = Text.replace("\t", "")

# розділяємо файл на рядки по пробілам та видаляємо пусті рядки
Text = Text.split(sep='\n')

# відділяємо питання
pattern = r'^\d{1,3}\.'  # рядок починається з 1 або 2 цифр, а далі йде крапка (max питань - 999)
Text_q = [i for i in Text if len(re.findall(pattern, i)) != 0]
print('Number of questions:', len(Text_q))

# відділяємо відповіді
pattern = r'^[A-Z]'  # рядок починається з будь-якої великої англійскої літери
Text_a = [i for i in Text if len(re.findall(pattern, i)) != 0]
print('Number of answers:', len(Text_a))

# створюємо список з відповідями без "+" та масив з мітками
pattern = r'\+'  # шукаємо рядки з міткою "+"
Text_a_last = []
flags = np.zeros(320)

for i, st in enumerate(Text_a):
    if len(re.findall(pattern, st)) != 0:  # якщо у рядку є ці мітки
        new_i = re.sub(r'\+', '', st)  # видаляємо ВСІ мітки
        Text_a_last.append(new_i)
        flags[i] = 1
    else:
        Text_a_last.append(st)

Text_a = Text_a_last
print('Number of correct answers:', flags.sum())


################################################################
# Вибір режиму (Рандомний порядок вопросов vs звичайний порядок)
################################################################

window = tk.Tk()
window.title('Test')
window.resizable(width=False, height=False)
window.geometry('240x60+700+300')
window['bg'] = 'white'

# функція закриття вікна при виборі рандомного порядку
def accept():
    window.destroy()

RandomState = tk.IntVar()  # в цю змінну записується стан box (1 или 0)
box = Checkbutton(window, text='Random choice',
                  variable=RandomState,
                  font=('Consolas', 10),
                  relief='solid',
                  bd='1'
                  )
box['command'] = accept
box.place(x=12, y=20)

window.mainloop()


####################################
# Отримання списку з порядком питань
####################################

Text_q_dict = {}
for i, q in enumerate(Text_q):
    Text_q_dict[i] = q

np1 = np.arange(len(Text_q))
order_list = np1.tolist()

# Якщо обрано рандомний режим, то перемішуємо питання
if RandomState.get():
    random.shuffle(order_list)


####################
# Блок обробки подій
####################

class Block:

    # Ініціалізація об'єктов
    def __init__(self, master):

        # лічильник кількості питань
        self.qc = 0

        # лічильник кількості правильних відповідей
        self.true_points = 0

        # Ініціалізація питання та відповідей
        self.quest = scrolledtext.ScrolledText(window, width=75, height=5)
        index = order_list[self.qc]  # індекс питання визначаємо по order_list
        self.quest.insert(tk.INSERT, Text_q[index])

        self.ans = scrolledtext.ScrolledText(window, width=75, height=15)
        self.ans.insert(tk.INSERT,
                        f'''
        {Text_a[4 * index + 0]}
        {Text_a[4 * index + 1]}
        {Text_a[4 * index + 2]}
        {Text_a[4 * index + 3]}
        '''
                        )

        # Ініціалізація боксів вибору відповідей
        self.check1 = tk.IntVar()  # в цю змінну записується стан box1 (1 або 0)
        self.box1 = Checkbutton(text='A', variable=self.check1, font=('Consolas', 14))

        self.check2 = tk.IntVar()
        self.box2 = Checkbutton(text='B', variable=self.check2, font=('Consolas', 14))

        self.check3 = tk.IntVar()
        self.box3 = Checkbutton(text='C', variable=self.check3, font=('Consolas', 14))

        self.check4 = tk.IntVar()
        self.box4 = Checkbutton(text='D', variable=self.check4, font=('Consolas', 14))

        # Ініціалізація лейблів та кнопок
        self.mark = tk.Label(window, text='Choose the answer: ', font=('Consolas', 12), fg='Green', bg='white')

        self.ButGiveAns = Button(text='Answer', font=('Consolas', 12))  # кнопка переходу в стан "ПЕРЕВІРКА"
        self.ButGiveAns['command'] = self.show_res

        self.ButNext = Button(text='Next', font=('Consolas', 12))  # кнопка переходу в стан "ЗМІНА ПИТАННЯ"
        self.ButNext['command'] = self.next_q

        # Позиціювання віджитів
        self.quest.place(x=50, y=25)
        self.ans.place(x=50, y=150)

        self.box1.place(x=270, y=420)
        self.box2.place(x=320, y=420)
        self.box3.place(x=370, y=420)
        self.box4.place(x=420, y=420)

        self.mark.place(x=50, y=420)
        self.ButGiveAns.place(x=500, y=420)
        self.ButNext.place(x=600, y=420)

    # Функція обробки події "ПЕРЕВІРКА" (натиснення кнопки "Answer")
    def show_res(self):

        # визначаємо поточний індекс питання
        index = order_list[self.qc]

        # створюємо вектор таргетів та відповідей
        targets = flags[4 * index: 4 * index + 4]
        answers = np.zeros(4)

        answers[0] = self.check1.get()  # записуємо стан box1 (0 або 1) в нульовий біт вектора answers
        answers[1] = self.check2.get()
        answers[2] = self.check3.get()
        answers[3] = self.check4.get()

        # підсвічуємо правильні відповіді зеленим колорьом (задній фон чекбоксів)
        for i, box in enumerate([self.box1, self.box2, self.box3, self.box4]):
            if targets[i] == 1:
                box['bg'] = 'green'

        # перевірка відповіді користувача (порівняння вектору відповіді з вектором таргету)
        if (targets == answers).sum() == 4:
            self.mark['text'] = 'CORRECR!'  # змінюємо текст мітки на статус "Correct!"
            self.true_points += 1  # якщо все вірно, то додаємо бал
        else:
            self.mark['text'] = 'INCORRECT!'

    # Функція обробки події "ЗМІНА ПИТАННЯ" (натиснення кнопки "Next")
    def next_q(self):

        # інкрементуємо лічильник питань
        self.qc += 1

        # коли відповіли на всі питання -> підводимо підсумки
        if self.qc >= len(Text_q):
            self.FinalScore = tk.Label(window, text=f'Number of correct answers: {self.true_points}',
                                       font=('Consolas', 14), fg='white', bg='grey')
            self.FinalScore.place(x=360, y=210)

        else:  # в інших випадках:

            # визначаємо поточний індекс питання
            index = order_list[self.qc]

            # видаляємо підсвітку чукбоксів
            for i, box in enumerate([self.box1, self.box2, self.box3, self.box4]):
                box['bg'] = 'white'
                box.deselect()

            # зміна питання
            self.quest.delete('1.0', 'end')  # очищаемо все поле з индексу "1" до останнього "end"
            self.quest.insert(tk.INSERT, Text_q[index])  # виводимо наступне питання

            # зміна відповідей
            self.ans.delete('1.0', 'end')
            self.ans.insert(tk.INSERT,
                            f'''
            {Text_a[4 * index + 0]}
            {Text_a[4 * index + 1]}
            {Text_a[4 * index + 2]}
            {Text_a[4 * index + 3]}
            '''
                            )

            # змінюємо статус мітки
            self.mark['text'] = 'Choose the answer: '


###############
# Основний цикл
###############

window = tk.Tk()
window.title('Test')
window.resizable(width=False, height=False)
window.geometry('720x480+400+100')
window['bg'] = 'grey'

first_block = Block(window)

window.mainloop()