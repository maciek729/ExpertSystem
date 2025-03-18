import os
import sys
import rule_engine
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QWidget, \
    QStackedWidget
from PyQt5.uic.Compiler.qtproxies import QtCore
from PyQt5.uic.properties import QtGui
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


    def create_option_page(self):
        option_page = QWidget()

        option_layout = QVBoxLayout()

        self.column1_options = ["Strzelanka", "RPG", "Strategia", "Przygodowy", "Symulator", "Horror"]
        self.column2_options = ["Kooperacja", "Multiplayer", "Single-player"]
        self.column3_options = ["Walka i rywalizacja", "Eksploracja i przygoda", "Przetrwanie i wyzwanie",
                                "Budowanie i rozwoj"]
        self.column1_images = ["typ gry\strzelanka.png", "typ gry\Rpg.png", "typ gry\strategia.png",
                               "typ gry\przygodowa.png",
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
        self.pb1_column1.setFixedSize(150, 50)
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

        self.column1_layout.addWidget(self.lb_column1, alignment=Qt.AlignCenter)
        self.column1_layout.addWidget(self.img_column1)
        self.column1_layout.addWidget(self.desc_column1, alignment=Qt.AlignCenter)
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

        self.column2_layout.addWidget(self.lb_column2, alignment=Qt.AlignCenter)
        self.column2_layout.addWidget(self.img_column2)
        self.column2_layout.addWidget(self.desc_column2, alignment=Qt.AlignCenter)
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

        self.column3_layout.addWidget(self.lb_column3, alignment=Qt.AlignCenter)
        self.column3_layout.addWidget(self.img_column3)
        self.column3_layout.addWidget(self.desc_column3, alignment=Qt.AlignCenter)
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
        self.stacked_widget.setCurrentWidget(self.result_page)
        self.evaluate_rules()

    def go_to_options(self):
        self.stacked_widget.setCurrentWidget(self.option_page)

    def evaluate_rules(self):
        facts = [
            {'typ_gry': self.desc_column1.text(),
             'tryb_gry': self.desc_column2.text(),
             'doswiadczenie': self.desc_column3.text(),
             }
        ]
        print(facts)
        # Inicjalizacja pustej listy na wyniki

        results = []
        rules = [
            # Strzelanka - Single-player
            {
                'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Single-player' and doswiadczenie == 'Walka i rywalizacja'",
                'action': lambda fact: {'wyjscie': 'DOOM Eternal',
                                        "description": "Dynamiczna strzelanka pierwszoosobowa, w której wcielasz się w Doom Slayera, walcząc z hordami demonów na Ziemi i w piekle.",
                                        "image": "result/doom_eternal.jpg"}},
            {
                'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Single-player' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Metro Exodus', "description": "Postapokaliptyczna gra akcji z elementami skradanki, gdzie przemierzasz Rosję, walcząc z mutantami i ludźmi.",
                                        "image": "result/metro_exodus.jpg"}},
            {
                'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Single-player' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Resident Evil Village',
                                        "description": "Survival horror osadzony w tajemniczej wiosce, gdzie musisz zmierzyć się z potworami i odkryć sekrety swojej przeszłości.",
                                        "image": "result/resident_evil_village.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Single-player' and doswiadczenie == 'Budowanie i rozwoj'",
                'action': lambda fact: {'wyjscie': 'Far Cry 5',
                                        "description": "Otwarty świat gry akcji, w którym walczysz z kultem religijnym w malowniczym Hope County.",
                                        "image": "result/far_cry_5.jpg"
                                        }},

            # Strzelanka - Multiplayer
            {
                'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Walka i rywalizacja'",
                'action': lambda fact: {'wyjscie': 'Call of Duty: Warzone',
                                        "description": "Darmowa gra battle royale z szybką akcją i rozgrywką drużynową.",
                                        "image": "result/warzone.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Battlefield 2042',
                                        "description": "Strzelanka wieloosobowa osadzona w przyszłości, oferująca ogromne mapy i intensywne bitwy.",
                                        "image": "result/battlefield_2042.jpg"
                                        }},
            {'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Przetrwanie i wyzwanie'",
             'action': lambda fact: {'wyjscie': 'Apex Legends',
                                     "description": "Dynamiczna gra battle royale z bohaterami o unikalnych umiejętnościach.",
                                     "image": "result/apex_legends.jpg"
                                     }},

            {'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Fortnite',
                                     "description": "Popularna gra battle royale z budowaniem i kreskówkową oprawą graficzną.",
                                     "image": "result/fortnite.jpg"
                                     }},

            # Strzelanka - Kooperacja
            {'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Left 4 Dead 2',
                                     "description": "Kooperacyjna strzelanka, w której czterech graczy walczy z hordami zombie.",
                                     "image": "result/left_4_dead_2.jpg"
                                     }},
            {
                'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Payday 2',
                                        "description": "Kooperacyjna gra akcji, w której gracze wykonują skoki na banki i inne misje przestępcze.",
                                        "image": "result/payday_2.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Tom Clancyâ€™s The Division 2',
                                        "description": "Gra akcji RPG osadzona w postapokaliptycznym Waszyngtonie, gdzie walczysz o odbudowę społeczeństwa.",
                                        "image": "result/division_2.jpg"
                                        }},
            {'condition': "typ_gry == 'Strzelanka' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Deep Rock Galactic',
                                     "description": "Kooperacyjna gra, w której gracze wcielają się w kosmicznych krasnoludów eksplorujących podziemia.",
                                     "image": "result/deep_rock_galactic.jpg"
                                     }},

            # RPG - Single-player
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Single-player' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Cyberpunk 2077',
                                     "description": "RPG osadzone w dystopijnym Night City, oferujące bogatą fabułę i otwarty świat.",
                                     "image": "result/cyberpunk_2077.jpg"
                                     }},
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Single-player' and doswiadczenie == 'Eksploracja i przygoda'",
             'action': lambda fact: {'wyjscie': 'The Witcher 3: Wild Hunt',
                                     "description": "Epicka gra RPG, w której wcielasz się w Geralta z Rivii, polując na potwory i podejmując trudne decyzje moralne.",
                                     "image": "result/witcher_3.jpg"
                                     }},
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Single-player' and doswiadczenie == 'Przetrwanie i wyzwanie'",
             'action': lambda fact: {'wyjscie': 'Fallout 4',
                                     "description": "Gra RPG osadzona w postapokaliptycznym świecie, gdzie eksplorujesz ruiny i budujesz osady.",
                                     "image": "result/fallout_4.jpg"
                                     }},
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Single-player' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Dark Souls III',
                                     "description": "Wyzwanie dla graczy w formie RPG akcji z mrocznym klimatem i wymagającymi walkami.",
                                     "image": "result/dark_souls_3.jpg"
                                     }},

            # RPG - Multiplayer
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Elden Ring',
                                     "description": "Epicka gra RPG akcji od twórców serii Dark Souls, osadzona w otwartym świecie.",
                                     "image": "result/elden_ring.jpg"
                                     }},
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Eksploracja i przygoda'",
             'action': lambda fact: {'wyjscie': 'World of Warcraft',
                                     "description": "Popularne MMORPG, w którym gracze odkrywają świat Azeroth, wykonując zadania i walcząc z innymi graczami.",
                                     "image": "result/world_of_warcraft.jpg"
                                     }},
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Przetrwanie i wyzwanie'",
             'action': lambda fact: {'wyjscie': 'Destiny 2',
                                     "description": "Strzelanka MMO z elementami RPG, w której gracze walczą w drużynach i odkrywają kosmiczne światy.",
                                     "image": "result/destiny_2.jpg"
                                     }},
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Final Fantasy XIV',
                                     "description": "MMORPG osadzone w świecie fantasy, oferujące bogatą fabułę i współpracę z innymi graczami.",
                                     "image": "result/final_fantasy_xiv.jpg"
                                     }},

            # RPG - Kooperacja
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Monster Hunter: World',
                                     "description": "Gra akcji RPG, w której polujesz na ogromne potwory w dynamicznych środowiskach.",
                                     "image": "result/monster_hunter_world.jpg"
                                     }},
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Eksploracja i przygoda'",
             'action': lambda fact: {'wyjscie': 'Diablo III',
                                     "description": "Hack and slash RPG, w którym eksplorujesz lochy i walczysz z hordami demonów.",
                                     "image": "result/diablo_3.jpg"
                                     }},
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Przetrwanie i wyzwanie'",
             'action': lambda fact: {'wyjscie': 'Borderlands 3',
                                     "description": "Strzelanka RPG z charakterystycznym stylem graficznym i humorem, oferująca rozgrywkę w kooperacji.",
                                     "image": "result/borderlands_3.jpg"
                                     }},
            {'condition': "typ_gry == 'RPG' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Torchlight III',
                                     "description": "Hack and slash RPG osadzone w świecie fantasy, z rozgrywką skupioną na łupach i eksploracji.",
                                     "image": "result/torchlight_3.jpg"
                                     }},

            # Strategia - Single-player
            {
                'condition': "typ_gry == 'Strategia' and tryb_gry == 'Single-player' and doswiadczenie == 'Walka i rywalizacja'",
                'action': lambda fact: {'wyjscie': 'Total War: Three Kingdoms',
                                        "description": "Gra strategiczna osadzona w starożytnych Chinach, łącząca walki taktyczne z zarządzaniem imperium.",
                                        "image": "result/total_war_three_kingdoms.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Strategia' and tryb_gry == 'Single-player' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Endless Legend',
                                        "description": "Turowa gra strategiczna, w której budujesz cywilizację w fantastycznym świecie.",
                                        "image": "result/endless_legend.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Strategia' and tryb_gry == 'Single-player' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Frostpunk',
                                        "description": "Gra strategiczna o przetrwaniu, gdzie zarządzasz miastem w mroźnym świecie.",
                                        "image": "result/frostpunk.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Strategia' and tryb_gry == 'Single-player' and doswiadczenie == 'Budowanie i rozwoj'",
                'action': lambda fact: {'wyjscie': 'Civilization VI',
                                        "description": "Turowa gra strategiczna, w której budujesz cywilizację od podstaw i rywalizujesz z innymi liderami.",
                                        "image": "result/civilization_vi.jpg"
                                        }},

            # Strategia - Multiplayer
            {'condition': "typ_gry == 'Strategia' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Age of Empires IV',
                                     "description": "Strategia czasu rzeczywistego, w której kierujesz imperium przez różne epoki historyczne.",
                                     "image": "result/age_of_empires_iv.jpg"
                                     }},
            {
                'condition': "typ_gry == 'Strategia' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Command & Conquer: Rivals',
                                        "description": "Strategiczna gra mobilna, w której rywalizujesz z innymi graczami w czasie rzeczywistym.",
                                        "image": "result/command_conquer_rivals.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Strategia' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'They Are Billions',
                                        "description": "Gra strategiczna o przetrwaniu, gdzie bronisz swojej kolonii przed hordami zombie.",
                                        "image": "result/they_are_billions.jpg"
                                        }},
            {'condition': "typ_gry == 'Strategia' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'StarCraft II',
                                     "description": "Klasyczna strategia czasu rzeczywistego osadzona w kosmosie, z trzema zróżnicowanymi rasami.",
                                     "image": "result/starcraft_ii.jpg"
                                     }},

            # Strategia - Kooperacja
            {'condition': "typ_gry == 'Strategia' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Northgard',
                                     "description": "Strategia czasu rzeczywistego inspirowana mitologią nordycką, w której zarządzasz klanem Wikingów.",
                                     "image": "result/northgard.jpg"
                                     }},
            {
                'condition': "typ_gry == 'Strategia' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Endless Space 2',
                                        "description": "Turowa strategia kosmiczna, w której budujesz imperium międzygwiezdne.",
                                        "image": "result/endless_space_2.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Strategia' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Halo Wars 2',
                                        "description": "Strategia czasu rzeczywistego osadzona w uniwersum Halo, z dynamicznymi walkami.",
                                        "image": "result/halo_wars_2.jpg"
                                        }},
            {'condition': "typ_gry == 'Strategia' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Company of Heroes 3',
                                     "description": "Gra strategiczna osadzona w realiach II wojny światowej, z taktycznymi bitwami.",
                                     "image": "result/company_of_heroes_3.jpg"
                                     }},

            {'condition': "typ_gry == 'Strategia' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Company of Heroes 3',
                                     "description": "Gra strategiczna osadzona w realiach II wojny światowej, z taktycznymi bitwami.",
                                     "image": "result/company_of_heroes_3.jpg"
                                     }},

            # Przygodowa - Single-player
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Single-player' and doswiadczenie == 'Walka i rywalizacja'",
                'action': lambda fact: {'wyjscie': 'Red Dead Redemption 2',
                                        "description": "Otwarty świat gry akcji osadzony na Dzikim Zachodzie, z bogatą fabułą i wciągającym światem.",
                                        "image": "result/red_dead_redemption_2.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Single-player' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Skyrim',
                                        "description": "Gra RPG osadzona w fantastycznym świecie, w której eksplorujesz otwarty świat i walczysz ze smokami.",
                                        "image": "result/skyrim.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Single-player' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'The Last of Us Part II',
                                        "description": "Narracyjna gra akcji, w której śledzisz historię Ellie w brutalnym, postapokaliptycznym świecie.",
                                        "image": "result/last_of_us_part_ii.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Single-player' and doswiadczenie == 'Budowanie i rozwoj'",
                'action': lambda fact: {'wyjscie': 'My Time at Portia',
                                        "description": "Symulator życia i zarządzania warsztatem w kolorowym świecie fantasy.",
                                        "image": "result/my_time_at_portia.jpg"
                                        }},

            # Przygodowa - Multiplayer
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Walka i rywalizacja'",
                'action': lambda fact: {'wyjscie': 'Sea of Thieves',
                                        "description": "Kooperacyjna gra akcji, w której wcielasz się w pirata, eksplorujesz morza i szukasz skarbów.",
                                        "image": "result/sea_of_thieves.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'No Manâ€™s Sky',
                                        "description": "Gra eksploracyjna osadzona w proceduralnie generowanym wszechświecie, gdzie odkrywasz planety i życie.",
                                        "image": "result/no_mans_sky.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Donâ€™t Starve Together',
                                        "description": "Kooperacyjna gra survivalowa z unikalnym stylem graficznym, gdzie walczysz o przetrwanie w dziczy.",
                                        "image": "result/dont_starve_together.jpg"
                                        }},
            {'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Valheim',
                                     "description": "Kooperacyjna gra survivalowa inspirowana mitologią nordycką, z otwartym światem i budowaniem.",
                                     "image": "result/valheim.jpg"
                                     }},

            # Przygodowa - Kooperacja
            {'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Minecraft Dungeons',
                                     "description": "Gra akcji osadzona w uniwersum Minecrafta, z dynamicznymi walkami i eksploracją lochów.",
                                     "image": "result/minecraft_dungeons.jpg"
                                     }},
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'It Takes Two',
                                        "description": "Kooperacyjna gra przygodowa, w której wcielasz się w małżeństwo próbujące uratować swój związek.",
                                        "image": "result/it_takes_two.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Raft',
                                        "description": "Gra survivalowa, w której budujesz tratwę i przetrwasz na oceanie, zbierając zasoby.",
                                        "image": "result/raft.jpg"
                                        }},
            {'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Grounded',
                                     "description": "Gra survivalowa, w której wcielasz się w miniaturową postać walczącą o przetrwanie w ogrodzie.",
                                     "image": "result/grounded.jpg"
                                     }},

            # Przygodowa - Single-player (cont.)
            {
                'condition': "typ_gry == 'Przygodowa' and tryb_gry == 'Single-player' and doswiadczenie == 'Walka i rywalizacja'",
                'action': lambda fact: {'wyjscie': 'The Sims 4',
                                        "description": "Symulator życia, w którym tworzysz i zarządzasz rodzinami w wirtualnym świecie.",
                                        "image": "result/sims_4.jpg"
                                        }},

            # Symulator - Single-player
            {
                'condition': "typ_gry == 'Symulator' and tryb_gry == 'Single-player' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Microsoft Flight Simulator',
                                        "description": "Realistyczny symulator lotu, oferujący szczegółowe odwzorowanie świata i samolotów.",
                                        "image": "result/flight_simulator.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Symulator' and tryb_gry == 'Single-player' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Surviving Mars',
                                        "description": "Gra strategiczna, w której budujesz i zarządzasz kolonią na Marsie.",
                                        "image": "result/surviving_mars.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Symulator' and tryb_gry == 'Single-player' and doswiadczenie == 'Budowanie i rozwoj'",
                'action': lambda fact: {'wyjscie': 'Kerbal Space Program',
                                        "description": "Symulator kosmiczny, w którym budujesz statki kosmiczne i eksplorujesz kosmos.",
                                        "image": "result/kerbal_space_program.jpg"
                                        }},

            # Symulator - Multiplayer
            {'condition': "typ_gry == 'Symulator' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Cities: Skylines Multiplayer',
                                     "description": "Gra strategiczna, w której budujesz i zarządzasz miastem, tym razem z opcją gry wieloosobowej.",
                                     "image": "result/cities_skylines_multiplayer.jpg"
                                     }},
            {
                'condition': "typ_gry == 'Symulator' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Farming Simulator 22',
                                        "description": "Symulator rolnictwa, w którym zarządzasz farmą i uprawiasz pola.",
                                        "image": "result/farming_simulator_22.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Symulator' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Eco',
                                        "description": "Gra survivalowa z ekologicznym podejściem, gdzie budujesz społeczność i chronisz środowisko.",
                                        "image": "result/eco.jpg"
                                        }},
            {'condition': "typ_gry == 'Symulator' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Roblox (tryby symulacyjne)',
                                     "description": "Platforma gier z różnorodnymi trybami symulacyjnymi tworzonymi przez społeczność.",
                                     "image": "result/roblox.jpg"
                                     }},

            # Symulator - Kooperacja
            {'condition': "typ_gry == 'Symulator' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Satisfactory',
                                     "description": "Gra o budowaniu fabryk w otwartym świecie, z elementami eksploracji.",
                                     "image": "result/satisfactory.jpg"
                                     }},
            {
                'condition': "typ_gry == 'Symulator' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Astroneer',
                                        "description": "Gra eksploracyjna, w której odkrywasz planety i zbierasz zasoby w kolorowym świecie sci-fi.",
                                        "image": "result/astroneer.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Symulator' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Space Engineers',
                                        "description": "Symulator konstrukcji i eksploracji kosmicznej, gdzie budujesz statki i bazy.",
                                        "image": "result/space_engineers.jpg"
                                        }},
            {'condition': "typ_gry == 'Symulator' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Factorio',
                                     "description": "Gra o budowie i optymalizacji fabryk, z elementami strategii.",
                                     "image": "result/factorio.jpg"
                                     }},

            # Symulator - Single-player (cont.)
            {
                'condition': "typ_gry == 'Symulator' and tryb_gry == 'Single-player' and doswiadczenie == 'Walka i rywalizacja'",
                'action': lambda fact: {'wyjscie': 'Resident Evil 4 Remake',
                                        "description": "Odświeżona wersja klasycznego survival horroru, w którym walczysz z przeciwnikami w tajemniczej wiosce.",
                                        "image": "result/resident_evil_4_remake.jpg"
                                        }},

            # Horror - Single-player
            {
                'condition': "typ_gry == 'Horror' and tryb_gry == 'Single-player' and doswiadczenie == 'Eksploracja i przygoda'",
                'action': lambda fact: {'wyjscie': 'Amnesia: The Dark Descent',
                                        "description": "Psychologiczny survival horror, w którym odkrywasz mroczne tajemnice opuszczonego zamku.",
                                        "image": "result/amnesia.jpg"
                                        }},
            {
                'condition': "typ_gry == 'Horror' and tryb_gry == 'Single-player' and doswiadczenie == 'Przetrwanie i wyzwanie'",
                'action': lambda fact: {'wyjscie': 'Outlast',
                                        "description": "Gra horrorowa z widokiem z pierwszej osoby, gdzie odkrywasz sekrety nawiedzonego szpitala psychiatrycznego.",
                                        "image": "result/outlast.jpg"
                                        }},
            {'condition': "typ_gry == 'Horror' and tryb_gry == 'Single-player' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'The Forest',
                                     "description": "Gra survivalowa, w której budujesz schronienia i walczysz z kanibalami na opuszczonej wyspie.",
                                     "image": "result/the_forest.jpg"
                                     }},

            # Horror - Multiplayer
            {'condition': "typ_gry == 'Horror' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Dead by Daylight',
                                     "description": "Asymetryczna gra wieloosobowa, w której jeden gracz wciela się w zabójcę, a inni próbują przetrwać.",
                                     "image": "result/dead_by_daylight.jpg"
                                     }},
            {'condition': "typ_gry == 'Horror' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Eksploracja i przygoda'",
             'action': lambda fact: {'wyjscie': 'Phasmophobia',
                                     "description": "Kooperacyjna gra horrorowa, w której badacie nawiedzone miejsca i próbujecie zidentyfikować duchy.",
                                     "image": "result/phasmophobia.jpg"
                                     }},
            {'condition': "typ_gry == 'Horror' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Przetrwanie i wyzwanie'",
             'action': lambda fact: {'wyjscie': 'The Forest',
                                     "description": "Gra survivalowa, w której budujesz schronienia i walczysz z kanibalami na opuszczonej wyspie.",
                                     "image": "result/the_forest.jpg"
                                     }},
            {'condition': "typ_gry == 'Horror' and tryb_gry == 'Multiplayer' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Don’t Starve Together',
                                     "description": "Kooperacyjna gra survivalowa z unikalnym stylem graficznym, gdzie walczysz o przetrwanie w dziczy.",
                                     "image": "result/dont_starve_together.jpg"
                                     }},

            # Horror - Kooperacja
            {'condition': "typ_gry == 'Horror' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Walka i rywalizacja'",
             'action': lambda fact: {'wyjscie': 'Dead by Daylight',
                                     "description": "Asymetryczna gra wieloosobowa, w której jeden gracz wciela się w zabójcę, a inni próbują przetrwać.",
                                     "image": "result/dead_by_daylight.jpg"
                                     }},
            {'condition': "typ_gry == 'Horror' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Eksploracja i przygoda'",
             'action': lambda fact: {'wyjscie': 'Phasmophobia',
                                     "description": "Kooperacyjna gra horrorowa, w której badacie nawiedzone miejsca i próbujecie zidentyfikować duchy.",
                                     "image": "result/phasmophobia.jpg"
                                     }},
            {'condition': "typ_gry == 'Horror' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Przetrwanie i wyzwanie'",
             'action': lambda fact: {'wyjscie': 'The Forest (Koop)',
                                     "description": "Gra survivalowa, w której wcielasz się w postać ocalałego z katastrofy lotniczej. Twoim zadaniem jest przetrwać na tajemniczej, opuszczonej wyspie, pełnej niebezpieczeństw. W trybie kooperacji możesz grać z innymi graczami, wspólnie budując schronienia, zbierając zasoby, polując na zwierzęta i walcząc z kanibalami oraz innymi zagrożeniami. Gra kładzie duży nacisk na eksplorację, craftowanie i przetrwanie w brutalnym środowisku, które nie daje wytchnienia.",
                                     "image": "result/the_forest_koop.jpg"
                                     }},
            {'condition': "typ_gry == 'Horror' and tryb_gry == 'Kooperacja' and doswiadczenie == 'Budowanie i rozwoj'",
             'action': lambda fact: {'wyjscie': 'Green Hell',
                                     "description": "Gra survivalowa osadzona w amazońskiej dżungli, gdzie walczysz o przetrwanie, mierząc się z dziką przyrodą, głodem i własną psychiką.",
                                     "image": "result/green_hell.jpg"
                                     }}]


          # Tworzymy instancję silnika reguł i przetwarzamy fakty
        for fact in facts:
            for rule in rules:
                try:
                    # Sprawdzanie warunku dla każdej reguły (przykład z użyciem eval)
                    if eval(rule['condition'], {}, fact):
                        # Jeśli warunek spełniony, dodajemy wynik do listy
                        results.append(rule['action'](fact))
                except Exception as e:
                    print(f"Error processing rule {rule['condition']}: {e}")

        # Wyświetlanie wyników (pierwszy wynik)
        if results:
            result = results[0]
            self.lb_result_prediction.setText(result['wyjscie'])
            self.result_desc_lb.setText(result['description'])
            pixmap = QPixmap(result['image'])
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
