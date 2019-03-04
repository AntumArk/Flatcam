from FlatCAMTool import FlatCAMTool
from ObjectCollection import *
from FlatCAMApp import *
from shapely.geometry import box


class CutOut(FlatCAMTool):

    toolName = "Cutout PCB"
    gapFinished = pyqtSignal()

    def __init__(self, app):
        FlatCAMTool.__init__(self, app)

        self.app = app
        self.canvas = app.plotcanvas

        ## Title
        title_label = QtWidgets.QLabel("%s" % self.toolName)
        title_label.setStyleSheet("""
                        QLabel
                        {
                            font-size: 16px;
                            font-weight: bold;
                        }
                        """)
        self.layout.addWidget(title_label)

        ## Form Layout
        form_layout = QtWidgets.QFormLayout()
        self.layout.addLayout(form_layout)

        ## Type of object to be cutout
        self.type_obj_combo = QtWidgets.QComboBox()
        self.type_obj_combo.addItem("Gerber")
        self.type_obj_combo.addItem("Excellon")
        self.type_obj_combo.addItem("Geometry")

        # we get rid of item1 ("Excellon") as it is not suitable for creating film
        self.type_obj_combo.view().setRowHidden(1, True)
        self.type_obj_combo.setItemIcon(0, QtGui.QIcon("share/flatcam_icon16.png"))
        # self.type_obj_combo.setItemIcon(1, QtGui.QIcon("share/drill16.png"))
        self.type_obj_combo.setItemIcon(2, QtGui.QIcon("share/geometry16.png"))

        self.type_obj_combo_label = QtWidgets.QLabel("Obj Type:")
        self.type_obj_combo_label.setToolTip(
            "Specify the type of object to be cutout.\n"
            "It can be of type: Gerber or Geometry.\n"
            "What is selected here will dictate the kind\n"
            "of objects that will populate the 'Object' combobox."
        )
        self.type_obj_combo_label.setFixedWidth(60)
        form_layout.addRow(self.type_obj_combo_label, self.type_obj_combo)

        ## Object to be cutout
        self.obj_combo = QtWidgets.QComboBox()
        self.obj_combo.setModel(self.app.collection)
        self.obj_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
        self.obj_combo.setCurrentIndex(1)

        self.object_label = QtWidgets.QLabel("Object:")
        self.object_label.setToolTip(
            "Object to be cutout.                        "
        )
        form_layout.addRow(self.object_label, self.obj_combo)

        # Tool Diameter
        self.dia = FCEntry()
        self.dia_label = QtWidgets.QLabel("Tool Dia:")
        self.dia_label.setToolTip(
            "Diameter of the tool used to cutout\n"
            "the PCB shape out of the surrounding material."
        )
        form_layout.addRow(self.dia_label, self.dia)

        # Margin
        self.margin = FCEntry()
        self.margin_label = QtWidgets.QLabel("Margin:")
        self.margin_label.setToolTip(
            "Margin over bounds. A positive value here\n"
            "will make the cutout of the PCB further from\n"
            "the actual PCB border"
        )
        form_layout.addRow(self.margin_label, self.margin)

        # Gapsize
        self.gapsize = FCEntry()
        self.gapsize_label = QtWidgets.QLabel("Gap size:")
        self.gapsize_label.setToolTip(
            "The size of the bridge gaps in the cutout\n"
            "used to keep the board connected to\n"
            "the surrounding material (the one \n"
            "from which the PCB is cutout)."
        )
        form_layout.addRow(self.gapsize_label, self.gapsize)

        # How gaps wil be rendered:
        # lr    - left + right
        # tb    - top + bottom
        # 4     - left + right +top + bottom
        # 2lr   - 2*left + 2*right
        # 2tb   - 2*top + 2*bottom
        # 8     - 2*left + 2*right +2*top + 2*bottom

        ## Title2
        title_param_label = QtWidgets.QLabel("<font size=4><b>A. Automatic Bridge Gaps</b></font>")
        title_param_label.setToolTip(
            "This section handle creation of automatic bridge gaps."
        )
        self.layout.addWidget(title_param_label)

        ## Form Layout
        form_layout_2 = QtWidgets.QFormLayout()
        self.layout.addLayout(form_layout_2)

        # Gaps
        gaps_label = QtWidgets.QLabel('Gaps:')
        gaps_label.setToolTip(
            "Number of gaps used for the Automatic cutout.\n"
            "There can be maximum 8 bridges/gaps.\n"
            "The choices are:\n"
            "- lr    - left + right\n"
            "- tb    - top + bottom\n"
            "- 4     - left + right +top + bottom\n"
            "- 2lr   - 2*left + 2*right\n"
            "- 2tb  - 2*top + 2*bottom\n"
            "- 8     - 2*left + 2*right +2*top + 2*bottom"
        )
        gaps_label.setFixedWidth(60)

        self.gaps = FCComboBox()
        gaps_items = ['LR', 'TB', '4', '2LR', '2TB', '8']
        for it in gaps_items:
            self.gaps.addItem(it)
            self.gaps.setStyleSheet('background-color: rgb(255,255,255)')
        form_layout_2.addRow(gaps_label, self.gaps)

        ## Buttons
        hlay = QtWidgets.QHBoxLayout()
        self.layout.addLayout(hlay)

        title_ff_label = QtWidgets.QLabel("<b>FreeForm:</b>")
        title_ff_label.setToolTip(
            "The cutout shape can be of ny shape.\n"
            "Useful when the PCB has a non-rectangular shape."
        )
        hlay.addWidget(title_ff_label)

        hlay.addStretch()

        self.ff_cutout_object_btn = QtWidgets.QPushButton("Generate Geo")
        self.ff_cutout_object_btn.setToolTip(
            "Cutout the selected object.\n"
            "The cutout shape can be of any shape.\n"
            "Useful when the PCB has a non-rectangular shape."
        )
        hlay.addWidget(self.ff_cutout_object_btn)

        hlay2 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(hlay2)

        title_rct_label = QtWidgets.QLabel("<b>Rectangular:</b>")
        title_rct_label.setToolTip(
            "The resulting cutout shape is\n"
            "always a rectangle shape and it will be\n"
            "the bounding box of the Object."
        )
        hlay2.addWidget(title_rct_label)

        hlay2.addStretch()
        self.rect_cutout_object_btn = QtWidgets.QPushButton("Generate Geo")
        self.rect_cutout_object_btn.setToolTip(
            "Cutout the selected object.\n"
            "The resulting cutout shape is\n"
            "always a rectangle shape and it will be\n"
            "the bounding box of the Object."
        )
        hlay2.addWidget(self.rect_cutout_object_btn)

        ## Title5
        title_manual_label = QtWidgets.QLabel("<font size=4><b>B. Manual Bridge Gaps</b></font>")
        title_manual_label.setToolTip(
            "This section handle creation of manual bridge gaps.\n"
            "This is done by mouse clicking on the perimeter of the\n"
            "Geometry object that is used as a cutout object. "
        )
        self.layout.addWidget(title_manual_label)

        ## Form Layout
        form_layout_3 = QtWidgets.QFormLayout()
        self.layout.addLayout(form_layout_3)

        ## Manual Geo Object
        self.man_object_combo = QtWidgets.QComboBox()
        self.man_object_combo.setModel(self.app.collection)
        self.man_object_combo.setRootModelIndex(self.app.collection.index(2, 0, QtCore.QModelIndex()))
        self.man_object_combo.setCurrentIndex(1)

        self.man_object_label = QtWidgets.QLabel("Geo Obj:")
        self.man_object_label.setToolTip(
            "Geometry object used to create the manual cutout."
        )
        self.man_object_label.setFixedWidth(60)
        # e_lab_0 = QtWidgets.QLabel('')

        form_layout_3.addRow(self.man_object_label, self.man_object_combo)
        # form_layout_3.addRow(e_lab_0)

        hlay3 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(hlay3)

        self.man_geo_label = QtWidgets.QLabel("Manual Geo:")
        self.man_geo_label.setToolTip(
            "If the object to be cutout is a Gerber\n"
            "first create a Geometry that surrounds it,\n"
            "to be used as the cutout, if one doesn't exist yet.\n"
            "Select the source Gerber file in the top object combobox."
        )
        hlay3.addWidget(self.man_geo_label)

        hlay3.addStretch()
        self.man_geo_creation_btn = QtWidgets.QPushButton("Generate Geo")
        self.man_geo_creation_btn.setToolTip(
            "If the object to be cutout is a Gerber\n"
            "first create a Geometry that surrounds it,\n"
            "to be used as the cutout, if one doesn't exist yet.\n"
            "Select the source Gerber file in the top object combobox."
        )
        hlay3.addWidget(self.man_geo_creation_btn)

        hlay4 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(hlay4)

        self.man_bridge_gaps_label = QtWidgets.QLabel("Manual Add Bridge Gaps:")
        self.man_bridge_gaps_label.setToolTip(
            "Use the left mouse button (LMB) click\n"
            "to create a bridge gap to separate the PCB from\n"
            "the surrounding material."
        )
        hlay4.addWidget(self.man_bridge_gaps_label)

        hlay4.addStretch()
        self.man_gaps_creation_btn = QtWidgets.QPushButton("Generate Gap")
        self.man_gaps_creation_btn.setToolTip(
            "Use the left mouse button (LMB) click\n"
            "to create a bridge gap to separate the PCB from\n"
            "the surrounding material.\n"
            "The LMB click has to be done on the perimeter of\n"
            "the Geometry object used as a cutout geometry."
        )
        hlay4.addWidget(self.man_gaps_creation_btn)

        self.layout.addStretch()

        self.cutting_gapsize = 0.0
        self.cutting_dia = 0.0

        # true if we want to repeat the gap without clicking again on the button
        self.repeat_gap = False

    def on_type_obj_index_changed(self, index):
        obj_type = self.type_obj_combo.currentIndex()
        self.obj_combo.setRootModelIndex(self.app.collection.index(obj_type, 0, QtCore.QModelIndex()))
        self.obj_combo.setCurrentIndex(0)

    def run(self):
        self.app.report_usage("ToolCutOut()")

        # if the splitter is hidden, display it, else hide it but only if the current widget is the same
        if self.app.ui.splitter.sizes()[0] == 0:
            self.app.ui.splitter.setSizes([1, 1])
        else:
            try:
                if self.app.ui.tool_scroll_area.widget().objectName() == self.toolName:
                    self.app.ui.splitter.setSizes([0, 1])
            except AttributeError:
                pass
        FlatCAMTool.run(self)
        self.set_tool_ui()

        self.app.ui.notebook.setTabText(2, "Cutout Tool")

    def install(self, icon=None, separator=None, **kwargs):
        FlatCAMTool.install(self, icon, separator, shortcut='ALT+U', **kwargs)

    def set_tool_ui(self):
        self.reset_fields()

        self.dia.set_value(float(self.app.defaults["tools_cutouttooldia"]))
        self.margin.set_value(float(self.app.defaults["tools_cutoutmargin"]))
        self.gapsize.set_value(float(self.app.defaults["tools_cutoutgapsize"]))
        self.gaps.set_value(4)

        ## Signals
        self.ff_cutout_object_btn.clicked.connect(self.on_freeform_cutout)
        self.rect_cutout_object_btn.clicked.connect(self.on_rectangular_cutout)

        self.type_obj_combo.currentIndexChanged.connect(self.on_type_obj_index_changed)
        self.man_geo_creation_btn.clicked.connect(self.on_manual_geo)
        self.man_gaps_creation_btn.clicked.connect(self.on_manual_gap_click)

        self.gapFinished.connect(self.on_gap_finished)

    def on_freeform_cutout(self):

        def subtract_rectangle(obj_, x0, y0, x1, y1):
            pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            obj_.subtract_polygon(pts)

        name = self.obj_combo.currentText()

        # Get source object.
        try:
            cutout_obj = self.app.collection.get_by_name(str(name))
        except:
            self.app.inform.emit("[ERROR_NOTCL]Could not retrieve object: %s" % name)
            return "Could not retrieve object: %s" % name

        if cutout_obj is None:
            self.app.inform.emit("[ERROR_NOTCL]There is no object selected for Cutout.\nSelect one and try again.")
            return

        try:
            dia = float(self.dia.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                dia = float(self.dia.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Tool diameter value is missing or wrong format. "
                                     "Add it and retry.")
                return


        if 0 in {dia}:
            self.app.inform.emit("[WARNING_NOTCL]Tool Diameter is zero value. Change it to a positive integer.")
            return "Tool Diameter is zero value. Change it to a positive integer."

        try:
            margin = float(self.margin.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                margin = float(self.margin.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Margin value is missing or wrong format. "
                                     "Add it and retry.")
                return

        try:
            gapsize = float(self.gapsize.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                gapsize = float(self.gapsize.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Gap size value is missing or wrong format. "
                                     "Add it and retry.")
                return

        try:
            gaps = self.gaps.get_value()
        except TypeError:
            self.app.inform.emit("[WARNING_NOTCL] Number of gaps value is missing. Add it and retry.")
            return

        if gaps not in ['LR', 'TB', '2LR', '2TB', '4', '8']:
            self.app.inform.emit("[WARNING_NOTCL] Gaps value can be only one of: 'lr', 'tb', '2lr', '2tb', 4 or 8. "
                                 "Fill in a correct value and retry. ")
            return

        if cutout_obj.multigeo is True:
            self.app.inform.emit("[ERROR]Cutout operation cannot be done on a multi-geo Geometry.\n"
                                 "Optionally, this Multi-geo Geometry can be converted to Single-geo Geometry,\n"
                                 "and after that perform Cutout.")
            return

        # Get min and max data for each object as we just cut rectangles across X or Y
        xmin, ymin, xmax, ymax = cutout_obj.bounds()
        px = 0.5 * (xmin + xmax) + margin
        py = 0.5 * (ymin + ymax) + margin
        lenghtx = (xmax - xmin) + (margin * 2)
        lenghty = (ymax - ymin) + (margin * 2)

        gapsize = gapsize / 2 + (dia / 2)

        if isinstance(cutout_obj,FlatCAMGeometry):
            # rename the obj name so it can be identified as cutout
            cutout_obj.options["name"] += "_cutout"
        else:
            def geo_init(geo_obj, app_obj):
                geo = cutout_obj.solid_geometry.convex_hull
                geo_obj.solid_geometry = geo.buffer(margin + abs(dia / 2))

            outname = cutout_obj.options["name"] + "_cutout"
            self.app.new_object('geometry', outname, geo_init)

            cutout_obj = self.app.collection.get_by_name(outname)

        if gaps == '8' or gaps == '2LR':
            subtract_rectangle(cutout_obj,
                               xmin - gapsize,  # botleft_x
                               py - gapsize + lenghty / 4,  # botleft_y
                               xmax + gapsize,  # topright_x
                               py + gapsize + lenghty / 4)  # topright_y
            subtract_rectangle(cutout_obj,
                               xmin - gapsize,
                               py - gapsize - lenghty / 4,
                               xmax + gapsize,
                               py + gapsize - lenghty / 4)

        if gaps == '8' or gaps == '2TB':
            subtract_rectangle(cutout_obj,
                               px - gapsize + lenghtx / 4,
                               ymin - gapsize,
                               px + gapsize + lenghtx / 4,
                               ymax + gapsize)
            subtract_rectangle(cutout_obj,
                               px - gapsize - lenghtx / 4,
                               ymin - gapsize,
                               px + gapsize - lenghtx / 4,
                               ymax + gapsize)

        if gaps == '4' or gaps == 'LR':
            subtract_rectangle(cutout_obj,
                               xmin - gapsize,
                               py - gapsize,
                               xmax + gapsize,
                               py + gapsize)

        if gaps == '4' or gaps == 'TB':
            subtract_rectangle(cutout_obj,
                               px - gapsize,
                               ymin - gapsize,
                               px + gapsize,
                               ymax + gapsize)

        cutout_obj.plot()
        self.app.inform.emit("[success] Any form CutOut operation finished.")
        self.app.ui.notebook.setCurrentWidget(self.app.ui.project_tab)
        self.app.should_we_save = True

    def on_rectangular_cutout(self):

        def subtract_rectangle(obj_, x0, y0, x1, y1):
            pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            obj_.subtract_polygon(pts)

        name = self.obj_combo.currentText()

        # Get source object.
        try:
            cutout_obj = self.app.collection.get_by_name(str(name))
        except:
            self.app.inform.emit("[ERROR_NOTCL]Could not retrieve object: %s" % name)
            return "Could not retrieve object: %s" % name

        if cutout_obj is None:
            self.app.inform.emit("[ERROR_NOTCL]Object not found: %s" % cutout_obj)

        try:
            dia = float(self.dia.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                dia = float(self.dia.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Tool diameter value is missing or wrong format. "
                                     "Add it and retry.")
                return

        if 0 in {dia}:
            self.app.inform.emit("[ERROR_NOTCL]Tool Diameter is zero value. Change it to a positive integer.")
            return "Tool Diameter is zero value. Change it to a positive integer."

        try:
            margin = float(self.margin.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                margin = float(self.margin.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Margin value is missing or wrong format. "
                                     "Add it and retry.")
                return

        try:
            gapsize = float(self.gapsize.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                gapsize = float(self.gapsize.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Gap size value is missing or wrong format. "
                                     "Add it and retry.")
                return

        try:
            gaps = self.gaps.get_value()
        except TypeError:
            self.app.inform.emit("[WARNING_NOTCL] Number of gaps value is missing. Add it and retry.")
            return

        if gaps not in ['LR', 'TB', '2LR', '2TB', '4', '8']:
            self.app.inform.emit("[WARNING_NOTCL] Gaps value can be only one of: 'lr', 'tb', '2lr', '2tb', 4 or 8. "
                                 "Fill in a correct value and retry. ")
            return

        if cutout_obj.multigeo is True:
            self.app.inform.emit("[ERROR]Cutout operation cannot be done on a multi-geo Geometry.\n"
                                 "Optionally, this Multi-geo Geometry can be converted to Single-geo Geometry,\n"
                                 "and after that perform Cutout.")
            return

        # Get min and max data for each object as we just cut rectangles across X or Y
        xmin, ymin, xmax, ymax = cutout_obj.bounds()
        geo = box(xmin, ymin, xmax, ymax)

        px = 0.5 * (xmin + xmax) + margin
        py = 0.5 * (ymin + ymax) + margin
        lenghtx = (xmax - xmin) + (margin * 2)
        lenghty = (ymax - ymin) + (margin * 2)

        gapsize = gapsize / 2 + (dia / 2)

        def geo_init(geo_obj, app_obj):
            geo_obj.solid_geometry = geo.buffer(margin + abs(dia / 2))

        outname = cutout_obj.options["name"] + "_cutout"
        self.app.new_object('geometry', outname, geo_init)

        cutout_obj = self.app.collection.get_by_name(outname)

        if gaps == '8' or gaps == '2LR':
            subtract_rectangle(cutout_obj,
                               xmin - gapsize,  # botleft_x
                               py - gapsize + lenghty / 4,  # botleft_y
                               xmax + gapsize,  # topright_x
                               py + gapsize + lenghty / 4)  # topright_y
            subtract_rectangle(cutout_obj,
                               xmin - gapsize,
                               py - gapsize - lenghty / 4,
                               xmax + gapsize,
                               py + gapsize - lenghty / 4)

        if gaps == '8' or gaps == '2TB':
            subtract_rectangle(cutout_obj,
                               px - gapsize + lenghtx / 4,
                               ymin - gapsize,
                               px + gapsize + lenghtx / 4,
                               ymax + gapsize)
            subtract_rectangle(cutout_obj,
                               px - gapsize - lenghtx / 4,
                               ymin - gapsize,
                               px + gapsize - lenghtx / 4,
                               ymax + gapsize)

        if gaps == '4' or gaps == 'LR':
            subtract_rectangle(cutout_obj,
                               xmin - gapsize,
                               py - gapsize,
                               xmax + gapsize,
                               py + gapsize)

        if gaps == '4' or gaps == 'TB':
            subtract_rectangle(cutout_obj,
                               px - gapsize,
                               ymin - gapsize,
                               px + gapsize,
                               ymax + gapsize)

        cutout_obj.plot()
        self.app.inform.emit("[success] Any form CutOut operation finished.")
        self.app.ui.notebook.setCurrentWidget(self.app.ui.project_tab)
        self.app.should_we_save = True

    def on_manual_gap_click(self):
        self.app.inform.emit("Click on the selected geometry object perimeter to create a bridge gap ...")
        self.app.geo_editor.tool_shape.enabled = True

        try:
            self.cutting_dia = float(self.dia.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                self.cutting_dia = float(self.dia.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Tool diameter value is missing or wrong format. "
                                     "Add it and retry.")
                return

        if 0 in {self.cutting_dia}:
            self.app.inform.emit("[ERROR_NOTCL]Tool Diameter is zero value. Change it to a positive integer.")
            return "Tool Diameter is zero value. Change it to a positive integer."

        try:
            self.cutting_gapsize = float(self.gapsize.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                self.cutting_gapsize = float(self.gapsize.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Gap size value is missing or wrong format. "
                                     "Add it and retry.")
                return

        self.app.plotcanvas.vis_disconnect('key_press', self.app.ui.keyPressEvent)
        self.app.plotcanvas.vis_disconnect('mouse_press', self.app.on_mouse_click_over_plot)
        self.app.plotcanvas.vis_disconnect('mouse_release', self.app.on_mouse_click_release_over_plot)
        self.app.plotcanvas.vis_disconnect('mouse_move', self.app.on_mouse_move_over_plot)
        self.app.plotcanvas.vis_connect('key_press', self.on_key_press)
        self.app.plotcanvas.vis_connect('mouse_move', self.on_mouse_move)
        self.app.plotcanvas.vis_connect('mouse_release', self.doit)

    # To be called after clicking on the plot.
    def doit(self, event):
        # do paint single only for left mouse clicks
        if event.button == 1:
            self.app.inform.emit("Making manual bridge gap...")
            pos = self.app.plotcanvas.vispy_canvas.translate_coords(event.pos)
            self.on_manual_cutout(click_pos=pos)

            self.app.plotcanvas.vis_disconnect('key_press', self.on_key_press)
            self.app.plotcanvas.vis_disconnect('mouse_move', self.on_mouse_move)
            self.app.plotcanvas.vis_disconnect('mouse_release', self.doit)
            self.app.plotcanvas.vis_connect('key_press', self.app.ui.keyPressEvent)
            self.app.plotcanvas.vis_connect('mouse_press', self.app.on_mouse_click_over_plot)
            self.app.plotcanvas.vis_connect('mouse_release', self.app.on_mouse_click_release_over_plot)
            self.app.plotcanvas.vis_connect('mouse_move', self.app.on_mouse_move_over_plot)

            self.app.geo_editor.tool_shape.clear(update=True)
            self.app.geo_editor.tool_shape.enabled = False
            self.gapFinished.emit()

    def on_manual_cutout(self, click_pos):
        name = self.man_object_combo.currentText()

        # Get source object.
        try:
            cutout_obj = self.app.collection.get_by_name(str(name))
        except:
            self.app.inform.emit("[ERROR_NOTCL]Could not retrieve Geoemtry object: %s" % name)
            return "Could not retrieve object: %s" % name

        if cutout_obj is None:
            self.app.inform.emit("[ERROR_NOTCL]Geometry object for manual cutout not found: %s" % cutout_obj)
            return

        # use the snapped position as reference
        snapped_pos = self.app.geo_editor.snap(click_pos[0], click_pos[1])

        cut_poly = self.cutting_geo(pos=(snapped_pos[0], snapped_pos[1]))
        cutout_obj.subtract_polygon(cut_poly)

        cutout_obj.plot()
        self.app.inform.emit("[success] Added manual Bridge Gap.")

        self.app.should_we_save = True

    def on_gap_finished(self):
        # if CTRL key modifier is pressed then repeat the bridge gap cut
        key_modifier = QtWidgets.QApplication.keyboardModifiers()
        if key_modifier == Qt.ControlModifier:
            self.on_manual_gap_click()

    def on_manual_geo(self):
        name = self.obj_combo.currentText()

        # Get source object.
        try:
            cutout_obj = self.app.collection.get_by_name(str(name))
        except:
            self.app.inform.emit("[ERROR_NOTCL]Could not retrieve Gerber object: %s" % name)
            return "Could not retrieve object: %s" % name

        if cutout_obj is None:
            self.app.inform.emit("[ERROR_NOTCL]There is no Gerber object selected for Cutout.\n"
                                 "Select one and try again.")
            return

        if not isinstance(cutout_obj, FlatCAMGerber):
            self.app.inform.emit("[ERROR_NOTCL]The selected object has to be of Gerber type.\n"
                                 "Select a Gerber file and try again.")
            return

        try:
            dia = float(self.dia.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                dia = float(self.dia.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Tool diameter value is missing or wrong format. "
                                     "Add it and retry.")
                return

        if 0 in {dia}:
            self.app.inform.emit("[ERROR_NOTCL]Tool Diameter is zero value. Change it to a positive integer.")
            return "Tool Diameter is zero value. Change it to a positive integer."

        try:
            margin = float(self.margin.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                margin = float(self.margin.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit("[WARNING_NOTCL] Margin value is missing or wrong format. "
                                     "Add it and retry.")
                return

        def geo_init(geo_obj, app_obj):
            geo = cutout_obj.solid_geometry.convex_hull
            geo_obj.solid_geometry = geo.buffer(margin + abs(dia / 2))

        outname = cutout_obj.options["name"] + "_cutout"
        self.app.new_object('geometry', outname, geo_init)

    def cutting_geo(self, pos):
        self.cutting_gapsize = self.cutting_gapsize / 2 + (self.cutting_dia / 2)
        offset = self.cutting_gapsize / 2

        # cutting area definition
        orig_x = pos[0]
        orig_y = pos[1]
        xmin = orig_x - offset
        ymin = orig_y - offset
        xmax = orig_x + offset
        ymax = orig_y + offset

        cut_poly = box(xmin, ymin, xmax, ymax)
        return cut_poly

    def on_mouse_move(self, event):

        self.app.on_mouse_move_over_plot(event=event)

        pos = self.canvas.vispy_canvas.translate_coords(event.pos)
        event.xdata, event.ydata = pos[0], pos[1]

        try:
            x = float(event.xdata)
            y = float(event.ydata)
        except TypeError:
            return

        snap_x, snap_y = self.app.geo_editor.snap(x, y)

        geo = self.cutting_geo(pos=(snap_x, snap_y))

        # Remove any previous utility shape
        self.app.geo_editor.tool_shape.clear(update=True)
        self.draw_utility_geometry(geo=geo)

    def draw_utility_geometry(self, geo):
        self.app.geo_editor.tool_shape.add(
            shape=geo,
            color=(self.app.defaults["global_draw_color"] + '80'),
            update=False,
            layer=0,
            tolerance=None)
        self.app.geo_editor.tool_shape.redraw()

    def on_key_press(self, event):
        # events out of the self.app.collection view (it's about Project Tab) are of type int
        if type(event) is int:
            key = event
        # events from the GUI are of type QKeyEvent
        elif type(event) == QtGui.QKeyEvent:
            key = event.key()
        # events from Vispy are of type KeyEvent
        else:
            key = event.key

        # Escape = Deselect All
        if key == QtCore.Qt.Key_Escape or key == 'Escape':
            self.app.plotcanvas.vis_disconnect('key_press', self.on_key_press)
            self.app.plotcanvas.vis_disconnect('mouse_move', self.on_mouse_move)
            self.app.plotcanvas.vis_disconnect('mouse_release', self.doit)
            self.app.plotcanvas.vis_connect('key_press', self.app.ui.keyPressEvent)
            self.app.plotcanvas.vis_connect('mouse_press', self.app.on_mouse_click_over_plot)
            self.app.plotcanvas.vis_connect('mouse_release', self.app.on_mouse_click_release_over_plot)
            self.app.plotcanvas.vis_connect('mouse_move', self.app.on_mouse_move_over_plot)

            # Remove any previous utility shape
            self.app.geo_editor.tool_shape.clear(update=True)
            self.app.geo_editor.tool_shape.enabled = False

    def reset_fields(self):
        self.obj_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))