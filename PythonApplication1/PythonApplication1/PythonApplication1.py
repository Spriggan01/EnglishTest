import numpy as np
import re
import random
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext


####################################
# ������������ ����� �� ���� �������
####################################

window = tk.Tk()

# ���������� ����� ���� �� txt �����
text_path = filedialog.askopenfilename(title='Choose the test, please')

window.destroy()

# ������� ���� ����� �� ��������� ���������
with open(text_path, 'r', encoding='utf-8') as file:
    Text = file.read()
    Text = Text.replace("\t", "")

# ��������� ���� �� ����� �� ������� �� ��������� ���� �����
Text = Text.split(sep='\n')

# �������� �������
pattern = r'^\d{1,3}\.'  # ����� ���������� � 1 ��� 2 ����, � ��� ��� ������ (max ������ - 999)
Text_q = [i for i in Text if len(re.findall(pattern, i)) != 0]
print('Number of questions:', len(Text_q))

# �������� ������
pattern = r'^[A-Z]'  # ����� ���������� � ����-��� ������ �������� �����
Text_a = [i for i in Text if len(re.findall(pattern, i)) != 0]
print('Number of answers:', len(Text_a))

# ��������� ������ � ��������� ��� "+" �� ����� � ������
pattern = r'\+'  # ������ ����� � ����� "+"
Text_a_last = []
flags = np.zeros(320)

for i, st in enumerate(Text_a):
    if len(re.findall(pattern, st)) != 0:  # ���� � ����� � �� ����
        new_i = re.sub(r'\+', '', st)  # ��������� �Ѳ ����
        Text_a_last.append(new_i)
        flags[i] = 1
    else:
        Text_a_last.append(st)

Text_a = Text_a_last
print('Number of correct answers:', flags.sum())


################################################################
# ���� ������ (��������� ������� �������� vs ��������� �������)
################################################################

window = tk.Tk()
window.title('Test')
window.resizable(width=False, height=False)
window.geometry('240x60+700+300')
window['bg'] = 'white'

# ������� �������� ���� ��� ����� ���������� �������
def accept():
    window.destroy()

RandomState = tk.IntVar()  # � �� ����� ���������� ���� box (1 ��� 0)
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
# ��������� ������ � �������� ������
####################################

Text_q_dict = {}
for i, q in enumerate(Text_q):
    Text_q_dict[i] = q

np1 = np.arange(len(Text_q))
order_list = np1.tolist()

# ���� ������ ��������� �����, �� ��������� �������
if RandomState.get():
    random.shuffle(order_list)


####################
# ���� ������� ����
####################

class Block:

    # ����������� ��'�����
    def __init__(self, master):

        # �������� ������� ������
        self.qc = 0

        # �������� ������� ���������� ��������
        self.true_points = 0

        # ����������� ������� �� ��������
        self.quest = scrolledtext.ScrolledText(window, width=75, height=5)
        index = order_list[self.qc]  # ������ ������� ��������� �� order_list
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

        # ����������� ����� ������ ��������
        self.check1 = tk.IntVar()  # � �� ����� ���������� ���� box1 (1 ��� 0)
        self.box1 = Checkbutton(text='A', variable=self.check1, font=('Consolas', 14))

        self.check2 = tk.IntVar()
        self.box2 = Checkbutton(text='B', variable=self.check2, font=('Consolas', 14))

        self.check3 = tk.IntVar()
        self.box3 = Checkbutton(text='C', variable=self.check3, font=('Consolas', 14))

        self.check4 = tk.IntVar()
        self.box4 = Checkbutton(text='D', variable=self.check4, font=('Consolas', 14))

        # ����������� ������ �� ������
        self.mark = tk.Label(window, text='Choose the answer: ', font=('Consolas', 12), fg='Green', bg='white')

        self.ButGiveAns = Button(text='Answer', font=('Consolas', 12))  # ������ �������� � ���� "����²���"
        self.ButGiveAns['command'] = self.show_res

        self.ButNext = Button(text='Next', font=('Consolas', 12))  # ������ �������� � ���� "�̲�� �������"
        self.ButNext['command'] = self.next_q

        # ������������ ������
        self.quest.place(x=50, y=25)
        self.ans.place(x=50, y=150)

        self.box1.place(x=270, y=420)
        self.box2.place(x=320, y=420)
        self.box3.place(x=370, y=420)
        self.box4.place(x=420, y=420)

        self.mark.place(x=50, y=420)
        self.ButGiveAns.place(x=500, y=420)
        self.ButNext.place(x=600, y=420)

    # ������� ������� ��䳿 "����²���" (���������� ������ "Answer")
    def show_res(self):

        # ��������� �������� ������ �������
        index = order_list[self.qc]

        # ��������� ������ ������� �� ��������
        targets = flags[4 * index: 4 * index + 4]
        answers = np.zeros(4)

        answers[0] = self.check1.get()  # �������� ���� box1 (0 ��� 1) � �������� �� ������� answers
        answers[1] = self.check2.get()
        answers[2] = self.check3.get()
        answers[3] = self.check4.get()

        # �������� �������� ������ ������� �������� (����� ��� ��������)
        for i, box in enumerate([self.box1, self.box2, self.box3, self.box4]):
            if targets[i] == 1:
                box['bg'] = 'green'

        # �������� ������ ����������� (��������� ������� ������ � �������� �������)
        if (targets == answers).sum() == 4:
            self.mark['text'] = 'CORRECR!'  # ������� ����� ���� �� ������ "Correct!"
            self.true_points += 1  # ���� ��� ����, �� ������ ���
        else:
            self.mark['text'] = 'INCORRECT!'

    # ������� ������� ��䳿 "�̲�� �������" (���������� ������ "Next")
    def next_q(self):

        # ������������ �������� ������
        self.qc += 1

        # ���� ������� �� �� ������� -> �������� �������
        if self.qc >= len(Text_q):
            self.FinalScore = tk.Label(window, text=f'Number of correct answers: {self.true_points}',
                                       font=('Consolas', 14), fg='white', bg='grey')
            self.FinalScore.place(x=360, y=210)

        else:  # � ����� ��������:

            # ��������� �������� ������ �������
            index = order_list[self.qc]

            # ��������� ������� ��������
            for i, box in enumerate([self.box1, self.box2, self.box3, self.box4]):
                box['bg'] = 'white'
                box.deselect()

            # ���� �������
            self.quest.delete('1.0', 'end')  # �������� ��� ���� � ������� "1" �� ���������� "end"
            self.quest.insert(tk.INSERT, Text_q[index])  # �������� �������� �������

            # ���� ��������
            self.ans.delete('1.0', 'end')
            self.ans.insert(tk.INSERT,
                            f'''
            {Text_a[4 * index + 0]}
            {Text_a[4 * index + 1]}
            {Text_a[4 * index + 2]}
            {Text_a[4 * index + 3]}
            '''
                            )

            # ������� ������ ����
            self.mark['text'] = 'Choose the answer: '


###############
# �������� ����
###############

window = tk.Tk()
window.title('Test')
window.resizable(width=False, height=False)
window.geometry('720x480+400+100')
window['bg'] = 'grey'

first_block = Block(window)

window.mainloop()