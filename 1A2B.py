from PyQt6.QtWidgets import (QMainWindow, QWidget, QPushButton, QLineEdit,
         QApplication, QLabel, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox
         , QHeaderView, QTableView, QTableWidgetItem )
import sys
import random

class GameEngine():
    def __init__(self, max_round = 10):
        self.max_rounds = max_round
        self.new_game()
        
    def new_game(self):
        self.answer = "".join(random.sample('0123456789', 4))
        self.curr_round = 1
        self.finished = False
        self.won = False
        
    def valid_guess(self, text: str):
        t = text.strip()
        if not t.isdigit():
            return False, "請輸入數字!"
        if len(t) != 4:
            return False, "請輸入 4 位數字!"
        digits = str(t)
        if len(set(t)) != 4:
            return False, "請輸入 4 個不同數字!"
        return True, ""
        
    def score(self, guess: str):
        A = sum(1 for i in range(4) if guess[i] == self.answer[i])
        B = sum(1 for ch in guess if ch in self.answer) - A
        
        if A == 4:
            self.won = True
            self.finished = True
        else:
            self.curr_round += 1
            if self.curr_round > self.max_rounds:
                self.finished = True
        return A, B
    
    def is_over(self):
        return self.finished
    
    def is_win(self):
        return self.won
    
    def reveal(self):
        return self.answer

class guess_number_1A2B(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('1A2B')
        
        self.central = QWidget(self)
        self.setCentralWidget(self.central)
        self.root_Layout = QVBoxLayout(self.central)
        
        self.initUI()
        
        self.engine = GameEngine()
        self.filled_rows = 0
        
        self.Enter_btn.clicked.connect(self.on_submit)
        self.Reset_btn.clicked.connect(self.on_reset)
        self.guessEdit.returnPressed.connect(self.on_submit)
        self.Stop_btn.clicked.connect(self.on_stop)
        
        self.statusBar().showMessage("開始遊戲")
        
        self.resize(500, 420)
        self.center()
        self.show()
        
    def initUI(self):
        
        # ===== Input =====
        Input_Row = QHBoxLayout()
        
        self.inputLabel = QLabel('Input 4 Numbers : ', self)
        Input_Row.addWidget(self.inputLabel)
        
        self.guessEdit = QLineEdit("", self)
        self.guessEdit.setPlaceholderText("0~9 input 4 different Numbers")
        self.guessEdit.setMaxLength(4)
        Input_Row.addWidget(self.guessEdit, 1)
        
        self.Enter_btn = QPushButton("Enter", self)
        Input_Row.addWidget(self.Enter_btn)
        # 將上方掛在主版面
        self.root_Layout.addLayout(Input_Row)
        
        # ===== 表格(已猜過) =====
        self.table = QTableWidget(10, 2, self)
        self.table.setHorizontalHeaderLabels(["Guess", "Result"]) #"Rounds"
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.root_Layout.addWidget(self.table)
        
        for i in range(10):
            self.table.setVerticalHeaderItem(i, QTableWidgetItem(str(i + 1)))
            
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.root_Layout.addWidget(self.table)
        
        # ===== 控制按鈕 =====
        Ctrl_Row = QHBoxLayout()
        
        self.Reset_btn = QPushButton("Reset", self)
        Ctrl_Row.addWidget(self.Reset_btn)
        
        self.Stop_btn = QPushButton("Stop", self)
        Ctrl_Row.addWidget(self.Stop_btn)
        
        self.root_Layout.addLayout(Ctrl_Row)
        
    def on_submit(self):
        text = self.guessEdit.text()
        
        if self.engine.is_over():
            QMessageBox.information(self, "遊戲狀態 ", "遊戲已結束， 請按 Reset 開始新遊戲")
            return
        
        ok, reason = self.engine.valid_guess(text)
        
        if not ok:
            QMessageBox.warning(self, "輸入錯誤", reason)
            self.guessEdit.setFocus()
            self.guessEdit.selectAll()
            return
        
        A, B = self.engine.score(text)
        
        row = self.filled_rows
        if row < self.table.rowCount():
            self.table.setItem(row, 0, QTableWidgetItem(text))
            self.table.setItem(row, 1, QTableWidgetItem(f"{A} A {B} B"))
            self.filled_rows += 1
            self.table.scrollToBottom()
            
        if self.engine.is_win():
            QMessageBox.information(self, "You Win!", f"答對了! 答案是 {self.engine.reveal()}")
            self.guessEdit.setEnabled(False)
            self.Enter_btn.setEnabled(False)
            return
        
        if self.engine.is_over():
            QMessageBox.information(self, "You Lose!", f"回合結束! 答案是 {self.engine.reveal()}")
            self.guessEdit.setEnabled(False)
            self.Enter_btn.setEnabled(False)
            return

        self.guessEdit.clear()
        self.guessEdit.setFocus()
        self.guessEdit.selectAll()
        
    def on_reset(self):
        self.engine.new_game()
        self.filled_rows = 0
        self.table.clearContents()
        self.guessEdit.clear()
        self.guessEdit.setEnabled(True)
        self.Enter_btn.setEnabled(True)
        self.guessEdit.setFocus()
        self.statusBar().showMessage("開始遊戲")
                    
    def on_stop(self):
        if not self.engine.is_over():
            QMessageBox.information(self, "已暫停", f"答案: {self.engine.reveal()}")
            self.engine.finished = True
        self.guessEdit.setEnabled(False)
        self.Enter_btn.setEnabled(False)
        self.statusBar().showMessage("遊戲暫停")
        
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


        
def main():
    

    app = QApplication(sys.argv)
    game = guess_number_1A2B()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
