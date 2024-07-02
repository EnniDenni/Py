import sys
import os
import requests
from bs4 import BeautifulSoup as bs
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog, QScrollArea
from PyQt5.QtGui import QPixmap
from io import BytesIO
from PIL import Image

class ParserApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.image_widgets = []  # Список для хранения виджетов QLabel с изображениями
        
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
        
        self.save_images_button = QPushButton('Сохранить фото', self)
        self.save_images_button.clicked.connect(self.save_images)
        layout.addWidget(self.save_images_button)
        
        self.clear_button = QPushButton('Очистить', self)
        self.clear_button.clicked.connect(self.clear_results)
        layout.addWidget(self.clear_button)
        
        self.result_text = QTextEdit(self)
        layout.addWidget(self.result_text)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        
        self.setLayout(layout)
        
    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.result_text.toPlainText())
        
    def save_images(self):
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения фото")
        if directory:
            for idx, widget in enumerate(self.image_widgets, start=1):
                pixmap = widget.pixmap()
                if not pixmap:
                    continue
                image = pixmap.toImage()
                image.save(os.path.join(directory, f"image_{idx}.jpg"))
        
    def clear_results(self):
        self.result_text.clear()
        for widget in self.image_widgets:
            widget.clear()
        self.image_widgets = []
        self.scroll_area.takeWidget()  # Удаление текущего виджета из ScrollArea, если он есть
        
    def start_parsing(self):
        URL_TEMPLATE = self.url_input.text()
        r = requests.get(URL_TEMPLATE)
        
        soup = bs(r.text, "html.parser")
        titles = soup.find_all('div', class_='flex flex-col gap-2 py-6 first:pt-0')
        hrefs = []
        for i in titles:
            hrefs.append(i.find_all("a")[2].attrs["href"])
            
        results = ""
        image_layout = QVBoxLayout()
        for href in hrefs:
            r = requests.get(href)
            soup = bs(r.text, "html.parser")
            h1 = soup.find_all('h1', class_='sm:max-w-4xl text-xl sm:text-3xl leading-tight font-bold break-words dark:text-gray-300')[0].text
            results += f"Title: {h1}\n"
            
            img = soup.find_all("img", class_="w-full rounded-md")
            for idx, image in enumerate(img, start=1):
                img_url = image.attrs["src"]
                results += f"Image {idx}: {img_url}\n"
                self.display_image(img_url, image_layout)
                
            textp = soup.find_all("p")[0].text
            results += f"Text: {textp}\n\n"
        
        self.result_text.setPlainText(results)
        self.scroll_area.takeWidget()  # Удаление текущего виджета из ScrollArea, если он есть
        widget = QWidget()
        widget.setLayout(image_layout)
        self.scroll_area.setWidget(widget)
        
    def display_image(self, img_url, layout):
        response = requests.get(img_url)
        image_data = BytesIO(response.content)
        pixmap = QPixmap()
        pixmap.loadFromData(image_data.getvalue())
        
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)
        self.image_widgets.append(image_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ParserApp()
    ex.show()
    sys.exit(app.exec_())
