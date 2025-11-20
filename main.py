import requests
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

api_key = ""

class weatherwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 200, 450, 350)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.bg = QPixmap("bg.jpg")
        self.offset = None

        self.title_bar = QWidget()
        self.title_bar.setStyleSheet("background-color: #CBC3E3;")
        self.title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        name = QLabel("WeatherApp")
        name.setStyleSheet("color: Purple;")
        font_id = QFontDatabase.addApplicationFont("Pixelify_Sans/static/PixelifySans-Regular.ttf")
        self.family = QFontDatabase.applicationFontFamilies(font_id)[0]
        name.setFont(QFont(self.family, 13))
        title_layout.addWidget(name)
        title_layout.addStretch()
        cross_btn = QPushButton("x")
        cross_btn.setStyleSheet("""
            QPushButton {
                background-color: #B19CD9;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #D8BFD8;
            }
        """)
        cross_btn.setFont(QFont(self.family, 13))
        cross_btn.setFixedSize(20, 20)
        cross_btn.clicked.connect(self.close)
        title_layout.addWidget(cross_btn)

        self.stacked = QStackedWidget()
        self.page1 = self.search_page()
        self.page2 = self.result_page()
        self.stacked.addWidget(self.page1)
        self.stacked.addWidget(self.page2)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.stacked)
        self.setLayout(self.main_layout)

    def search_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setContentsMargins(20, 20, 20, 20)

        image2 = QLabel()
        moon = QPixmap("moon.png")
        moon = moon.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image2.setPixmap(moon)
        image2.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(image2)

        self.city_input = QLineEdit()
        self.city_input.setFont(QFont(self.family, 13))
        self.city_input.setPlaceholderText("Enter a city name..")
        self.city_input.setStyleSheet("""
            QLineEdit {
                background-color: #DFC5FE;
                border: 2px solid #B57EDC;
                border-radius: 14px;
                padding: 8px 12px;
                color: black;
            }
        """)
        self.city_input.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.city_input)

        search_btn = QPushButton("Search Weather")
        search_btn.setFont(QFont(self.family, 13))
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #DFC5FE;
                color: Purple;
                border-radius: 7px;
                border: 2px solid #B57EDC;
                padding: 4px 8px;
            }
        """)
        search_btn.clicked.connect(self.show_weather_page)
        content_layout.addWidget(search_btn)

        layout.addWidget(content)
        return page

    def result_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignTop)

        self.weather_label = QLabel("Weather will appear here")
        self.weather_label.setFont(QFont(self.family, 15))
        self.weather_label.setStyleSheet("color: purple;")
        self.weather_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.weather_label)
        
        back_btn = QPushButton("Back")
        back_btn.setFont(QFont(self.family, 13))
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        layout.addSpacing(20)

        self.temp_condition = QLabel("waiting for weather data")
        self.temp_condition.setFont(QFont(self.family, 18))
        self.temp_condition.setStyleSheet("color: purple;")
        self.temp_condition.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.temp_condition)

        self.weather_icon = QLabel()
        self.weather_icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.weather_icon)

        return page

    def show_weather_page(self):
        city = self.city_input.text()
        if city.strip() == "":
            return
        self.weather_label.setText(f"Weather for: {city}")
        self.get_weather()
        self.stacked.setCurrentIndex(1)

    def go_back(self):
        self.stacked.setCurrentIndex(0)

    def get_weather(self):
        city = self.city_input.text()
        if city: 
            url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
            reponse = requests.get(url)
            print("Status:", reponse.status_code)  
            print("Response:", reponse.text)
            if reponse.status_code == 200:
                data = reponse.json()
                temp = data["current"]["temp_c"]
                weather = data["current"]["condition"]["text"]
                self.temp_condition.setText(f"temperature: {temp}°C\nCondition: {weather}")
            else:
                self.temp_condition.setText("city not found!")   

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() <= 40:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg.scaled(self.size(), Qt.IgnoreAspectRatio))
        super().paintEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = weatherwindow()
    window.show()
    sys.exit(app.exec())





        



            
