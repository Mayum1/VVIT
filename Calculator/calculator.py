import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()

        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_fourth = QHBoxLayout()
        self.hbox_result = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_fourth)
        self.vbox.addLayout(self.hbox_result)

        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)

        self.b_delete = QPushButton("C", self)
        self.hbox_first.addWidget(self.b_delete)

        self.b_change = QPushButton("+/-", self)
        self.hbox_first.addWidget(self.b_change)

        self.b_percent = QPushButton("%", self)
        self.hbox_first.addWidget(self.b_percent)

        self.b_1 = QPushButton("1", self)
        self.hbox_fourth.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_fourth.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_fourth.addWidget(self.b_3)

        self.b_4 = QPushButton("4", self)
        self.hbox_third.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_third.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_third.addWidget(self.b_6)

        self.b_7 = QPushButton("7", self)
        self.hbox_second.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_second.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_second.addWidget(self.b_9)

        self.b_0 = QPushButton("0", self)
        self.hbox_result.addWidget(self.b_0)

        self.b_plus = QPushButton("+", self)
        self.hbox_fourth.addWidget(self.b_plus)

        self.b_minus = QPushButton("-", self)
        self.hbox_third.addWidget(self.b_minus)

        self.b_multiply = QPushButton("*", self)
        self.hbox_second.addWidget(self.b_multiply)

        self.b_division = QPushButton("/", self)
        self.hbox_first.addWidget(self.b_division)

        self.b_dot = QPushButton(".", self)
        self.hbox_result.addWidget(self.b_dot)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.b_plus.clicked.connect(lambda: self._operation("+"))
        self.b_minus.clicked.connect(lambda: self._operation("-"))
        self.b_multiply.clicked.connect(lambda: self._operation("*"))
        self.b_division.clicked.connect(lambda: self._operation("/"))
        self.b_delete.clicked.connect(lambda: self._operation("C"))
        self.b_result.clicked.connect(self._result)

        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_dot.clicked.connect(lambda: self._button("."))
        self.b_change.clicked.connect(lambda: self._button("+/-"))
        self.b_percent.clicked.connect(lambda: self._button("%"))

        self.input.setText('0')

    def _button(self, param):
        if self.input.text() == '0' and param != "+/-" and param != "%" and param != ".":
            self.input.setText(param)
        elif (self.input.text() == '0' or self.input.text() == '') and param == '.':
            self.input.setText("0" + param)
        elif param == "+/-" and self.input.text() != "0":
            line = float(self.input.text())
            self.input.setText(str(line * -1))
        elif param == "%" and self.input.text() != "0":
            line = float(self.input.text())
            self.input.setText(str(line / 100))
        elif ('.' not in self.input.text() or param != '.') and param != "+/-" and param != "%":
            line = self.input.text()
            self.input.setText(line + param)

    operation = 0

    def _operation(self, op):
        if op == 'C':
            Calculator.operation = 0
            self.input.setText('0')
        else:
            self.num_1 = float(self.input.text())
            self.op = op
            self.input.setText("")
            Calculator.operation = 1

    def _result(self):
        if Calculator.operation == 1:
            self.num_2 = float(self.input.text())
            if self.num_1 != int(self.num_1) or self.num_2 != int(self.num_2):
                if self.op == "+":
                    self.input.setText(str(self.num_1 + self.num_2))
                if self.op == "-":
                    if int(self.num_1 - self.num_2) == (self.num_1 - self.num_2):
                        self.input.setText(str(int(self.num_1 - self.num_2)))
                    else:
                        self.input.setText(str(self.num_1 - self.num_2))
                if self.op == "*":
                    self.input.setText(str(round(self.num_1 * self.num_2, 6)))
                if self.op == "/":
                    if self.num_2 == 0:
                        self.input.setText('Ошибка')
                    else:
                        self.input.setText(str(round(self.num_1 / self.num_2, 6)))
            else:
                if self.op == "+":
                    self.input.setText(str(round(self.num_1 + self.num_2)))
                if self.op == "-":
                    self.input.setText(str(round(self.num_1 - self.num_2)))
                if self.op == "*":
                    self.input.setText(str(round(self.num_1 * self.num_2)))
                if self.op == "/":
                    if self.num_2 == 0:
                        self.input.setText('Ошибка')
                    elif self.num_1 % self.num_2 != 0:
                        self.input.setText(str(round(self.num_1 / self.num_2, 6)))
                    else:
                        self.input.setText(str(round(self.num_1 / self.num_2)))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Calculator()
    win.show()

    sys.exit(app.exec_())
