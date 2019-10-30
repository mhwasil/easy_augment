import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
from shutil import copy
import os
import Main_Window
import main
from generate_artificial_images import perform_augmentation
from arguments import *
import progress_bar

class MainWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setGeometry(100,100,650,500)
        self.aig_form()
    def aig_form(self):
        self.nameLabel_num_images = QLabel(self)
        self.nameLabel_num_images.setText('Number of images:')
        self.nameLabel_num_images.move(50, 20)
        self.nameLabel_num_images.resize(200,40)
        self.num_images = QLineEdit(self)
        self.onlyInt = QIntValidator()
        self.num_images.setValidator(self.onlyInt)
        self.num_images.textChanged.connect(self.button_status)
        self.num_images.move(300, 20)
        self.num_images.resize(200,40)

        self.nameLabel_image_type = QLabel(self)
        self.nameLabel_image_type.setText('Image format:')
        self.nameLabel_image_type.move(50, 70)
        self.nameLabel_image_type.resize(200,40)
        self.image_type = QComboBox(self)
        self.image_type.addItem(".png")
        self.image_type.addItem(".jpg")
        self.image_type.move(300, 70)

        self.nameLabel_max_objects = QLabel(self)
        self.nameLabel_max_objects.setText('Maximum objects:')
        self.nameLabel_max_objects.move(50, 120)
        self.nameLabel_max_objects.resize(200,40)
        self.max_objects = QLineEdit(self)
        self.onlyInt = QIntValidator()
        self.max_objects.setValidator(self.onlyInt)
        self.max_objects.setText(str(3))
        self.max_objects.move(300, 120)
        self.max_objects.resize(200,40)

        self.nameLabel_image_folder = QLabel(self)
        self.nameLabel_image_folder.setText('Image folder path:')
        self.nameLabel_image_folder.move(50, 170)
        self.nameLabel_image_folder.resize(200,40)
        self.image_folder = QLineEdit(self)
        self.image_folder.setText('./images')
        self.image_folder.move(300, 170)
        self.image_folder.resize(200,40)
        self.button2 = QPushButton("Change",self)
        self.button2.clicked.connect(self.change_image_folder)
        self.button2.move(520,170)
        self.button2.resize(100,40)

        self.nameLabel_label_folder = QLabel(self)
        self.nameLabel_label_folder.setText('Semantic labels folder path:')
        self.nameLabel_label_folder.move(50, 220)
        self.nameLabel_label_folder.resize(200,40)
        self.label_folder = QLineEdit(self)
        self.label_folder.setText('./semantic_labels')
        self.label_folder.move(300, 220)
        self.label_folder.resize(200,40)
        self.button3 = QPushButton("Change",self)
        self.button3.clicked.connect(self.change_labels_folder)
        self.button3.move(520,220)
        self.button3.resize(100,40)

        self.button1 = QPushButton("Ok",self)
        self.button1.clicked.connect(self.ok_button)
        self.button1.resize(150,20)
        self.button1.move(200,450)
        self.button1.setEnabled(False)
        return self.num_images.text()

    def change_image_folder(self):
        folderpath_dlg = QFileDialog()
        folderpath_dlg.setFileMode(QFileDialog.Directory)
        folderpath = folderpath_dlg.getExistingDirectory()
        self.image_folder.setText(folderpath)
    def change_labels_folder(self):
        folderpath_dlg = QFileDialog()
        folderpath_dlg.setFileMode(QFileDialog.Directory)
        folderpath = folderpath_dlg.getExistingDirectory()
        self.label_folder.setText(folderpath)
    def button_status(self):
        if len(self.num_images.text())>0:
            self.button1.setEnabled(True)
    def ok_button(self):
        generator_options = GeneratorOptions()
        generator_options.set_num_images(int(self.num_images.text()))
        generator_options.set_image_type(self.image_type.currentText())
        generator_options.set_max_objects(int(self.max_objects.text()))
        generator_options.set_image_path(self.image_folder.text())
        generator_options.set_label_path(self.label_folder.text())
        flag = perform_augmentation()
        if flag:
            self.progress_bar_obj = progress_bar.MainWindow()
            self.progress_bar_obj.show()
            self.hide()
