import json
from PyQt5 import QtWidgets
from Classes import MainWindow, InfoWindow, ErrorWindow


class JSONConvert_Main(QtWidgets.QMainWindow, MainWindow.JSONConvert_GUI):
    def __init__(self):
        super(JSONConvert_Main, self).__init__()

        # Set up base GUI parameters
        self.setupUi(self)
        self.Set_Functions()
        self.CSM_Text_Edit.setReadOnly(True)
        self.KorOwOzin_Label.setOpenExternalLinks(True)

        self.Head_Button.setToolTip("Convert all JSON data to use BOX:HEAD tag")
        self.Body_Button.setToolTip("Convert all JSON data to use BOX:BODY tag")
        self.Arm0_Button.setToolTip("Convert all JSON data to use BOX:ARM0 tag")
        self.Arm1_Button.setToolTip("Convert all JSON data to use BOX:ARM1 tag")
        self.Leg0_Button.setToolTip("Convert all JSON data to use BOX:LEG0 tag")
        self.Leg1_Button.setToolTip("Convert all JSON data to use BOX:LEG1 tag")
        self.Dynamic_Button.setToolTip("Convert JSON data dynamically based on \
                                                existing type (EG: Head data will be converted\
                                                to BOX:HEAD) if bb_main data exists, you can\
                                                choose the tag that gets assigned")

        # Initialize Error / Info windows
        self.ErrorWindow = ErrorWindow.ErrorWindow()
        self.InfoWindow = InfoWindow.InfoWindow()


    def Set_Functions(self):
        self.Clear_Button.clicked.connect(self.Clear_Form)
        self.Copy_Button.clicked.connect(self.Copy_Form_Contents)
        self.Dynamic_Button.clicked.connect(self.Dynamic_Convert_JSON)

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
                'bb_main': 'NULL',
                'Head': 'HEAD',
                'Body': 'BODY',
                'RightArm': 'ARM0',
                'LeftArm': 'ARM1',
                'RightLeg': 'LEG0',
                'LeftLeg': 'LEG1'
            }

            Lines = []
            for Bone in Data["minecraft:geometry"][0]["bones"]:
                if "cubes" not in Bone:
                    continue
                bone_name = Bone["name"]
                if not any([bone_name.startswith("bb_main"), bone_name in Bone_Dict]):
                    continue
                bone_type = Bone_Dict.get(bone_name, Bone_Dict["bb_main"])
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
        except json.decoder.JSONDecodeError as e:
            self.ErrorWindow.CreateWindow("JSON Error!",
                                         f"{e}<br/><br/>Invalid or empty JSON Data",
                                         500, 200)
            self.ErrorWindow.show()


    def Dynamic_Convert_JSON(self):
        try:
            data = json.loads(self.JSON_Text_Edit.toPlainText())
            self.CSM_Text_Edit.clear()

            box_names = {
                'bb_main': 'NULL',
                'Head': 'HEAD',
                'Body': 'BODY',
                'RightArm': 'ARM0',
                'LeftArm': 'ARM1',
                'RightLeg': 'LEG0',
                'LeftLeg': 'LEG1'
            }

            # Get a list of all the box names except 'bb_main'
            valid_box_names = [box_names[name] for name in box_names if 'bb_main' not in name]

            # Show a dialog box with a list of valid options for the user to choose from
            chosen_bb_main_tag = None  
            box_name, ok = QtWidgets.QInputDialog.getItem(self, "Choose a tag", "Choose a tag for all bb_main instances from the following options:", valid_box_names)
            if not ok:
                return
            chosen_bb_main_tag = box_name

            boxes = []
            for bone in data['minecraft:geometry'][0]['bones']:
                if 'bb_main' in bone['name']:
                    box_name_bone = chosen_bb_main_tag
                else:
                    box_name_bone = box_names.get(bone['name'], None)
                    if not box_name_bone:
                        # If the bone name is not recognized, skip it
                        continue

                for cube in bone['cubes']:
                    origin = cube['origin']
                    size = cube['size']
                    uv = cube['uv']
                    boxes.append(f"BOX:{box_name_bone} {origin[0]} {origin[1]} {origin[2]} {size[0]} {size[1]} {size[2]} {uv[0]} {uv[1]}")

            box_string = "\n".join(boxes)
            self.CSM_Text_Edit.insertPlainText(box_string)
        except json.decoder.JSONDecodeError as e:
            self.ErrorWindow.CreateWindow("JSON Error!",
                                         f"{e}<br/><br/>Invalid or empty JSON Data",
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
