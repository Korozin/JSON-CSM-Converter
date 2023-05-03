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
        self.Dynamic_Button.setToolTip("Convert JSON data dynamically based on existing type\n"
                                       "(EG: Head data will be converted to BOX:HEAD) if bb_main\n"
                                       "data exists, you can choose the tag that gets assigned")
        self.CSM_Button.setToolTip("Dynamically converts JSON data to CSM Format. \n"
                                   "Both outputs to CSM / BOX Text Box and 'model.csm'")

        # Initialize Error / Info windows
        self.ErrorWindow = ErrorWindow.ErrorWindow()
        self.InfoWindow = InfoWindow.InfoWindow()


    def Set_Functions(self):
        self.Clear_Button.clicked.connect(self.Clear_Form)
        self.Copy_Button.clicked.connect(self.Copy_Form_Contents)
        self.Dynamic_Button.clicked.connect(self.Dynamic_Convert_JSON)
        self.CSM_Button.clicked.connect(self.Convert_JSON_To_CSM)

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
        except Exception as e:
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

            boxes = []
            show_bb_main_dialog = any('bb_main' in bone['name'] for bone in data['minecraft:geometry'][0]['bones'])

            if show_bb_main_dialog:
                # Show a dialog box with a list of valid options for the user to choose from
                chosen_bb_main_tag = None  
                box_name, ok = QtWidgets.QInputDialog.getItem(self, "Choose a tag", "Choose a tag for all bb_main instances from the following options:", valid_box_names)
                if not ok:
                    return
                chosen_bb_main_tag = box_name

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
                    boxes.append(f"BOX:{box_name_bone} {origin[0]} {origin[1]} " 
                                 f"{origin[2]} {size[0]} {size[1]} {size[2]} {uv[0]} {uv[1]}")

            box_string = "\n".join(boxes)
            self.CSM_Text_Edit.insertPlainText(box_string)
        except Exception as e:
            self.ErrorWindow.CreateWindow("JSON Error!",
                                         f"{e}<br/><br/>Invalid or empty JSON Data",
                                         500, 200)
            self.ErrorWindow.show()


    def Convert_JSON_To_CSM(self):
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

            # Ask the user which conversion option they'd like to use
            text, okPressed = QtWidgets.QInputDialog.getItem(self, "Conversion Options","What conversion option would you like to use?", 
                                                ("Old", "New"), 0, False)
            if okPressed:
                choice = text
            else:
                choice = "Old"

            # Get a list of all the box names except 'bb_main'
            valid_box_names = [box_names[name] for name in box_names if 'bb_main' not in name]

            # Determine if bb_main dialog should show
            boxes = []
            show_bb_main_dialog = any('bb_main' in bone['name'] for bone in data['minecraft:geometry'][0]['bones'])

            # If the variable is true, show the bb_main dialog
            if show_bb_main_dialog:
                # Show a dialog box with a list of valid options for the user to choose from
                chosen_bb_main_tag = None  
                box_name, ok = QtWidgets.QInputDialog.getItem(self, "Choose a tag", "Choose a tag for all bb_main instances from the following options:", valid_box_names)
                if not ok:
                    return
                chosen_bb_main_tag = box_name

            # Main conversion logic
            for bone in data['minecraft:geometry'][0]['bones']:
                if 'bb_main' in bone['name']:
                    bone_type = chosen_bb_main_tag
                else:
                    bone_type = box_names.get(bone['name'], None)
                    if not bone_type:
                        # If the bone name is not recognized, skip it
                        continue

                for i, cube in enumerate(bone["cubes"]):
                    if choice == "Old":
                        boxes.append(f"{bone_type} {i}\n{bone_type}\n{bone_type} {i}\n"
                                     f"{cube['origin'][0]}\n"
                                     f"{cube['origin'][1]}\n"
                                     f"{cube['origin'][2]}\n"
                                     f"{cube['size'][0]}\n"
                                     f"{cube['size'][1]}\n"
                                     f"{cube['size'][2]}\n"
                                     f"{cube['uv'][0]}\n"
                                     f"{cube['uv'][1]}\n")
                    else:
                        boxes.append(f"{bone_type}\nPckStudio.generateModel+ModelPart\n{bone_type}\n"
                                     f"{cube['origin'][0]}\n"
                                     f"{cube['origin'][1]}\n"
                                     f"{cube['origin'][2]}\n"
                                     f"{cube['size'][0]}\n"
                                     f"{cube['size'][1]}\n"
                                     f"{cube['size'][2]}\n"
                                     f"{cube['uv'][0]}\n"
                                     f"{cube['uv'][1]}\n")

            # Make string readable
            box_string = "\n".join(boxes)

            # Format the text to have no extra lines
            lines = [line for line in box_string.split("\n") if line.strip()]
            new_lines = []
            for i, line in enumerate(lines):
                if i < len(lines) - 1 and line == lines[i+1]:
                    new_lines.append("\n".join([line, lines[i+1]]))
                else:
                    new_lines.append(line)
            new_text = "\n".join(new_lines)

            # Both output and save the CSM data
            self.CSM_Text_Edit.insertPlainText(new_text)
            open("model.csm", "w").write(new_text)

            # Show dialog alerting the user the CSM has been saved
            self.InfoWindow.CreateWindow("CSM Generated!",
                                         f"CSM saved to 'model.csm'",
                                         500, 200)
            self.InfoWindow.show()
        except Exception as e:
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
