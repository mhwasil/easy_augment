import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
from shutil import copy, rmtree
import os
from utils.arguments import *
from utils.generate_artificial_images import perform_augmentation
from utils.labelme2voc import convert_to_voc
from utils.make_semantic_labels import generate_semantic_labels
import gui.progress_bar
from utils.preprocessing import resize_images, rename_images_labels, rename_backgrounds
from pathlib import Path
from gui import camera_window, aig_window_2



class MainWindow(QWidget):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(
            os.path.realpath(__file__))+'/data/b-it-bots.jpg'))
        self.setGeometry(100, 100, 700, 500)
        self.aig_form()

    def aig_form(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.home_path = str(Path.home())

        self.capture_button = QPushButton("Capture", self)
        self.capture_button.clicked.connect(self.capture_button_action)
        self.capture_button.resize(150, 20)
        self.capture_button.move(275, 50)
        self.capture_button.setEnabled(True)

        self.nameLabel_save_folder = QLabel(self)
        self.nameLabel_save_folder.setText('Save folder path:')
        self.nameLabel_save_folder.move(50, 100)
        self.nameLabel_save_folder.resize(200, 40)
        self.nameLabel_save_folder.hide()
        self.save_folder = QLineEdit(self)
        self.save_folder.setText(self.home_path)
        self.save_folder.move(300, 100)
        self.save_folder.resize(200, 40)
        self.save_folder.hide()
        self.change_save_dir_button = QPushButton("Change", self)
        self.change_save_dir_button.clicked.connect(self.change_save_folder)
        self.change_save_dir_button.move(520, 110)
        self.change_save_dir_button.resize(100, 20)
        self.change_save_dir_button.hide()

        self.continue_button = QPushButton("Continue", self)
        self.continue_button.clicked.connect(self.continue_button_action)
        self.continue_button.resize(150, 20)
        self.continue_button.move(175, 200)
        self.continue_button.setEnabled(True)
        self.continue_button.hide()
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.back_button_action)
        self.back_button.resize(150, 20)
        self.back_button.move(375, 200)
        self.back_button.setEnabled(True)
        self.back_button.hide()

        self.annotations_button = QPushButton("Have Annotations", self)
        self.annotations_button.clicked.connect(self.annotations_button_action)
        self.annotations_button.resize(150, 20)
        self.annotations_button.move(275, 150)
        self.annotations_button.setEnabled(True)

        self.source_folder_label = QLabel(self)
        self.source_folder_label.setText('Source folder path:')
        self.source_folder_label.move(100, 200)
        self.source_folder_label.resize(200, 40)
        self.source_folder_label.hide()
        self.source_folder = QLineEdit(self)
        self.source_folder.setText(self.home_path)
        self.source_folder.move(300, 200)
        self.source_folder.resize(200, 40)
        self.source_folder.hide()
        self.change_src_dir_button = QPushButton("Change", self)
        self.change_src_dir_button.clicked.connect(self.change_source_folder)
        self.change_src_dir_button.move(520, 210)
        self.change_src_dir_button.resize(100, 20)
        self.change_src_dir_button.hide()

        self.nameLabel_save_folder_2 = QLabel(self)
        self.nameLabel_save_folder_2.setText('Save folder path:')
        self.nameLabel_save_folder_2.move(100, 250)
        self.nameLabel_save_folder_2.resize(200, 40)
        self.nameLabel_save_folder_2.hide()
        self.save_folder_2 = QLineEdit(self)
        self.save_folder_2.setText(self.home_path)
        self.save_folder_2.move(300, 250)
        self.save_folder_2.resize(200, 40)
        self.save_folder_2.hide()
        self.button9 = QPushButton("Change", self)
        self.button9.clicked.connect(self.change_save_folder_2)
        self.button9.move(520, 260)
        self.button9.resize(100, 20)
        self.button9.hide()

        self.nameLabel_labels_file_path = QLabel(self)
        self.nameLabel_labels_file_path.setText('Labels.txt file path:')
        self.nameLabel_labels_file_path.move(100, 300)
        self.nameLabel_labels_file_path.resize(200, 40)
        self.nameLabel_labels_file_path.hide()
        self.labels_file_path = QLineEdit(self)
        self.labels_file_path.setText(self.home_path)
        self.labels_file_path.move(300, 300)
        self.labels_file_path.resize(200, 40)
        self.labels_file_path.hide()
        self.capture_button0 = QPushButton("Change", self)
        self.capture_button0.clicked.connect(self.change_labels_file_path)
        self.capture_button0.move(520, 310)
        self.capture_button0.resize(100, 20)
        self.capture_button0.hide()

        self.button7 = QPushButton("Continue", self)
        #self.button7.clicked.connect(self.continue_button_action_annotations)
        self.button7.resize(150, 20)
        self.button7.move(175, 350)
        self.button7.setEnabled(True)
        self.button7.hide()
        self.button8 = QPushButton("Back", self)
        self.button8.clicked.connect(self.back_button_action)
        self.button8.resize(150, 20)
        self.button8.move(375, 350)
        self.button8.setEnabled(True)
        self.button8.hide()

    def change_save_folder(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.folderpath_dlg_3 = QFileDialog()
        self.folderpath_dlg_3.setFileMode(QFileDialog.Directory)
        folderpath = self.folderpath_dlg_3.getExistingDirectory()
        self.save_folder.setText(folderpath)

    def change_source_folder(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.folderpath_dlg_3 = QFileDialog()
        self.folderpath_dlg_3.setFileMode(QFileDialog.Directory)
        folderpath = self.folderpath_dlg_3.getExistingDirectory()
        self.source_folder.setText(folderpath)

    def change_save_folder_2(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.folderpath_dlg_3 = QFileDialog()
        self.folderpath_dlg_3.setFileMode(QFileDialog.Directory)
        folderpath = self.folderpath_dlg_3.getExistingDirectory()
        self.save_folder_2.setText(folderpath)

    def change_labels_file_path(self):
        filepath = QFileDialog.getOpenFileNames(filter='*.txt')
        self.labels_file_path.setText(filepath[0][0])

    def capture_button_action(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.nameLabel_save_folder.show()
        self.save_folder.show()
        self.change_save_dir_button.show()
        self.continue_button.show()
        self.back_button.show()
        self.annotations_button.hide()

        self.capture_button.setEnabled(False)
        self.annotations_button.setEnabled(False)

    def annotations_button_action(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.source_folder_label.show()
        self.nameLabel_save_folder_2.show()
        self.nameLabel_labels_file_path.show()
        self.save_folder_2.show()
        self.source_folder.show()
        self.labels_file_path.show()
        self.change_src_dir_button.show()
        self.button7.show()
        self.button8.show()
        self.button9.show()
        self.capture_button0.show()

        self.capture_button.setEnabled(False)
        self.annotations_button.setEnabled(False)

    def back_button_action(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.nameLabel_save_folder_2.hide()
        self.nameLabel_save_folder.hide()
        self.source_folder_label.hide()
        self.nameLabel_labels_file_path.hide()
        self.save_folder_2.hide()
        self.save_folder.hide()
        self.source_folder.hide()
        self.labels_file_path.hide()
        self.change_save_dir_button.hide()
        self.continue_button.hide()
        self.back_button.hide()
        self.change_src_dir_button.hide()
        self.button9.hide()
        self.capture_button0.hide()
        self.button7.hide()
        self.button8.hide()

        self.annotations_button.show()

        self.capture_button.setEnabled(True)
        self.annotations_button.setEnabled(True)

    def continue_button_action(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        if not os.path.exists(self.save_folder.text()+"/captured_data/images/"):
            os.makedirs(self.save_folder.text()+"/captured_data/images/",)
        elif os.path.exists(self.save_folder.text()+"/captured_data/images/"):
            rmtree(self.save_folder.text()+"/captured_data/images/")
            os.makedirs(self.save_folder.text()+"/captured_data/images/",)
        if not os.path.exists(self.save_folder.text()+"/captured_data/labels/"):
            os.makedirs(self.save_folder.text()+"/captured_data/labels/",)
        elif os.path.exists(self.save_folder.text()+"/captured_data/labels/"):
            rmtree(self.save_folder.text()+"/captured_data/labels/")
            os.makedirs(self.save_folder.text()+"/captured_data/labels/",)
        if not os.path.exists(self.save_folder.text()+"/captured_data/obj_det_label/"):
            os.makedirs(self.save_folder.text()+"/captured_data/obj_det_label/",)
        elif os.path.exists(self.save_folder.text()+"/captured_data/obj_det_label/"):
            rmtree(self.save_folder.text()+"/captured_data/obj_det_label/")
            os.makedirs(self.save_folder.text()+"/captured_data/obj_det_label/",)
        if not os.path.exists(self.save_folder.text()+"/captured_data/pointclouds/"):
            os.makedirs(self.save_folder.text()+"/captured_data/pointclouds/",)
        elif os.path.exists(self.save_folder.text()+"/captured_data/pointclouds/"):
            rmtree(self.save_folder.text()+"/captured_data/pointclouds/")
            os.makedirs(self.save_folder.text()+"/captured_data/pointclouds/",)
        if not os.path.exists(self.save_folder.text()+"/captured_data/frame_data/"):
            os.makedirs(self.save_folder.text()+"/captured_data/frame_data/",)
        elif os.path.exists(self.save_folder.text()+"/captured_data/frame_data/"):
            rmtree(self.save_folder.text()+"/captured_data/frame_data/")
            os.makedirs(self.save_folder.text()+"/captured_data/frame_data/",)

        generator_options = GeneratorOptions()
        generator_options.set_image_path(self.save_folder.text()+"/captured_data/images/")
        generator_options.set_label_path(self.save_folder.text()+"/captured_data/labels/")
        self.cam_window = camera_window.App(generator_options, self.save_folder.text())
        self.cam_window.show()
        self.hide()

    def continue_button_annotations(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        convert_to_voc(self.source_folder.text(), self.save_folder_2.text(),
                       self.labels_file_path.text())
        generate_semantic_labels(self.save_folder_2.text()+"/voc_data", self.save_folder_2.text())
        generator_options = GeneratorOptions()
        generator_options.set_image_path(self.save_folder_2.text()+"/voc_data/JPEGImages")
        generator_options.set_label_path(self.save_folder_2.text()+"/semantic_labels")
        generator_options.set_labels_file_path(self.labels_file_path.text())
        self.aig_window = aig_window_2.MainWindow(generator_options)
        self.aig_window.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
