import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
from shutil import copy, rmtree
import os
from utils.arguments import *
from utils.generate_artificial_images import perform_augmentation
import progress_bar
import utils.image_resize as image_resize
from pathlib import Path

print("inside AIG_Window")

class MainWindow(QWidget):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__))+'/b-it-bots.jpg'))
        self.setGeometry(100,100,650,700)
        self.aig_form()
    def aig_form(self):
        self.home_path = str(Path.home())

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
        self.image_folder.setText(self.home_path)
        self.image_folder.move(300, 170)
        self.image_folder.resize(200,40)
        self.button2 = QPushButton("Change",self)
        self.button2.clicked.connect(self.change_image_folder)
        self.image_folder.textChanged.connect(self.button_status)
        self.button2.move(520,170)
        self.button2.resize(100,40)

        self.nameLabel_label_folder = QLabel(self)
        self.nameLabel_label_folder.setText('Semantic labels folder path:')
        self.nameLabel_label_folder.move(50, 220)
        self.nameLabel_label_folder.resize(200,40)
        self.label_folder = QLineEdit(self)
        self.label_folder.setText(self.home_path)
        self.label_folder.move(300, 220)
        self.label_folder.resize(200,40)
        self.button3 = QPushButton("Change",self)
        self.button3.clicked.connect(self.change_labels_folder)
        self.button3.move(520,220)
        self.button3.resize(100,40)

        self.nameLabel_backgrounds_folder = QLabel(self)
        self.nameLabel_backgrounds_folder.setText('Backgrounds folder path:')
        self.nameLabel_backgrounds_folder.move(50, 270)
        self.nameLabel_backgrounds_folder.resize(200,40)
        self.backgrounds_folder = QLineEdit(self)
        self.backgrounds_folder.setText(self.home_path)
        self.backgrounds_folder.move(300, 270)
        self.backgrounds_folder.resize(200,40)
        self.button3 = QPushButton("Change",self)
        self.button3.clicked.connect(self.change_backgrounds_folder)
        self.button3.move(520,270)
        self.button3.resize(100,40)

        self.nameLabel_image_dimension = QLabel(self)
        self.nameLabel_image_dimension.setText('Output image dimension:')
        self.nameLabel_image_dimension.move(50, 320)
        self.nameLabel_image_dimension.resize(200,40)
        self.image_dimension2 = QLineEdit(self)
        self.image_dimension2.setText('640')
        self.image_dimension2.move(300, 320)
        self.image_dimension2.resize(90,40)
        self.image_dimension1 = QLineEdit(self)
        self.image_dimension1.setText('480')
        self.image_dimension1.move(400, 320)
        self.image_dimension1.resize(90,40)
        self.onlyInt = QIntValidator()
        self.image_dimension1.setValidator(self.onlyInt)
        self.image_dimension2.setValidator(self.onlyInt)

        self.nameLabel_labels_file_path = QLabel(self)
        self.nameLabel_labels_file_path.setText('Labels.txt file path:')
        self.nameLabel_labels_file_path.move(50, 370)
        self.nameLabel_labels_file_path.resize(200,40)
        self.labels_file_path = QLineEdit(self)
        self.labels_file_path.setText(self.home_path)
        self.labels_file_path.move(300, 370)
        self.labels_file_path.resize(200,40)
        self.button5 = QPushButton("Change",self)
        self.button5.clicked.connect(self.change_labels_file_path)
        self.button5.move(520,370)
        self.button5.resize(100,40)

        self.nameLabel_image_save_path = QLabel(self)
        self.nameLabel_image_save_path.setText('Images and labels save path:')
        self.nameLabel_image_save_path.move(50, 420)
        self.nameLabel_image_save_path.resize(200,40)
        self.image_save_path = QLineEdit(self)
        self.image_save_path.setText(self.home_path)
        self.image_save_path.move(300, 420)
        self.image_save_path.resize(200,40)
        self.button6 = QPushButton("Change",self)
        self.button6.clicked.connect(self.change_image_save_path)
        self.button6.move(520,420)
        self.button6.resize(100,40)

        self.group_1 = QGroupBox(self)
        self.nameLabel_save_obj_det_label = QLabel(self)
        self.nameLabel_save_obj_det_label.setText('Save object detection label:')
        self.nameLabel_save_obj_det_label.move(50, 470)
        self.nameLabel_save_obj_det_label.resize(200,40)
        self.rbutton1 = QRadioButton("True",self)
        # self.rbutton1.move(300,470)
        self.rbutton2 = QRadioButton("False",self)
        self.rbutton2.setChecked(True)
        # self.rbutton2.move(400,470)
        self.hbox_1 = QHBoxLayout(self)
        self.hbox_1.addWidget(self.rbutton1)
        self.hbox_1.addWidget(self.rbutton2)
        self.hbox_1.addStretch(1)
        self.group_1.setLayout(self.hbox_1)
        self.group_1.move(300,450)
        self.group_1.resize(200,60)
        self.rbutton1.toggled.connect(self.button_status)
        self.label_flag = False

        self.group_2 = QGroupBox(self)
        self.nameLabel_save_mask = QLabel(self)
        self.nameLabel_save_mask.setText('Save mask of generated data:')
        self.nameLabel_save_mask.move(50, 520)
        self.nameLabel_save_mask.resize(200,40)
        self.rbutton3 = QRadioButton("True",self)
        self.rbutton4 = QRadioButton("False",self)
        self.rbutton4.setChecked(True)
        self.hbox_2 = QHBoxLayout(self)
        self.hbox_2.addWidget(self.rbutton3)
        self.hbox_2.addWidget(self.rbutton4)
        self.hbox_2.addStretch(1)
        self.group_2.setLayout(self.hbox_2)
        self.group_2.move(300,500)
        self.group_2.resize(200,60)
        self.save_mask_flag = False


        self.button1 = QPushButton("Ok",self)
        self.button1.clicked.connect(self.ok_button)
        self.button1.resize(150,20)
        self.button1.move(200,600)
        self.button1.setEnabled(False)
        return self.num_images.text()

    def change_save_obj_det_label_path_folder(self):
        folderpath_dlg = QFileDialog()
        folderpath_dlg.setFileMode(QFileDialog.Directory)
        folderpath = folderpath_dlg.getExistingDirectory()
        self.save_obj_det_label_path.setText(folderpath)
    def change_labels_file_path(self):
        filepath = QFileDialog.getOpenFileNames(filter='*.txt')
        self.labels_file_path.setText(filepath[0][0])

    def change_image_save_path(self):
        folderpath_dlg = QFileDialog()
        folderpath_dlg.setFileMode(QFileDialog.Directory)
        folderpath = folderpath_dlg.getExistingDirectory()
        self.image_save_path.setText(folderpath)
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
    def change_backgrounds_folder(self):
        folderpath_dlg = QFileDialog()
        folderpath_dlg.setFileMode(QFileDialog.Directory)
        folderpath = folderpath_dlg.getExistingDirectory()
        self.backgrounds_folder.setText(folderpath)
    def button_status(self):
        if len(self.num_images.text())>0 and self.image_folder.text() != self.home_path and self.label_folder.text() != self.home_path and self.backgrounds_folder.text() != self.home_path:
            print(self.image_folder.text()!=self.home_path)
            print("inside button status")
            self.button1.setEnabled(True)
        else :
            self.button1.setEnabled(False)
    def ok_button(self):
        if not os.path.exists(self.backgrounds_folder.text()+"/temp/"):
            os.makedirs(self.backgrounds_folder.text()+"/temp/",)
        elif os.path.exists(self.backgrounds_folder.text()+"/temp/"):
            rmtree(self.backgrounds_folder.text()+"/temp/")
            os.makedirs(self.backgrounds_folder.text()+"/temp/",)
        if not os.path.exists(self.image_folder.text()+"/temp/"):
            os.makedirs(self.image_folder.text()+"/temp/",)
        elif os.path.exists(self.image_folder.text()+"/temp/"):
            rmtree(self.image_folder.text()+"/temp/")
            os.makedirs(self.image_folder.text()+"/temp/",)
        if not os.path.exists(self.label_folder.text()+"/temp/"):
            os.makedirs(self.label_folder.text()+"/temp/",)
        elif os.path.exists(self.label_folder.text()+"/temp/"):
            rmtree(self.label_folder.text()+"/temp/")
            os.makedirs(self.label_folder.text()+"/temp/",)
        if not os.path.exists(self.image_save_path.text()+"/augmented/images/"):
            os.makedirs(self.image_save_path.text()+"/augmented/images/",)
        elif os.path.exists(self.image_save_path.text()+"/augmented/images/"):
            rmtree(self.image_save_path.text()+"/augmented/images/")
            os.makedirs(self.image_save_path.text()+"/augmented/images/",)
        if not os.path.exists(self.image_save_path.text()+"/augmented/labels/"):
            os.makedirs(self.image_save_path.text()+"/augmented/labels/",)
        elif os.path.exists(self.image_save_path.text()+"/augmented/labels/"):
            rmtree(self.image_save_path.text()+"/augmented/labels/")
            os.makedirs(self.image_save_path.text()+"/augmented/labels/",)
        if not os.path.exists(self.image_save_path.text()+"/augmented/obj_det_label/"):
            os.makedirs(self.image_save_path.text()+"/augmented/obj_det_label/",)
        elif os.path.exists(self.image_save_path.text()+"/augmented/obj_det_label/"):
            rmtree(self.image_save_path.text()+"/augmented/obj_det_label/")
            os.makedirs(self.image_save_path.text()+"/augmented/obj_det_label/",)
        if not os.path.exists(self.image_save_path.text()+"/augmented/masks/"):
            os.makedirs(self.image_save_path.text()+"/augmented/masks/",)
        elif os.path.exists(self.image_save_path.text()+"/augmented/masks/"):
            rmtree(self.image_save_path.text()+"/augmented/masks/")
            os.makedirs(self.image_save_path.text()+"/augmented/masks/",)
        if self.rbutton1.isChecked():
            self.label_flag = True
        elif self.rbutton2.isChecked():
            self.label_flag = False
        if self.rbutton3.isChecked():
            self.save_mask_flag = True
        elif self.rbutton4.isChecked():
            self.save_mask_flag = False
        image_resize.resize_images(self.backgrounds_folder.text(),[int(self.image_dimension1.text()),int(self.image_dimension2.text())])
        image_resize.resize_images(self.image_folder.text(),[int(self.image_dimension1.text()),int(self.image_dimension2.text())])
        image_resize.resize_images(self.label_folder.text(),[int(self.image_dimension1.text()),int(self.image_dimension2.text())])
        generator_options = GeneratorOptions()
        generator_options.set_num_images(int(self.num_images.text()))
        generator_options.set_image_type(self.image_type.currentText())
        generator_options.set_max_objects(int(self.max_objects.text()))
        generator_options.set_image_path(self.image_folder.text()+"/temp/")
        generator_options.set_label_path(self.label_folder.text()+"/temp/")
        generator_options.set_backgrounds_path(self.backgrounds_folder.text()+"/temp/")
        generator_options.set_image_dimension([int(self.image_dimension1.text()),int(self.image_dimension2.text())])
        generator_options.set_save_obj_det_label(self.label_flag)
        generator_options.set_obj_det_save_path(self.image_save_path.text()+"/augmented/obj_det_label")
        generator_options.set_image_save_path(self.image_save_path.text()+"/augmented/images")
        generator_options.set_label_save_path(self.image_save_path.text()+"/augmented/labels")
        generator_options.set_labels_file_path(self.labels_file_path.text())
        generator_options.set_save_mask(self.save_mask_flag)
        generator_options.set_mask_save_path(self.image_save_path.text()+"/augmented/masks")

        flag = perform_augmentation(generator_options)
        if flag:
            self.progress_bar_obj = progress_bar.MainWindow()
            self.progress_bar_obj.show()
            self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
