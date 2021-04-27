import logging
import random

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
    global_instance = []

    def __init__(self):
        super(ScatterToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(400)
        self.setMaximumWidth(1200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()

    def create_connections(self):
        self.scatter_btn.clicked.connect(self.scatter_function)
        self.fill_selected_one_btn.clicked.connect(self.fill_selected_one_function)
        self.fill_selected_two_btn.clicked.connect(self.fill_selected_two_function)

    @QtCore.Slot()
    def scatter_function(self):
        percentage = self.percent_spinbox.value() * .01
        cmds.select(clear=True)
        names = list(self.second_select.text().split(", "))
        names = names[:-1]
        random_nums = []
        selected_vtx = []

        i = 0
        for obj in names:
            cmds.select(names[i], add=True)
            i += 1

        if ".vtx" not in names[0]:
            for x in range(500):
                """Used 500 as it should be large enough for any polygon that is in the scene"""
                cmds.select(names[0] + ".vtx[" + str(x) + "]", add=True)

        selected_vtx = cmds.filterExpand(expand=True, sm=31)
        value = 0
        nums_track = 0

        total = len(selected_vtx)
        vertex_make = percentage * total
        vertex_make = int(vertex_make)

        for x in range(0, vertex_make):
            random_nums = random.sample(range(total), k=vertex_make)
            nums_track += 1

        for vertex in selected_vtx:
            new_obj = cmds.instance(ScatterToolUI.global_instance)
            location = cmds.pointPosition(selected_vtx[random_nums[value]], w=True)
            self.set_transforms(new_obj)
            cmds.move(location[0], location[1], location[2], new_obj[0], a=True, ws=True)
            value += 1

    @QtCore.Slot()
    def fill_selected_one_function(self):
        selected = cmds.ls(sl=True, o=True)
        ScatterToolUI.global_instance = selected[0]
        self.first_select.setText(selected[0])

    @QtCore.Slot()
    def fill_selected_two_function(self):
        selected = cmds.ls(sl=True, fl=True)
        selected_text = ""
        i = 0
        for obj in selected:
            selected_text += selected[i] + ", "
            i += 1
        self.second_select.setText(selected_text)

    def set_transforms(self, new_obj):
        """Sets the transform of the object"""
        x_rot = random.uniform(self.rot_x_sbx_min.value(), self.rot_x_sbx_max.value())
        y_rot = random.uniform(self.rot_y_sbx_min.value(), self.rot_y_sbx_max.value())
        z_rot = random.uniform(self.rot_z_sbx_min.value(), self.rot_z_sbx_max.value())
        x_scl = random.uniform(self.size_x_sbx_min.value(), self.size_x_sbx_max.value())
        y_scl = random.uniform(self.size_y_sbx_min.value(), self.size_y_sbx_max.value())
        z_scl = random.uniform(self.size_z_sbx_min.value(), self.size_z_sbx_max.value())
        cmds.rotate(x_rot, y_rot, z_rot, new_obj)
        cmds.scale(x_scl, y_scl, z_scl, new_obj)

    def create_ui(self):
        """Creates the UI layout"""
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
        """Creates the buttons in the UI"""
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
        """Creates the rest of the layout. Line edits and spin boxes"""
        layout = self.create_labels()
        self.create_spinboxes()
        self.second_select = QtWidgets.QLineEdit("Type in an existing polygon name!")
        self.first_select = QtWidgets.QLineEdit("Type in an existing polygon name!")
        self.first_select.setFixedWidth(450)
        layout.addWidget(self.second_select, 7, 0)
        layout.addWidget(self.first_select, 1, 0)
        self.add_widgets(layout)
        self.create_percent(layout)
        return layout

    def add_widgets(self, layout):
        """Simply adds spinbox widgets. Using this to clean up one function"""
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

    def create_percent(self, layout):
        """Creates percentage spinbox and assigns properties, uses double for more complex percentages"""
        self.percent_spinbox = QtWidgets.QDoubleSpinBox()
        self.percent_spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.percent_spinbox.setFixedWidth(60)
        self.percent_spinbox.setValue(100.0)
        self.percent_spinbox.setMaximum(100.0)
        self.percent_spinbox.setMinimum(0)
        self.percent_spinbox.setSingleStep(1.0)
        percentage_label = QtWidgets.QLabel("Percentage of Vertices")
        percentage_label.setStyleSheet("font: bold")
        layout.addWidget(percentage_label, 12, 7)
        layout.addWidget(self.percent_spinbox, 12, 5)
        layout.addWidget(QtWidgets.QLabel("%"), 12, 6)

    def create_spinboxes(self):
        """Creates the spinboxes"""
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
        """Sets properties of normal (integer) spinboxes"""
        spinbox = QtWidgets.QSpinBox()
        spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        spinbox.setFixedWidth(50)
        spinbox.setValue(0)
        spinbox.setMaximum(360)
        spinbox.setSingleStep(15)
        return spinbox

    def _set_dsbx_properties(self):
        """Sets properties of the double spinboxes"""
        spinbox = QtWidgets.QDoubleSpinBox()
        spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        spinbox.setFixedWidth(50)
        spinbox.setValue(1.0)
        spinbox.setMaximum(20)
        spinbox.setSingleStep(.2)
        return spinbox

    def create_labels(self):
        """Creates the labels"""
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
