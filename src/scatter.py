import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterToolUI(QtWidgets.QDialog):
    """Smart save ui class"""

    def __init__(self):
        super(ScatterToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(400)
        self.setMaximumWidth(1200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.button_lay = self._create_button_ui()
        layout = self._create_selection_layouts()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(layout)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    def _create_selection_layouts(self):
        self.item_to_scatter_header_lbl = QtWidgets.QLabel("Item to Scatter")
        self.item_to_scatter_header_lbl.setStyleSheet("font: bold")
        self.scatter_to_lbl = QtWidgets.QLabel("Scatter To")
        self.scatter_to_lbl.setStyleSheet("font: bold")
        self.rotation_lbl = QtWidgets.QLabel("Rotation")
        self.rotation_lbl.setStyleSheet("font: bold")
        self.resize_lbl = QtWidgets.QLabel("Scale")
        self.resize_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        #layout_rot = self._create_rotation_boxes()
        #layout_scl = self._create_size_boxes()
        second_select = self._create_select_second_ui()
        first_select = self._create_select_first_ui()
        layout.addWidget(self.item_to_scatter_header_lbl, 0, 0)
        layout.addWidget(self.scatter_to_lbl, 4, 0)
        layout.addWidget(second_select, 5, 0)
        layout.addWidget(first_select, 1, 0)
        layout.addWidget(self.resize_lbl, 7, 0)
        layout.addWidget(self.rotation_lbl, 9, 0)
        return layout

    def _create_rotation_boxes(self):
        self.x_sbx = QtWidgets.QSpinBox()
        self.x_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.x_sbx.setFixedWidth(50)
        self.x_sbx.setValue(0)
        self.x_sbx.setMaximum(180)
        self.x_sbx.setSingleStep(15)
        self.x_lbl = QtWidgets.QLabel("x")
        return self.x_sbx


    def _create_select_second_ui(self):
        layout = QtWidgets.QLineEdit("Type in an existing polygon name")
        return layout

    def _create_select_first_ui(self):
        layout = QtWidgets.QLineEdit("Type in an existing polygon name or type of polygon (ex. polySphere)")
        return layout
