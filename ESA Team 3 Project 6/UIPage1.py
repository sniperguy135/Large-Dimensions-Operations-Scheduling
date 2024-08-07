# Import libraries
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", '-r', 'requirements.txt'])
from PyQt5 import QtCore, QtGui, QtWidgets
from UIPage2 import Ui_Page2Window
import data_input
import heuristics
import data_output

# UI Page 1: Inputs
class Ui_Page1Window(object):
    """ Configuration of Features """
    def setupUi(self, Page1Window):
        Page1Window.setObjectName("Page1Window")
        Page1Window.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(Page1Window)
        self.centralwidget.setObjectName("centralwidget")

        # Page Header
        self.Page1Header = QtWidgets.QLabel(self.centralwidget)
        self.Page1Header.setGeometry(QtCore.QRect(460, 20, 1000, 50))
        self.Page1Header.setText("")
        self.Page1Header.setPixmap(QtGui.QPixmap("page 1 head.jpg"))
        self.Page1Header.setScaledContents(True)
        self.Page1Header.setObjectName("Page1Header")

        # Text Boxes
        self.Section1Text1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.Section1Text1.setGeometry(QtCore.QRect(460, 70, 1000, 300))
        self.Section1Text1.setObjectName("Section1Text1")

        self.Section1Text2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.Section1Text2.setGeometry(QtCore.QRect(460, 520, 1000, 150))
        self.Section1Text2.setObjectName("Section1Text2")

        self.Section1Text3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.Section1Text3.setGeometry(QtCore.QRect(460, 760, 1000, 150))
        self.Section1Text3.setObjectName("Section1Text3")

        # Input 1: MRP
        # MRP Labels
        self.MRPLabel = QtWidgets.QLabel(self.centralwidget)
        self.MRPLabel.setGeometry(QtCore.QRect(460, 380, 100, 35))
        self.MRPLabel.setObjectName("MRPLabel")

        self.MRPStartLabel = QtWidgets.QLabel(self.centralwidget)
        self.MRPStartLabel.setGeometry(QtCore.QRect(460, 450, 100, 35))
        self.MRPStartLabel.setObjectName("MRPStartLabel")

        self.MRPEndLabel = QtWidgets.QLabel(self.centralwidget)
        self.MRPEndLabel.setGeometry(QtCore.QRect(885, 450, 100, 35))
        self.MRPEndLabel.setObjectName("MRPEndLabel")

        # MRP Directory Input
        self.MRPLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.MRPLineEdit.setGeometry(QtCore.QRect(580, 380, 710, 35))
        self.MRPLineEdit.setText("")
        self.MRPLineEdit.setObjectName("MRPLineEdit")

        # MRP Directory Error Label
        self.MRPErrorLabel = QtWidgets.QLabel(self.centralwidget)
        self.MRPErrorLabel.setGeometry(QtCore.QRect(460, 415, 830, 25))
        self.MRPErrorLabel.setText("")
        self.MRPErrorLabel.setObjectName("MRPErrorLabel")

        # MRP Start and End Period Input
        self.MRPStartLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.MRPStartLineEdit.setGeometry(QtCore.QRect(580, 450, 285, 35))
        self.MRPStartLineEdit.setObjectName("MRPStartLineEdit")

        self.MRPEndLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.MRPEndLineEdit.setGeometry(QtCore.QRect(1005, 450, 285, 35))
        self.MRPEndLineEdit.setObjectName("MRPEndLineEdit")

        # MRP Start and End Error Label
        self.MRPStartErrorLabel = QtWidgets.QLabel(self.centralwidget)
        self.MRPStartErrorLabel.setGeometry(QtCore.QRect(460, 485, 830, 25))
        self.MRPStartErrorLabel.setText("")
        self.MRPStartErrorLabel.setObjectName("MRPStartErrorLabel")

        # MRP Submit Button
        self.MRPButton = QtWidgets.QPushButton(self.centralwidget)
        self.MRPButton.setGeometry(QtCore.QRect(1310, 450, 150, 35))
        self.MRPButton.setObjectName("MRPButton")
        # Connect Action Function
        self.MRPButton.clicked.connect(self.MRPButtonClicked)        

        # Input 2: Routing
        # Routing Labels
        self.RoutingLabel = QtWidgets.QLabel(self.centralwidget)
        self.RoutingLabel.setGeometry(QtCore.QRect(460, 690, 100, 35))
        self.RoutingLabel.setObjectName("RoutingLabel")

        # Routing Directory Input
        self.RoutingLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.RoutingLineEdit.setGeometry(QtCore.QRect(580, 690, 710, 35))
        self.RoutingLineEdit.setText("")
        self.RoutingLineEdit.setObjectName("RoutingLineEdit")

        # Routing Error Label
        self.RoutingErrorLabel = QtWidgets.QLabel(self.centralwidget)
        self.RoutingErrorLabel.setGeometry(QtCore.QRect(460, 725, 830, 25))
        self.RoutingErrorLabel.setText("")
        self.RoutingErrorLabel.setObjectName("RoutingErrorLabel")

        # Input 3: Capacity
        # Capacity Labels
        self.CapacityLabel = QtWidgets.QLabel(self.centralwidget)
        self.CapacityLabel.setGeometry(QtCore.QRect(460, 920, 100, 35))
        self.CapacityLabel.setObjectName("CapacityLabel")

        # Capacity Directory Input
        self.CapacityLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.CapacityLineEdit.setGeometry(QtCore.QRect(580, 920, 710, 35))
        self.CapacityLineEdit.setText("")
        self.CapacityLineEdit.setObjectName("CapacityLineEdit")

        # Capacity Error Label
        self.CapacityErrorLabel = QtWidgets.QLabel(self.centralwidget)
        self.CapacityErrorLabel.setGeometry(QtCore.QRect(460, 955, 830, 25))
        self.CapacityErrorLabel.setText("")
        self.CapacityErrorLabel.setObjectName("CapacityErrorLabel")

        # Capacity Submit Button
        self.CapacityButton = QtWidgets.QPushButton(self.centralwidget)
        self.CapacityButton.setGeometry(QtCore.QRect(1310, 920, 150, 35))
        self.CapacityButton.setObjectName("CapacityButton")
        # Connect Action Function
        self.CapacityButton.clicked.connect(self.CapacityButtonClicked)

        # Next Page Button
        self.NextPageButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.NextPageButton1.setGeometry(QtCore.QRect(1310, 980, 150, 35))
        self.NextPageButton1.setObjectName("NextPageButton1")
        # Connect Action Function
        self.NextPageButton1.clicked.connect(self.NextPageButton1Clicked)

        # (unused) Menu and Status Bar
        Page1Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Page1Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 22))
        self.menubar.setObjectName("menubar")
        Page1Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Page1Window)
        self.statusbar.setObjectName("statusbar")
        Page1Window.setStatusBar(self.statusbar)

        # (default) Configuration
        self.retranslateUi(Page1Window)
        QtCore.QMetaObject.connectSlotsByName(Page1Window)


    """Action Functions"""
    # MRP Submit Button Action Function
    def MRPButtonClicked(self):
        # Clear Error Labels
        self.MRPErrorLabel.setText("")
        self.MRPStartErrorLabel.setText("")
        if self.RoutingErrorLabel.text()=="Routing Input has been validated and stored successfully.":
            pass
        else:
            self.RoutingErrorLabel.setText("")
        if self.CapacityErrorLabel.text()=="Capacity Input has been validated and stored successfully.":
            pass
        else:
            self.CapacityErrorLabel.setText("")

        # Make Inputs Global Variables
        global MRPDirectory
        global MRPStartPeriod
        global MRPEndPeriod
        # Take Line Edit Input
        MRPDirectory = str(self.MRPLineEdit.text())
        MRPStartPeriod = str(self.MRPStartLineEdit.text())
        MRPEndPeriod = str(self.MRPEndLineEdit.text())

        # Ensure Valid Formating
        try:
            assert MRPDirectory != "", "Invalid input. The MRP directory field is blank."
            assert MRPStartPeriod != "", "Invalid input. The Start Period field is blank."
            assert MRPEndPeriod != "", "Invalid input. The End Period field is blank."
            # Change File to .xlsx and Return Directory
            MRPDirectory = data_input.MRP_input_validate(MRPDirectory, MRPStartPeriod, MRPEndPeriod)
            # Change Label to display Successfully Stored Inputs
            self.MRPErrorLabel.setText("All MRP Inputs are validated and stored successfully.")

        # Defining all Possible Errors (and adjusting label accordingly)
        except FileNotFoundError as errFile:
            what_was_error = str(errFile)
            self.MRPErrorLabel.setText(what_was_error)

        except TypeError as errType:
            # Error: Unsupported File Type
            what_was_error = str(errType)
            if "Type to convert - check if the MRP file" in what_was_error:
                self.MRPErrorLabel.setText(what_was_error)
            elif "Type - check if the MRP file" in what_was_error:
                self.MRPErrorLabel.setText(what_was_error)

        except ValueError as errValue:
            what_was_error = str(errValue)
            if "Invalid MRP file contents" in what_was_error:
                self.MRPErrorLabel.setText(what_was_error)
            elif "Start column is before End column" in what_was_error:
                self.MRPStartErrorLabel.setText(what_was_error)
            elif "Start or End columns invalid" in what_was_error:
                self.MRPStartErrorLabel.setText(what_was_error)
            elif "Start/end column cannot be A, Column A is reserved for part letters. Refer to template MRP." in what_was_error:
                self.MRPStartErrorLabel.setText(what_was_error)
            elif "Columns selected do not have specified period. Refer to template MRP." in what_was_error:
                self.MRPStartErrorLabel.setText(what_was_error)
            elif "No jobs scheduled in specified columns" in what_was_error:
                self.MRPStartErrorLabel.setText(what_was_error)
            elif "More than 10 columns chosen" in what_was_error:
                self.MRPStartErrorLabel.setText(what_was_error)

        except AssertionError as errAss:
            what_was_error = str(errAss)
            # Error: Blank Inputs
            if "End Period field" in what_was_error:
                self.MRPStartErrorLabel.setText(what_was_error)
            elif "Start Period field" in what_was_error:
                self.MRPStartErrorLabel.setText(what_was_error)
            elif "MRP directory field" in what_was_error:
                self.MRPErrorLabel.setText(what_was_error)

        except Exception as errGeneric:
            what_was_error = str(errGeneric)
            # Generic Errors
            self.MRPErrorLabel.setText(what_was_error)
        
    
    # Capacity Submit Button Action Function
    def CapacityButtonClicked(self):
        # Clear Error Labels
        if self.MRPErrorLabel.text()=="All MRP Inputs are validated and stored successfully.":
            pass
        else:
            self.MRPErrorLabel.setText("")
            self.MRPStartErrorLabel.setText("")
        self.RoutingErrorLabel.setText("")
        self.CapacityErrorLabel.setText("")

        # Take Line Edit Input
        RoutingDirectory = str(self.RoutingLineEdit.text())
        CapacityDirectory = str(self.CapacityLineEdit.text())

        # Ensure Valid Formating
        try:
            assert CapacityDirectory != "", "Invalid input. The Capacity directory field is blank."
            assert RoutingDirectory != "", "Invalid input. The Routing directory field is blank."
            # Make jobs_dict and capacity_dict global variables
            global job_dictionary
            global capacity_dictionary
            # Run Main Function (checks validity, creates job and capacity dictionary if valid)
            job_dictionary, capacity_dictionary = data_input.data_input_main(RoutingDirectory, MRPDirectory, CapacityDirectory, MRPStartPeriod, MRPEndPeriod)
            # Change Label to display Successfully Stored Inputs
            self.RoutingErrorLabel.setText("Routing Input has been validated and stored successfully.")
            self.CapacityErrorLabel.setText("Capacity Input has been validated and stored successfully.")
        
        # Defining all Possible Errors (and adjusting label accordingly)
        except FileNotFoundError as errFile:
            what_was_error = str(errFile)
            self.CapacityErrorLabel.setText(what_was_error)

        except TypeError as errType:
            what_was_error = str(errType)
            # Error: Unsupported File Type
            if "Type to convert - check if the MRP file" in what_was_error:
                self.MRPErrorLabel.setText(what_was_error)
            elif "Type - check if the MRP file" in what_was_error:
                self.MRPErrorLabel.setText(what_was_error)
            elif "Type to convert - check if the routing file" in what_was_error:
                self.RoutingErrorLabel.setText(what_was_error)
            elif "Type - check if the routing file" in what_was_error:
                self.RoutingErrorLabel.setText(what_was_error)
            elif "Type to convert - check if the capacity file" in what_was_error:
                self.CapacityErrorLabel.setText(what_was_error)
            elif "Type - check if the capacity file" in what_was_error:
                self.CapacityErrorLabel.setText(what_was_error)

        except ValueError as errValue:
            what_was_error = str(errValue)
            if "Invalid capacity file contents" in what_was_error:
                self.CapacityErrorLabel.setText(what_was_error)
            elif "Invalid routing file contents" in what_was_error:
                self.RoutingErrorLabel.setText(what_was_error)
            elif "MRP file does not match routing contents" in what_was_error:
                self.RoutingErrorLabel.setText(what_was_error)
            elif "Mising machines in capacity file" in what_was_error:
                self.CapacityErrorLabel.setText(what_was_error)
            elif "ValueError for BOM attributes beyond spec" in what_was_error:
                self.RoutingErrorLabel.setText(what_was_error)

        except AssertionError as errAss:
            what_was_error = str(errAss)
            # Error: Blank Input
            if "Capacity directory field" in what_was_error:
                self.CapacityErrorLabel.setText(what_was_error)
            elif "Routing directory field" in what_was_error:
                self.RoutingErrorLabel.setText(what_was_error)

        except Exception as errGeneric:
            what_was_error = str(errGeneric)
            # Generic Errors
            self.CapacityErrorLabel.setText(what_was_error)
    
    # Next Page Button Action Function
    def NextPageButton1Clicked(self):
        # Ensure All Inputs Valid
        if self.MRPErrorLabel.text()=="All MRP Inputs are validated and stored successfully." and self.RoutingErrorLabel.text()=="Routing Input has been validated and stored successfully." and self.CapacityErrorLabel.text()=="Capacity Input has been validated and stored successfully.":
            # Open page 2 Window
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_Page2Window()
            self.ui.setupUi(self.window)
            self.window.show()
            # Run heuristics
            scheduled_list_of_dict = heuristics.heuristics_main(job_dictionary, capacity_dictionary)
            # Generate Outputs
            data_output.data_output_main(scheduled_list_of_dict)
            # Update Progress Bar
            self.ui.progressBar.setProperty("value", 100)
            





    """ Paths and Text """
    def retranslateUi(self, Page1Window):
        _translate = QtCore.QCoreApplication.translate
        Page1Window.setWindowTitle(_translate("Page1Window", "MainWindow"))
        self.CapacityLabel.setText(_translate("Page1Window", "Directory:"))
        self.MRPLabel.setText(_translate("Page1Window", "Directory:"))
        self.Section1Text1.setHtml(_translate("Page1Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">1. Input Data</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">To produce an operation schedule, the data inputs required are the Material Requirements Planning (MRP), the Routing and the Capacity. Copy this link (https://drive.google.com/drive/folders/1mmP-mXgQkxaUPPcsBC9w3MBs-5Fbt1Px?usp=drive_link) to access the \'TemplateFiles\' folder. Referencing the files in the \'TemplateFiles\' folder, adjust your data input files to match the required formatting. Files can be excepted as csv, xlsx, xls or tsv. Please close all inputs files before continuing.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">1.1 Materials Requirement Planning (MRP)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">State the directory linked to your MRP file. An example of a valid directory format for an xlsx file named MRP is &quot;C:\\Users\\Mary Tan\\Documents\\DataInputs\\MRP.xlsx&quot;, excluding the inverted commas.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">A maximum of 10 periods can be chosen for the MRP folder. Indicate your starting and ending period below by entering its column letters following your MRP excel sheet (e.g. Start Period: A and End Period: J). Press the \'submit\' button.</span></p></body></html>"))
        self.Section1Text2.setHtml(_translate("Page1Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">1.2 Routing</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">State the directory linked to your Routing file. An example of a valid directory format for an xlsx file named Routing is &quot;C:\\Users\\Mary Tan\\Documents\\DataInputs\\Routing.xlsx&quot;, excluding the inverted commas. This input will be submitted with the Capacity file under input 1.3.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The Routing file can have a maximum of 14 layers and 7 children per node.</span></p></body></html>"))
        self.RoutingLabel.setText(_translate("Page1Window", "Directory:"))
        self.MRPButton.setText(_translate("Page1Window", "Submit"))
        self.MRPStartLabel.setText(_translate("Page1Window", "Start Period:"))
        self.Section1Text3.setHtml(_translate("Page1Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">1.3 Capacity</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">State the directory linked to your Capacity file. An example of a valid directory format for an xlsx file named Capacity is &quot;C:\\Users\\Mary Tan\\Documents\\DataInputs\\Capacity.xlsx&quot;, excluding the inverted commas. Press the \'Submit\' button.</span></p></body></html>"))
        self.MRPEndLabel.setText(_translate("Page1Window", "End Period:"))
        self.CapacityButton.setText(_translate("Page1Window", "Submit"))
        self.NextPageButton1.setText(_translate("Page1Window", "Next Page"))



""" Main System """
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Page1Window = QtWidgets.QMainWindow()
    ui = Ui_Page1Window()
    ui.setupUi(Page1Window)
    Page1Window.show()
    sys.exit(app.exec_())