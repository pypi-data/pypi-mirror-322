#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# MIT License

# Copyright (c) 2025 Anthony Pecquenard

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

## --------------------------------------------------------------------------------- ##
# STEM EDX ML

# This program provides a graphical user interface (GUI) for managing and analyzing
# STEM-EDX data using machine learning algorithms. The main window allows users to
# load data files, visualize images, and apply decomposition algorithms such as PCA
# and NMF. The application is built using PySide6 for the GUI components and includes
# various widgets for user interaction.
## --------------------------------------------------------------------------------- ##

import sys
import numpy as np

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFileDialog,
    QProgressDialog,
)
from PySide6.QtCore import Qt, Signal, QObject

# Manage STEM-EDX data and decomposition algorithms.
try:
    import stem
except:
    import STEM_EDX.stem as stem

# Classes and tools for GUI layouts and wigets.
try:
    from utils import *
except:
    from STEM_EDX.utils import *


class Window(QMainWindow):
    """
    Window Class

    This class represents the main application window for STEM EDX ML.
    It manages the user interface, signals, and interactions with the
    objects and graphs.

    Attributes
    ----------
    key : str
        A default key identifier for object selection.
    objects : ObjectsManager
        Manages the objects within the application. (Objects designed
        STEM-EDX data or results from decomposition algorithms).
    signals : dict
        A dictionary storing different signal instances for UI updates.
    graphs : list
        A list storing references to currently added graphs. (Graphs
        designed the plots from decomposition results).
    selected_object : object
        Keeps track of the currently selected object in the tree view.

    Methods
    -------
    __onLoadFileClicked():
        Opens a file dialog to load a .pts file and adds it to the
        object manager.
    __onAddGraphClicked():
        Handles the addition of graphs based on selected objects in the
        tree widget.
    __onSelectObjectChanged():
        Updates the displayed image based on the selected object and
        colourscale.
    __onPCAClicked():
        Applies the PCA algorithm on selected objects and displays
        progress.
    __onNMFClicked():
        Applies the NMF algorithm on selected objects and displays
        progress.
    __onImageTitleChanged(title):
        Updates the image title based on user input.
    """

    class SignalManager(QObject):
        """
        Signal Manager Class

        s : Signal - A signal that transmits three object parameters.
        """

        s = Signal(object, object, object)

    def __init__(self):
        """
        Constructor for the Window class.

        Initializes the main window and its components, including the
        objects manager, signals, and UI elements.
        """

        super().__init__()

        # All widgets are created with a key attribute.
        self.key = "W"

        # Initialize the objects manager storing STEM-EDX and ML data.
        self.objects = ObjectsManager(self)

        # Selected object identifies the currently selected object.
        # It is used to add graphs of decomposition results.
        self.selected_object = None

        # Initialize the list of graphs to store added graphs.
        self.graphs = []

        self.setWindowTitle("STEM EDX ML")
        self.size = (self.width(), self.height())

        # ------------------------ Signals ------------------------ #
        # Signals are used to update the UI components.
        # Signals can be connected to functions to update the UI.
        # Signals are emitted with the .emit() method.
        self.signals = {}
        for i in range(1, 4):
            self.__dict__[f"S_{i}"] = self.SignalManager()
            self.__dict__[f"signal_{i}"] = self.__dict__[f"S_{i}"].s
            self.signals[f"signal_{i}"] = self.__dict__[f"signal_{i}"]

        # Signal 1 : Update TreeWidget.
        # Signal 2 : Update SelectObjectCombobox.
        # Signal 3 : Update image in Image_Label.
        # --------------------------------------------------------- #

        # The structure of the UI is defined below.
        # The UI is structured using layouts and widgets.
        # The UI is divided into two main sections: Left and Right.
        # The Left section contains the tree view and configuration tabs.
        # The Right section contains the image display and graph tabs.
        # Each widget and layout is defined with __enter__ and __exit__ methods,
        # allowing for a clean and readable tree structure using the keyword "with".

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        with x_QHBoxLayout(self.central_widget, "Main") as MainLayout:

            with x_QVBoxLayout(MainLayout, "Left_Layout", ratio=2) as LeftLayout:
                # Ratio is used to set the size of the layout (proportions in the screen).

                with x_QTabWidget(LeftLayout, "Configuration") as TabWidget:

                    with x_QTab(TabWidget, "General") as TabGeneral:

                        self.LoadFileButton = x_QPushButton(
                            TabGeneral,
                            "Load File",
                            self.objects,
                            tooltip="Load a file",
                            label="Add an object :",
                        )
                        self.LoadFileButton.button.clicked.connect(
                            self.__onLoadFileClicked
                        )

                    with x_QTab(TabWidget, "Image") as TabImage:

                        self.SelectObjectCombobox = x_QComboBox(
                            TabImage,
                            "Select Object",
                            self.objects,
                            self.signals,
                            signal="signal_2",
                            tooltip="Select an object",
                            label="Select an object to show :",
                        )
                        self.SelectObjectCombobox.combobox.currentIndexChanged.connect(
                            self.__onSelectObjectChanged
                        )

                        self.ColorscaleCombobox = x_QComboBox(
                            TabImage,
                            "Select Colorscale",
                            self.objects,
                            self.signals,
                            tooltip="Select a colorscale",
                            label="Colorscale :",
                        )
                        self.ColorscaleCombobox.combobox.addItems(
                            ["Greyscale", "Jet", "Hot", "Viridis", "Plasma", "Inferno"]
                        )
                        self.ColorscaleCombobox.combobox.currentIndexChanged.connect(
                            self.__onSelectObjectChanged
                        )

                        self.ImageTitleLineEdit = x_QLineEdit(
                            TabImage,
                            "Image Title",
                            tooltip="Set the image title",
                            label="Title :",
                            placeholder="Enter image title here.",
                            default="Image",
                        )
                        self.ImageTitleLineEdit.line_edit.textChanged.connect(
                            self.__onImageTitleChanged
                        )

                    with x_QTab(TabWidget, "Graph") as TabGraph:

                        self.AddGraphButton = x_QPushButton(
                            TabGraph,
                            "Add Graph",
                            self.objects,
                            tooltip="Add a graph",
                            label="Add a graph :",
                        )
                        self.AddGraphButton.button.clicked.connect(
                            self.__onAddGraphClicked
                        )

                        self.SaveGraphButton = x_QPushButton(
                            TabGraph,
                            "Save Graph",
                            self.objects,
                            tooltip="Save current graph",
                            label="Save the current graph :",
                        )
                        self.SaveGraphButton.button.clicked.connect(
                            self.__onSaveGraphClicked
                        )

                    with x_QTab(TabWidget, "Machine Learning") as TabML:

                        x_QLabel(TabML, "Apply to the selected objects.")
                        x_QLabel(TabML, "<u><h3>Decomposition algorithms</h3></u>")

                        self.PCAButton = x_QPushButton(
                            TabML,
                            "Apply PCA algorithm",
                            self.objects,
                            tooltip="Apply PCA",
                            label="PCA :",
                        )
                        self.PCAButton.button.clicked.connect(self.__onPCAClicked)

                        self.NMFButton = x_QPushButton(
                            TabML,
                            "Apply NMF algorithm",
                            self.objects,
                            tooltip="Apply NMF",
                            label="NMF :",
                        )
                        self.NMFButton.button.clicked.connect(self.__onNMFClicked)

                        self.NMFComponentSpinBox = x_QSpinBox(
                            TabML,
                            "NMF Components",
                            tooltip="Set the number of components for NMF",
                            label="Components for NMF :",
                            )

                x_QSeparator(self, LeftLayout, "H")

                with x_QVBoxLayout(LeftLayout, "TreeLayout") as TreeLayout:
                    # The tree structure represents the objects and sub-objects,
                    # meaning the STEM-EDX datas and decomposition results.
                    # The tree is used to select objects to display or add as graphs.

                    with x_QTreeWidget(
                        TreeLayout,
                        "Objects",
                        self.objects,
                        signals=self.signals,
                        window=self,
                        columns=3,
                        headers=["Object", "Type", "Size", "Key"],
                    ) as TreeWidget:

                        self.TreeWidget = TreeWidget
                        # The tree is updated automatically using the signal_1.
                        # See the __onLoadFileClicked method for more details.

            x_QSeparator(self, MainLayout, "V")

            with x_QVBoxLayout(MainLayout, "Right_Layout", ratio=3) as RightLayout:

                with x_QVBoxLayout(RightLayout, "Image_Layout", ratio=1) as ImageLayout:

                    self.Image_Coordinates_Label = x_QLabel(
                        ImageLayout, alignment=Qt.AlignCenter
                    )
                    self.Image_Coordinates_Label.label.setText(
                        self.ImageTitleLineEdit.line_edit.text()
                    )

                    self.Image_Label = x_QImage_Label(
                        ImageLayout,
                        signals=self.signals,
                        signal="signal_3",
                        coord_label=self.Image_Coordinates_Label,
                        title_input=self.ImageTitleLineEdit,
                    )

                x_QSeparator(self, RightLayout, "H")

                with x_QVBoxLayout(RightLayout, "Graph_Layout", ratio=1) as GraphLayout:

                    with x_QTabWidget(
                        GraphLayout, "Graph_Tab", movable=True
                    ) as GraphTab:

                        self.GraphTab = GraphTab
                        # Tabs are added automatically using the AddGraphButton.
                        # See the __onAddGraphClicked method for more details.

    def __onLoadFileClicked(self):
        """
        Slot for handling the event when the 'Load File' button is clicked.
        This function opens a file dialog to select a .pts file, generates a unique
        object name, adds the object to the collection, and emits a signal.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Only .pts files are currently accepted.
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "(*.pts)")
        
        # Name for the object is generated based on the object count.
        correct_name = False
        while not correct_name:
            if "Object n°" + str(self.objects.id) in self.objects.objects:
                self.objects.id += 1
            else:
                correct_name = True

        # Using the ObjectsManager, a new STEM_EDX object is created and added.
        self.objects.add_object(
            stem.STEM_EDX_DATA(file, name=f"Object n°{self.objects.id}")
        )

        # The signal_1 is emitted to update the TreeWidget.
        # No parameters are needed as the TreeWidget is updated automatically.
        self.signal_1.emit(None, None, None)

    def __onAddGraphClicked(self):
        """
        Handles the event when the 'Add Graph' button is clicked.
        This function checks if a valid item is selected in the tree widget.
        If a sub-object is selected, it creates a new graph tab for the 
        selected sub-object and adds it to the graph tab widget. If no 
        sub-object is selected, it shows an error message.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Check if an item is selected in the tree widget.
        if self.TreeWidget.tree.currentItem() is not None:
            # Check if the item is a sub-object (decomposition result, plotable).
            if self.TreeWidget.tree.currentItem().parent() is not None:
                child_object_key = self.TreeWidget.tree.currentItem().text(3)
                parent_object_text = self.TreeWidget.tree.currentItem().parent().text(0)

                parent_object = self.objects[parent_object_text]
                self.selected_object = self.objects[parent_object_text].sub_items[child_object_key]

                # Check if the graph is already added.
                if f"{parent_object_text} - {child_object_key}" not in self.graphs:

                    # Add a new graph tab for the selected sub-object.
                    graph_tab = x_GraphTabWidget(
                        key=f"{parent_object_text} - {child_object_key}",
                        parent=self,
                        parent_object=parent_object,
                        child_object=self.selected_object,
                    )

                    self.GraphTab.addTab(
                        graph_tab, f"{parent_object_text} - {self.selected_object.name}"
                    )

                    # Store the added graph in the list (used to avoid duplicates).
                    self.graphs.append(f"{parent_object_text} - {child_object_key}")

            else:
                show_message(
                    "Error", "Please select a sub-object to add as a graph.", "error"
                )
        else:
            show_message(
                "Error", "Please select a plotable object to add as a graph.", "error"
            )
    
    def __onSaveGraphClicked(self):

        if self.selected_object is not None:
            file, _ = QFileDialog.getSaveFileName(self, "Save Graph", "", "(*.png)")
            self.selected_object.save_plot(file)

    def __onSelectObjectChanged(self, *args):
        """
        Handles the event when the selected object in the combobox changes.
        
        Parameters
        ----------
        *args : tuple
            Additional arguments passed to the event handler.
        
        Emits
        -----
        signal_3 : PyQt5.QtCore.pyqtSignal
            Emits a signal with the following parameters:
            - np.array or str: The sum of the object's data along axis 2 if an 
              object is selected, otherwise an empty string.
            - str: The current text of the ColorscaleCombobox.
            - QLabel: The Image_Coordinates_Label.
        """

        current = self.SelectObjectCombobox.combobox.currentText()

        if current != "":
            # Emit signal_3 to update the image in the Image_Label.
            self.signal_3.emit(
                np.array(self.objects[current].data.sum(axis=2)),
                self.ColorscaleCombobox.combobox.currentText(),
                self.Image_Coordinates_Label,
            )
        else:
            # If no object is selected, emit signal_3 with an empty string.
            self.signal_3.emit(
                "",
                self.ColorscaleCombobox.combobox.currentText(),
                self.Image_Coordinates_Label,
            )

    def __onPCAClicked(self):
        """
        Handles the PCA button click event.
        This method is triggered when the PCA button is clicked. It collects the 
        selected objects from the TreeWidget, validates the selection, and starts 
        a background thread to apply PCA on the selected objects. It also manages 
        the progress dialog and handles any errors that occur during the process.

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        def finished():
            """
            Handles the completion of the PCA thread.

            This function is called when the PCA thread is finished. It checks if
            any errors occurred during the process and displays an error message if
            necessary.
            """

            if self.pca_thread.errors:
                show_message(
                    "Error",
                    f"An error occured while applying PCA on the following objects : {self.pca_thread.errors}",
                    "error",
                )

        ## -- Get the selected objects from the TreeWidget. -- ##
        root = self.TreeWidget.tree.invisibleRootItem()
        selected_objects = []

        for row in range(root.childCount()):
            item = root.child(row)
            if item and item.checkState(0) == Qt.CheckState.Checked:
                selected_objects.append(item.text(0))
        ## --------------------------------------------------- ##

        if not selected_objects:
            show_message("Error", "No object selected.", "error")
            return

        # Create a progress dialog to show the progress of the PCA process.
        self.progress_dialog = QProgressDialog(
            "Applying PCA on selected objects...", "Cancel", 0, 100, self
        )
        self.progress_dialog.setGeometry(400, 400, 400, 100)
        self.progress_dialog.setWindowTitle("Processing")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)

        # Start a background thread to apply PCA on the selected objects.
        # See the Worker class for more details on the thread.
        self.pca_thread = Worker(self.objects, selected_objects, "PCA")
        self.pca_thread.progress.connect(self.progress_dialog.setValue)
        self.progress_dialog.canceled.connect(self.pca_thread.terminate)

        # Connect the signals to update the UI and handle the completion of the thread.
        self.pca_thread.finished.connect(self.progress_dialog.close)
        self.pca_thread.finished.connect(lambda: self.signal_1.emit(None, None, None))
        self.pca_thread.finished.connect(finished)

        self.pca_thread.start()

    def __onNMFClicked(self):
        """
        Handles the event when the NMF button is clicked.
        This function retrieves the selected objects from the TreeWidget, checks if 
        any objects are selected, and if so, starts a worker thread to apply NMF 
        (Non-negative Matrix Factorisation) on the selected objects. It also 
        displays a progress dialog and handles errors if they occur.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """


        def finished():
            """
            Handles the completion of the NMF thread.

            This function is called when the NMF thread is finished. It checks if
            any errors occurred during the process and displays an error message if
            necessary.
            """

            if self.nmf_thread.errors:
                show_message(
                    "Error",
                    f"An error occured while applying NMF on the following objects : {self.nmf_thread.errors}",
                    "error",
                )

        ## -- Get the selected objects from the TreeWidget. -- ##
        root = self.TreeWidget.tree.invisibleRootItem()
        selected_objects = []

        for row in range(root.childCount()):
            item = root.child(row)
            if item and item.checkState(0) == Qt.CheckState.Checked:
                selected_objects.append(item.text(0))
        ## --------------------------------------------------- ##

        if not selected_objects:
            show_message("Error", "No object selected.", "error")
            return

        # Create a progress dialog to show the progress of the NMF process.
        self.progress_dialog = QProgressDialog(
            "Applying NMF on selected objects...", "Cancel", 0, 100, self
        )
        self.progress_dialog.setGeometry(400, 400, 400, 100)
        self.progress_dialog.setWindowTitle("Processing")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)

        # Start a background thread to apply NMF on the selected objects.
        # See the Worker class for more details on the thread.
        self.nmf_thread = Worker(self.objects, selected_objects, "NMF", self.NMFComponentSpinBox.spinbox.value())
        self.nmf_thread.progress.connect(self.progress_dialog.setValue)
        self.progress_dialog.canceled.connect(self.nmf_thread.terminate)

        # Connect the signals to update the UI and handle the completion of the thread.
        self.nmf_thread.finished.connect(self.progress_dialog.close)
        self.nmf_thread.finished.connect(lambda: self.signal_1.emit(None, None, None))
        self.nmf_thread.finished.connect(finished)

        self.nmf_thread.start()

    def __onImageTitleChanged(self, title):
        """
        Updates the text of the Image_Coordinates_Label with the given title.
        Parameters
        ----------
        title : str
            The new title to set for the Image_Coordinates_Label.
            Automatically updated when the user changes the title in the QLineEdit.
        """

        self.Image_Coordinates_Label.label.setText(title)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Get sccreen size to define app window geometry.
    (width, height) = app.screens()[0].size().toTuple()

    window = Window()
    window.setFixedSize(width * 0.9, height * 0.9)
    window.show()

    sys.exit(app.exec())
