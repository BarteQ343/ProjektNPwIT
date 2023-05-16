from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QCheckBox, QFileDialog, QMainWindow
from PyQt5.QtCore import Qt
import os
import sys
import json
import yaml
import xmltodict
import threading

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Konwerter plików")
        self.setGeometry(100, 100, 570, 600)
        widget = QWidget()
        self.setCentralWidget(widget)
        self.setStyleSheet("""
            QPushButton {
                border-style: solid;
                border-width: 2px;
                border-radius: 8px;
                border-color: #4F4F4F;
                padding: 5px;
                background-color: #1E1E1E;
                color: #F0F0F0;
            }
            QPushButton:hover {
                border-color: #2196F3;
                color: #2196F3;
            }
            QPushButton:pressed {
                background-color: #2196F3;
                color: #FFFFFF;
            }
            QWidget {
                background-color: #212121;
                color: #FFFFFF;
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 32px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #2c2c2c;
                color: #FFFFFF;
                padding: 10px;
            }
        """)

        max_width = int(self.width() * 0.95)

        big_label = QLabel("Konwerter plików XML, YML, JSON", widget)
        big_label.setAlignment(Qt.AlignCenter)
        big_label.setStyleSheet("margin-bottom: 16px; margin-left: 0")

        self.small_label = QLabel("Wybierz plik do konwersji:", widget)
        self.small_label.setAlignment(Qt.AlignCenter)
        self.small_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-right: 16px")
        self.small_label.setMaximumWidth(max_width)

        self.button = QPushButton("Przeglądaj...", widget)
        self.button.setMaximumWidth(max_width)
        self.button.clicked.connect(self.openFileDialog)

        self.checkBoxXML = QCheckBox("Konwertuj na XML", widget)
        self.checkBoxYML = QCheckBox("Konwertuj na YML", widget)
        self.checkBoxJSON = QCheckBox("Konwertuj na JSON", widget)
        self.checkBoxXML.setEnabled(False)
        self.checkBoxJSON.setEnabled(False)
        self.checkBoxYML.setEnabled(False)

        self.small_label2 = QLabel("Obecnie wybrany katalog zapisu:\n"+ROOT_DIR, widget)
        self.small_label2.setAlignment(Qt.AlignCenter)
        self.small_label2.setStyleSheet("font-size: 16px; font-weight: bold; margin-right: 16px")

        self.button2 = QPushButton("Przeglądaj...", widget)
        self.button2.setMaximumWidth(max_width)
        self.button2.clicked.connect(self.openFolderDialog)

        self.button3 = QPushButton("Konwertuj", widget)
        self.button3.setMaximumWidth(max_width)
        self.button3.clicked.connect(self.Convert)

        self.small_label3 = QLabel("", widget)
        self.small_label3.setAlignment(Qt.AlignCenter)
        self.small_label3.setStyleSheet("font-size: 16px; font-weight: bold; margin-right: 16px")

        self.small_label4 = QLabel("", widget)
        self.small_label4.setAlignment(Qt.AlignCenter)
        self.small_label4.setStyleSheet("font-size: 16px; font-weight: bold; margin-right: 16px")

        v_layout = QVBoxLayout()

        sub_layout0 = QHBoxLayout()
        sub_layout0.addWidget(big_label)
        sub_layout0.setContentsMargins(10, 5, 10, 0)
        sub_layout0.setSpacing(0)
        v_layout.addLayout(sub_layout0)

        sub_layout1 = QHBoxLayout()
        sub_layout1.addWidget(self.small_label)
        sub_layout1.addWidget(self.button)
        checkBoxLayout = QVBoxLayout()
        checkBoxLayout.addWidget(self.checkBoxXML)
        checkBoxLayout.addWidget(self.checkBoxYML)
        checkBoxLayout.addWidget(self.checkBoxJSON)
        sub_layout1.addLayout(checkBoxLayout)
        sub_layout1.setContentsMargins(10, 0, 10, 10)
        sub_layout1.setSpacing(10)
        v_layout.addLayout(sub_layout1)

        sub_layout2 = QVBoxLayout()
        sub_layout2.addWidget(self.small_label2)
        sub_layout2.addWidget(self.button2)
        sub_layout2.addWidget(self.button3)
        sub_layout2.setContentsMargins(10, 0, 10, 10)
        sub_layout2.setSpacing(10)
        v_layout.addLayout(sub_layout2)

        sub_layout3 = QVBoxLayout()
        sub_layout3.addWidget(self.small_label3)
        sub_layout3.addWidget(self.small_label4)
        sub_layout3.setContentsMargins(10, 0, 10, 10)
        sub_layout3.setSpacing(10)
        v_layout.addLayout(sub_layout3)

        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)

        widget.setLayout(h_layout)

        self.fileDir = ROOT_DIR

    def openFolderDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        self.fileDir = ROOT_DIR
        fileDirTmp = QFileDialog.getExistingDirectory(self,"Wybierz miejsce zapisu", "", options=options)
        if fileDirTmp == "":
            fileDirLoc = "Obecnie wybrany katalog zapisu:\n"+ROOT_DIR
            self.small_label2.setText(fileDirLoc)
        else:
            self.fileDir = fileDirTmp
            fileDirLoc = "Obecnie wybrany katalog zapisu:\n"+self.fileDir
            self.small_label2.setText(fileDirLoc)

    def openFileDialog(self):
        self.checkBoxXML.setChecked(False)
        self.checkBoxJSON.setChecked(False)
        self.checkBoxYML.setChecked(False)
        options = QFileDialog.Options()
        filter = "Config files (*.xml *.json *.yml *.yaml)"
        fileTmp = QFileDialog.getOpenFileName(self,"Wybierz plik do konwersji", "", filter, options=options)
        fileTmp = ','.join(map(str, (fileTmp))).split(',')[0]
        if fileTmp == "":
            fileLoc = "Nie wybrano żadnego pliku\n"
            self.small_label.setText(fileLoc)
        else:
            self.file = fileTmp
            fileLoc = "Obecnie wybrany plik:\n"+self.file
            self.small_label.setText(fileLoc)
            self.fileExtension = self.file.split('.')[-1]
            if self.fileExtension == 'xml':
                self.checkBoxXML.setEnabled(False)
                self.checkBoxJSON.setEnabled(True)
                self.checkBoxYML.setEnabled(True)
            elif self.fileExtension == 'json':
                self.checkBoxXML.setEnabled(True)
                self.checkBoxJSON.setEnabled(False)
                self.checkBoxYML.setEnabled(True)
            else:
                self.checkBoxXML.setEnabled(True)
                self.checkBoxJSON.setEnabled(True)
                self.checkBoxYML.setEnabled(False)

    def Convert(self):

        def conv_to_xml():
            outputFile = self.file.split('/')[-1]
            outputPath = fileDir+'\\'+outputFile.split('.')[0]+'.xml'
            if fileExtension == 'yml' or fileExtension == 'yaml':
                xml_file = open(outputPath, "w")
                xmltodict.unparse(data, output=xml_file, pretty=True)
                xml_file.close()
            elif fileExtension == 'json':
                    xml_file = open(outputPath, "w")
                    xmltodict.unparse(data, output=xml_file, pretty=True)
                    xml_file.close()

        def conv_to_yaml():
            outputFile = self.file.split('/')[-1]
            outputPath = fileDir+'\\'+outputFile.split('.')[0]+'.yaml'
            if fileExtension == 'json':
                with open(outputPath, 'w') as file:
                    yaml.dump(data, file, indent=4)
                    file.close()
            elif fileExtension == 'xml':
                yaml_data = yaml.dump(data, indent=4)
                with open(outputPath, "w") as yaml_file:
                    yaml_file.write(yaml_data)
                    yaml_file.close()

        def conv_to_json():
            outputFile = self.file.split('/')[-1]
            outputPath = fileDir+'\\'+outputFile.split('.')[0]+'.json'
            if fileExtension == 'yml' or fileExtension == 'yaml':
                    with open(outputPath, 'w') as file:
                        json.dump(data, file, indent=4)
                        file.close()
            elif fileExtension == 'xml':
                json_data = json.dumps(data, indent=4)
                with open(outputPath, "w") as json_file:
                    json_file.write(json_data)
                    json_file.close()

        if hasattr(self, 'file'):
            file = self.file
            fileExtension = self.fileExtension
            fileDir = self.fileDir
            print(file)
            self.small_label3.setText("")
            self.small_label4.setText("")
            if fileExtension == 'json':
                with open(file, 'r') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError as e:
                        self.small_label3.setText('Plik uszkodzony.', str(e))
            if fileExtension == 'yaml' or fileExtension == 'yml':
                with open(file, 'r') as file:
                    try:
                        data = yaml.safe_load(file)
                    except yaml.YAMLError as e:
                        self.small_label3.setText('Plik uszkodzony.', str(e))
            if fileExtension == 'xml':
                try:
                    with open(file) as xml_file:
                        data = xmltodict.parse(xml_file.read())
                except xmltodict.ExpatError as e:
                    self.small_label3.setText('Plik uszkodzony.', str(e))
            if self.checkBoxJSON.isChecked() == False and self.checkBoxXML.isChecked() == False and self.checkBoxYML.isChecked() == False:
                self.small_label3.setText("Wybierz na co przekonwertować plik!")
            else:
                if self.checkBoxXML.isChecked():
                    xmlTH = threading.Thread(target=conv_to_xml)
                    xmlTH.start()
                    self.small_label3.setText("Konwersja na plik XML ukończona")
                else:
                    print("XML_False")
                if self.checkBoxYML.isChecked():
                    yamlTH = threading.Thread(target=conv_to_yaml)
                    yamlTH.start()
                    if self.small_label3.text() == "Konwersja na plik XML ukończona":
                        self.small_label4.setText("Konwersja na plik YAML ukończona")
                    else:
                        self.small_label3.setText("Konwersja na plik YAML ukończona")
                else:
                    print("YML_False")
                if self.checkBoxJSON.isChecked():
                    jsonTH = threading.Thread(target=conv_to_json)
                    jsonTH.start()
                    if self.small_label3.text() == "":
                        self.small_label3.setText("Konwersja na plik JSON ukończona")
                    else:
                        self.small_label4.setText("Konwersja na plik JSON ukończona")
                else:
                    print("JSON_False")
        else:
            self.small_label.setText("Wybierz najpierw plik do konwersji")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
