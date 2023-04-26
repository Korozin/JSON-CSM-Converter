from PyQt5 import QtCore, QtGui, QtWidgets


class JSONConvert_GUI(object):
    def setupUi(self, JSONConvert_GUI):
        JSONConvert_GUI.setObjectName("JSONConvert_GUI")
        JSONConvert_GUI.resize(534, 644)
        self.centralwidget = QtWidgets.QWidget(JSONConvert_GUI)
        self.centralwidget.setObjectName("centralwidget")
        self.Clear_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Clear_Button.setGeometry(QtCore.QRect(20, 420, 91, 31))
        self.Clear_Button.setObjectName("Clear_Button")
        self.JSON_Group_Box = QtWidgets.QGroupBox(self.centralwidget)
        self.JSON_Group_Box.setGeometry(QtCore.QRect(10, 20, 511, 131))
        self.JSON_Group_Box.setObjectName("JSON_Group_Box")
        self.JSON_Text_Edit = QtWidgets.QPlainTextEdit(self.JSON_Group_Box)
        self.JSON_Text_Edit.setGeometry(QtCore.QRect(8, 29, 495, 96))
        self.JSON_Text_Edit.setObjectName("JSON_Text_Edit")
        self.Parts_Group_Box = QtWidgets.QGroupBox(self.centralwidget)
        self.Parts_Group_Box.setGeometry(QtCore.QRect(10, 170, 111, 241))
        self.Parts_Group_Box.setObjectName("Parts_Group_Box")
        self.Leg1_Button = QtWidgets.QPushButton(self.Parts_Group_Box)
        self.Leg1_Button.setGeometry(QtCore.QRect(10, 203, 91, 31))
        self.Leg1_Button.setObjectName("Leg1_Button")
        self.Head_Button = QtWidgets.QPushButton(self.Parts_Group_Box)
        self.Head_Button.setGeometry(QtCore.QRect(11, 28, 91, 31))
        self.Head_Button.setObjectName("Head_Button")
        self.Body_Button = QtWidgets.QPushButton(self.Parts_Group_Box)
        self.Body_Button.setGeometry(QtCore.QRect(10, 62, 91, 31))
        self.Body_Button.setObjectName("Body_Button")
        self.Arm0_Button = QtWidgets.QPushButton(self.Parts_Group_Box)
        self.Arm0_Button.setGeometry(QtCore.QRect(10, 97, 91, 31))
        self.Arm0_Button.setObjectName("Arm0_Button")
        self.Leg0_Button = QtWidgets.QPushButton(self.Parts_Group_Box)
        self.Leg0_Button.setGeometry(QtCore.QRect(10, 168, 91, 31))
        self.Leg0_Button.setObjectName("Leg0_Button")
        self.Arm1_Button = QtWidgets.QPushButton(self.Parts_Group_Box)
        self.Arm1_Button.setGeometry(QtCore.QRect(10, 133, 91, 31))
        self.Arm1_Button.setObjectName("Arm1_Button")
        self.CSM_Group_Box = QtWidgets.QGroupBox(self.centralwidget)
        self.CSM_Group_Box.setGeometry(QtCore.QRect(190, 170, 331, 465))
        self.CSM_Group_Box.setObjectName("CSM_Group_Box")
        self.CSM_Text_Edit = QtWidgets.QPlainTextEdit(self.CSM_Group_Box)
        self.CSM_Text_Edit.setGeometry(QtCore.QRect(10, 30, 311, 391))
        self.CSM_Text_Edit.setObjectName("CSM_Text_Edit")
        self.Copy_Button = QtWidgets.QPushButton(self.CSM_Group_Box)
        self.Copy_Button.setGeometry(QtCore.QRect(10, 426, 311, 31))
        self.Copy_Button.setObjectName("Copy_Button")
        self.KorOwOzin_Label = QtWidgets.QLabel(self.centralwidget)
        self.KorOwOzin_Label.setGeometry(QtCore.QRect(10, 610, 71, 18))
        self.KorOwOzin_Label.setObjectName("KorOwOzin_Label")
        JSONConvert_GUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(JSONConvert_GUI)
        QtCore.QMetaObject.connectSlotsByName(JSONConvert_GUI)

    def retranslateUi(self, JSONConvert_GUI):
        _translate = QtCore.QCoreApplication.translate
        JSONConvert_GUI.setWindowTitle(_translate("JSONConvert_GUI", "JSONConvert - KorOwOzin"))
        self.Clear_Button.setText(_translate("JSONConvert_GUI", "CLEAR"))
        self.JSON_Group_Box.setTitle(_translate("JSONConvert_GUI", "JSON"))
        self.Parts_Group_Box.setTitle(_translate("JSONConvert_GUI", "PARTS"))
        self.Leg1_Button.setText(_translate("JSONConvert_GUI", "LEG1"))
        self.Head_Button.setText(_translate("JSONConvert_GUI", "HEAD"))
        self.Body_Button.setText(_translate("JSONConvert_GUI", "BODY"))
        self.Arm0_Button.setText(_translate("JSONConvert_GUI", "ARM0"))
        self.Leg0_Button.setText(_translate("JSONConvert_GUI", "LEG0"))
        self.Arm1_Button.setText(_translate("JSONConvert_GUI", "ARM1"))
        self.CSM_Group_Box.setTitle(_translate("JSONConvert_GUI", "CSM / BOX DATA"))
        self.Copy_Button.setText(_translate("JSONConvert_GUI", "COPY"))
        self.KorOwOzin_Label.setText(_translate("JSONConvert_GUI", "<html><head/><body><p><a href=\"https://github.com/Korozin\"><span style=\" text-decoration: underline; color:#0000ff;\">KorOwOzin</span></a></p></body></html>"))