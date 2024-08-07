# Import libraries
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", '-r', 'requirements.txt'])
from PyQt5 import QtCore, QtGui, QtWidgets
from UIPage3 import Ui_Page3Window

# UI Page 2: Generation
class Ui_Page2Window(object):
    def setupUi(self, Page2Window):
        """ Configuration of Features """
        Page2Window.setObjectName("Page2Window")
        Page2Window.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(Page2Window)
        self.centralwidget.setObjectName("centralwidget")

        # Page Header
        self.Page2Header = QtWidgets.QLabel(self.centralwidget)
        self.Page2Header.setGeometry(QtCore.QRect(460, 20, 1000, 50))
        self.Page2Header.setText("")
        self.Page2Header.setPixmap(QtGui.QPixmap("page 2 head.jpg"))
        self.Page2Header.setScaledContents(True)
        self.Page2Header.setObjectName("Page2Header")

        # Labels
        # 'Generating...'
        self.GeneratingLabel = QtWidgets.QLabel(self.centralwidget)
        self.GeneratingLabel.setGeometry(QtCore.QRect(900, 200, 120, 50))
        self.GeneratingLabel.setObjectName("GeneratingLabel")

        # 'Do not press...'
        self.DoNotPressLabel = QtWidgets.QLabel(self.centralwidget)
        self.DoNotPressLabel.setGeometry(QtCore.QRect(660, 470, 600, 50))
        self.DoNotPressLabel.setObjectName("DoNotPressLabel")

        # Progress Bar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(760, 270, 400, 50))
        self.progressBar.setProperty("value", 25)
        self.progressBar.setObjectName("progressBar")

        # Next Page Button
        self.NextPageButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.NextPageButton2.setGeometry(QtCore.QRect(885, 400, 150, 50))
        self.NextPageButton2.setObjectName("NextPageButton2")
        # Connect Action Function
        self.NextPageButton2.clicked.connect(self.NextPageButton2Clicked)
        
        # (unused) Menu and Status bar
        Page2Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Page2Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 22))
        self.menubar.setObjectName("menubar")
        Page2Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Page2Window)
        self.statusbar.setObjectName("statusbar")
        Page2Window.setStatusBar(self.statusbar)

        # (default) Configuration
        self.retranslateUi(Page2Window)
        QtCore.QMetaObject.connectSlotsByName(Page2Window)


    """ Action Functions """
    def NextPageButton2Clicked(self):
        if self.progressBar.value()==100:
            # Open page 3 Window
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_Page3Window()
            self.ui.setupUi(self.window)
            self.window.show()
            self.centralwidget.close()
            


    """ Paths and Text """
    def retranslateUi(self, Page2Window):
        _translate = QtCore.QCoreApplication.translate
        Page2Window.setWindowTitle(_translate("Page2Window", "MainWindow"))
        self.GeneratingLabel.setText(_translate("Page2Window", "Generating..."))
        self.NextPageButton2.setText(_translate("Page2Window", "Next Page"))
        self.DoNotPressLabel.setText(_translate("Page2Window", "Button proceeds to the next page when the progress bar reaches 100%"))


""" Main System """
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Page2Window = QtWidgets.QMainWindow()
    ui = Ui_Page2Window()
    ui.setupUi(Page2Window)
    Page2Window.show()
    sys.exit(app.exec_())
