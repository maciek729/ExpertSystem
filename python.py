import os
import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QWidget, QStackedWidget
import pandas as pd
from PyQt5.uic.Compiler.qtproxies import QtCore
from PyQt5.uic.properties import QtGui
from sklearn.tree import DecisionTreeClassifier
from game_data import game_data
class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wybór Gry")
        self.setFixedSize(1600, 800)

        self.setStyleSheet("""
            QDialog {
                background-color: #bbdefb; /* Light blue-gray */
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #333;
            }
            QLabel#img_column1, QLabel#img_column2, QLabel#img_column3 {
                border: 3px solid #16329e; /* Optional: Adds a border for better visibility */
                background-color: white; /* Ensures no background artifacts */
                overflow: hidden; /* Clips the image to fit rounded corners */
            }
            QLabel#option_label{
                color:#0d47a1;
                font-size:30px;
            }
            QLabel{
                color:#0d47a1;
                font-size:20px; 
            }
            QPushButton{
                background-color:#e3f2fd;
                border: 2px solid #0077b6;
                border-radius:15px;
                color:#0d47a1;
                font-size:20px; 
                
            }
            QPushButton:hover{
                background-color:white;
            }
            QPushButton:pressed{
                background-color:#e3f2fd;

            }
            QLabel#result_desc_lb{
                font-size:40px;
            }
            QLabel#lb_result_prediction{
                font-size:60px;
            }
            QLabel#result_img{
                border: 3px solid #16329e; /* Optional: Adds a border for better visibility */
                background-color: white; /* Ensures no background artifacts */
                overflow: hidden; /* Clips the image to fit rounded corners */
                background-color:#e3f2fd;
            }
             QToolTip {
                background-color:#e3f2fd ;  /* Dark background */
                color: #0d47a1;  /* White text */
                border: 1px solid #0077b6;  /* Border color */
                padding: 10px;  /* Space around the text */
                font-size: 22px;  /* Font size */
                border-radius: 5px;  /* Rounded corners */
        }
        """)

        self.stacked_widget = QStackedWidget(self)

        self.option_page = self.create_option_page()
        self.result_page = self.create_result_page()
        self.stacked_widget.addWidget(self.option_page)
        self.stacked_widget.addWidget(self.result_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        try:
            self.df = pd.read_csv("Gra.csv", sep=";")
        except FileNotFoundError:
            QMessageBox.critical(self, "Błąd", "Plik 'Gra.csv' nie został znaleziony!")
            sys.exit()

        self.d_game_type = {'Strzelanka': 0, 'RPG': 1, 'Strategia': 2, 'Przygodowa': 3, 'Symulator': 4, 'Horror': 5}
        self.d_game_mode = {'Single-player': 0, 'Multiplayer': 1, 'Kooperacja': 2}
        self.d_experience = {'Walka i rywalizacja': 0, 'Eksploracja i przygoda': 1, 'Przetrwanie i wyzwanie': 2, 'Budowanie i rozwoj': 3}

        self.df['typ_gry'] = self.df['typ_gry'].map(self.d_game_type)
        self.df['tryb_gry'] = self.df['tryb_gry'].map(self.d_game_mode)
        self.df['doswiadczenie'] = self.df['doswiadczenie'].map(self.d_experience)

        features = ['typ_gry', 'tryb_gry', 'doswiadczenie']
        X = self.df[features]
        y = self.df['wyjscie']
        self.dtree = DecisionTreeClassifier()
        self.dtree.fit(X, y)

    def create_option_page(self):
        option_page = QWidget()

        option_layout = QVBoxLayout()

        self.column1_options = ["Strzelanka", "RPG", "Strategia", "Przygodowy", "Symulator", "Horror"]
        self.column2_options = ["Kooperacja", "Multiplayer", "Single-player"]
        self.column3_options = ["Walka i rywalizacja", "Eksploracja i przygoda", "Przetrwanie i wyzwanie", "Budowanie i rozwoj"]
        self.column1_images = ["typ gry\strzelanka.png", "typ gry\Rpg.png", "typ gry\strategia.png", "typ gry\przygodowa.png",
                               "typ gry\symulator.png", "typ gry\horror.png"]
        self.column2_images = ["tryb gry\kooperacja.png", "tryb gry\multiplayer.png", "tryb gry\singleplayer.png"]
        self.column3_images = ["doswiadczenie\walka i rywalizacja.png", "doswiadczenie\eksploracja i przygoda.png",
                               "doswiadczenie\przetrwanie i wyzwanie.png", "doswiadczenie\Budowa i rozwoj.png"]

        self.column1_tooltips = ["Gry, w których głównym elementem jest walka przy użyciu broni palnej i szybka akcja.",
                                 "Gry fabularne, gdzie wcielasz się w postać i rozwijasz jej umiejętności poprzez zadania i eksplorację.",
                                 "Gry wymagające planowania i zarządzania zasobami, by osiągnąć przewagę nad przeciwnikiem.",
                                 "Gry skupiające się na eksploracji, rozwiązywaniu zagadek i odkrywaniu historii.",
                                 "Gry symulujące realistyczne aspekty życia, pracy lub prowadzenia pojazdów.",
                                 "Gry, które wprowadzają w atmosferę strachu i napięcia, często z elementami zaskoczenia i niebezpieczeństwa. Idealne dla graczy, którzy szukają adrenaliny i nie boją się mrocznych klimatów."
                                 ]
        self.column2_tooltips = ["Współpracuj z innymi graczami, aby osiągnąć wspólny cel.",
                                 "Dołącz do gry wieloosobowej i walcz z innymi graczami.",
                                 "Zagraj samodzielnie i przeżyj przygodę w trybie singleplayer."
                              ]
        self.column3_tooltips = ["Stań do walki z przeciwnikami w intensywnych starciach.",
                                 "Przeżyj niesamowite przygody podczas odkrywania nowych terenów.",
                                 "Pokonaj trudności i przeżyj w nieprzyjaznym świecie.",
                                 "Buduj, rozwijaj i zarządzaj swoimi zasobami, by osiągnąć sukces.",
                                 ]
        self.column1_index = 0
        self.column2_index = 0
        self.column3_index = 0

        self.option_label = QLabel("Wybierz poniższe opcje")
        self.option_label.setObjectName("option_label")
        self.option_label.setAlignment(Qt.AlignCenter)
        option_layout.addWidget(self.option_label, alignment=Qt.AlignTop)

        columns_layout = QHBoxLayout()
        left_icon_path = "strzalki/left-arrow.png"
        pixmap_icon_left = QPixmap(left_icon_path)
        right_icon_path = "strzalki/right-arrow.png"
        pixmap_icon_right = QPixmap(right_icon_path)
        self.column1_layout = QVBoxLayout()
        self.lb_column1 = QLabel("Typ gry")
        self.lb_column1.setObjectName("lb_column1")
        self.img_column1 = QLabel()
        self.img_column1.setObjectName("img_column1")
        self.img_column1.setFixedSize(500, 500) 
        self.img_column1.setContentsMargins(0, 0, 0, 0)
        pixmap = QPixmap(self.column1_images[self.column1_index]).scaled(
            self.img_column1.width(), self.img_column1.height()
        )
        self.img_column1.setPixmap(pixmap)
        self.img_column1.setToolTip(self.column1_tooltips[0])
        self.desc_column1 = QLabel(self.column1_options[0])
        self.desc_column1.setObjectName("desc_column1")
        self.pb1_column1 = QPushButton(self)
        self.pb1_column1.setToolTip("Przesuń w lewo, aby zobaczyć poprzednią opcję")
        self.pb1_column1.setIcon(QIcon(pixmap_icon_left))
        self.pb1_column1.setFixedSize(150,50)
        self.pb1_column1.setIconSize(QSize(70, 40))  
        self.pb1_column1.setObjectName("pb1_column1")
        self.pb2_column1 = QPushButton(self)
        self.pb2_column1.setToolTip("Przesuń w prawo, aby zobaczyć kolejną opcję")
        self.pb2_column1.setIcon(QIcon(pixmap_icon_right))
        self.pb2_column1.setFixedSize(150, 50)
        self.pb2_column1.setIconSize(QSize(70, 40))
        self.pb2_column1.setObjectName("pb2_column1")
        self.pb1_column1.clicked.connect(self.prev_column1)
        self.pb2_column1.clicked.connect(self.next_column1)

        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.pb1_column1)
        button_layout1.addWidget(self.pb2_column1)

        self.column1_layout.addWidget(self.lb_column1,alignment=Qt.AlignCenter)
        self.column1_layout.addWidget(self.img_column1)
        self.column1_layout.addWidget(self.desc_column1,alignment=Qt.AlignCenter)
        self.column1_layout.addLayout(button_layout1)

        self.column2_layout = QVBoxLayout()
        self.lb_column2 = QLabel("Tryb gry")
        self.lb_column2.setObjectName("lb_column2")
        self.img_column2 = QLabel()
        self.img_column2.setObjectName("img_column2")
        self.img_column2.setFixedSize(500, 500)  # Set fixed size for QLabel
        self.img_column2.setContentsMargins(0, 0, 0, 0)
        pixmap = QPixmap(self.column2_images[self.column2_index]).scaled(
            self.img_column2.width(), self.img_column2.height()
        )
        self.img_column2.setPixmap(pixmap)
        self.img_column2.setToolTip(self.column2_tooltips[0])

        self.desc_column2 = QLabel(self.column2_options[0])
        self.desc_column2.setObjectName("desc_column2")
        self.pb1_column2 = QPushButton(self)
        self.pb1_column2.setToolTip("Przesuń w lewo, aby zobaczyć poprzednią opcję")
        self.pb1_column2.setIcon(QIcon(pixmap_icon_left))
        self.pb1_column2.setFixedSize(150, 50)
        self.pb1_column2.setIconSize(QSize(70, 40))
        self.pb1_column2.setObjectName("pb1_column2")
        self.pb2_column2 = QPushButton(self)
        self.pb2_column2.setToolTip("Przesuń w prawo, aby zobaczyć kolejną opcję")
        self.pb2_column2.setIcon(QIcon(pixmap_icon_right))
        self.pb2_column2.setFixedSize(150, 50)
        self.pb2_column2.setIconSize(QSize(70, 40))
        self.pb2_column2.setObjectName("pb2_column2")

        self.pb1_column2.clicked.connect(self.prev_column2)
        self.pb2_column2.clicked.connect(self.next_column2)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.pb1_column2)
        button_layout2.addWidget(self.pb2_column2)

        self.column2_layout.addWidget(self.lb_column2,alignment=Qt.AlignCenter)
        self.column2_layout.addWidget(self.img_column2)
        self.column2_layout.addWidget(self.desc_column2,alignment=Qt.AlignCenter)
        self.column2_layout.addLayout(button_layout2)

        self.column3_layout = QVBoxLayout()
        self.lb_column3 = QLabel("Doświadczenie")
        self.lb_column3.setObjectName("lb_column3")
        self.img_column3 = QLabel()
        self.img_column3.setObjectName("img_column3")
        self.img_column3.setFixedSize(500, 500)  
        self.img_column3.setContentsMargins(0, 0, 0, 0)
        pixmap = QPixmap(self.column3_images[self.column3_index])
        pixmap = pixmap.scaled(
            self.img_column3.width(), self.img_column3.height()
        )
        self.img_column3.setPixmap(pixmap)
        self.img_column3.setToolTip(self.column3_tooltips[0])

        self.desc_column3 = QLabel(self.column3_options[0])
        self.desc_column3.setObjectName("desc_column3")
        self.pb1_column3 = QPushButton(self)
        self.pb1_column3.setToolTip("Przesuń w lewo, aby zobaczyć poprzednią opcję")
        self.pb1_column3.setIcon(QIcon(pixmap_icon_left))
        self.pb1_column3.setFixedSize(150, 50)
        self.pb1_column3.setIconSize(QSize(70, 40))
        self.pb1_column3.setObjectName("pb1_column3")
        self.pb2_column3 = QPushButton(self)
        self.pb2_column3.setToolTip("Przesuń w prawo, aby zobaczyć kolejną opcję")
        self.pb2_column3.setIcon(QIcon(pixmap_icon_right))

        self.pb2_column3.setFixedSize(150, 50)
        self.pb2_column3.setIconSize(QSize(70, 40))
        self.pb2_column3.setObjectName("pb2_column3")
        self.pb1_column3.clicked.connect(self.prev_column3)
        self.pb2_column3.clicked.connect(self.next_column3)

        button_layout3 = QHBoxLayout()
        button_layout3.addWidget(self.pb1_column3)
        button_layout3.addWidget(self.pb2_column3)

        self.column3_layout.addWidget(self.lb_column3,alignment=Qt.AlignCenter)
        self.column3_layout.addWidget(self.img_column3)
        self.column3_layout.addWidget(self.desc_column3,alignment=Qt.AlignCenter)
        self.column3_layout.addLayout(button_layout3)

        columns_layout.addLayout(self.column1_layout)
        columns_layout.addLayout(self.column2_layout)
        columns_layout.addLayout(self.column3_layout)

        option_layout.addLayout(columns_layout)

        self.result_button = QPushButton("Przejdź do wyniku")
        self.result_button.setObjectName("result_button")
        self.result_button.setFixedSize(370, 50)
        self.result_button.clicked.connect(self.go_to_result)
        option_layout.addWidget(self.result_button, alignment=Qt.AlignCenter)

        option_page.setLayout(option_layout)
        return option_page

    def prev_column1(self):
        self.column1_index = (self.column1_index - 1) % len(self.column1_options)
        self.desc_column1.setText(self.column1_options[self.column1_index])
        pixmap = QPixmap(self.column1_images[self.column1_index])
        scaled_pixmap = pixmap.scaled(500, 500, Qt.IgnoreAspectRatio)
        self.img_column1.setPixmap(scaled_pixmap)
        self.img_column1.setToolTip(self.column1_tooltips[self.column1_index])

    def next_column1(self):
        self.column1_index = (self.column1_index + 1) % len(self.column1_options)
        self.desc_column1.setText(self.column1_options[self.column1_index])
        pixmap = QPixmap(self.column1_images[self.column1_index])
        scaled_pixmap = pixmap.scaled(500, 500, Qt.IgnoreAspectRatio)
        self.img_column1.setPixmap(scaled_pixmap)
        self.img_column1.setToolTip(self.column1_tooltips[self.column1_index])


    def prev_column2(self):
        self.column2_index = (self.column2_index - 1) % len(self.column2_options)
        self.desc_column2.setText(self.column2_options[self.column2_index])
        pixmap = QPixmap(self.column2_images[self.column2_index])
        scaled_pixmap = pixmap.scaled(500, 500, Qt.IgnoreAspectRatio)
        self.img_column2.setPixmap(scaled_pixmap)
        self.img_column2.setToolTip(self.column2_tooltips[self.column2_index])


    def next_column2(self):
        self.column2_index = (self.column2_index + 1) % len(self.column2_options)
        self.desc_column2.setText(self.column2_options[self.column2_index])
        pixmap = QPixmap(self.column2_images[self.column2_index])
        scaled_pixmap = pixmap.scaled(500, 500, Qt.IgnoreAspectRatio)
        self.img_column2.setPixmap(scaled_pixmap)
        self.img_column2.setToolTip(self.column2_tooltips[self.column2_index])


    def prev_column3(self):
        self.column3_index = (self.column3_index - 1) % len(self.column3_options)
        self.desc_column3.setText(self.column3_options[self.column3_index])
        pixmap = QPixmap(self.column3_images[self.column3_index])
        scaled_pixmap = pixmap.scaled(500, 500, Qt.IgnoreAspectRatio)
        self.img_column3.setPixmap(scaled_pixmap)
        self.img_column3.setToolTip(self.column3_tooltips[self.column3_index])


    def next_column3(self):
        self.column3_index = (self.column3_index + 1) % len(self.column3_options)
        self.desc_column3.setText(self.column3_options[self.column3_index])
        pixmap = QPixmap(self.column3_images[self.column3_index])
        scaled_pixmap = pixmap.scaled(500, 500, Qt.IgnoreAspectRatio)
        self.img_column3.setPixmap(scaled_pixmap)
        self.img_column3.setToolTip(self.column3_tooltips[self.column3_index])
    def create_result_page(self):


        result_page = QWidget()

        result_main_layout = QVBoxLayout()

        self.lb_result_prediction = QLabel(self)
        self.lb_result_prediction.setObjectName("lb_result_prediction")
        self.lb_result_prediction.setAlignment(Qt.AlignCenter)
        result_main_layout.addWidget(self.lb_result_prediction)

        result_layout = QHBoxLayout()

        self.result_desc_lb = QLabel(self)
        self.result_desc_lb.setObjectName("result_desc_lb")
        self.result_desc_lb.setWordWrap(True)
        self.result_img = QLabel(self)
        self.result_img.setObjectName("result_img")
        self.result_img.setAlignment(Qt.AlignCenter)

        result_layout.addWidget(self.result_desc_lb)
        result_layout.addWidget(self.result_img)

        button_layout = QVBoxLayout()

        self.go_to_options_btn = QPushButton("Wróć")
        self.go_to_options_btn.setFixedSize(370, 50)
        self.go_to_options_btn.setObjectName("go_to_options_btn")
        self.go_to_options_btn.clicked.connect(self.go_to_options)

        button_layout.addWidget(self.go_to_options_btn)

        result_main_layout.addLayout(result_layout)
        result_main_layout.addLayout(button_layout)
        result_page.setLayout(result_main_layout)

        return result_page

    def go_to_result(self):
        self.predict()
        self.stacked_widget.setCurrentWidget(self.result_page)

    def go_to_options(self):
        self.stacked_widget.setCurrentWidget(self.option_page)
    def predict(self):
        input_data = [
            self.column1_index,  # typ_gry
            self.column2_index,  # tryb_gry
            self.column3_index  # doswiadczenie
        ]

        prediction = self.dtree.predict([input_data])[0]
        print(prediction)
        self.lb_result_prediction.setText(prediction)
        for game_name, game_info in game_data.items(): 
            if game_name == prediction:
                self.result_desc_lb.setText(game_info["description"])
                pixmap = QPixmap(game_info['image'])
                self.result_img.setFixedSize(700, 500)

                pixmap = pixmap.scaled(
                    self.result_img.width(), self.result_img.height(),
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )

                self.result_img.setPixmap(pixmap)





if __name__ == '__main__':
    app = QApplication([])
    window = DlgMain()
    window.show()
    app.exec_()
