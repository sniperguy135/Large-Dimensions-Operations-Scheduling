# Import libraries
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", '-r', 'requirements.txt'])
from PyQt5 import QtCore, QtGui, QtWidgets
import data_output
import heuristics

# UI Page 3: Outputs
class Ui_Page3Window(object):
    def setupUi(self, Page3Window):
        """ Configuration of Features """
        # Main Window
        Page3Window.setObjectName("Page3Window")
        Page3Window.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(Page3Window)
        self.centralwidget.setObjectName("centralwidget")

        # Page Header
        self.Page3Header = QtWidgets.QLabel(self.centralwidget)
        self.Page3Header.setGeometry(QtCore.QRect(460, 20, 1000, 50))
        self.Page3Header.setText("")
        self.Page3Header.setPixmap(QtGui.QPixmap("page 3 head.jpg"))
        self.Page3Header.setScaledContents(True)
        self.Page3Header.setObjectName("Page3Header")

        # Gantt Chart
        self.TitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.TitleLabel.setGeometry(QtCore.QRect(460, 80, 300, 35))
        self.TitleLabel.setObjectName("TitleLabel")

        self.GanttChartLabel = QtWidgets.QLabel(self.centralwidget)
        self.GanttChartLabel.setGeometry(QtCore.QRect(460, 130, 500, 500))
        self.GanttChartLabel.setText("")
        self.GanttChartLabel.setPixmap(QtGui.QPixmap("gantt machine.png"))
        self.GanttChartLabel.setScaledContents(True)
        self.GanttChartLabel.setObjectName("GanttChartLabel")

        # # Filter 1: Machines
        # self.Section3Text1 = QtWidgets.QTextBrowser(self.centralwidget)
        # self.Section3Text1.setGeometry(QtCore.QRect(960, 130, 500, 200))
        # self.Section3Text1.setObjectName("Section3Text1")

        # self.MachineLabel = QtWidgets.QLabel(self.centralwidget)
        # self.MachineLabel.setGeometry(QtCore.QRect(960, 335, 100, 35))
        # self.MachineLabel.setObjectName("MachineLabel")

        # self.MachineLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # self.MachineLineEdit.setGeometry(QtCore.QRect(1070, 335, 230, 35))
        # self.MachineLineEdit.setObjectName("MachineLineEdit")

        # self.MachineButton = QtWidgets.QPushButton(self.centralwidget)
        # self.MachineButton.setGeometry(QtCore.QRect(1310, 335, 150, 35))
        # self.MachineButton.setObjectName("MachineButton")
        # Connect Action Function
        #self.MachineButton.clicked.connect(self.MachineButtonClicked)

        # self.MachineErrorLabel = QtWidgets.QLabel(self.centralwidget)
        # self.MachineErrorLabel.setGeometry(QtCore.QRect(960, 375, 100, 25))
        # self.MachineErrorLabel.setText("")
        # self.MachineErrorLabel.setObjectName("MachineErrorLabel")

        # Filter 2: Toggle Y-Axis
        self.Section3Text2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.Section3Text2.setGeometry(QtCore.QRect(960, 130, 500, 130))
        self.Section3Text2.setObjectName("Section3Text2")

        self.MachinesButton = QtWidgets.QPushButton(self.centralwidget)
        self.MachinesButton.setGeometry(QtCore.QRect(1310, 265, 150, 35))
        self.MachinesButton.setObjectName("MachinesButton")
        # Connect Action Function (Change Image)
        self.MachinesButton.clicked.connect(self.MachinesButtonClicked)

        self.JobsButton = QtWidgets.QPushButton(self.centralwidget)
        self.JobsButton.setGeometry(QtCore.QRect(960, 265, 150, 35))
        self.JobsButton.setObjectName("JobsButton")
        # Connect Action Function (Change Image)
        self.JobsButton.clicked.connect(self.JobsButtonClicked)

        # Return to Page 1
        self.NextPageButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.NextPageButton3.setGeometry(QtCore.QRect(1210, 595, 250, 40))
        self.NextPageButton3.setObjectName("NextPageButton3")
        # Connect Action Function (Close Page 3)
        self.NextPageButton3.clicked.connect(Page3Window.close)

        # (unused) Menu and Status Bar
        Page3Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Page3Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 22))
        self.menubar.setObjectName("menubar")
        Page3Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Page3Window)
        self.statusbar.setObjectName("statusbar")
        Page3Window.setStatusBar(self.statusbar)

        # (default) Configuration
        self.retranslateUi(Page3Window)
        QtCore.QMetaObject.connectSlotsByName(Page3Window)


    """ Action Functions """
    def MachinesButtonClicked(self):
        self.GanttChartLabel.setPixmap(QtGui.QPixmap('gantt machine.png'))
        self.GanttChartLabel.setScaledContents(True)

    def JobsButtonClicked(self):
        self.GanttChartLabel.setPixmap(QtGui.QPixmap('gantt jobs.png'))
        self.GanttChartLabel.setScaledContents(True)

    # def MachineButtonClicked(self):
    #     # Clear Error Labels
    #     self.MachineErrorLabel.setText("")

    #     # Take Line Edit Input
    #     MachineDesired = str(self.MachineLineEdit.text())

    #     # Ensure Valid Formatting
    #     try:
    #         assert MachineDesired != "", "Invalid input, the field is blank."
    #         # Create new Output
    #         data_output.data_output_main(scheduled_list_of_dict, MachineDesired)

    #     except Exception as expErr:
    #         self.MachineErrorLabel.setText(str(expErr)) 
            


    

    """ Paths and Text """
    def retranslateUi(self, Page3Window):
        _translate = QtCore.QCoreApplication.translate
        Page3Window.setWindowTitle(_translate("Page3Window", "MainWindow"))
        self.TitleLabel.setText(_translate("Page3Window", "Obtained Operation Schedule:"))
#         self.MachineButton.setText(_translate("Page3Window", "Submit"))
#         self.Section3Text1.setHtml(_translate("Page3Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
# "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Filters</span></p>\n"
# "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">1. Machines</span></p>\n"
# "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Indicate the machines to be displayed on the gannt chart. An example of a valid format if machine 1, 4 and 6 are desired is &quot;1,4,6&quot; excluding the inverted commas. Press the \'Submit\' button.</span></p>\n"
# "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
#         self.MachineLabel.setText(_translate("Page3Window", "Machines:"))
        self.Section3Text2.setHtml(_translate("Page3Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">1. Toggle Y-Axis</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Press the button below to toggle between the gantt charts with machines or jobs on its y-axis.</span></p></body></html>"))
        self.MachinesButton.setText(_translate("Page3Window", "Machines"))
        self.JobsButton.setText(_translate("Page3Window", "Jobs"))
        self.NextPageButton3.setText(_translate("Page3Window", "Restart"))


""" Main System """
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Page3Window = QtWidgets.QMainWindow()
    ui = Ui_Page3Window()
    ui.setupUi(Page3Window)
    Page3Window.show()
    sys.exit(app.exec_())
