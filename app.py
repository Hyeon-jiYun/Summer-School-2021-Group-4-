# Inspired from https://github.com/MariyaSha/TriviaGame/blob/main/Trivia%20-%20Complete%20App/functions.py
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QFrame
from PyQt5.QtGui import QPixmap, QTextBlock
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

widgets = {
    "button":[],
    "question1":[],
    "answer1":[],
    "answer2":[]
}

# Initialise the GUI application and determine the window and settings
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Welcome to your Medibox!")
window.setFixedWidth(1500)
window.setFixedHeight(1500)
window.setStyleSheet("background: #808080;")

grid = QGridLayout()

def clear_widgets():
    for widget in widgets:
        if widgets[widgets] != []:
            for i in range(0, len(widgets[widget])): # getting rid of widget from global widgets
                widgets[widget].pop()

def start_app():
    clear_widgets()
    frame2()

# creating buttons
def create_buttons(answer):
        button = QPushButton(answer)
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setFixedWidth(500)
        button.setStyleSheet(
        "*{border: 15px solid '#289D8C';" + 
        "border-radius: 30px;" +
        "font-size: 60px;" +
        "height: 300;" +
        "width: 300;" +
        "color: 'white';}"  +
        "*:hover{background: '#289D8C';}"
    )
        return button

# creating different frames
#display button
def frame1():
    button = QPushButton("WELCOME TO YOUR MEDIBOX! LET'S START!")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
    "*{border: 15px solid '#289D8C';" + 
    "border-radius: 30px;" +
    "font-size: 60px;" +
    "height: 500;" +
    "width: 500;" +
    "color: 'white';}"  +
    "*:hover{background: '#289D8C';}"
    )
    widgets["button"].append(button)
    button.clicked.connect(start_app) # connect does not work.
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)
  
frame1()

def frame2(): # create the first question
    question1 = QLabel("Do you want to add a medecine to your medibox?")
    question1.setAlignment(QtCore.Qt.AlignCenter)
    question1.setStyleSheet(
    "*{border: 15px solid '#289D8C';" + 
    "border-radius: 30px;" +
    "font-size: 60px;" +
    "height: 500;" +
    "width: 500;" +
    "color: 'white';}"  +
    "*:hover{background: '#289D8C';}"
    )
    widgets["question1"].append(question1)
    
    # The answer button widgets
    button1 = create_buttons("answer1")
    button2 = create_buttons("answer2")

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)


    #placing the widget on the grid
    grid.addWidget(widgets["question1"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)

frame2() 


window.setLayout(grid)
window.show()
sys.exit(app.exec())


