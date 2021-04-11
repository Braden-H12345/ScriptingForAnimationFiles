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
        layout = self.create_labels()
        rot_x_sbx = self._set_sbx_properties()
        rot_y_sbx = self._set_sbx_properties()
        rot_z_sbx = self._set_sbx_properties()
        size_x_sbx = self._set_dsbx_properties()
        size_y_sbx = self._set_dsbx_properties()
        size_z_sbx = self._set_dsbx_properties()
        self.second_select = QtWidgets.QLineEdit("Type in an existing polygon name")
        self.first_select = QtWidgets.QLineEdit("Type in an existing polygon name or type of polygon (ex. polySphere)")
        self.first_select.setFixedWidth(450)
        layout.addWidget(self.second_select, 5, 0)
        layout.addWidget(self.first_select, 1, 0)

        layout.addWidget(rot_x_sbx, 1, 1)
        layout.addWidget(QtWidgets.QLabel("x"), 1, 2)
        layout.addWidget(rot_y_sbx, 1, 3)
        layout.addWidget(QtWidgets.QLabel("y"), 1, 4)
        layout.addWidget(rot_z_sbx, 1, 5)
        layout.addWidget(QtWidgets.QLabel("z"), 1, 6)

        layout.addWidget(size_x_sbx, 5, 1)
        layout.addWidget(QtWidgets.QLabel("x"), 5, 2)
        layout.addWidget(size_y_sbx, 5, 3)
        layout.addWidget(QtWidgets.QLabel("y"), 5, 4)
        layout.addWidget(size_z_sbx, 5, 5)
        layout.addWidget(QtWidgets.QLabel("z"), 5, 6)
        return layout

    def _set_sbx_properties(self):
        spinbox = QtWidgets.QSpinBox()
        spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        spinbox.setFixedWidth(50)
        spinbox.setValue(0)
        spinbox.setMaximum(180)
        spinbox.setSingleStep(15)
        return spinbox

    def _set_dsbx_properties(self):
        spinbox = QtWidgets.QDoubleSpinBox()
        spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        spinbox.setFixedWidth(50)
        spinbox.setValue(0)
        spinbox.setMaximum(50)
        spinbox.setSingleStep(.5)
        return spinbox

    def create_labels(self):
        layout = QtWidgets.QGridLayout()
        layout.setHorizontalSpacing(20)
        self.item_to_scatter_header_lbl = QtWidgets.QLabel("Item to Scatter")
        self.item_to_scatter_header_lbl.setStyleSheet("font: bold")
        self.scatter_to_lbl = QtWidgets.QLabel("Scatter To")
        self.scatter_to_lbl.setStyleSheet("font: bold")
        self.rotation_lbl = QtWidgets.QLabel("Rotation")
        self.rotation_lbl.setStyleSheet("font: bold")
        self.resize_lbl = QtWidgets.QLabel("Scale")
        self.resize_lbl.setStyleSheet("font: bold")
        layout.addWidget(self.item_to_scatter_header_lbl, 0, 0)
        layout.addWidget(self.scatter_to_lbl, 4, 0)
        layout.addWidget(self.resize_lbl, 4, 5)
        layout.addWidget(self.rotation_lbl, 0, 5)
        return layout

