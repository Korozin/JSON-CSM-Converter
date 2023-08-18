import os, json, datetime
from PyQt5 import QtWidgets
from Classes import MainWindow, InfoWindow, ErrorWindow


box_names = {
    'bb_main': 'NULL',
    'Head': 'HEAD',
    'Body': 'BODY',
    'RightArm': 'ARM0',
    'LeftArm': 'ARM1',
    'RightLeg': 'LEG0',
    'LeftLeg': 'LEG1'
}


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


    def generate_file_name(self, prefix, file_extension):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        file_extension = "csm"
        base_file_name = f"{prefix}_{current_date}"
        file_name = f"{base_file_name}.{file_extension}"
        version = 1

        while os.path.exists(file_name):
            file_name = f"{base_file_name}_({version}).{file_extension}"
            version += 1

        return file_name


    def Convert_JSON(self, mode_text):
        try:
            data = json.loads(self.JSON_Text_Edit.toPlainText())
            self.CSM_Text_Edit.clear()

            boxes = []

            for bone in data.get('minecraft:geometry', [])[0].get('bones', []):
                for cube in bone.get('cubes', []):
                    origin = cube['origin']
                    size = cube['size']
                    uv = cube['uv']
                    boxes.append(f"BOX:{mode_text} "
                        f"{origin[0]} "
                        f"{origin[1]} "
                        f"{origin[2]} "
                        f"{size[0]} "
                        f"{size[1]} "
                        f"{size[2]} "
                        f"{uv[0]} "
                        f"{uv[1]}"
                    )

            box_string = "\n".join(boxes)
            self.CSM_Text_Edit.insertPlainText(box_string)
        except Exception as e:
            self.ErrorWindow.CreateWindow(
                "JSON Error!",
                f"{e}<br/><br/>Invalid or empty JSON Data",
                500, 200
            )
            self.ErrorWindow.show()


    def Dynamic_Convert_JSON(self):
        try:
            data = json.loads(self.JSON_Text_Edit.toPlainText())
            self.CSM_Text_Edit.clear()

            valid_box_names = [box_names[name] for name in box_names if 'bb_main' not in name]

            boxes = []
            show_bb_main_dialog = any('bb_main' in bone['name'] for bone in data['minecraft:geometry'][0]['bones'])

            if show_bb_main_dialog:
                chosen_bb_main_tag, ok = QtWidgets.QInputDialog.getItem(
                    self,
                    "Choose a tag",
                    "Choose a tag for all bb_main instances from the following options:",
                    valid_box_names
                )
                if not ok:
                    return

            for bone in data['minecraft:geometry'][0]['bones']:
                box_name_bone = chosen_bb_main_tag if 'bb_main' in bone['name'] else box_names.get(bone['name'], None)
            
                if not box_name_bone:
                    continue

                for cube in bone['cubes']:
                    origin = cube['origin']
                    size = cube['size']
                    uv = cube['uv']
                    boxes.append(f"BOX:{box_name_bone} "
                        f"{origin[0]} "
                        f"{origin[1]} "
                        f"{origin[2]} "
                        f"{size[0]} "
                        f"{size[1]} "
                        f"{size[2]} "
                        f"{uv[0]} "
                        f"{uv[1]}"
                    )

            box_string = "\n".join(boxes)
            self.CSM_Text_Edit.insertPlainText(box_string)
        except Exception as e:
            self.ErrorWindow.CreateWindow(
                "JSON Error!",
                f"{e}<br/><br/>Invalid or empty JSON Data",
                500, 200
            )
            self.ErrorWindow.show()


    def Convert_JSON_To_CSM(self):
        try:
            data = json.loads(self.JSON_Text_Edit.toPlainText())
            self.CSM_Text_Edit.clear()

            valid_box_names = [box_names[name] for name in box_names if 'bb_main' not in name]

            boxes = []
            show_bb_main_dialog = any('bb_main' in bone['name'] for bone in data['minecraft:geometry'][0]['bones'])

            if show_bb_main_dialog:
                chosen_bb_main_tag, ok = QtWidgets.QInputDialog.getItem(
                    self,
                    "Choose a tag",
                    "Choose a tag for all bb_main instances from the following options:",
                    valid_box_names
                )
                if not ok:
                    return

            for bone in data['minecraft:geometry'][0]['bones']:
                box_name_bone = chosen_bb_main_tag if 'bb_main' in bone['name'] else box_names.get(bone['name'], None)
            
                if not box_name_bone:
                    continue

                for cube in bone['cubes']:
                    origin = cube['origin']
                    size = cube['size']
                    uv = cube['uv']
                    boxes.append(
                        f"PckStudio.generateModel+ModelPart\n"
                        f"{box_name_bone}\n"
                        f"PckStudio.generateModel+ModelPart\n"
                        f"{origin[0]}\n"
                        f"{origin[1]}\n"
                        f"{origin[2]}\n"
                        f"{size[0]}\n"
                        f"{size[1]}\n"
                        f"{size[2]}\n"
                        f"{uv[0]}\n"
                        f"{uv[1]}"
                    )

            box_string = "\n".join(boxes)
            self.CSM_Text_Edit.insertPlainText(box_string)

            file_name = self.generate_file_name("model", "csm")
            open(file_name, "w").write(box_string)

            self.InfoWindow.CreateWindow(
                "CSM Generated!",
                f"CSM saved to '{file_name}'",
                500, 200
            )
            self.InfoWindow.show()
        except Exception as e:
            self.ErrorWindow.CreateWindow(
                "JSON Error!",
                f"{e}<br/><br/>Invalid or empty JSON Data",
                500, 200
            )
            self.ErrorWindow.show()


    def Clear_Form(self):
        self.JSON_Text_Edit.clear()
        self.CSM_Text_Edit.clear()


    def Copy_Form_Contents(self):
        Text_To_Copy = self.CSM_Text_Edit.toPlainText()
        if Text_To_Copy == "":
            self.ErrorWindow.CreateWindow(
                "Clipboard Manager",
                f"CSM / BOX DATA Text box is empty!",
                500, 200
            )
            self.ErrorWindow.show()
        else:
            Lines = len(Text_To_Copy.split("\n"))
            Clipboard = QtWidgets.QApplication.clipboard()
            Clipboard.setText(Text_To_Copy)
            self.InfoWindow.CreateWindow(
                "Clipboard Manager",
                f"Successfully copied {Lines} line(s)!",
                500, 200
            )
            self.InfoWindow.show()


if __name__ == "__main__":
    import sys
    JSONConvert_App = QtWidgets.QApplication(sys.argv)
    JSONConvert_Var = JSONConvert_Main()
    JSONConvert_Var.show()
    sys.exit(JSONConvert_App.exec_())
