import json
from PyQt5 import QtGui, QtWidgets
from Classes import MainWindow, InfoWindow, ErrorWindow


class JSONConvert_Main(QtWidgets.QMainWindow, MainWindow.JSONConvert_GUI):
    def __init__(self):
        super(JSONConvert_Main, self).__init__()

        self.setupUi(self)
        self.Set_Functions()
        self.CSM_Text_Edit.setReadOnly(True)
        self.KorOwOzin_Label.setOpenExternalLinks(True)

        self.ErrorWindow = ErrorWindow.ErrorWindow()
        self.InfoWindow = InfoWindow.InfoWindow()


    def Set_Functions(self):
        self.Clear_Button.clicked.connect(self.Clear_Form)
        self.Copy_Button.clicked.connect(self.Copy_Form_Contents)

        Button_Text_Pairs = [(self.Head_Button, "HEAD"), (self.Body_Button, "BODY"),
                            (self.Arm0_Button, "ARM0"), (self.Arm1_Button, "ARM1"),
                            (self.Leg0_Button, "LEG0"), (self.Leg1_Button, "LEG1")]

        for Button, Text in Button_Text_Pairs:
            Button.clicked.connect(lambda checked, arg=Text: self.Convert_JSON(arg))


    def Convert_JSON(self, mode_text):
        try:
            Data = json.loads(self.JSON_Text_Edit.toPlainText())
            self.CSM_Text_Edit.clear()

            Bone_Dict = {
                "bb_main": "BODY",
                "Head": "HEAD",
                "Body": "BODY",
                "RightArm": "ARM",
                "LeftArm": "ARM",
                "RightLeg": "LEG",
                "LeftLeg": "LEG"
            }

            Lines = []
            for Bone in Data["minecraft:geometry"][0]["bones"]:
                if "cubes" not in Bone:
                    continue
                if Bone["name"] not in Bone_Dict:
                    continue
                for Cube in Bone["cubes"]:
                    CSM_Data = f"BOX:{mode_text}", \
                               Cube["origin"][0], \
                               Cube["origin"][1], \
                               Cube["origin"][2], \
                               Cube["size"][0], \
                               Cube["size"][1], \
                               Cube["size"][2], \
                               Cube["uv"][0], \
                               Cube["uv"][1]
                    Lines.append(' '.join(map(str, CSM_Data)))

            self.CSM_Text_Edit.insertPlainText('\n'.join(Lines))
            if Lines:
                self.CSM_Text_Edit.moveCursor(QtGui.QTextCursor.EndOfLine)
        except json.decoder.JSONDecodeError as e:
            self.ErrorWindow.CreateWindow("JSON Error!",
                                         f"{e}<br/><br/>Invalid JSON Data",
                                         500, 200)
            self.ErrorWindow.show()


    def Clear_Form(self):
        self.JSON_Text_Edit.clear()
        self.CSM_Text_Edit.clear()


    def Copy_Form_Contents(self):
        Text_To_Copy = self.CSM_Text_Edit.toPlainText()
        if Text_To_Copy == "":
            self.ErrorWindow.CreateWindow("Clipboard Manager",
                                         f"CSM / BOX DATA Text box is empty!",
                                         500, 200)
            self.ErrorWindow.show()
        else:
            Lines = len(Text_To_Copy.split("\n"))
            Clipboard = QtWidgets.QApplication.clipboard()
            Clipboard.setText(Text_To_Copy)
            self.InfoWindow.CreateWindow("Clipboard Manager",
                                         f"Successfully copied {Lines} line(s)!",
                                         500, 200)
            self.InfoWindow.show()


if __name__ == "__main__":
    import sys
    JSONConvert_App = QtWidgets.QApplication(sys.argv)
    JSONConvert_Var = JSONConvert_Main()
    JSONConvert_Var.show()
    sys.exit(JSONConvert_App.exec_())
