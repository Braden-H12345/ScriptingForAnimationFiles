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
        self.button_lay = self._create_buttons_ui()
        layout = self._create_selection_layouts()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(layout)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_buttons_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter!")
        self.scatter_btn.setStyleSheet("font: bold")
        self.fill_selected_one_btn = QtWidgets.QPushButton("Fill Selected to 'Item to Scatter'")
        self.fill_selected_two_btn = QtWidgets.QPushButton("Fill Selected to 'Scatter To'")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.fill_selected_one_btn)
        layout.addWidget(self.fill_selected_two_btn)
        layout.addWidget(self.scatter_btn)
        return layout

    def _create_selection_layouts(self):
        layout = self.create_labels()
        self.create_spinboxes()
        self.second_select = QtWidgets.QLineEdit("Type in an existing polygon name")
        self.first_select = QtWidgets.QLineEdit("Type in an existing polygon name or type of polygon (ex. polySphere)")
        self.first_select.setFixedWidth(450)
        layout.addWidget(self.second_select, 7, 0)
        layout.addWidget(self.first_select, 1, 0)
        self.add_widgets(layout)
        return layout

    def add_widgets(self, layout):
        """Simply adds widgets. Using this to clean up one function"""
        layout.addWidget(self.rot_x_sbx_min, 1, 1)
        layout.addWidget(QtWidgets.QLabel("x"), 1, 2)
        layout.addWidget(self.rot_y_sbx_min, 1, 3)
        layout.addWidget(QtWidgets.QLabel("y"), 1, 4)
        layout.addWidget(self.rot_z_sbx_min, 1, 5)
        layout.addWidget(QtWidgets.QLabel("z"), 1, 6)

        layout.addWidget(self.size_x_sbx_min, 5, 1)
        layout.addWidget(QtWidgets.QLabel("x"), 5, 2)
        layout.addWidget(self.size_y_sbx_min, 5, 3)
        layout.addWidget(QtWidgets.QLabel("y"), 5, 4)
        layout.addWidget(self.size_z_sbx_min, 5, 5)
        layout.addWidget(QtWidgets.QLabel("z"), 5, 6)

        layout.addWidget(self.rot_x_sbx_max, 8, 1)
        layout.addWidget(QtWidgets.QLabel("x"), 8, 2)
        layout.addWidget(self.rot_y_sbx_max, 8, 3)
        layout.addWidget(QtWidgets.QLabel("y"), 8, 4)
        layout.addWidget(self.rot_z_sbx_max, 8, 5)
        layout.addWidget(QtWidgets.QLabel("z"), 8, 6)

        layout.addWidget(self.size_x_sbx_max, 11, 1)
        layout.addWidget(QtWidgets.QLabel("x"), 11, 2)
        layout.addWidget(self.size_y_sbx_max, 11, 3)
        layout.addWidget(QtWidgets.QLabel("y"), 11, 4)
        layout.addWidget(self.size_z_sbx_max, 11, 5)
        layout.addWidget(QtWidgets.QLabel("z"), 11, 6)

    def create_spinboxes(self):
        self.rot_x_sbx_min = self._set_sbx_properties()
        self.rot_y_sbx_min = self._set_sbx_properties()
        self.rot_z_sbx_min = self._set_sbx_properties()
        self.rot_x_sbx_max = self._set_sbx_properties()
        self.rot_y_sbx_max = self._set_sbx_properties()
        self.rot_z_sbx_max = self._set_sbx_properties()
        self.size_x_sbx_min = self._set_dsbx_properties()
        self.size_y_sbx_min = self._set_dsbx_properties()
        self.size_z_sbx_min = self._set_dsbx_properties()
        self.size_x_sbx_max = self._set_dsbx_properties()
        self.size_y_sbx_max = self._set_dsbx_properties()
        self.size_z_sbx_max = self._set_dsbx_properties()

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
        spinbox.setValue(1.0)
        spinbox.setMaximum(20)
        spinbox.setSingleStep(.2)
        return spinbox

    def create_labels(self):
        layout = QtWidgets.QGridLayout()
        layout.setHorizontalSpacing(5)
        self.item_to_scatter_header_lbl = QtWidgets.QLabel("Item to Scatter")
        self.item_to_scatter_header_lbl.setStyleSheet("font: bold")
        self.scatter_to_lbl = QtWidgets.QLabel("Scatter To")
        self.scatter_to_lbl.setStyleSheet("font: bold")
        self.rotation_min_lbl = QtWidgets.QLabel("Minimum Rotation")
        self.rotation_min_lbl.setStyleSheet("font: bold")
        self.resize_min_lbl = QtWidgets.QLabel("Minimum Scale")
        self.resize_min_lbl.setStyleSheet("font: bold")
        self.rotation_max_lbl = QtWidgets.QLabel("Maximum Rotation")
        self.rotation_max_lbl.setStyleSheet("font: bold")
        self.resize_max_lbl = QtWidgets.QLabel("Maximum Scale")
        self.resize_max_lbl.setStyleSheet("font: bold")
        layout.addWidget(self.item_to_scatter_header_lbl, 0, 0)
        layout.addWidget(self.scatter_to_lbl, 6, 0)
        layout.addWidget(self.resize_min_lbl, 5, 7)
        layout.addWidget(self.rotation_min_lbl, 1, 7)
        layout.addWidget(self.rotation_max_lbl, 8, 7)
        layout.addWidget(self.resize_max_lbl, 11, 7)
        return layout

