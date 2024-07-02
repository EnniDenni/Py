import sys
import requests
from bs4 import BeautifulSoup as bs
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog

class ParserApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Web Parser')
        
        layout = QVBoxLayout()
        
        self.url_label = QLabel('URL:')
        layout.addWidget(self.url_label)
        
        self.url_input = QLineEdit(self)
        self.url_input.setText('https://shazoo.ru/tags/105/movies')
        layout.addWidget(self.url_input)
        
        self.start_button = QPushButton('Начать парсинг', self)
        self.start_button.clicked.connect(self.start_parsing)
        layout.addWidget(self.start_button)
        
        self.save_button = QPushButton('Сохранить в файл', self)
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)
        
        self.result_text = QTextEdit(self)
        layout.addWidget(self.result_text)
        
        self.setLayout(layout)
        
    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.result_text.toPlainText())
        
    def start_parsing(self):
        URL_TEMPLATE = self.url_input.text()
        r = requests.get(URL_TEMPLATE)
        
        soup = bs(r.text, "html.parser")
        titles = soup.find_all('div', class_='flex flex-col gap-2 py-6 first:pt-0')
        hrefs = []
        for i in titles:
            hrefs.append(i.find_all("a")[2].attrs["href"])
            
        results = ""
        for href in hrefs:
            r = requests.get(href)
            soup = bs(r.text, "html.parser")
            h1 = soup.find_all('h1', class_='sm:max-w-4xl text-xl sm:text-3xl leading-tight font-bold break-words dark:text-gray-300')[0].text
            results += f"Title: {h1}\n"
            
            img = soup.find_all("img", class_="w-full rounded-md")[0].attrs["src"]
            results += f"Image: {img}\n"
            
            textp = soup.find_all("p")[0].text
            results += f"Text: {textp}\n\n"
        
        self.result_text.setPlainText(results)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ParserApp()
    ex.show()
    sys.exit(app.exec_())
