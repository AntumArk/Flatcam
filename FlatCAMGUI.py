############################################################
# FlatCAM: 2D Post-processing for Manufacturing            #
# http://flatcam.org                                       #
# Author: Juan Pablo Caram (c)                             #
# Date: 2/5/2014                                           #
# MIT Licence                                              #
############################################################

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSettings
from GUIElements import *
import platform


class FlatCAMGUI(QtWidgets.QMainWindow):
    # Emitted when persistent window geometry needs to be retained
    geom_update = QtCore.pyqtSignal(int, int, int, int, int, name='geomUpdate')
    final_save = QtCore.pyqtSignal(name='saveBeforeExit')

    def __init__(self, version, beta, app):
        super(FlatCAMGUI, self).__init__()

        self.app = app
        # Divine icon pack by Ipapun @ finicons.com

        #####################################
        ### BUILDING THE GUI IS DONE HERE ###
        #####################################

        ############
        ### Menu ###
        ############
        self.menu = self.menuBar()

        ### File ###
        self.menufile = self.menu.addMenu('&File')

        # New
        self.menufilenew = QtWidgets.QAction(QtGui.QIcon('share/file16.png'), '&New Project ...\tCTRL+N', self)
        self.menufile.addAction(self.menufilenew)

        self.menufile_open = self.menufile.addMenu(QtGui.QIcon('share/folder32_bis.png'), 'Open')
        # Open gerber ...
        self.menufileopengerber = QtWidgets.QAction(QtGui.QIcon('share/flatcam_icon24.png'),
                                                    'Open &Gerber ...\tCTRL+G', self)
        self.menufile_open.addAction(self.menufileopengerber)

        # Open gerber with follow...
        self.menufileopengerber_follow = QtWidgets.QAction(QtGui.QIcon('share/flatcam_icon24.png'),
                                                       'Open &Gerber (w/ Follow) ...', self)
        self.menufile_open.addAction(self.menufileopengerber_follow)
        self.menufile_open.addSeparator()

        # Open Excellon ...
        self.menufileopenexcellon = QtWidgets.QAction(QtGui.QIcon('share/open_excellon32.png'),
                                                      'Open &Excellon ...\tCTRL+E',
                                                  self)
        self.menufile_open.addAction(self.menufileopenexcellon)

        # Open G-Code ...
        self.menufileopengcode = QtWidgets.QAction(QtGui.QIcon('share/code.png'), 'Open G-&Code ...', self)
        self.menufile_open.addAction(self.menufileopengcode)

        # Open Project ...
        self.menufileopenproject = QtWidgets.QAction(QtGui.QIcon('share/folder16.png'), 'Open &Project ...', self)
        self.menufile_open.addAction(self.menufileopenproject)

        # Recent
        self.recent = self.menufile.addMenu(QtGui.QIcon('share/recent_files.png'), "Recent files")

        # Separator
        self.menufile.addSeparator()

        # Run Scripts
        self.menufilerunscript = QtWidgets.QAction(QtGui.QIcon('share/script16.png'), 'Run Script ...\tSHIFT+S', self)
        self.menufile.addAction(self.menufilerunscript)

        # Separator
        self.menufile.addSeparator()

        # Import ...
        self.menufileimport = self.menufile.addMenu(QtGui.QIcon('share/import.png'), 'Import')
        self.menufileimportsvg = QtWidgets.QAction(QtGui.QIcon('share/svg16.png'),
                                               '&SVG as Geometry Object ...', self)
        self.menufileimport.addAction(self.menufileimportsvg)
        self.menufileimportsvg_as_gerber = QtWidgets.QAction(QtGui.QIcon('share/svg16.png'),
                                                         '&SVG as Gerber Object ...', self)
        self.menufileimport.addAction(self.menufileimportsvg_as_gerber)
        self.menufileimport.addSeparator()

        self.menufileimportdxf = QtWidgets.QAction(QtGui.QIcon('share/dxf16.png'),
                                               '&DXF as Geometry Object ...', self)
        self.menufileimport.addAction(self.menufileimportdxf)
        self.menufileimportdxf_as_gerber = QtWidgets.QAction(QtGui.QIcon('share/dxf16.png'),
                                                         '&DXF as Gerber Object ...', self)
        self.menufileimport.addAction(self.menufileimportdxf_as_gerber)
        self.menufileimport.addSeparator()

        # Export ...
        self.menufileexport = self.menufile.addMenu(QtGui.QIcon('share/export.png'), 'Export')
        self.menufileexportsvg = QtWidgets.QAction(QtGui.QIcon('share/export.png'), 'Export &SVG ...', self)
        self.menufileexport.addAction(self.menufileexportsvg)

        self.menufileexportdxf = QtWidgets.QAction(QtGui.QIcon('share/export.png'), 'Export DXF ...', self)
        self.menufileexport.addAction(self.menufileexportdxf)

        self.menufileexport.addSeparator()

        self.menufileexportpng = QtWidgets.QAction(QtGui.QIcon('share/export_png32.png'), 'Export &PNG ...', self)
        self.menufileexport.addAction(self.menufileexportpng)

        self.menufileexport.addSeparator()

        self.menufileexportexcellon = QtWidgets.QAction(QtGui.QIcon('share/drill32.png'), 'Export &Excellon ...', self)
        self.menufileexport.addAction(self.menufileexportexcellon)

        self.menufileexportexcellon_altium = QtWidgets.QAction(QtGui.QIcon('share/drill32.png'),
                                                           'Export Excellon 2:4 LZ INCH ...', self)
        self.menufileexport.addAction(self.menufileexportexcellon_altium)

        # Separator
        self.menufile.addSeparator()

        # Save Defaults
        self.menufilesavedefaults = QtWidgets.QAction(QtGui.QIcon('share/defaults.png'), 'Save &Defaults', self)
        self.menufile.addAction(self.menufilesavedefaults)

        # Separator
        self.menufile.addSeparator()

        self.menufile_save = self.menufile.addMenu(QtGui.QIcon('share/save_as.png'), 'Save')
        # Save Project
        self.menufilesaveproject = QtWidgets.QAction(QtGui.QIcon('share/floppy16.png'), '&Save Project ...', self)
        self.menufile_save.addAction(self.menufilesaveproject)

        # Save Project As ...
        self.menufilesaveprojectas = QtWidgets.QAction(QtGui.QIcon('share/save_as.png'),
                                                       'Save Project &As ...\tCTRL+S', self)
        self.menufile_save.addAction(self.menufilesaveprojectas)

        # Save Project Copy ...
        self.menufilesaveprojectcopy = QtWidgets.QAction(QtGui.QIcon('share/floppy16.png'), 'Save Project C&opy ...',
                                                     self)
        self.menufile_save.addAction(self.menufilesaveprojectcopy)

        # Separator
        self.menufile.addSeparator()

        # Quit
        self.menufile_exit = QtWidgets.QAction(QtGui.QIcon('share/power16.png'), 'E&xit', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        self.menufile.addAction(self.menufile_exit)

        ### Edit ###
        self.menuedit = self.menu.addMenu('&Edit')
        self.menueditnew = self.menuedit.addAction(QtGui.QIcon('share/new_geo16.png'), '&New Geometry\tN')
        self.menueditnewexc = self.menuedit.addAction(QtGui.QIcon('share/new_geo16.png'), 'New Excellon\tL')
        # Separator
        self.menuedit.addSeparator()
        self.menueditedit = self.menuedit.addAction(QtGui.QIcon('share/edit16.png'), 'Edit Object\tE')
        self.menueditok = self.menuedit.addAction(QtGui.QIcon('share/edit_ok16.png'), 'Save && Close Editor\tCTRL+S')
        # Separator
        self.menuedit.addSeparator()
        self.menuedit_convert = self.menuedit.addMenu(QtGui.QIcon('share/convert24.png'), 'Conversion')
        self.menuedit_convertjoin = self.menuedit_convert.addAction(
            QtGui.QIcon('share/join16.png'), '&Join Geo/Gerber/Exc -> Geo')
        self.menuedit_convertjoin.setToolTip(
            "Merge a selection of objects, which can be of type:\n"
            "- Gerber\n"
            "- Excellon\n"
            "- Geometry\n"
            "into a new combo Geometry object.")
        self.menuedit_convertjoinexc = self.menuedit_convert.addAction(
            QtGui.QIcon('share/join16.png'), 'Join Excellon(s) -> Excellon')
        self.menuedit_convertjoinexc.setToolTip(
            "Merge a selection of Excellon objects into a new combo Excellon object.")
        self.menuedit_convertjoingrb = self.menuedit_convert.addAction(
            QtGui.QIcon('share/join16.png'), 'Join Gerber(s) -> Gerber')
        self.menuedit_convertjoingrb.setToolTip(
            "Merge a selection of Gerber objects into a new combo Gerber object.")
        # Separator
        self.menuedit_convert.addSeparator()
        self.menuedit_convert_sg2mg = self.menuedit_convert.addAction(
            QtGui.QIcon('share/convert24.png'), 'Convert Single to MultiGeo')
        self.menuedit_convert_sg2mg.setToolTip(
            "Will convert a Geometry object from single_geometry type\n"
            "to a multi_geometry type.")
        self.menuedit_convert_mg2sg = self.menuedit_convert.addAction(
            QtGui.QIcon('share/convert24.png'), 'Convert Multi to SingleGeo')
        self.menuedit_convert_mg2sg.setToolTip(
            "Will convert a Geometry object from multi_geometry type\n"
            "to a single_geometry type.")
        self.menuedit_convert.setToolTipsVisible(True)

        # Separator
        self.menuedit.addSeparator()
        self.menueditcopyobject = self.menuedit.addAction(QtGui.QIcon('share/copy.png'), '&Copy Object\tCTRL+C')
        self.menueditcopyobjectasgeom = self.menuedit.addAction(QtGui.QIcon('share/copy_geo.png'),
                                                                'Copy as &Geom')
        # Separator
        self.menuedit.addSeparator()
        self.menueditdelete = self.menuedit.addAction(QtGui.QIcon('share/trash16.png'), '&Delete\tDEL')

        # Separator
        self.menuedit.addSeparator()
        self.menueditorigin = self.menuedit.addAction(QtGui.QIcon('share/origin.png'), 'Se&t Origin\tO')
        self.menueditjump = self.menuedit.addAction(QtGui.QIcon('share/jump_to16.png'), 'Jump to Location\tJ')

        # Separator
        self.menuedit.addSeparator()
        self.menuedittoggleunits= self.menuedit.addAction(QtGui.QIcon('share/toggle_units16.png'),
                                                         'Toggle Units\tQ')
        self.menueditselectall = self.menuedit.addAction(QtGui.QIcon('share/select_all.png'),
                                                         '&Select All\tCTRL+A')

        # Separator
        self.menuedit.addSeparator()
        self.menueditpreferences = self.menuedit.addAction(QtGui.QIcon('share/pref.png'), '&Preferences\tSHIFT+P')

        ### Options ###
        self.menuoptions = self.menu.addMenu('&Options')
        # self.menuoptions_transfer = self.menuoptions.addMenu(QtGui.QIcon('share/transfer.png'), 'Transfer options')
        # self.menuoptions_transfer_a2p = self.menuoptions_transfer.addAction("Application to Project")
        # self.menuoptions_transfer_p2a = self.menuoptions_transfer.addAction("Project to Application")
        # self.menuoptions_transfer_p2o = self.menuoptions_transfer.addAction("Project to Object")
        # self.menuoptions_transfer_o2p = self.menuoptions_transfer.addAction("Object to Project")
        # self.menuoptions_transfer_a2o = self.menuoptions_transfer.addAction("Application to Object")
        # self.menuoptions_transfer_o2a = self.menuoptions_transfer.addAction("Object to Application")

        # Separator
        # self.menuoptions.addSeparator()

        # self.menuoptions_transform = self.menuoptions.addMenu(QtGui.QIcon('share/transform.png'),
        #                                                       '&Transform Object')
        self.menuoptions_transform_rotate = self.menuoptions.addAction(QtGui.QIcon('share/rotate.png'),
                                                                                 "&Rotate Selection\tSHIFT+(R)")
        # Separator
        self.menuoptions.addSeparator()

        self.menuoptions_transform_skewx = self.menuoptions.addAction(QtGui.QIcon('share/skewX.png'),
                                                                                "&Skew on X axis\tSHIFT+X")
        self.menuoptions_transform_skewy = self.menuoptions.addAction(QtGui.QIcon('share/skewY.png'),
                                                                                "S&kew on Y axis\tSHIFT+Y")

        # Separator
        self.menuoptions.addSeparator()
        self.menuoptions_transform_flipx = self.menuoptions.addAction(QtGui.QIcon('share/flipx.png'),
                                                                                "Flip on &X axis\tX")
        self.menuoptions_transform_flipy = self.menuoptions.addAction(QtGui.QIcon('share/flipy.png'),
                                                                                "Flip on &Y axis\tY")
        # Separator
        self.menuoptions.addSeparator()

        ### View ###
        self.menuview = self.menu.addMenu('&View')
        self.menuviewenable = self.menuview.addAction(QtGui.QIcon('share/replot16.png'), 'Enable all plots\tALT+1')
        self.menuviewdisableall = self.menuview.addAction(QtGui.QIcon('share/clear_plot16.png'),
                                                          'Disable all plots\tALT+2')
        self.menuviewdisableother = self.menuview.addAction(QtGui.QIcon('share/clear_plot16.png'),
                                                            'Disable non-selected\tALT+3')
        # Separator
        self.menuview.addSeparator()
        self.menuview_zoom_fit = self.menuview.addAction(QtGui.QIcon('share/zoom_fit32.png'), "&Zoom Fit\tV")
        self.menuview_zoom_in = self.menuview.addAction(QtGui.QIcon('share/zoom_in32.png'), "&Zoom In\t-")
        self.menuview_zoom_out = self.menuview.addAction(QtGui.QIcon('share/zoom_out32.png'), "&Zoom Out\t=")

        self.menuview.addSeparator()
        self.menuview_toggle_fscreen = self.menuview.addAction(
            QtGui.QIcon('share/fscreen32.png'), "&Toggle FullScreen\tALT+F10")
        self.menuview_toggle_parea = self.menuview.addAction(
            QtGui.QIcon('share/plot32.png'), "&Toggle Plot Area\tCTRL+F10")

        self.menuview.addSeparator()
        self.menuview_toggle_grid = self.menuview.addAction(QtGui.QIcon('share/grid32.png'), "&Toggle Grid\tG")
        self.menuview_toggle_axis = self.menuview.addAction(QtGui.QIcon('share/axis32.png'), "&Toggle Axis\tSHIFT+G")
        self.menuview_toggle_workspace = self.menuview.addAction(QtGui.QIcon('share/workspace24.png'),
                                                                 "Toggle Workspace\tSHIFT+W")

        ### Tool ###
        # self.menutool = self.menu.addMenu('&Tool')
        self.menutool = QtWidgets.QMenu('&Tool')
        self.menutoolaction = self.menu.addMenu(self.menutool)
        self.menutoolshell = self.menutool.addAction(QtGui.QIcon('share/shell16.png'), '&Command Line\tS')

        ### Help ###
        self.menuhelp = self.menu.addMenu('&Help')
        self.menuhelp_about = self.menuhelp.addAction(QtGui.QIcon('share/tv16.png'), 'About FlatCAM')
        self.menuhelp_home = self.menuhelp.addAction(QtGui.QIcon('share/home16.png'), 'Home')
        self.menuhelp_manual = self.menuhelp.addAction(QtGui.QIcon('share/globe16.png'), 'Manual\tF1')
        self.menuhelp.addSeparator()
        self.menuhelp_shortcut_list = self.menuhelp.addAction(QtGui.QIcon('share/shortcuts24.png'), 'Shortcuts List\t`')
        self.menuhelp_videohelp = self.menuhelp.addAction(QtGui.QIcon('share/videohelp24.png'), 'See on YouTube\tF2')


        ### FlatCAM Editor menu ###
        # self.editor_menu = QtWidgets.QMenu("Editor")
        # self.menu.addMenu(self.editor_menu)
        self.geo_editor_menu = QtWidgets.QMenu(">Geo Editor<")
        self.menu.addMenu(self.geo_editor_menu)

        # self.select_menuitem = self.menu.addAction(QtGui.QIcon('share/pointer16.png'), "Select 'Esc'")
        self.geo_add_circle_menuitem = self.geo_editor_menu.addAction(
            QtGui.QIcon('share/circle32.png'), 'Add Circle\tO'
        )
        self.geo_add_arc_menuitem = self.geo_editor_menu.addAction(QtGui.QIcon('share/arc16.png'), 'Add Arc\tA')
        self.geo_editor_menu.addSeparator()
        self.geo_add_rectangle_menuitem = self.geo_editor_menu.addAction(
            QtGui.QIcon('share/rectangle32.png'), 'Add Rectangle\tR'
        )
        self.geo_add_polygon_menuitem = self.geo_editor_menu.addAction(
            QtGui.QIcon('share/polygon32.png'), 'Add Polygon\tN'
        )
        self.geo_add_path_menuitem = self.geo_editor_menu.addAction(QtGui.QIcon('share/path32.png'), 'Add Path\tP')
        self.geo_editor_menu.addSeparator()
        self.geo_add_text_menuitem = self.geo_editor_menu.addAction(QtGui.QIcon('share/text32.png'), 'Add Text\tT')
        self.geo_editor_menu.addSeparator()
        self.geo_union_menuitem = self.geo_editor_menu.addAction(QtGui.QIcon('share/union16.png'), 'Polygon Union\tU')
        self.geo_intersection_menuitem = self.geo_editor_menu.addAction(QtGui.QIcon('share/intersection16.png'),
                                                         'Polygon Intersection\tE')
        self.geo_subtract_menuitem = self.geo_editor_menu.addAction(
            QtGui.QIcon('share/subtract16.png'), 'Polygon Subtraction\tS'
        )
        self.geo_editor_menu.addSeparator()
        self.geo_cutpath_menuitem = self.geo_editor_menu.addAction(QtGui.QIcon('share/cutpath16.png'), 'Cut Path\tX')
        # self.move_menuitem = self.menu.addAction(QtGui.QIcon('share/move16.png'), "Move Objects 'm'")
        self.geo_copy_menuitem = self.geo_editor_menu.addAction(QtGui.QIcon('share/copy16.png'), "Copy Geom\tC")
        self.geo_delete_menuitem = self.geo_editor_menu.addAction(
            QtGui.QIcon('share/deleteshape16.png'), "Delete Shape\tDEL"
        )
        self.geo_editor_menu.addSeparator()
        self.geo_move_menuitem = self.geo_editor_menu.addAction(QtGui.QIcon('share/move32.png'), "Move\tM")
        self.geo_buffer_menuitem = self.geo_editor_menu.addAction(
            QtGui.QIcon('share/buffer16.png'), "Buffer Selection\tB"
        )
        self.geo_paint_menuitem = self.geo_editor_menu.addAction(
            QtGui.QIcon('share/paint16.png'), "Paint Selection\tI"
        )
        self.geo_editor_menu.addSeparator()
        self.geo_cornersnap_menuitem = self.geo_editor_menu.addAction(
            QtGui.QIcon('share/corner32.png'), "Toggle Corner Snap\tK"
        )

        self.exc_editor_menu = QtWidgets.QMenu(">Excellon Editor<")
        self.menu.addMenu(self.exc_editor_menu)

        self.exc_add_array_drill_menuitem = self.exc_editor_menu.addAction(
            QtGui.QIcon('share/rectangle32.png'), 'Add Drill Array\tA')
        self.exc_add_drill_menuitem = self.exc_editor_menu.addAction(QtGui.QIcon('share/plus16.png'), 'Add Drill\tD')
        self.exc_editor_menu.addSeparator()

        self.exc_resize_drill_menuitem = self.exc_editor_menu.addAction(
            QtGui.QIcon('share/resize16.png'), 'Resize Drill(S)\tR'
        )
        self.exc_copy_drill_menuitem = self.exc_editor_menu.addAction(QtGui.QIcon('share/copy32.png'), 'Copy\tC')
        self.exc_delete_drill_menuitem = self.exc_editor_menu.addAction(
            QtGui.QIcon('share/deleteshape32.png'), 'Delete\tDEL'
        )
        self.exc_editor_menu.addSeparator()

        self.exc_move_drill_menuitem = self.exc_editor_menu.addAction(
            QtGui.QIcon('share/move32.png'), 'Move Drill(s)\tM')

        self.geo_editor_menu.menuAction().setVisible(False)
        self.geo_editor_menu.setDisabled(True)

        self.exc_editor_menu.menuAction().setVisible(False)
        self.exc_editor_menu.setDisabled(True)


        ################################
        ### Project Tab Context menu ###
        ################################

        self.menuproject = QtWidgets.QMenu()
        self.menuprojectenable = self.menuproject.addAction(QtGui.QIcon('share/replot32.png'), 'Enable Plot')
        self.menuprojectdisable = self.menuproject.addAction(QtGui.QIcon('share/clear_plot32.png'), 'Disable Plot')
        self.menuproject.addSeparator()
        self.menuprojectgeneratecnc = self.menuproject.addAction(QtGui.QIcon('share/cnc32.png'), 'Generate CNC')
        self.menuproject.addSeparator()
        self.menuprojectcopy = self.menuproject.addAction(QtGui.QIcon('share/copy32.png'), 'Copy')
        self.menuprojectdelete = self.menuproject.addAction(QtGui.QIcon('share/delete32.png'), 'Delete')
        self.menuprojectedit = self.menuproject.addAction(QtGui.QIcon('share/edit_ok32.png'), 'Edit')
        self.menuproject.addSeparator()
        self.menuprojectproperties = self.menuproject.addAction(QtGui.QIcon('share/properties32.png'), 'Properties')

        ################
        ### Splitter ###
        ################

        # IMPORTANT #
        # The order: SPITTER -> NOTEBOOK -> SNAP TOOLBAR is important and without it the GUI will not be initialized as
        # desired.
        self.splitter = QtWidgets.QSplitter()
        self.setCentralWidget(self.splitter)

        # self.notebook = QtWidgets.QTabWidget()
        self.notebook = FCDetachableTab(protect=True)
        self.notebook.setTabsClosable(False)
        self.notebook.useOldIndex(True)

        self.splitter.addWidget(self.notebook)

        self.splitter_left = QtWidgets.QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.splitter_left)
        self.splitter_left.addWidget(self.notebook)
        self.splitter_left.setHandleWidth(0)

        ###############
        ### Toolbar ###
        ###############

        ### TOOLBAR INSTALLATION ###
        self.toolbarfile = QtWidgets.QToolBar('File Toolbar')
        self.toolbarfile.setObjectName('File_TB')
        self.addToolBar(self.toolbarfile)
        self.toolbargeo = QtWidgets.QToolBar('Edit Toolbar')
        self.toolbargeo.setObjectName('Edit_TB')
        self.addToolBar(self.toolbargeo)
        self.toolbarview = QtWidgets.QToolBar('View Toolbar')
        self.toolbarview.setObjectName('View_TB')
        self.addToolBar(self.toolbarview)
        self.toolbartools = QtWidgets.QToolBar('Tools Toolbar')
        self.toolbartools.setObjectName('Tools_TB')
        self.addToolBar(self.toolbartools)
        self.exc_edit_toolbar = QtWidgets.QToolBar('Excellon Editor Toolbar')
        self.exc_edit_toolbar.setObjectName('ExcEditor_TB')
        self.addToolBar(self.exc_edit_toolbar)
        self.geo_edit_toolbar = QtWidgets.QToolBar('Geometry Editor Toolbar')
        self.geo_edit_toolbar.setObjectName('GeoEditor_TB')
        self.addToolBar(self.geo_edit_toolbar)

        self.snap_toolbar = QtWidgets.QToolBar('Grid Toolbar')
        self.snap_toolbar.setObjectName('Snap_TB')

        settings = QSettings("Open Source", "FlatCAM")
        if settings.contains("theme"):
            theme = settings.value('theme', type=str)
            if theme == 'standard':
                self.addToolBar(self.snap_toolbar)
            elif theme == 'compact':
                self.snap_toolbar.setMaximumHeight(30)
                self.splitter_left.addWidget(self.snap_toolbar)
        else:
            self.addToolBar(self.snap_toolbar)

        ### File Toolbar ###
        self.file_open_gerber_btn = self.toolbarfile.addAction(QtGui.QIcon('share/flatcam_icon32.png'),
                                                               "Open GERBER")
        self.file_open_excellon_btn = self.toolbarfile.addAction(QtGui.QIcon('share/drill32.png'), "Open EXCELLON")
        self.toolbarfile.addSeparator()
        self.file_open_btn = self.toolbarfile.addAction(QtGui.QIcon('share/folder32.png'), "Open project")
        self.file_save_btn = self.toolbarfile.addAction(QtGui.QIcon('share/floppy32.png'), "Save project")

        ### Edit Toolbar ###
        self.newgeo_btn = self.toolbargeo.addAction(QtGui.QIcon('share/new_geo32_bis.png'), "New Blank Geometry")
        self.newexc_btn = self.toolbargeo.addAction(QtGui.QIcon('share/new_exc32.png'), "New Blank Excellon")
        self.toolbargeo.addSeparator()
        self.editgeo_btn = self.toolbargeo.addAction(QtGui.QIcon('share/edit32.png'), "Editor")
        self.update_obj_btn = self.toolbargeo.addAction(
            QtGui.QIcon('share/edit_ok32_bis.png'), "Save Object and close the Editor"
        )

        self.toolbargeo.addSeparator()
        self.delete_btn = self.toolbargeo.addAction(QtGui.QIcon('share/cancel_edit32.png'), "&Delete")

        ### View Toolbar ###
        self.replot_btn = self.toolbarview.addAction(QtGui.QIcon('share/replot32.png'), "&Replot")
        self.clear_plot_btn = self.toolbarview.addAction(QtGui.QIcon('share/clear_plot32.png'), "&Clear plot")
        self.zoom_in_btn = self.toolbarview.addAction(QtGui.QIcon('share/zoom_in32.png'), "Zoom In")
        self.zoom_out_btn = self.toolbarview.addAction(QtGui.QIcon('share/zoom_out32.png'), "Zoom Out")
        self.zoom_fit_btn = self.toolbarview.addAction(QtGui.QIcon('share/zoom_fit32.png'), "Zoom Fit")

        # self.toolbarview.setVisible(False)

        ### Tools Toolbar ###
        self.shell_btn = self.toolbartools.addAction(QtGui.QIcon('share/shell32.png'), "&Command Line")

        ### Drill Editor Toolbar ###
        self.select_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/pointer32.png'), "Select 'Esc'")
        self.add_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/plus16.png'), 'Add Drill Hole')
        self.add_drill_array_btn = self.exc_edit_toolbar.addAction(
            QtGui.QIcon('share/addarray16.png'), 'Add Drill Hole Array')
        self.resize_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/resize16.png'), 'Resize Drill')
        self.exc_edit_toolbar.addSeparator()

        self.copy_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/copy32.png'), 'Copy Drill')
        self.delete_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/deleteshape32.png'), "Delete Drill")

        self.exc_edit_toolbar.addSeparator()
        self.move_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/move32.png'), "Move Drill")

        ### Geometry Editor Toolbar ###
        self.geo_select_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/pointer32.png'), "Select 'Esc'")
        self.geo_add_circle_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/circle32.png'), 'Add Circle')
        self.geo_add_arc_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/arc32.png'), 'Add Arc')
        self.geo_add_rectangle_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/rectangle32.png'),
                                                                     'Add Rectangle')

        self.geo_edit_toolbar.addSeparator()
        self.geo_add_path_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/path32.png'), 'Add Path')
        self.geo_add_polygon_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/polygon32.png'), 'Add Polygon')
        self.geo_edit_toolbar.addSeparator()
        self.geo_add_text_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/text32.png'), 'Add Text')
        self.geo_add_buffer_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/buffer16-2.png'), 'Add Buffer')
        self.geo_add_paint_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/paint20_1.png'), 'Paint Shape')

        self.geo_edit_toolbar.addSeparator()
        self.geo_union_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/union32.png'), 'Polygon Union')
        self.geo_intersection_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/intersection32.png'),
                                                                    'Polygon Intersection')
        self.geo_subtract_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/subtract32.png'),
                                                                'Polygon Subtraction')

        self.geo_edit_toolbar.addSeparator()
        self.geo_cutpath_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/cutpath32.png'), 'Cut Path')
        self.geo_copy_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/copy32.png'), "Copy Objects 'c'")
        self.geo_rotate_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/rotate.png'), "Rotate Objects 'Space'")
        self.geo_delete_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/deleteshape32.png'),
                                                              "Delete Shape '-'")

        self.geo_edit_toolbar.addSeparator()
        self.geo_move_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/move32.png'), "Move Objects 'm'")

        ### Snap Toolbar ###
        # Snap GRID toolbar is always active to facilitate usage of measurements done on GRID
        # self.addToolBar(self.snap_toolbar)

        self.grid_snap_btn = self.snap_toolbar.addAction(QtGui.QIcon('share/grid32.png'), 'Snap to grid')
        self.grid_gap_x_entry = FCEntry2()
        self.grid_gap_x_entry.setMaximumWidth(70)
        self.grid_gap_x_entry.setToolTip("Grid X distance")
        self.snap_toolbar.addWidget(self.grid_gap_x_entry)

        self.grid_gap_y_entry = FCEntry2()
        self.grid_gap_y_entry.setMaximumWidth(70)
        self.grid_gap_y_entry.setToolTip("Grid Y distance")
        self.snap_toolbar.addWidget(self.grid_gap_y_entry)

        self.grid_space_label = QtWidgets.QLabel("  ")
        self.snap_toolbar.addWidget(self.grid_space_label)
        self.grid_gap_link_cb = FCCheckBox()
        self.grid_gap_link_cb.setToolTip("When active, value on Grid_X\n"
                                         "is copied to the Grid_Y value.")
        self.snap_toolbar.addWidget(self.grid_gap_link_cb)

        self.ois_grid = OptionalInputSection(self.grid_gap_link_cb, [self.grid_gap_y_entry], logic=False)

        self.corner_snap_btn = self.snap_toolbar.addAction(QtGui.QIcon('share/corner32.png'), 'Snap to corner')

        self.snap_max_dist_entry = FCEntry()
        self.snap_max_dist_entry.setMaximumWidth(70)
        self.snap_max_dist_entry.setToolTip("Max. magnet distance")
        self.snap_magnet = self.snap_toolbar.addWidget(self.snap_max_dist_entry)


        ################
        ### Notebook ###
        ################

        ### Project ###
        self.project_tab = QtWidgets.QWidget()
        # project_tab.setMinimumWidth(250)  # Hack
        self.project_tab_layout = QtWidgets.QVBoxLayout(self.project_tab)
        self.project_tab_layout.setContentsMargins(2, 2, 2, 2)
        self.notebook.addTab(self.project_tab, "Project")

        ### Selected ###
        self.selected_tab = QtWidgets.QWidget()
        self.selected_tab_layout = QtWidgets.QVBoxLayout(self.selected_tab)
        self.selected_tab_layout.setContentsMargins(2, 2, 2, 2)
        self.selected_scroll_area = VerticalScrollArea()
        self.selected_tab_layout.addWidget(self.selected_scroll_area)
        self.notebook.addTab(self.selected_tab, "Selected")

        ### Tool ###
        self.tool_tab = QtWidgets.QWidget()
        self.tool_tab_layout = QtWidgets.QVBoxLayout(self.tool_tab)
        self.tool_tab_layout.setContentsMargins(2, 2, 2, 2)
        self.notebook.addTab(self.tool_tab, "Tool")
        self.tool_scroll_area = VerticalScrollArea()
        self.tool_tab_layout.addWidget(self.tool_scroll_area)

        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.splitter.addWidget(self.right_widget)

        self.right_lay = QtWidgets.QVBoxLayout()
        self.right_lay.setContentsMargins(0, 0, 0, 0)
        self.right_widget.setLayout(self.right_lay)
        # self.plot_tab_area = FCTab()
        self.plot_tab_area = FCDetachableTab(protect=False, protect_by_name=['Plot Area'])
        self.plot_tab_area.useOldIndex(True)

        self.right_lay.addWidget(self.plot_tab_area)
        self.plot_tab_area.setTabsClosable(True)

        self.plot_tab = QtWidgets.QWidget()
        self.plot_tab.setObjectName("plotarea")
        self.plot_tab_area.addTab(self.plot_tab, "Plot Area")

        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.setContentsMargins(2, 2, 2, 2)
        self.plot_tab.setLayout(self.right_layout)

        # remove the close button from the Plot Area tab (first tab index = 0) as this one will always be ON
        self.plot_tab_area.protectTab(0)

        ########################################
        ### HERE WE BUILD THE PREF. TAB AREA ###
        ########################################
        self.preferences_tab = QtWidgets.QWidget()
        self.pref_tab_layout = QtWidgets.QVBoxLayout(self.preferences_tab)
        self.pref_tab_layout.setContentsMargins(2, 2, 2, 2)

        self.pref_tab_area = FCTab()
        self.pref_tab_area.setTabsClosable(False)
        self.pref_tab_area_tabBar = self.pref_tab_area.tabBar()
        self.pref_tab_area_tabBar.setStyleSheet("QTabBar::tab{width:80px;}")
        self.pref_tab_area_tabBar.setExpanding(True)
        self.pref_tab_layout.addWidget(self.pref_tab_area)

        self.general_tab = QtWidgets.QWidget()
        self.pref_tab_area.addTab(self.general_tab, "General")
        self.general_tab_lay = QtWidgets.QVBoxLayout()
        self.general_tab_lay.setContentsMargins(2, 2, 2, 2)
        self.general_tab.setLayout(self.general_tab_lay)

        self.hlay1 = QtWidgets.QHBoxLayout()
        self.general_tab_lay.addLayout(self.hlay1)

        self.options_combo = QtWidgets.QComboBox()
        self.options_combo.addItem("APP.  DEFAULTS")
        self.options_combo.addItem("PROJ. OPTIONS ")
        self.hlay1.addWidget(self.options_combo)

        # disable this button as it may no longer be useful
        self.options_combo.setVisible(False)
        self.hlay1.addStretch()

        self.general_scroll_area = VerticalScrollArea()
        self.general_tab_lay.addWidget(self.general_scroll_area)

        self.gerber_tab = QtWidgets.QWidget()
        self.pref_tab_area.addTab(self.gerber_tab, "GERBER")
        self.gerber_tab_lay = QtWidgets.QVBoxLayout()
        self.gerber_tab_lay.setContentsMargins(2, 2, 2, 2)
        self.gerber_tab.setLayout(self.gerber_tab_lay)

        self.gerber_scroll_area = VerticalScrollArea()
        self.gerber_tab_lay.addWidget(self.gerber_scroll_area)

        self.excellon_tab = QtWidgets.QWidget()
        self.pref_tab_area.addTab(self.excellon_tab, "EXCELLON")
        self.excellon_tab_lay = QtWidgets.QVBoxLayout()
        self.excellon_tab_lay.setContentsMargins(2, 2, 2, 2)
        self.excellon_tab.setLayout(self.excellon_tab_lay)

        self.excellon_scroll_area = VerticalScrollArea()
        self.excellon_tab_lay.addWidget(self.excellon_scroll_area)

        self.geometry_tab = QtWidgets.QWidget()
        self.pref_tab_area.addTab(self.geometry_tab, "GEOMETRY")
        self.geometry_tab_lay = QtWidgets.QVBoxLayout()
        self.geometry_tab_lay.setContentsMargins(2, 2, 2, 2)
        self.geometry_tab.setLayout(self.geometry_tab_lay)

        self.geometry_scroll_area = VerticalScrollArea()
        self.geometry_tab_lay.addWidget(self.geometry_scroll_area)

        self.cncjob_tab = QtWidgets.QWidget()
        self.pref_tab_area.addTab(self.cncjob_tab, "CNC-JOB")
        self.cncjob_tab_lay = QtWidgets.QVBoxLayout()
        self.cncjob_tab_lay.setContentsMargins(2, 2, 2, 2)
        self.cncjob_tab.setLayout(self.cncjob_tab_lay)

        self.cncjob_scroll_area = VerticalScrollArea()
        self.cncjob_tab_lay.addWidget(self.cncjob_scroll_area)

        self.tools_tab = QtWidgets.QWidget()
        self.pref_tab_area.addTab(self.tools_tab, "TOOLS")
        self.tools_tab_lay = QtWidgets.QVBoxLayout()
        self.tools_tab_lay.setContentsMargins(2, 2, 2, 2)
        self.tools_tab.setLayout(self.tools_tab_lay)

        self.tools_scroll_area = VerticalScrollArea()
        self.tools_tab_lay.addWidget(self.tools_scroll_area)

        self.pref_tab_bottom_layout = QtWidgets.QHBoxLayout()
        self.pref_tab_bottom_layout.setAlignment(QtCore.Qt.AlignVCenter)
        self.pref_tab_layout.addLayout(self.pref_tab_bottom_layout)

        self.pref_tab_bottom_layout_1 = QtWidgets.QHBoxLayout()
        self.pref_tab_bottom_layout_1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.pref_tab_bottom_layout.addLayout(self.pref_tab_bottom_layout_1)

        self.pref_import_button = QtWidgets.QPushButton()
        self.pref_import_button.setText("Import Preferences")
        self.pref_import_button.setFixedWidth(130)
        self.pref_import_button.setToolTip(
            "Import a full set of FlatCAM settings from a file\n"
            "previously saved on HDD.\n\n"
            "FlatCAM automatically save a 'factory_defaults' file\n"
            "on the first start. Do not delete that file.")
        self.pref_tab_bottom_layout_1.addWidget(self.pref_import_button)

        self.pref_export_button = QtWidgets.QPushButton()
        self.pref_export_button.setText("Export Preferences")
        self.pref_export_button.setFixedWidth(130)
        self.pref_export_button.setToolTip(
            "Export a full set of FlatCAM settings in a file\n"
            "that is saved on HDD.")
        self.pref_tab_bottom_layout_1.addWidget(self.pref_export_button)

        self.pref_open_button = QtWidgets.QPushButton()
        self.pref_open_button.setText("Open Pref Folder")
        self.pref_open_button.setFixedWidth(130)
        self.pref_open_button.setToolTip(
            "Open the folder where FlatCAM save the preferences files.")
        self.pref_tab_bottom_layout_1.addWidget(self.pref_open_button)

        self.pref_tab_bottom_layout_2 = QtWidgets.QHBoxLayout()
        self.pref_tab_bottom_layout_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.pref_tab_bottom_layout.addLayout(self.pref_tab_bottom_layout_2)

        self.pref_save_button = QtWidgets.QPushButton()
        self.pref_save_button.setText("Save Preferences")
        self.pref_save_button.setFixedWidth(130)
        self.pref_save_button.setToolTip(
            "Save the current settings in the 'current_defaults' file\n"
            "which is the file storing the working default preferences.")
        self.pref_tab_bottom_layout_2.addWidget(self.pref_save_button)

        ########################################
        ### HERE WE BUILD THE SHORTCUTS LIST. TAB AREA ###
        ########################################
        self.shortcuts_tab = QtWidgets.QWidget()
        self.sh_tab_layout = QtWidgets.QVBoxLayout()
        self.sh_tab_layout.setContentsMargins(2, 2, 2, 2)
        self.shortcuts_tab.setLayout(self.sh_tab_layout)

        self.sh_hlay = QtWidgets.QHBoxLayout()
        self.sh_title = QtWidgets.QTextEdit(
            '<b>Shortcut Key List</b>')
        self.sh_title.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.sh_title.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.sh_title.setMaximumHeight(30)
        font = self.sh_title.font()
        font.setPointSize(12)
        self.sh_title.setFont(font)

        self.sh_tab_layout.addWidget(self.sh_title)
        self.sh_tab_layout.addLayout(self.sh_hlay)

        self.app_sh_msg = '''<b>General Shortcut list</b><br>
<table border="0" cellpadding="0" cellspacing="0" style="width:283px">
	<tbody>
		<tr height="20">
			<td height="20" width="89"><strong>~</strong></td>
			<td width="194"><span style="color:#006400"><strong>&nbsp;SHOW SHORTCUT LIST</strong></span></td>
		</tr>
		<tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>1</strong></td>
			<td>&nbsp;Switch to Project Tab</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>2</strong></td>
			<td>&nbsp;Switch to Selected Tab</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>3</strong></td>
			<td>&nbsp;Switch to Tool Tab</td>
		</tr>
        <tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>E</strong></td>
			<td>&nbsp;Edit Object (if selected)</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>G</strong></td>
			<td>&nbsp;Grid On/Off</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>J</strong></td>
			<td>&nbsp;Jump to Coordinates</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>L</strong></td>
			<td>&nbsp;New Excellon</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>M</strong></td>
			<td>&nbsp;Move Obj</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>N</strong></td>
			<td>&nbsp;New Geometry</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>O</strong></td>
			<td>&nbsp;Set Origin</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>Q</strong></td>
			<td>&nbsp;Change Units</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>P</strong></td>
			<td>&nbsp;Open Properties Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>R</strong></td>
			<td>&nbsp;Rotate by 90 degree CW</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>S</strong></td>
			<td>&nbsp;Shell Toggle</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>V</strong></td>
			<td>&nbsp;Zoom Fit</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>X</strong></td>
			<td>&nbsp;Flip on X_axis</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>Y</strong></td>
			<td>&nbsp;Flip on Y_axis</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>&#39;=&#39;</strong></td>
			<td>&nbsp;Zoom Out</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>&#39;-&#39;</strong></td>
			<td>&nbsp;Zoom In</td>
		</tr>
		<tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+A</strong></td>
			<td>&nbsp;Select All</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+C</strong></td>
			<td>&nbsp;Copy Obj</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+E</strong></td>
			<td>&nbsp;Open Excellon File</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+G</strong></td>
			<td>&nbsp;Open Gerber File</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+N</strong></td>
			<td>&nbsp;New Project</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+M</strong></td>
			<td>&nbsp;Measurement Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+O</strong></td>
			<td>&nbsp;Open Project</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+S</strong></td>
			<td>&nbsp;Save Project As</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+F10</strong></td>
			<td>&nbsp;Toggle Plot Area</td>
		</tr>
		<tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>SHIFT+C</strong></td>
			<td>&nbsp;Copy Obj_Name</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>SHIFT+G</strong></td>
			<td>&nbsp;Toggle the axis</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>SHIFT+P</strong></td>
			<td>&nbsp;Open Preferences Window</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>SHIFT+R</strong></td>
			<td>&nbsp;Rotate by 90 degree CCW</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>SHIFT+S</strong></td>
			<td>&nbsp;Run a Script</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>SHIFT+W</strong></td>
			<td>&nbsp;Toggle the workspace</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>SHIFT+X</strong></td>
			<td>&nbsp;Skew on X axis</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>SHIFT+Y</strong></td>
			<td>&nbsp;Skew on Y axis</td>
		</tr>
		<tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+C</strong></td>
			<td>&nbsp;Calculators Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+D</strong></td>
			<td>&nbsp;2-Sided PCB Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+L</strong></td>
			<td>&nbsp;Film PCB Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+N</strong></td>
			<td>&nbsp;Non-Copper Clearing Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+P</strong></td>
			<td>&nbsp;Paint Area Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+R</strong></td>
			<td>&nbsp;Transformation Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+U</strong></td>
			<td>&nbsp;Cutout PCB Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+1</strong></td>
			<td>&nbsp;Enable all Plots</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+2</strong></td>
			<td>&nbsp;Disable all Plots</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+3</strong></td>
			<td>&nbsp;Disable Non-selected Plots</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ALT+F10</strong></td>
			<td>&nbsp;Toggle Full Screen</td>
		</tr>
		<tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>F1</strong></td>
			<td>&nbsp;Open Online Manual</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>F2</strong></td>
			<td>&nbsp;Open Online Tutorials</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>Del</strong></td>
			<td>&nbsp;Delete Obj</td>
		</tr>
        <tr height="20">
			<td height="20"><strong>SPACE</strong></td>
			<td>&nbsp;En(Dis)able Obj Plot</td>
		</tr>
	</tbody>
</table>

'''

        self.sh_app = QtWidgets.QTextEdit()
        self.sh_app.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        self.sh_app.setText(self.app_sh_msg)
        self.sh_app.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.sh_hlay.addWidget(self.sh_app)

        self.editor_sh_msg = '''<b>Editor Shortcut list</b><br>
<br>
<strong><span style="color:#0000ff">GEOMETRY EDITOR</span></strong><br>

<table border="0" cellpadding="0" cellspacing="0" style="width:283px">
	<tbody>
		<tr height="20">
			<td height="20" width="89"><strong>A</strong></td>
			<td width="194">&nbsp;Draw an Arc</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>B</strong></td>
			<td>&nbsp;Buffer Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>C</strong></td>
			<td>&nbsp;Copy Geo Item</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>E</strong></td>
			<td>&nbsp;Polygon Intersection Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>I</strong></td>
			<td>&nbsp;Paint Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>K</strong></td>
			<td>&nbsp;Toggle Corner Snap</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>M</strong></td>
			<td>&nbsp;Move Geo Item</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>N</strong></td>
			<td>&nbsp;Draw a Polygon</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>O</strong></td>
			<td>&nbsp;Draw a Circle</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>P</strong></td>
			<td>&nbsp;Draw a Path</td>
		</tr>
		<tr height="20">
			<td height="20">R</td>
			<td>&nbsp;Draw Rectangle</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>S</strong></td>
			<td>&nbsp;Polygon Substraction Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>T</strong></td>
			<td>&nbsp;Add Text Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>U</strong></td>
			<td>&nbsp;Polygon Union Tool</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>X</strong></td>
			<td>&nbsp;Polygon Cut Tool</td>
		</tr>
		<tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+S</strong></td>
			<td>&nbsp;Save Object and Exit Editor</td>
		</tr>
		<tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>Space</strong></td>
			<td>&nbsp;Rotate Geometry</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ENTER</strong></td>
			<td>&nbsp;Finish drawing for certain tools</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ESC</strong></td>
			<td>&nbsp;Abort and return to Select</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>Del</strong></td>
			<td>&nbsp;Delete Shape</td>
		</tr>
	</tbody>
</table>
<br>
<br>
<strong><span style="color:#ff0000">EXCELLON EDITOR</span></strong><br>
<table border="0" cellpadding="0" cellspacing="0" style="width:283px">
	<tbody>
		<tr height="20">
			<td height="20" width="89"><strong>A</strong></td>
			<td width="194">&nbsp;Add Drill Array</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>C</strong></td>
			<td>&nbsp;Copy Drill(s)</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>D</strong></td>
			<td>&nbsp;Add Drill</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>M</strong></td>
			<td>&nbsp;Move Drill(s)</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>R</strong></td>
			<td>&nbsp;Resize Drill(s)</td>
		</tr>
		<tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>Del</strong></td>
			<td>&nbsp;Delete Drill(s)</td>
		</tr>
		<tr height="20">
			<td height="20">&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>ESC</strong></td>
			<td>&nbsp;Abort and return to Select</td>
		</tr>
		<tr height="20">
			<td height="20"><strong>CTRL+S</strong></td>
			<td>&nbsp;Save Object and Exit Editor</td>
		</tr>
	</tbody>
</table>
        '''
        self.sh_editor = QtWidgets.QTextEdit()
        self.sh_editor.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.sh_editor.setText(self.editor_sh_msg)
        self.sh_editor.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.sh_hlay.addWidget(self.sh_editor)


        ##############################################################
        ### HERE WE BUILD THE CONTEXT MENU FOR RMB CLICK ON CANVAS ###
        ##############################################################
        self.popMenu = QtWidgets.QMenu()

        self.cmenu_newmenu = self.popMenu.addMenu(QtGui.QIcon('share/file32.png'), "New")
        self.popmenu_new_geo = self.cmenu_newmenu.addAction(QtGui.QIcon('share/new_geo32_bis.png'), "Geo Obj")
        self.popmenu_new_exc = self.cmenu_newmenu.addAction(QtGui.QIcon('share/new_exc32.png'), "Exc. Obj")
        self.cmenu_newmenu.addSeparator()
        self.popmenu_new_prj = self.cmenu_newmenu.addAction(QtGui.QIcon('share/file16.png'), "Project")
        self.popMenu.addSeparator()

        self.cmenu_gridmenu = self.popMenu.addMenu(QtGui.QIcon('share/grid32_menu.png'), "Grids")
        self.gridmenu_1 = self.cmenu_gridmenu.addAction(QtGui.QIcon('share/grid32_menu.png'), "0.05")
        self.gridmenu_2 = self.cmenu_gridmenu.addAction(QtGui.QIcon('share/grid32_menu.png'), "0.10")
        self.gridmenu_3 = self.cmenu_gridmenu.addAction(QtGui.QIcon('share/grid32_menu.png'), "0.20")
        self.gridmenu_4 = self.cmenu_gridmenu.addAction(QtGui.QIcon('share/grid32_menu.png'), "0.50")
        self.gridmenu_5 = self.cmenu_gridmenu.addAction(QtGui.QIcon('share/grid32_menu.png'), "1.00")

        self.cmenu_viewmenu = self.popMenu.addMenu(QtGui.QIcon('share/view64.png'), "View")
        self.zoomfit = self.cmenu_viewmenu.addAction(QtGui.QIcon('share/zoom_fit32.png'), "Zoom Fit")
        self.clearplot = self.cmenu_viewmenu.addAction(QtGui.QIcon('share/clear_plot32.png'), "Clear Plot")
        self.replot = self.cmenu_viewmenu.addAction(QtGui.QIcon('share/replot32.png'), "Replot")
        self.popMenu.addSeparator()

        self.g_editor_cmenu = self.popMenu.addMenu(QtGui.QIcon('share/draw32.png'), "Geo Editor")
        self.draw_line = self.g_editor_cmenu.addAction(QtGui.QIcon('share/path32.png'), "Line")
        self.draw_rect = self.g_editor_cmenu.addAction(QtGui.QIcon('share/rectangle32.png'), "Rectangle")
        self.draw_cut = self.g_editor_cmenu.addAction(QtGui.QIcon('share/cutpath32.png'), "Cut")
        self.g_editor_cmenu.addSeparator()
        self.draw_move = self.g_editor_cmenu.addAction(QtGui.QIcon('share/move32.png'), "Move")

        self.e_editor_cmenu = self.popMenu.addMenu(QtGui.QIcon('share/drill32.png'), "Exc Editor")
        self.drill = self.e_editor_cmenu.addAction(QtGui.QIcon('share/drill32.png'), "Add Drill")
        self.drill_array = self.e_editor_cmenu.addAction(QtGui.QIcon('share/addarray32.png'), "Add Drill Array")
        self.drill_copy = self.e_editor_cmenu.addAction(QtGui.QIcon('share/copy32.png'), "Copy Drill(s)")

        self.popMenu.addSeparator()
        self.popmenu_copy = self.popMenu.addAction(QtGui.QIcon('share/copy32.png'), "Copy")
        self.popmenu_delete = self.popMenu.addAction(QtGui.QIcon('share/delete32.png'), "Delete")
        self.popmenu_edit = self.popMenu.addAction(QtGui.QIcon('share/edit32.png'), "Edit")
        self.popmenu_save = self.popMenu.addAction(QtGui.QIcon('share/floppy32.png'), "Save && Close Edit")
        self.popmenu_save.setVisible(False)
        self.popMenu.addSeparator()

        self.popmenu_move = self.popMenu.addAction(QtGui.QIcon('share/move32.png'), "Move")
        self.popmenu_properties = self.popMenu.addAction(QtGui.QIcon('share/properties32.png'), "Properties")


        ####################################
        ### Here we build the CNCJob Tab ###
        ####################################
        self.cncjob_tab = QtWidgets.QWidget()
        self.cncjob_tab_layout = QtWidgets.QGridLayout(self.cncjob_tab)
        self.cncjob_tab_layout.setContentsMargins(2, 2, 2, 2)
        self.cncjob_tab.setLayout(self.cncjob_tab_layout)

        self.code_editor = QtWidgets.QTextEdit()
        stylesheet = """
                        QTextEdit { selection-background-color:yellow;
                                    selection-color:black;
                        }
                     """

        self.code_editor.setStyleSheet(stylesheet)

        self.buttonPreview = QtWidgets.QPushButton('Print Preview')
        self.buttonPrint = QtWidgets.QPushButton('Print CNC Code')
        self.buttonFind = QtWidgets.QPushButton('Find in CNC Code')
        self.buttonFind.setFixedWidth(100)
        self.buttonPreview.setFixedWidth(100)
        self.entryFind = FCEntry()
        self.entryFind.setMaximumWidth(200)
        self.buttonReplace = QtWidgets.QPushButton('Replace With')
        self.buttonReplace.setFixedWidth(100)
        self.entryReplace = FCEntry()
        self.entryReplace.setMaximumWidth(200)
        self.sel_all_cb = QtWidgets.QCheckBox('All')
        self.sel_all_cb.setToolTip(
            "When checked it will replace all instances in the 'Find' box\n"
            "with the text in the 'Replace' box.."
        )
        self.buttonOpen = QtWidgets.QPushButton('Open CNC Code')
        self.buttonSave = QtWidgets.QPushButton('Save CNC Code')

        self.cncjob_tab_layout.addWidget(self.code_editor, 0, 0, 1, 5)

        cnc_tab_lay_1 = QtWidgets.QHBoxLayout()
        cnc_tab_lay_1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        cnc_tab_lay_1.addWidget(self.buttonFind)
        cnc_tab_lay_1.addWidget(self.entryFind)
        cnc_tab_lay_1.addWidget(self.buttonReplace)
        cnc_tab_lay_1.addWidget(self.entryReplace)
        cnc_tab_lay_1.addWidget(self.sel_all_cb)
        self.cncjob_tab_layout.addLayout(cnc_tab_lay_1, 1, 0, 1, 1, QtCore.Qt.AlignLeft)

        cnc_tab_lay_3 = QtWidgets.QHBoxLayout()
        cnc_tab_lay_3.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        cnc_tab_lay_3.addWidget(self.buttonPreview)
        cnc_tab_lay_3.addWidget(self.buttonPrint)
        self.cncjob_tab_layout.addLayout(cnc_tab_lay_3, 2, 0, 1, 1, QtCore.Qt.AlignLeft)

        cnc_tab_lay_4 = QtWidgets.QHBoxLayout()
        cnc_tab_lay_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        cnc_tab_lay_4.addWidget(self.buttonOpen)
        cnc_tab_lay_4.addWidget(self.buttonSave)
        self.cncjob_tab_layout.addLayout(cnc_tab_lay_4, 2, 4, 1, 1)

        ##################################
        ### Build InfoBar is done here ###
        ##################################
        self.infobar = self.statusBar()
        self.fcinfo = FlatCAMInfoBar()
        self.infobar.addWidget(self.fcinfo, stretch=1)

        self.rel_position_label = QtWidgets.QLabel(
            "<b>Dx</b>: 0.0000&nbsp;&nbsp;   <b>Dy</b>: 0.0000&nbsp;&nbsp;&nbsp;&nbsp;")
        self.rel_position_label.setMinimumWidth(110)
        self.rel_position_label.setToolTip("Relative neasurement.\nReference is last click position")
        self.infobar.addWidget(self.rel_position_label)

        self.position_label = QtWidgets.QLabel(
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>X</b>: 0.0000&nbsp;&nbsp;   <b>Y</b>: 0.0000")
        self.position_label.setMinimumWidth(110)
        self.position_label.setToolTip("Absolute neasurement.\nReference is (X=0, Y= 0) position")
        self.infobar.addWidget(self.position_label)

        self.units_label = QtWidgets.QLabel("[in]")
        self.units_label.setMargin(2)
        self.infobar.addWidget(self.units_label)

        # disabled
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        # infobar.addWidget(self.progress_bar)

        self.activity_view = FlatCAMActivityView()
        self.infobar.addWidget(self.activity_view)

        self.app_icon = QtGui.QIcon()
        self.app_icon.addFile('share/flatcam_icon16.png', QtCore.QSize(16, 16))
        self.app_icon.addFile('share/flatcam_icon24.png', QtCore.QSize(24, 24))
        self.app_icon.addFile('share/flatcam_icon32.png', QtCore.QSize(32, 32))
        self.app_icon.addFile('share/flatcam_icon48.png', QtCore.QSize(48, 48))
        self.app_icon.addFile('share/flatcam_icon128.png', QtCore.QSize(128, 128))
        self.app_icon.addFile('share/flatcam_icon256.png', QtCore.QSize(256, 256))
        self.setWindowIcon(self.app_icon)

        self.setGeometry(100, 100, 1024, 650)
        self.setWindowTitle('FlatCAM %s %s - %s' % (version, ('BETA' if beta else ''), platform.architecture()[0]))
        self.show()

        self.filename = ""
        self.setAcceptDrops(True)

        # # restore the Toolbar State from file
        # try:
        #     with open(self.app.data_path + '\gui_state.config', 'rb') as stream:
        #         self.restoreState(QtCore.QByteArray(stream.read()))
        #     log.debug("FlatCAMGUI.__init__() --> UI state restored.")
        # except IOError:
        #     log.debug("FlatCAMGUI.__init__() --> UI state not restored. IOError")
        #     pass

        ######################
        ### INITIALIZE GUI ###
        ######################

        self.grid_snap_btn.setCheckable(True)
        self.corner_snap_btn.setCheckable(True)
        self.update_obj_btn.setEnabled(False)
        # start with GRID activated
        self.grid_snap_btn.trigger()

        self.g_editor_cmenu.setEnabled(False)
        self.e_editor_cmenu.setEnabled(False)

        # restore the Toolbar State from file
        settings = QSettings("Open Source", "FlatCAM")
        if settings.contains("saved_gui_state"):
            saved_gui_state = settings.value('saved_gui_state')
            self.restoreState(saved_gui_state)
            log.debug("FlatCAMGUI.__init__() --> UI state restored.")

        if settings.contains("theme"):
            theme = settings.value('theme', type=str)
            if theme == 'standard':
                self.exc_edit_toolbar.setVisible(False)
                self.exc_edit_toolbar.setDisabled(True)
                self.geo_edit_toolbar.setVisible(False)
                self.geo_edit_toolbar.setDisabled(True)

                self.corner_snap_btn.setVisible(False)
                self.snap_magnet.setVisible(False)
            elif theme == 'compact':
                self.exc_edit_toolbar.setDisabled(True)
                self.geo_edit_toolbar.setDisabled(True)
                self.snap_magnet.setVisible(True)
                self.corner_snap_btn.setVisible(True)
                self.snap_magnet.setDisabled(True)
                self.corner_snap_btn.setDisabled(True)
        else:
            self.exc_edit_toolbar.setVisible(False)
            self.exc_edit_toolbar.setDisabled(True)
            self.geo_edit_toolbar.setVisible(False)
            self.geo_edit_toolbar.setDisabled(True)

            self.corner_snap_btn.setVisible(False)
            self.snap_magnet.setVisible(False)

    def populate_toolbars(self):

        ### File Toolbar ###
        self.file_open_gerber_btn = self.toolbarfile.addAction(QtGui.QIcon('share/flatcam_icon32.png'),
                                                               "Open GERBER")
        self.file_open_excellon_btn = self.toolbarfile.addAction(QtGui.QIcon('share/drill32.png'), "Open EXCELLON")
        self.toolbarfile.addSeparator()
        self.file_open_btn = self.toolbarfile.addAction(QtGui.QIcon('share/folder32.png'), "Open project")
        self.file_save_btn = self.toolbarfile.addAction(QtGui.QIcon('share/floppy32.png'), "Save project")

        ### Edit Toolbar ###
        self.newgeo_btn = self.toolbargeo.addAction(QtGui.QIcon('share/new_geo32_bis.png'), "New Blank Geometry")
        self.newexc_btn = self.toolbargeo.addAction(QtGui.QIcon('share/new_exc32.png'), "New Blank Excellon")
        self.toolbargeo.addSeparator()
        self.editgeo_btn = self.toolbargeo.addAction(QtGui.QIcon('share/edit32.png'), "Editor")
        self.update_obj_btn = self.toolbargeo.addAction(
            QtGui.QIcon('share/edit_ok32_bis.png'), "Save Object and close the Editor"
        )

        self.toolbargeo.addSeparator()
        self.delete_btn = self.toolbargeo.addAction(QtGui.QIcon('share/cancel_edit32.png'), "&Delete")

        ### View Toolbar ###
        self.replot_btn = self.toolbarview.addAction(QtGui.QIcon('share/replot32.png'), "&Replot")
        self.clear_plot_btn = self.toolbarview.addAction(QtGui.QIcon('share/clear_plot32.png'), "&Clear plot")
        self.zoom_in_btn = self.toolbarview.addAction(QtGui.QIcon('share/zoom_in32.png'), "Zoom In")
        self.zoom_out_btn = self.toolbarview.addAction(QtGui.QIcon('share/zoom_out32.png'), "Zoom Out")
        self.zoom_fit_btn = self.toolbarview.addAction(QtGui.QIcon('share/zoom_fit32.png'), "Zoom Fit")

        # self.toolbarview.setVisible(False)

        ### Tools Toolbar ###
        self.shell_btn = self.toolbartools.addAction(QtGui.QIcon('share/shell32.png'), "&Command Line")

        ### Drill Editor Toolbar ###
        self.select_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/pointer32.png'), "Select 'Esc'")
        self.add_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/plus16.png'), 'Add Drill Hole')
        self.add_drill_array_btn = self.exc_edit_toolbar.addAction(
            QtGui.QIcon('share/addarray16.png'), 'Add Drill Hole Array')
        self.resize_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/resize16.png'), 'Resize Drill')
        self.exc_edit_toolbar.addSeparator()

        self.copy_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/copy32.png'), 'Copy Drill')
        self.delete_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/deleteshape32.png'), "Delete Drill")

        self.exc_edit_toolbar.addSeparator()
        self.move_drill_btn = self.exc_edit_toolbar.addAction(QtGui.QIcon('share/move32.png'), "Move Drill")

        ### Geometry Editor Toolbar ###
        self.geo_select_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/pointer32.png'), "Select 'Esc'")
        self.geo_add_circle_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/circle32.png'), 'Add Circle')
        self.geo_add_arc_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/arc32.png'), 'Add Arc')
        self.geo_add_rectangle_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/rectangle32.png'), 'Add Rectangle')

        self.geo_edit_toolbar.addSeparator()
        self.geo_add_path_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/path32.png'), 'Add Path')
        self.geo_add_polygon_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/polygon32.png'), 'Add Polygon')
        self.geo_edit_toolbar.addSeparator()
        self.geo_add_text_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/text32.png'), 'Add Text')
        self.geo_add_buffer_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/buffer16-2.png'), 'Add Buffer')
        self.geo_add_paint_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/paint20_1.png'), 'Paint Shape')

        self.geo_edit_toolbar.addSeparator()
        self.geo_union_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/union32.png'), 'Polygon Union')
        self.geo_intersection_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/intersection32.png'),
                                                               'Polygon Intersection')
        self.geo_subtract_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/subtract32.png'), 'Polygon Subtraction')

        self.geo_edit_toolbar.addSeparator()
        self.geo_cutpath_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/cutpath32.png'), 'Cut Path')
        self.geo_copy_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/copy32.png'), "Copy Objects 'c'")
        self.geo_rotate_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/rotate.png'), "Rotate Objects 'Space'")
        self.geo_delete_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/deleteshape32.png'), "Delete Shape '-'")

        self.geo_edit_toolbar.addSeparator()
        self.geo_move_btn = self.geo_edit_toolbar.addAction(QtGui.QIcon('share/move32.png'), "Move Objects 'm'")

        ### Snap Toolbar ###
        # Snap GRID toolbar is always active to facilitate usage of measurements done on GRID
        # self.addToolBar(self.snap_toolbar)

        self.grid_snap_btn = self.snap_toolbar.addAction(QtGui.QIcon('share/grid32.png'), 'Snap to grid')
        self.grid_gap_x_entry = FCEntry2()
        self.grid_gap_x_entry.setMaximumWidth(70)
        self.grid_gap_x_entry.setToolTip("Grid X distance")
        self.snap_toolbar.addWidget(self.grid_gap_x_entry)

        self.grid_gap_y_entry = FCEntry2()
        self.grid_gap_y_entry.setMaximumWidth(70)
        self.grid_gap_y_entry.setToolTip("Grid Y distance")
        self.snap_toolbar.addWidget(self.grid_gap_y_entry)

        self.grid_space_label = QtWidgets.QLabel("  ")
        self.snap_toolbar.addWidget(self.grid_space_label)
        self.grid_gap_link_cb = FCCheckBox()
        self.grid_gap_link_cb.setToolTip("When active, value on Grid_X\n"
                                         "is copied to the Grid_Y value.")
        self.snap_toolbar.addWidget(self.grid_gap_link_cb)

        self.ois_grid = OptionalInputSection(self.grid_gap_link_cb, [self.grid_gap_y_entry], logic=False)

        self.corner_snap_btn = self.snap_toolbar.addAction(QtGui.QIcon('share/corner32.png'), 'Snap to corner')

        self.snap_max_dist_entry = FCEntry()
        self.snap_max_dist_entry.setMaximumWidth(70)
        self.snap_max_dist_entry.setToolTip("Max. magnet distance")
        self.snap_magnet = self.snap_toolbar.addWidget(self.snap_max_dist_entry)

        self.grid_snap_btn.setCheckable(True)
        self.corner_snap_btn.setCheckable(True)
        self.update_obj_btn.setEnabled(False)
        # start with GRID activated
        self.grid_snap_btn.trigger()

        settings = QSettings("Open Source", "FlatCAM")
        if settings.contains("theme"):
            theme = settings.value('theme', type=str)
            if theme == 'standard':
                self.exc_edit_toolbar.setVisible(False)
                self.exc_edit_toolbar.setDisabled(True)
                self.geo_edit_toolbar.setVisible(False)
                self.geo_edit_toolbar.setDisabled(True)

                self.corner_snap_btn.setVisible(False)
                self.snap_magnet.setVisible(False)
            elif theme == 'compact':
                self.exc_edit_toolbar.setVisible(True)
                self.exc_edit_toolbar.setDisabled(True)
                self.geo_edit_toolbar.setVisible(True)
                self.geo_edit_toolbar.setDisabled(True)

                self.corner_snap_btn.setVisible(True)
                self.snap_magnet.setVisible(True)
                self.corner_snap_btn.setDisabled(True)
                self.snap_magnet.setDisabled(True)

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_1:
            self.app.on_select_tab('project')

        if event.key() == QtCore.Qt.Key_2:
            self.app.on_select_tab('selected')

        if event.key() == QtCore.Qt.Key_3:
            self.app.on_select_tab('tool')

        if event.key == QtCore.Qt.Key_Q:
            self.app.on_toggle_units_click()

        if event.key() == QtCore.Qt.Key_S:
            self.app.on_toggle_shell()

        # Show shortcut list
        if event.key() == QtCore.Qt.Key_Ampersand:
            self.app.on_shortcut_list()

        if event.key() == QtCore.Qt.Key_QuoteLeft:
            self.app.on_shortcut_list()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                self.filename = str(url.toLocalFile())

                if self.filename == "":
                    self.app.inform.emit("Open cancelled.")
                else:
                    if self.filename.lower().rpartition('.')[-1] in self.app.grb_list:
                        self.app.worker_task.emit({'fcn': self.app.open_gerber,
                                                   'params': [self.filename]})
                    else:
                        event.ignore()

                    if self.filename.lower().rpartition('.')[-1] in self.app.exc_list:
                        self.app.worker_task.emit({'fcn': self.app.open_excellon,
                                                   'params': [self.filename]})
                    else:
                        event.ignore()

                    if self.filename.lower().rpartition('.')[-1] in self.app.gcode_list:
                        self.app.worker_task.emit({'fcn': self.app.open_gcode,
                                                   'params': [self.filename]})
                    else:
                        event.ignore()

                    if self.filename.lower().rpartition('.')[-1] in self.app.svg_list:
                        object_type = 'geometry'
                        self.app.worker_task.emit({'fcn': self.app.import_svg,
                                                   'params': [self.filename, object_type, None]})

                    if self.filename.lower().rpartition('.')[-1] in self.app.dxf_list:
                        object_type = 'geometry'
                        self.app.worker_task.emit({'fcn': self.app.import_dxf,
                                                   'params': [self.filename, object_type, None]})

                    if self.filename.lower().rpartition('.')[-1] in self.app.prj_list:
                        # self.app.open_project() is not Thread Safe
                        self.app.open_project(self.filename)
                    else:
                        event.ignore()
        else:
            event.ignore()

    def closeEvent(self, event):
        grect = self.geometry()

        # self.splitter.sizes()[0] is actually the size of the "notebook"
        self.geom_update.emit(grect.x(), grect.y(), grect.width(), grect.height(), self.splitter.sizes()[0])
        self.final_save.emit()

        if self.app.should_we_quit is True:
            # # save toolbar state to file
            # with open(self.app.data_path + '\gui_state.config', 'wb') as stream:
            #     stream.write(self.saveState().data())
            #     log.debug("FlatCAMGUI.__init__() --> UI state saved.")
            # QtWidgets.qApp.quit()

            # save toolbar state to file
            settings = QSettings("Open Source", "FlatCAM")
            settings.setValue('saved_gui_state', self.saveState())

            # This will write the setting to the platform specific storage.
            del settings
            log.debug("FlatCAMGUI.__init__() --> UI state saved.")
            QtWidgets.qApp.quit()
        else:
            self.app.should_we_quit = True
            event.ignore()


class GeneralPreferencesUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.general_app_group = GeneralAppPrefGroupUI()
        self.general_app_group.setFixedWidth(250)

        self.general_gui_group = GeneralGUIPrefGroupUI()
        self.general_gui_group.setFixedWidth(250)

        self.layout.addWidget(self.general_app_group)
        self.layout.addWidget(self.general_gui_group)
        self.layout.addStretch()


class GerberPreferencesUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.gerber_gen_group = GerberGenPrefGroupUI()
        self.gerber_gen_group.setFixedWidth(250)
        self.gerber_opt_group = GerberOptPrefGroupUI()
        self.gerber_opt_group.setFixedWidth(250)

        self.layout.addWidget(self.gerber_gen_group)
        self.layout.addWidget(self.gerber_opt_group)
        self.layout.addStretch()


class ExcellonPreferencesUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.excellon_gen_group = ExcellonGenPrefGroupUI()
        self.excellon_gen_group.setFixedWidth(275)
        self.excellon_opt_group = ExcellonOptPrefGroupUI()
        self.excellon_opt_group.setFixedWidth(275)

        self.layout.addWidget(self.excellon_gen_group)
        self.layout.addWidget(self.excellon_opt_group)
        self.layout.addStretch()


class GeometryPreferencesUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.geometry_gen_group = GeometryGenPrefGroupUI()
        self.geometry_gen_group.setFixedWidth(275)
        self.geometry_opt_group = GeometryOptPrefGroupUI()
        self.geometry_opt_group.setFixedWidth(275)

        self.layout.addWidget(self.geometry_gen_group)
        self.layout.addWidget(self.geometry_opt_group)
        self.layout.addStretch()


class ToolsPreferencesUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.tools_ncc_group = ToolsNCCPrefGroupUI()
        self.tools_ncc_group.setFixedWidth(200)
        self.tools_paint_group = ToolsPaintPrefGroupUI()
        self.tools_paint_group.setFixedWidth(200)

        self.tools_cutout_group = ToolsCutoutPrefGroupUI()
        self.tools_cutout_group.setFixedWidth(200)

        self.tools_2sided_group = Tools2sidedPrefGroupUI()
        self.tools_2sided_group.setFixedWidth(200)

        self.tools_film_group = ToolsFilmPrefGroupUI()
        self.tools_film_group.setFixedWidth(200)

        self.tools_panelize_group = ToolsPanelizePrefGroupUI()
        self.tools_panelize_group.setFixedWidth(200)

        self.vlay = QtWidgets.QVBoxLayout()
        self.vlay.addWidget(self.tools_ncc_group)
        self.vlay.addWidget(self.tools_paint_group)

        self.vlay1 = QtWidgets.QVBoxLayout()
        self.vlay1.addWidget(self.tools_cutout_group)
        self.vlay1.addWidget(self.tools_2sided_group)
        self.vlay1.addWidget(self.tools_film_group)

        self.vlay2 = QtWidgets.QVBoxLayout()
        self.vlay2.addWidget(self.tools_panelize_group)

        self.layout.addLayout(self.vlay)
        self.layout.addLayout(self.vlay1)
        self.layout.addLayout(self.vlay2)

        self.layout.addStretch()

class CNCJobPreferencesUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.cncjob_gen_group = CNCJobGenPrefGroupUI()
        self.cncjob_gen_group.setFixedWidth(260)
        self.cncjob_opt_group = CNCJobOptPrefGroupUI()
        self.cncjob_opt_group.setFixedWidth(260)

        self.layout.addWidget(self.cncjob_gen_group)
        self.layout.addWidget(self.cncjob_opt_group)
        self.layout.addStretch()


class OptionsGroupUI(QtWidgets.QGroupBox):
    def __init__(self, title, parent=None):
        # QtGui.QGroupBox.__init__(self, title, parent=parent)
        super(OptionsGroupUI, self).__init__()
        self.setStyleSheet("""
        QGroupBox
        {
            font-size: 16px;
            font-weight: bold;
        }
        """)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)


class GeneralGUIPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        super(GeneralGUIPrefGroupUI, self).__init__(self)

        self.setTitle(str("GUI Preferences"))

        # Create a form layout for the Application general settings
        self.form_box = QtWidgets.QFormLayout()

        # Grid X Entry
        self.gridx_label = QtWidgets.QLabel('Grid X value:')
        self.gridx_label.setToolTip(
            "This is the Grid value on X axis\n"
        )
        self.gridx_entry = LengthEntry()

        # Grid Y Entry
        self.gridy_label = QtWidgets.QLabel('Grid Y value:')
        self.gridy_label.setToolTip(
            "This is the Grid value on Y axis\n"
        )
        self.gridy_entry = LengthEntry()

        # Snap Max Entry
        self.snap_max_label = QtWidgets.QLabel('Snap Max:')
        self.snap_max_label.setToolTip("Max. magnet distance")
        self.snap_max_dist_entry = FCEntry()

        # Workspace
        self.workspace_lbl = QtWidgets.QLabel('Workspace:')
        self.workspace_lbl.setToolTip(
            "Draw a delimiting rectangle on canvas.\n"
            "The purpose is to illustrate the limits for our work."
        )
        self.workspace_type_lbl = QtWidgets.QLabel('Wk. format:')
        self.workspace_type_lbl.setToolTip(
            "Select the type of rectangle to be used on canvas,\n"
            "as valid workspace."
        )
        self.workspace_cb = FCCheckBox()
        self.wk_cb = FCComboBox()
        self.wk_cb.addItem('A4P')
        self.wk_cb.addItem('A4L')
        self.wk_cb.addItem('A3P')
        self.wk_cb.addItem('A3L')

        self.wks = OptionalInputSection(self.workspace_cb, [self.workspace_type_lbl, self.wk_cb])

        # Plot Fill Color
        self.pf_color_label = QtWidgets.QLabel('Plot Fill:')
        self.pf_color_label.setToolTip(
            "Set the fill color for plotted objects.\n"
            "First 6 digits are the color and the last 2\n"
            "digits are for alpha (transparency) level."
        )
        self.pf_color_entry = FCEntry()
        self.pf_color_button = QtWidgets.QPushButton()
        self.pf_color_button.setFixedSize(15, 15)

        self.form_box_child_1 = QtWidgets.QHBoxLayout()
        self.form_box_child_1.addWidget(self.pf_color_entry)
        self.form_box_child_1.addWidget(self.pf_color_button)
        self.form_box_child_1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Plot Fill Transparency Level
        self.pf_alpha_label = QtWidgets.QLabel('Alpha Level:')
        self.pf_alpha_label.setToolTip(
            "Set the fill transparency for plotted objects."
        )
        self.pf_color_alpha_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.pf_color_alpha_slider.setMinimum(0)
        self.pf_color_alpha_slider.setMaximum(255)
        self.pf_color_alpha_slider.setSingleStep(1)

        self.pf_color_alpha_spinner = FCSpinner()
        self.pf_color_alpha_spinner.setFixedWidth(70)
        self.pf_color_alpha_spinner.setMinimum(0)
        self.pf_color_alpha_spinner.setMaximum(255)

        self.form_box_child_2 = QtWidgets.QHBoxLayout()
        self.form_box_child_2.addWidget(self.pf_color_alpha_slider)
        self.form_box_child_2.addWidget(self.pf_color_alpha_spinner)

        # Plot Line Color
        self.pl_color_label = QtWidgets.QLabel('Plot Line:')
        self.pl_color_label.setToolTip(
            "Set the line color for plotted objects."
        )
        self.pl_color_entry = FCEntry()
        self.pl_color_button = QtWidgets.QPushButton()
        self.pl_color_button.setFixedSize(15, 15)

        self.form_box_child_3 = QtWidgets.QHBoxLayout()
        self.form_box_child_3.addWidget(self.pl_color_entry)
        self.form_box_child_3.addWidget(self.pl_color_button)
        self.form_box_child_3.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Plot Selection (left - right) Fill Color
        self.sf_color_label = QtWidgets.QLabel('Sel. Fill:')
        self.sf_color_label.setToolTip(
            "Set the fill color for the selection box\n"
            "in case that the selection is done from left to right.\n"
            "First 6 digits are the color and the last 2\n"
            "digits are for alpha (transparency) level."
        )
        self.sf_color_entry = FCEntry()
        self.sf_color_button = QtWidgets.QPushButton()
        self.sf_color_button.setFixedSize(15, 15)

        self.form_box_child_4 = QtWidgets.QHBoxLayout()
        self.form_box_child_4.addWidget(self.sf_color_entry)
        self.form_box_child_4.addWidget(self.sf_color_button)
        self.form_box_child_4.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Plot Selection (left - right) Fill Transparency Level
        self.sf_alpha_label = QtWidgets.QLabel('Alpha Level:')
        self.sf_alpha_label.setToolTip(
            "Set the fill transparency for the 'left to right' selection box."
        )
        self.sf_color_alpha_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sf_color_alpha_slider.setMinimum(0)
        self.sf_color_alpha_slider.setMaximum(255)
        self.sf_color_alpha_slider.setSingleStep(1)

        self.sf_color_alpha_spinner = FCSpinner()
        self.sf_color_alpha_spinner.setFixedWidth(70)
        self.sf_color_alpha_spinner.setMinimum(0)
        self.sf_color_alpha_spinner.setMaximum(255)

        self.form_box_child_5 = QtWidgets.QHBoxLayout()
        self.form_box_child_5.addWidget(self.sf_color_alpha_slider)
        self.form_box_child_5.addWidget(self.sf_color_alpha_spinner)

        # Plot Selection (left - right) Line Color
        self.sl_color_label = QtWidgets.QLabel('Sel. Line:')
        self.sl_color_label.setToolTip(
            "Set the line color for the 'left to right' selection box."
        )
        self.sl_color_entry = FCEntry()
        self.sl_color_button = QtWidgets.QPushButton()
        self.sl_color_button.setFixedSize(15, 15)

        self.form_box_child_6 = QtWidgets.QHBoxLayout()
        self.form_box_child_6.addWidget(self.sl_color_entry)
        self.form_box_child_6.addWidget(self.sl_color_button)
        self.form_box_child_6.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Plot Selection (right - left) Fill Color
        self.alt_sf_color_label = QtWidgets.QLabel('Sel2. Fill:')
        self.alt_sf_color_label.setToolTip(
            "Set the fill color for the selection box\n"
            "in case that the selection is done from right to left.\n"
            "First 6 digits are the color and the last 2\n"
            "digits are for alpha (transparency) level."
        )
        self.alt_sf_color_entry = FCEntry()
        self.alt_sf_color_button = QtWidgets.QPushButton()
        self.alt_sf_color_button.setFixedSize(15, 15)

        self.form_box_child_7 = QtWidgets.QHBoxLayout()
        self.form_box_child_7.addWidget(self.alt_sf_color_entry)
        self.form_box_child_7.addWidget(self.alt_sf_color_button)
        self.form_box_child_7.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Plot Selection (right - left) Fill Transparency Level
        self.alt_sf_alpha_label = QtWidgets.QLabel('Alpha Level:')
        self.alt_sf_alpha_label.setToolTip(
            "Set the fill transparency for selection 'right to left' box."
        )
        self.alt_sf_color_alpha_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.alt_sf_color_alpha_slider.setMinimum(0)
        self.alt_sf_color_alpha_slider.setMaximum(255)
        self.alt_sf_color_alpha_slider.setSingleStep(1)

        self.alt_sf_color_alpha_spinner = FCSpinner()
        self.alt_sf_color_alpha_spinner.setFixedWidth(70)
        self.alt_sf_color_alpha_spinner.setMinimum(0)
        self.alt_sf_color_alpha_spinner.setMaximum(255)

        self.form_box_child_8 = QtWidgets.QHBoxLayout()
        self.form_box_child_8.addWidget(self.alt_sf_color_alpha_slider)
        self.form_box_child_8.addWidget(self.alt_sf_color_alpha_spinner)

        # Plot Selection (right - left) Line Color
        self.alt_sl_color_label = QtWidgets.QLabel('Sel2. Line:')
        self.alt_sl_color_label.setToolTip(
            "Set the line color for the 'right to left' selection box."
        )
        self.alt_sl_color_entry = FCEntry()
        self.alt_sl_color_button = QtWidgets.QPushButton()
        self.alt_sl_color_button.setFixedSize(15, 15)

        self.form_box_child_9 = QtWidgets.QHBoxLayout()
        self.form_box_child_9.addWidget(self.alt_sl_color_entry)
        self.form_box_child_9.addWidget(self.alt_sl_color_button)
        self.form_box_child_9.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Editor Draw Color
        self.draw_color_label = QtWidgets.QLabel('Editor Draw:')
        self.alt_sf_color_label.setToolTip(
            "Set the color for the shape."
        )
        self.draw_color_entry = FCEntry()
        self.draw_color_button = QtWidgets.QPushButton()
        self.draw_color_button.setFixedSize(15, 15)

        self.form_box_child_10 = QtWidgets.QHBoxLayout()
        self.form_box_child_10.addWidget(self.draw_color_entry)
        self.form_box_child_10.addWidget(self.draw_color_button)
        self.form_box_child_10.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Editor Draw Selection Color
        self.sel_draw_color_label = QtWidgets.QLabel('Editor Draw Sel.:')
        self.sel_draw_color_label.setToolTip(
            "Set the color of the shape when selected."
        )
        self.sel_draw_color_entry = FCEntry()
        self.sel_draw_color_button = QtWidgets.QPushButton()
        self.sel_draw_color_button.setFixedSize(15, 15)

        self.form_box_child_11 = QtWidgets.QHBoxLayout()
        self.form_box_child_11.addWidget(self.sel_draw_color_entry)
        self.form_box_child_11.addWidget(self.sel_draw_color_button)
        self.form_box_child_11.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Theme selection
        self.theme_label = QtWidgets.QLabel('Theme:')
        self.alt_sf_color_label.setToolTip(
            "Select a theme for FlatCAM."
        )
        self.theme_combo = FCComboBox()
        self.theme_combo.addItem("Standard")
        self.theme_combo.addItem("Compact")
        self.theme_combo.setCurrentIndex(0)

        # Just to add empty rows
        self.spacelabel = QtWidgets.QLabel('')

        # Add (label - input field) pair to the QFormLayout

        self.form_box.addRow(self.spacelabel, self.spacelabel)

        self.form_box.addRow(self.gridx_label, self.gridx_entry)
        self.form_box.addRow(self.gridy_label, self.gridy_entry)
        self.form_box.addRow(self.snap_max_label, self.snap_max_dist_entry)

        self.form_box.addRow(self.workspace_lbl, self.workspace_cb)
        self.form_box.addRow(self.workspace_type_lbl, self.wk_cb)
        self.form_box.addRow(self.spacelabel, self.spacelabel)
        self.form_box.addRow(self.pf_color_label, self.form_box_child_1)
        self.form_box.addRow(self.pf_alpha_label, self.form_box_child_2)
        self.form_box.addRow(self.pl_color_label, self.form_box_child_3)
        self.form_box.addRow(self.sf_color_label, self.form_box_child_4)
        self.form_box.addRow(self.sf_alpha_label, self.form_box_child_5)
        self.form_box.addRow(self.sl_color_label, self.form_box_child_6)
        self.form_box.addRow(self.alt_sf_color_label, self.form_box_child_7)
        self.form_box.addRow(self.alt_sf_alpha_label, self.form_box_child_8)
        self.form_box.addRow(self.alt_sl_color_label, self.form_box_child_9)
        self.form_box.addRow(self.draw_color_label, self.form_box_child_10)
        self.form_box.addRow(self.sel_draw_color_label, self.form_box_child_11)

        self.form_box.addRow(self.spacelabel, self.spacelabel)
        self.form_box.addRow(self.theme_label, self.theme_combo)
        # Add the QFormLayout that holds the Application general defaults
        # to the main layout of this TAB
        self.layout.addLayout(self.form_box)


class GeneralAppPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        super(GeneralAppPrefGroupUI, self).__init__(self)

        self.setTitle(str("App Preferences"))

        # Create a form layout for the Application general settings
        self.form_box = QtWidgets.QFormLayout()

        # Units for FlatCAM
        self.unitslabel = QtWidgets.QLabel('<b>Units:</b>')
        self.unitslabel.setToolTip("The default value for FlatCAM units.\n"
                                   "Whatever is selected here is set every time\n"
                                   "FLatCAM is started.")
        self.units_radio = RadioSet([{'label': 'IN', 'value': 'IN'},
                                     {'label': 'MM', 'value': 'MM'}])

        # Languages for FlatCAM
        self.languagelabel = QtWidgets.QLabel('<b>Languages:</b>')
        self.languagelabel.setToolTip("Set the language used throughout FlatCAM.")
        self.language_cb = FCComboBox()
        self.languagespace = QtWidgets.QLabel('')
        self.language_apply_btn = FCButton("Apply Language")

        # Shell StartUp CB
        self.shell_startup_label = QtWidgets.QLabel('Shell at StartUp:')
        self.shell_startup_label.setToolTip(
            "Check this box if you want the shell to\n"
            "start automatically at startup."
        )
        self.shell_startup_cb = FCCheckBox(label='')
        self.shell_startup_cb.setToolTip(
            "Check this box if you want the shell to\n"
            "start automatically at startup."
        )

        # Version Check CB
        self.version_check_label = QtWidgets.QLabel('Version Check:')
        self.version_check_label.setToolTip(
            "Check this box if you want to check\n"
            "for a new version automatically at startup."
        )
        self.version_check_cb = FCCheckBox(label='')
        self.version_check_cb.setToolTip(
            "Check this box if you want to check\n"
            "for a new version automatically at startup."
        )

        # Send Stats CB
        self.send_stats_label = QtWidgets.QLabel('Send Stats:')
        self.send_stats_label.setToolTip(
            "Check this box if you agree to send anonymous\n"
            "stats automatically at startup, to help improve FlatCAM."
        )
        self.send_stats_cb= FCCheckBox(label='')
        self.send_stats_cb.setToolTip(
            "Check this box if you agree to send anonymous\n"
            "stats automatically at startup, to help improve FlatCAM."
        )

        self.ois_version_check = OptionalInputSection(self.version_check_cb, [self.send_stats_cb])

        # Select mouse pan button
        self.panbuttonlabel = QtWidgets.QLabel('<b>Pan Button:</b>')
        self.panbuttonlabel.setToolTip("Select the mouse button to use for panning:\n"
                                       "- MMB --> Middle Mouse Button\n"
                                       "- RMB --> Right Mouse Button")
        self.pan_button_radio = RadioSet([{'label': 'MMB', 'value': '3'},
                                     {'label': 'RMB', 'value': '2'}])

        # Multiple Selection Modifier Key
        self.mselectlabel = QtWidgets.QLabel('<b>Multiple Sel:</b>')
        self.mselectlabel.setToolTip("Select the key used for multiple selection.")
        self.mselect_radio = RadioSet([{'label': 'CTRL', 'value': 'Control'},
                                     {'label': 'SHIFT', 'value': 'Shift'}])

        # # Mouse panning with "Space" key, CB
        # self.pan_with_space_label = QtWidgets.QLabel('Pan w/ Space:')
        # self.pan_with_space_label.setToolTip(
        #     "Check this box if you want to pan when mouse is moved,\n"
        #     "and key 'Space' is pressed."
        # )
        # self.pan_with_space_cb = FCCheckBox(label='')
        # self.pan_with_space_cb.setToolTip(
        #     "Check this box if you want to pan when mouse is moved,\n"
        #     "and key 'Space' is pressed."
        # )


        # Just to add empty rows
        self.spacelabel = QtWidgets.QLabel('')

        # Add (label - input field) pair to the QFormLayout
        self.form_box.addRow(self.unitslabel, self.units_radio)
        self.form_box.addRow(self.languagelabel, self.language_cb)
        self.form_box.addRow(self.languagespace, self.language_apply_btn)

        self.form_box.addRow(self.spacelabel, self.spacelabel)
        self.form_box.addRow(self.shell_startup_label, self.shell_startup_cb)
        self.form_box.addRow(self.version_check_label, self.version_check_cb)
        self.form_box.addRow(self.send_stats_label, self.send_stats_cb)

        self.form_box.addRow(self.panbuttonlabel, self.pan_button_radio)
        self.form_box.addRow(self.mselectlabel, self.mselect_radio)
        # self.form_box.addRow(self.pan_with_space_label, self.pan_with_space_cb)
        self.form_box.addRow(self.spacelabel, self.spacelabel)

        # Add the QFormLayout that holds the Application general defaults
        # to the main layout of this TAB
        self.layout.addLayout(self.form_box)


class GerberGenPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Gerber General Preferences", parent=parent)
        super(GerberGenPrefGroupUI, self).__init__(self)

        self.setTitle(str("Gerber General"))

        ## Plot options
        self.plot_options_label = QtWidgets.QLabel("<b>Plot Options:</b>")
        self.layout.addWidget(self.plot_options_label)

        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)
        # Plot CB
        self.plot_cb = FCCheckBox(label='Plot')
        self.plot_options_label.setToolTip(
            "Plot (show) this object."
        )
        grid0.addWidget(self.plot_cb, 0, 0)

        # Solid CB
        self.solid_cb = FCCheckBox(label='Solid')
        self.solid_cb.setToolTip(
            "Solid color polygons."
        )
        grid0.addWidget(self.solid_cb, 0, 1)

        # Multicolored CB
        self.multicolored_cb = FCCheckBox(label='M-Color')
        self.multicolored_cb.setToolTip(
            "Draw polygons in different colors."
        )
        grid0.addWidget(self.multicolored_cb, 0, 2)

        # Number of circle steps for circular aperture linear approximation
        self.circle_steps_label = QtWidgets.QLabel("Circle Steps:")
        self.circle_steps_label.setToolTip(
            "The number of circle steps for Gerber \n"
            "circular aperture linear approximation."
        )
        grid0.addWidget(self.circle_steps_label, 1, 0)
        self.circle_steps_entry = IntEntry()
        grid0.addWidget(self.circle_steps_entry, 1, 1)

        self.layout.addStretch()


class GerberOptPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Gerber Options Preferences", parent=parent)
        super(GerberOptPrefGroupUI, self).__init__(self)

        self.setTitle(str("Gerber Options"))


        ## Isolation Routing
        self.isolation_routing_label = QtWidgets.QLabel("<b>Isolation Routing:</b>")
        self.isolation_routing_label.setToolTip(
            "Create a Geometry object with\n"
            "toolpaths to cut outside polygons."
        )
        self.layout.addWidget(self.isolation_routing_label)

        # Cutting Tool Diameter
        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)

        tdlabel = QtWidgets.QLabel('Tool dia:')
        tdlabel.setToolTip(
            "Diameter of the cutting tool."
        )
        grid0.addWidget(tdlabel, 0, 0)
        self.iso_tool_dia_entry = LengthEntry()
        grid0.addWidget(self.iso_tool_dia_entry, 0, 1)

        # Nr of passes
        passlabel = QtWidgets.QLabel('Width (# passes):')
        passlabel.setToolTip(
            "Width of the isolation gap in\n"
            "number (integer) of tool widths."
        )
        grid0.addWidget(passlabel, 1, 0)
        self.iso_width_entry = IntEntry()
        grid0.addWidget(self.iso_width_entry, 1, 1)

        # Pass overlap
        overlabel = QtWidgets.QLabel('Pass overlap:')
        overlabel.setToolTip(
            "How much (fraction) of the tool width to overlap each tool pass.\n"
            "Example:\n"
            "A value here of 0.25 means an overlap of 25% from the tool diameter found above."
        )
        grid0.addWidget(overlabel, 2, 0)
        self.iso_overlap_entry = FloatEntry()
        grid0.addWidget(self.iso_overlap_entry, 2, 1)

        milling_type_label = QtWidgets.QLabel('Milling Type:')
        milling_type_label.setToolTip(
            "Milling type:\n"
            "- climb / best for precision milling and to reduce tool usage\n"
            "- conventional / useful when there is no backlash compensation"
        )
        grid0.addWidget(milling_type_label, 3, 0)
        self.milling_type_radio = RadioSet([{'label': 'Climb', 'value': 'cl'},
                                            {'label': 'Conv.', 'value': 'cv'}])
        grid0.addWidget(self.milling_type_radio, 3, 1)

        # Combine passes
        self.combine_passes_cb = FCCheckBox(label='Combine Passes')
        self.combine_passes_cb.setToolTip(
            "Combine all passes into one object"
        )
        grid0.addWidget(self.combine_passes_cb, 4, 0)

        ## Clear non-copper regions
        self.clearcopper_label = QtWidgets.QLabel("<b>Clear non-copper:</b>")
        self.clearcopper_label.setToolTip(
            "Create a Geometry object with\n"
            "toolpaths to cut all non-copper regions."
        )
        self.layout.addWidget(self.clearcopper_label)

        grid1 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid1)

        # Margin
        bmlabel = QtWidgets.QLabel('Boundary Margin:')
        bmlabel.setToolTip(
            "Specify the edge of the PCB\n"
            "by drawing a box around all\n"
            "objects with this minimum\n"
            "distance."
        )
        grid1.addWidget(bmlabel, 0, 0)
        self.noncopper_margin_entry = LengthEntry()
        grid1.addWidget(self.noncopper_margin_entry, 0, 1)

        # Rounded corners
        self.noncopper_rounded_cb = FCCheckBox(label="Rounded corners")
        self.noncopper_rounded_cb.setToolTip(
            "Creates a Geometry objects with polygons\n"
            "covering the copper-free areas of the PCB."
        )
        grid1.addWidget(self.noncopper_rounded_cb, 1, 0, 1, 2)

        ## Bounding box
        self.boundingbox_label = QtWidgets.QLabel('<b>Bounding Box:</b>')
        self.layout.addWidget(self.boundingbox_label)

        grid2 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid2)

        bbmargin = QtWidgets.QLabel('Boundary Margin:')
        bbmargin.setToolTip(
            "Distance of the edges of the box\n"
            "to the nearest polygon."
        )
        grid2.addWidget(bbmargin, 0, 0)
        self.bbmargin_entry = LengthEntry()
        grid2.addWidget(self.bbmargin_entry, 0, 1)

        self.bbrounded_cb = FCCheckBox(label="Rounded corners")
        self.bbrounded_cb.setToolTip(
            "If the bounding box is \n"
            "to have rounded corners\n"
            "their radius is equal to\n"
            "the margin."
        )
        grid2.addWidget(self.bbrounded_cb, 1, 0, 1, 2)
        self.layout.addStretch()


class ExcellonGenPrefGroupUI(OptionsGroupUI):

    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Excellon Options", parent=parent)
        super(ExcellonGenPrefGroupUI, self).__init__(self)

        self.setTitle(str("Excellon General"))

        # Plot options
        self.plot_options_label = QtWidgets.QLabel("<b>Plot Options:</b>")
        self.layout.addWidget(self.plot_options_label)

        grid1 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid1)

        self.plot_cb = FCCheckBox(label='Plot')
        self.plot_cb.setToolTip(
            "Plot (show) this object."
        )
        grid1.addWidget(self.plot_cb, 0, 0)

        self.solid_cb = FCCheckBox(label='Solid')
        self.solid_cb.setToolTip(
            "Plot as solid circles."
        )
        grid1.addWidget(self.solid_cb, 0, 1)

        # Excellon format
        self.excellon_format_label = QtWidgets.QLabel("<b>Excellon Format:</b>")
        self.excellon_format_label.setToolTip(
            "The NC drill files, usually named Excellon files\n"
            "are files that can be found in different formats.\n"
            "Here we set the format used when the provided\n"
            "coordinates are not using period.\n"
            "\n"
            "Possible presets:\n"
            "\n"
            "PROTEUS 3:3 MM LZ\n"
            "DipTrace 5:2 MM TZ\n"
            "DipTrace 4:3 MM LZ\n"
            "\n"
            "EAGLE 3:3 MM TZ\n"
            "EAGLE 4:3 MM TZ\n"
            "EAGLE 2:5 INCH TZ\n"
            "EAGLE 3:5 INCH TZ\n"
            "\n"
            "ALTIUM 2:4 INCH LZ\n"
            "Sprint Layout 2:4 INCH LZ"
            "\n"
            "KiCAD 3:5 INCH TZ"
        )
        self.layout.addWidget(self.excellon_format_label)

        hlay1 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(hlay1)
        self.excellon_format_in_label = QtWidgets.QLabel("INCH:")
        self.excellon_format_in_label.setAlignment(QtCore.Qt.AlignLeft)
        self.excellon_format_in_label.setToolTip(
            "Default values for INCH are 2:4")
        hlay1.addWidget(self.excellon_format_in_label, QtCore.Qt.AlignLeft)

        self.excellon_format_upper_in_entry = IntEntry()
        self.excellon_format_upper_in_entry.setMaxLength(1)
        self.excellon_format_upper_in_entry.setAlignment(QtCore.Qt.AlignRight)
        self.excellon_format_upper_in_entry.setFixedWidth(30)
        self.excellon_format_upper_in_entry.setToolTip(
            "This numbers signify the number of digits in\n"
            "the whole part of Excellon coordinates."
        )
        hlay1.addWidget(self.excellon_format_upper_in_entry, QtCore.Qt.AlignLeft)

        excellon_separator_in_label= QtWidgets.QLabel(':')
        excellon_separator_in_label.setFixedWidth(5)
        hlay1.addWidget(excellon_separator_in_label, QtCore.Qt.AlignLeft)

        self.excellon_format_lower_in_entry = IntEntry()
        self.excellon_format_lower_in_entry.setMaxLength(1)
        self.excellon_format_lower_in_entry.setAlignment(QtCore.Qt.AlignRight)
        self.excellon_format_lower_in_entry.setFixedWidth(30)
        self.excellon_format_lower_in_entry.setToolTip(
            "This numbers signify the number of digits in\n"
            "the decimal part of Excellon coordinates."
        )
        hlay1.addWidget(self.excellon_format_lower_in_entry, QtCore.Qt.AlignLeft)
        hlay1.addStretch()

        hlay2 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(hlay2)
        self.excellon_format_mm_label = QtWidgets.QLabel("METRIC:")
        self.excellon_format_mm_label.setAlignment(QtCore.Qt.AlignLeft)
        self.excellon_format_mm_label.setToolTip(
            "Default values for METRIC are 3:3")
        hlay2.addWidget(self.excellon_format_mm_label, QtCore.Qt.AlignLeft)

        self.excellon_format_upper_mm_entry = IntEntry()
        self.excellon_format_upper_mm_entry.setMaxLength(1)
        self.excellon_format_upper_mm_entry.setAlignment(QtCore.Qt.AlignRight)
        self.excellon_format_upper_mm_entry.setFixedWidth(30)
        self.excellon_format_upper_mm_entry.setToolTip(
            "This numbers signify the number of digits in\n"
            "the whole part of Excellon coordinates."
        )
        hlay2.addWidget(self.excellon_format_upper_mm_entry, QtCore.Qt.AlignLeft)

        excellon_separator_mm_label= QtWidgets.QLabel(':')
        excellon_separator_mm_label.setFixedWidth(5)
        hlay2.addWidget(excellon_separator_mm_label, QtCore.Qt.AlignLeft)

        self.excellon_format_lower_mm_entry = IntEntry()
        self.excellon_format_lower_mm_entry.setMaxLength(1)
        self.excellon_format_lower_mm_entry.setAlignment(QtCore.Qt.AlignRight)
        self.excellon_format_lower_mm_entry.setFixedWidth(30)
        self.excellon_format_lower_mm_entry.setToolTip(
            "This numbers signify the number of digits in\n"
            "the decimal part of Excellon coordinates."
        )
        hlay2.addWidget(self.excellon_format_lower_mm_entry, QtCore.Qt.AlignLeft)
        hlay2.addStretch()

        hlay3 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(hlay3)

        self.excellon_zeros_label = QtWidgets.QLabel('Default <b>Zeros</b>:')
        self.excellon_zeros_label.setAlignment(QtCore.Qt.AlignLeft)
        self.excellon_zeros_label.setToolTip(
            "This sets the type of Excellon zeros.\n"
            "If LZ then Leading Zeros are kept and\n"
            "Trailing Zeros are removed.\n"
            "If TZ is checked then Trailing Zeros are kept\n"
            "and Leading Zeros are removed."
        )
        hlay3.addWidget(self.excellon_zeros_label)

        self.excellon_zeros_radio = RadioSet([{'label': 'LZ', 'value': 'L'},
                                     {'label': 'TZ', 'value': 'T'}])
        self.excellon_zeros_radio.setToolTip(
            "This sets the default type of Excellon zeros.\n"
            "If it is not detected in the parsed file the value here\n"
            "will be used."
            "If LZ then Leading Zeros are kept and\n"
            "Trailing Zeros are removed.\n"
            "If TZ is checked then Trailing Zeros are kept\n"
            "and Leading Zeros are removed."
        )
        hlay3.addStretch()
        hlay3.addWidget(self.excellon_zeros_radio, QtCore.Qt.AlignRight)

        hlay4 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(hlay4)

        self.excellon_units_label = QtWidgets.QLabel('Default <b>Units</b>:')
        self.excellon_units_label.setAlignment(QtCore.Qt.AlignLeft)
        self.excellon_units_label.setToolTip(
            "This sets the default units of Excellon files.\n"
            "If it is not detected in the parsed file the value here\n"
            "will be used."
            "Some Excellon files don't have an header\n"
            "therefore this parameter will be used.\n"
        )
        hlay4.addWidget(self.excellon_units_label)

        self.excellon_units_radio = RadioSet([{'label': 'INCH', 'value': 'INCH'},
                                              {'label': 'MM', 'value': 'METRIC'}])
        self.excellon_units_radio.setToolTip(
            "This sets the units of Excellon files.\n"
            "Some Excellon files don't have an header\n"
            "therefore this parameter will be used.\n"
        )
        hlay4.addStretch()
        hlay4.addWidget(self.excellon_units_radio, QtCore.Qt.AlignRight)

        hlay5 = QtWidgets.QVBoxLayout()
        self.layout.addLayout(hlay5)

        self.empty_label = QtWidgets.QLabel("")
        hlay5.addWidget(self.empty_label)

        hlay6 = QtWidgets.QVBoxLayout()
        self.layout.addLayout(hlay6)

        self.excellon_general_label = QtWidgets.QLabel("<b>Excellon Optimization:</b>")
        hlay6.addWidget(self.excellon_general_label)

        # Create a form layout for the Excellon general settings
        form_box_excellon = QtWidgets.QFormLayout()
        hlay6.addLayout(form_box_excellon)

        self.excellon_optimization_label = QtWidgets.QLabel('Path Optimization:   ')
        self.excellon_optimization_label.setAlignment(QtCore.Qt.AlignLeft)
        self.excellon_optimization_label.setToolTip(
            "This sets the optimization type for the Excellon drill path.\n"
            "If MH is checked then Google OR-Tools algorithm with MetaHeuristic\n"
            "Guided Local Path is used. Default search time is 3sec.\n"
            "Use set_sys excellon_search_time value Tcl Command to set other values.\n"
            "If Basic is checked then Google OR-Tools Basic algorithm is used.\n"
            "\n"
            "If DISABLED, then FlatCAM works in 32bit mode and it uses \n"
            "Travelling Salesman algorithm for path optimization."
        )

        self.excellon_optimization_radio = RadioSet([{'label': 'MH', 'value': 'M'},
                                     {'label': 'Basic', 'value': 'B'}])
        self.excellon_optimization_radio.setToolTip(
            "This sets the optimization type for the Excellon drill path.\n"
            "If MH is checked then Google OR-Tools algorithm with MetaHeuristic\n"
            "Guided Local Path is used. Default search time is 3sec.\n"
            "Use set_sys excellon_search_time value Tcl Command to set other values.\n"
            "If Basic is checked then Google OR-Tools Basic algorithm is used.\n"
            "\n"
            "If DISABLED, then FlatCAM works in 32bit mode and it uses \n"
            "Travelling Salesman algorithm for path optimization."
        )

        form_box_excellon.addRow(self.excellon_optimization_label, self.excellon_optimization_radio)

        self.optimization_time_label = QtWidgets.QLabel('Optimization Time:   ')
        self.optimization_time_label.setAlignment(QtCore.Qt.AlignLeft)
        self.optimization_time_label.setToolTip(
            "When OR-Tools Metaheuristic (MH) is enabled there is a\n"
            "maximum threshold for how much time is spent doing the\n"
            "path optimization. This max duration is set here.\n"
            "In seconds."

        )

        self.optimization_time_entry = LengthEntry()
        form_box_excellon.addRow(self.optimization_time_label, self.optimization_time_entry)

        current_platform = platform.architecture()[0]
        if current_platform == '64bit':
            self.excellon_optimization_label.setDisabled(False)
            self.excellon_optimization_radio.setDisabled(False)
            self.optimization_time_label.setDisabled(False)
            self.optimization_time_entry.setDisabled(False)
            self.excellon_optimization_radio.activated_custom.connect(self.optimization_selection)

        else:
            self.excellon_optimization_label.setDisabled(True)
            self.excellon_optimization_radio.setDisabled(True)
            self.optimization_time_label.setDisabled(True)
            self.optimization_time_entry.setDisabled(True)

        self.layout.addStretch()

    def optimization_selection(self):
        if self.excellon_optimization_radio.get_value() == 'M':
            self.optimization_time_label.setDisabled(False)
            self.optimization_time_entry.setDisabled(False)
        else:
            self.optimization_time_label.setDisabled(True)
            self.optimization_time_entry.setDisabled(True)

class ExcellonOptPrefGroupUI(OptionsGroupUI):

    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Excellon Options", parent=parent)
        super(ExcellonOptPrefGroupUI, self).__init__(self)

        self.setTitle(str("Excellon Options"))

        ## Create CNC Job
        self.cncjob_label = QtWidgets.QLabel('<b>Create CNC Job</b>')
        self.cncjob_label.setToolTip(
            "Create a CNC Job object\n"
            "for this drill object."
        )
        self.layout.addWidget(self.cncjob_label)

        grid2 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid2)

        cutzlabel = QtWidgets.QLabel('Cut Z:')
        cutzlabel.setToolTip(
            "Drill depth (negative)\n"
            "below the copper surface."
        )
        grid2.addWidget(cutzlabel, 0, 0)
        self.cutz_entry = LengthEntry()
        grid2.addWidget(self.cutz_entry, 0, 1)

        travelzlabel = QtWidgets.QLabel('Travel Z:')
        travelzlabel.setToolTip(
            "Tool height when travelling\n"
            "across the XY plane."
        )
        grid2.addWidget(travelzlabel, 1, 0)
        self.travelz_entry = LengthEntry()
        grid2.addWidget(self.travelz_entry, 1, 1)

        # Tool change:
        toolchlabel = QtWidgets.QLabel("Tool change:")
        toolchlabel.setToolTip(
            "Include tool-change sequence\n"
            "in G-Code (Pause for tool change)."
        )
        self.toolchange_cb = FCCheckBox()
        grid2.addWidget(toolchlabel, 2, 0)
        grid2.addWidget(self.toolchange_cb, 2, 1)

        toolchangezlabel = QtWidgets.QLabel('Toolchange Z:')
        toolchangezlabel.setToolTip(
            "Toolchange Z position."
        )
        grid2.addWidget(toolchangezlabel, 3, 0)
        self.toolchangez_entry = LengthEntry()
        grid2.addWidget(self.toolchangez_entry, 3, 1)

        toolchange_xy_label = QtWidgets.QLabel('Toolchange X,Y:')
        toolchange_xy_label.setToolTip(
            "Toolchange X,Y position."
        )
        grid2.addWidget(toolchange_xy_label, 4, 0)
        self.toolchangexy_entry = FCEntry()
        grid2.addWidget(self.toolchangexy_entry, 4, 1)

        startzlabel = QtWidgets.QLabel('Start move Z:')
        startzlabel.setToolTip(
            "Height of the tool just after start.\n"
            "Delete the value if you don't need this feature."
        )
        grid2.addWidget(startzlabel, 5, 0)
        self.estartz_entry = FloatEntry()
        grid2.addWidget(self.estartz_entry, 5, 1)

        endzlabel = QtWidgets.QLabel('End move Z:')
        endzlabel.setToolTip(
            "Height of the tool after\n"
            "the last move at the end of the job."
        )
        grid2.addWidget(endzlabel, 6, 0)
        self.eendz_entry = LengthEntry()
        grid2.addWidget(self.eendz_entry, 6, 1)

        frlabel = QtWidgets.QLabel('Feedrate:')
        frlabel.setToolTip(
            "Tool speed while drilling\n"
            "(in units per minute)."
        )
        grid2.addWidget(frlabel, 7, 0)
        self.feedrate_entry = LengthEntry()
        grid2.addWidget(self.feedrate_entry, 7, 1)

        fr_rapid_label = QtWidgets.QLabel('Feedrate Rapids:')
        fr_rapid_label.setToolTip(
            "Tool speed while drilling\n"
            "with rapid move\n"
            "(in units per minute)."
        )
        grid2.addWidget(fr_rapid_label, 8, 0)
        self.feedrate_rapid_entry = LengthEntry()
        grid2.addWidget(self.feedrate_rapid_entry, 8, 1)

        # Spindle speed
        spdlabel = QtWidgets.QLabel('Spindle speed:')
        spdlabel.setToolTip(
            "Speed of the spindle\n"
            "in RPM (optional)"
        )
        grid2.addWidget(spdlabel, 9, 0)
        self.spindlespeed_entry = IntEntry(allow_empty=True)
        grid2.addWidget(self.spindlespeed_entry, 9, 1)

        # Dwell
        dwelllabel = QtWidgets.QLabel('Dwell:')
        dwelllabel.setToolTip(
            "Pause to allow the spindle to reach its\n"
            "speed before cutting."
        )
        dwelltime = QtWidgets.QLabel('Duration [m-sec.]:')
        dwelltime.setToolTip(
            "Number of milliseconds for spindle to dwell."
        )
        self.dwell_cb = FCCheckBox()
        self.dwelltime_entry = FCEntry()
        grid2.addWidget(dwelllabel, 10, 0)
        grid2.addWidget(self.dwell_cb, 10, 1)
        grid2.addWidget(dwelltime, 11, 0)
        grid2.addWidget(self.dwelltime_entry, 11, 1)

        self.ois_dwell_exc = OptionalInputSection(self.dwell_cb, [self.dwelltime_entry])

        # postprocessor selection
        pp_excellon_label = QtWidgets.QLabel("Postprocessor:")
        pp_excellon_label.setToolTip(
            "The postprocessor file that dictates\n"
            "gcode output."
        )
        grid2.addWidget(pp_excellon_label, 12, 0)
        self.pp_excellon_name_cb = FCComboBox()
        self.pp_excellon_name_cb.setFocusPolicy(Qt.StrongFocus)
        grid2.addWidget(self.pp_excellon_name_cb, 12, 1)

        # Probe depth
        self.pdepth_label = QtWidgets.QLabel("Probe Z depth:")
        self.pdepth_label.setToolTip(
            "The maximum depth that the probe is allowed\n"
            "to probe. Negative value, in current units."
        )
        grid2.addWidget(self.pdepth_label, 13, 0)
        self.pdepth_entry = FCEntry()
        grid2.addWidget(self.pdepth_entry, 13, 1)

        # Probe feedrate
        self.feedrate_probe_label = QtWidgets.QLabel("Feedrate Probe:")
        self.feedrate_probe_label.setToolTip(
            "The feedrate used while the probe is probing."
        )
        grid2.addWidget(self.feedrate_probe_label, 14, 0)
        self.feedrate_probe_entry = FCEntry()
        grid2.addWidget(self.feedrate_probe_entry, 14, 1)

        fplungelabel = QtWidgets.QLabel('Fast Plunge:')
        fplungelabel.setToolTip(
            "By checking this, the vertical move from\n"
            "Z_Toolchange to Z_move is done with G0,\n"
            "meaning the fastest speed available.\n"
            "WARNING: the move is done at Toolchange X,Y coords."
        )
        self.fplunge_cb = FCCheckBox()
        grid2.addWidget(fplungelabel, 15, 0)
        grid2.addWidget(self.fplunge_cb, 15, 1)

        #### Choose what to use for Gcode creation: Drills, Slots or Both
        excellon_gcode_type_label = QtWidgets.QLabel('<b>Gcode:    </b>')
        excellon_gcode_type_label.setToolTip(
            "Choose what to use for GCode generation:\n"
            "'Drills', 'Slots' or 'Both'.\n"
            "When choosing 'Slots' or 'Both', slots will be\n"
            "converted to drills."
        )
        self.excellon_gcode_type_radio = RadioSet([{'label': 'Drills', 'value': 'drills'},
                                          {'label': 'Slots', 'value': 'slots'},
                                          {'label': 'Both', 'value': 'both'}])
        grid2.addWidget(excellon_gcode_type_label, 16, 0)
        grid2.addWidget(self.excellon_gcode_type_radio, 16, 1)

        # until I decide to implement this feature those remain disabled
        excellon_gcode_type_label.setDisabled(True)
        self.excellon_gcode_type_radio.setDisabled(True)

        #### Milling Holes ####
        self.mill_hole_label = QtWidgets.QLabel('<b>Mill Holes</b>')
        self.mill_hole_label.setToolTip(
            "Create Geometry for milling holes."
        )
        self.layout.addWidget(self.mill_hole_label)

        grid3 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid3)
        tdlabel = QtWidgets.QLabel('Drill Tool dia:')
        tdlabel.setToolTip(
            "Diameter of the cutting tool."
        )
        grid3.addWidget(tdlabel, 0, 0)
        self.tooldia_entry = LengthEntry()
        grid3.addWidget(self.tooldia_entry, 0, 1)
        stdlabel = QtWidgets.QLabel('Slot Tool dia:')
        stdlabel.setToolTip(
            "Diameter of the cutting tool\n"
            "when milling slots."
        )
        grid3.addWidget(stdlabel, 1, 0)
        self.slot_tooldia_entry = LengthEntry()
        grid3.addWidget(self.slot_tooldia_entry, 1, 1)

        grid4 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid4)

        # Adding the Excellon Format Defaults Button
        self.excellon_defaults_button = QtWidgets.QPushButton()
        self.excellon_defaults_button.setText(str("Defaults"))
        self.excellon_defaults_button.setFixedWidth(80)
        grid4.addWidget(self.excellon_defaults_button, 0, 0, QtCore.Qt.AlignRight)

        self.layout.addStretch()


class GeometryGenPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Geometry General Preferences", parent=parent)
        super(GeometryGenPrefGroupUI, self).__init__(self)

        self.setTitle(str("Geometry General"))

        ## Plot options
        self.plot_options_label = QtWidgets.QLabel("<b>Plot Options:</b>")
        self.layout.addWidget(self.plot_options_label)

        # Plot CB
        self.plot_cb = FCCheckBox(label='Plot')
        self.plot_cb.setToolTip(
            "Plot (show) this object."
        )
        self.layout.addWidget(self.plot_cb)

        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)
        # Number of circle steps for circular aperture linear approximation
        self.circle_steps_label = QtWidgets.QLabel("Circle Steps:")
        self.circle_steps_label.setToolTip(
            "The number of circle steps for <b>Geometry</b> \n"
            "circle and arc shapes linear approximation."
        )
        grid0.addWidget(self.circle_steps_label, 1, 0)
        self.circle_steps_entry = IntEntry()
        grid0.addWidget(self.circle_steps_entry, 1, 1)

        # Tools
        self.tools_label = QtWidgets.QLabel("<b>Tools</b>")
        self.layout.addWidget(self.tools_label)

        grid1 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid1)

        # Tooldia
        tdlabel = QtWidgets.QLabel('Tool dia:                   ')
        tdlabel.setToolTip(
            "The diameter of the cutting\n"
            "tool (just for display)."
        )
        grid1.addWidget(tdlabel, 0, 0)
        self.cnctooldia_entry = LengthEntry()
        grid1.addWidget(self.cnctooldia_entry, 0, 1)

        self.layout.addStretch()


class GeometryOptPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Geometry Options Preferences", parent=parent)
        super(GeometryOptPrefGroupUI, self).__init__(self)

        self.setTitle(str("Geometry Options"))

        # ------------------------------
        ## Create CNC Job
        # ------------------------------
        self.cncjob_label = QtWidgets.QLabel('<b>Create CNC Job:</b>')
        self.cncjob_label.setToolTip(
            "Create a CNC Job object\n"
            "tracing the contours of this\n"
            "Geometry object."
        )
        self.layout.addWidget(self.cncjob_label)

        grid1 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid1)

        # Cut Z
        cutzlabel = QtWidgets.QLabel('Cut Z:')
        cutzlabel.setToolTip(
            "Cutting depth (negative)\n"
            "below the copper surface."
        )
        grid1.addWidget(cutzlabel, 0, 0)
        self.cutz_entry = LengthEntry()
        grid1.addWidget(self.cutz_entry, 0, 1)

        # Multidepth CheckBox
        self.multidepth_cb = FCCheckBox(label='Multidepth')
        self.multidepth_cb.setToolTip(
            "Multidepth usage: True or False."
        )
        grid1.addWidget(self.multidepth_cb, 1, 0)

        # Depth/pass
        dplabel = QtWidgets.QLabel('Depth/Pass:')
        dplabel.setToolTip(
            "The depth to cut on each pass,\n"
            "when multidepth is enabled.\n"
            "It has positive value although\n"
            "it is a fraction from the depth\n"
            "which has negative value."
        )

        grid1.addWidget(dplabel, 2, 0)
        self.depthperpass_entry = LengthEntry()
        grid1.addWidget(self.depthperpass_entry, 2, 1)

        self.ois_multidepth = OptionalInputSection(self.multidepth_cb, [self.depthperpass_entry])

        # Travel Z
        travelzlabel = QtWidgets.QLabel('Travel Z:')
        travelzlabel.setToolTip(
            "Height of the tool when\n"
            "moving without cutting."
        )
        grid1.addWidget(travelzlabel, 3, 0)
        self.travelz_entry = LengthEntry()
        grid1.addWidget(self.travelz_entry, 3, 1)

        # Tool change:
        toolchlabel = QtWidgets.QLabel("Tool change:")
        toolchlabel.setToolTip(
            "Include tool-change sequence\n"
            "in G-Code (Pause for tool change)."
        )
        self.toolchange_cb = FCCheckBox()
        grid1.addWidget(toolchlabel, 4, 0)
        grid1.addWidget(self.toolchange_cb, 4, 1)

        # Toolchange Z
        toolchangezlabel = QtWidgets.QLabel('Toolchange Z:')
        toolchangezlabel.setToolTip(
            "Toolchange Z position."
        )
        grid1.addWidget(toolchangezlabel, 5, 0)
        self.toolchangez_entry = LengthEntry()
        grid1.addWidget(self.toolchangez_entry, 5, 1)

        # Toolchange X,Y
        toolchange_xy_label = QtWidgets.QLabel('Toolchange X,Y:')
        toolchange_xy_label.setToolTip(
            "Toolchange X,Y position."
        )
        grid1.addWidget(toolchange_xy_label, 6, 0)
        self.toolchangexy_entry = FCEntry()
        grid1.addWidget(self.toolchangexy_entry, 6, 1)

        # Start move Z
        startzlabel = QtWidgets.QLabel('Start move Z:')
        startzlabel.setToolTip(
            "Height of the tool just after starting the work.\n"
            "Delete the value if you don't need this feature."
        )
        grid1.addWidget(startzlabel, 7, 0)
        self.gstartz_entry = FloatEntry()
        grid1.addWidget(self.gstartz_entry, 7, 1)

        # End move Z
        endzlabel = QtWidgets.QLabel('End move Z:')
        endzlabel.setToolTip(
            "Height of the tool after\n"
            "the last move at the end of the job."
        )
        grid1.addWidget(endzlabel, 8, 0)
        self.gendz_entry = LengthEntry()
        grid1.addWidget(self.gendz_entry, 8, 1)

        # Feedrate X-Y
        frlabel = QtWidgets.QLabel('Feed Rate X-Y:')
        frlabel.setToolTip(
            "Cutting speed in the XY\n"
            "plane in units per minute"
        )
        grid1.addWidget(frlabel, 9, 0)
        self.cncfeedrate_entry = LengthEntry()
        grid1.addWidget(self.cncfeedrate_entry, 9, 1)

        # Feedrate Z (Plunge)
        frz_label = QtWidgets.QLabel('Feed Rate Z:')
        frz_label.setToolTip(
            "Cutting speed in the XY\n"
            "plane in units per minute.\n"
            "It is called also Plunge."
        )
        grid1.addWidget(frz_label, 10, 0)
        self.cncplunge_entry = LengthEntry()
        grid1.addWidget(self.cncplunge_entry, 10, 1)

        # Feedrate rapids
        fr_rapid_label = QtWidgets.QLabel('Feed Rate Rapids:')
        fr_rapid_label.setToolTip(
            "Cutting speed in the XY\n"
            "plane in units per minute"
        )
        grid1.addWidget(fr_rapid_label, 11, 0)
        self.cncfeedrate_rapid_entry = LengthEntry()
        grid1.addWidget(self.cncfeedrate_rapid_entry, 11, 1)

        # End move extra cut
        self.extracut_cb = FCCheckBox(label='Cut over 1st pt.')
        self.extracut_cb.setToolTip(
            "In order to remove possible\n"
            "copper leftovers where first cut\n"
            "meet with last cut, we generate an\n"
            "extended cut over the first cut section."
        )
        grid1.addWidget(self.extracut_cb, 12, 0)

        # Spindle Speed
        spdlabel = QtWidgets.QLabel('Spindle speed:')
        spdlabel.setToolTip(
            "Speed of the spindle\n"
            "in RPM (optional)"
        )
        grid1.addWidget(spdlabel, 13, 0)
        self.cncspindlespeed_entry = IntEntry(allow_empty=True)
        grid1.addWidget(self.cncspindlespeed_entry, 13, 1)

        # Dwell
        self.dwell_cb = FCCheckBox(label='Dwell:')
        self.dwell_cb.setToolTip(
            "Pause to allow the spindle to reach its\n"
            "speed before cutting."
        )
        dwelltime = QtWidgets.QLabel('Duration [m-sec.]:')
        dwelltime.setToolTip(
            "Number of milliseconds for spindle to dwell."
        )
        self.dwelltime_entry = FCEntry()
        grid1.addWidget(self.dwell_cb, 14, 0)
        grid1.addWidget(dwelltime, 15, 0)
        grid1.addWidget(self.dwelltime_entry, 15, 1)

        self.ois_dwell = OptionalInputSection(self.dwell_cb, [self.dwelltime_entry])

        # postprocessor selection
        pp_label = QtWidgets.QLabel("Postprocessor:")
        pp_label.setToolTip(
            "The postprocessor file that dictates\n"
            "Machine Code output."
        )
        grid1.addWidget(pp_label, 16, 0)
        self.pp_geometry_name_cb = FCComboBox()
        self.pp_geometry_name_cb.setFocusPolicy(Qt.StrongFocus)
        grid1.addWidget(self.pp_geometry_name_cb, 16, 1)

        # Probe depth
        self.pdepth_label = QtWidgets.QLabel("Probe Z depth:")
        self.pdepth_label.setToolTip(
            "The maximum depth that the probe is allowed\n"
            "to probe. Negative value, in current units."
        )
        grid1.addWidget(self.pdepth_label, 17, 0)
        self.pdepth_entry = FCEntry()
        grid1.addWidget(self.pdepth_entry, 17, 1)

        # Probe feedrate
        self.feedrate_probe_label = QtWidgets.QLabel("Feedrate Probe:")
        self.feedrate_probe_label.setToolTip(
            "The feedrate used while the probe is probing."
        )
        grid1.addWidget(self.feedrate_probe_label, 18, 0)
        self.feedrate_probe_entry = FCEntry()
        grid1.addWidget(self.feedrate_probe_entry, 18, 1)

        # Fast Move from Z Toolchange
        fplungelabel = QtWidgets.QLabel('Fast Plunge:')
        fplungelabel.setToolTip(
            "By checking this, the vertical move from\n"
            "Z_Toolchange to Z_move is done with G0,\n"
            "meaning the fastest speed available.\n"
            "WARNING: the move is done at Toolchange X,Y coords."
        )
        self.fplunge_cb = FCCheckBox()
        grid1.addWidget(fplungelabel, 19, 0)
        grid1.addWidget(self.fplunge_cb, 19, 1)

        # Size of trace segment on X axis
        segx_label = QtWidgets.QLabel("Seg. X size:")
        segx_label.setToolTip(
            "The size of the trace segment on the X axis.\n"
            "Useful for auto-leveling.\n"
            "A value of 0 means no segmentation on the X axis."
        )
        grid1.addWidget(segx_label, 20, 0)
        self.segx_entry = FCEntry()
        grid1.addWidget(self.segx_entry, 20, 1)

        # Size of trace segment on Y axis
        segy_label = QtWidgets.QLabel("Seg. Y size:")
        segy_label.setToolTip(
            "The size of the trace segment on the Y axis.\n"
            "Useful for auto-leveling.\n"
            "A value of 0 means no segmentation on the Y axis."
        )
        grid1.addWidget(segy_label, 21, 0)
        self.segy_entry = FCEntry()
        grid1.addWidget(self.segy_entry, 21, 1)

        self.layout.addStretch()


class CNCJobGenPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "CNC Job General Preferences", parent=None)
        super(CNCJobGenPrefGroupUI, self).__init__(self)

        self.setTitle(str("CNC Job General"))

        ## Plot options
        self.plot_options_label = QtWidgets.QLabel("<b>Plot Options:</b>")
        self.layout.addWidget(self.plot_options_label)

        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)

        # Plot CB
        # self.plot_cb = QtWidgets.QCheckBox('Plot')
        self.plot_cb = FCCheckBox('Plot')
        self.plot_cb.setToolTip(
            "Plot (show) this object."
        )
        grid0.addWidget(self.plot_cb, 0, 0)

        # Number of circle steps for circular aperture linear approximation
        self.steps_per_circle_label = QtWidgets.QLabel("Circle Steps:")
        self.steps_per_circle_label.setToolTip(
            "The number of circle steps for <b>GCode</b> \n"
            "circle and arc shapes linear approximation."
        )
        grid0.addWidget(self.steps_per_circle_label, 1, 0)
        self.steps_per_circle_entry = IntEntry()
        grid0.addWidget(self.steps_per_circle_entry, 1, 1)

        # Tool dia for plot
        tdlabel = QtWidgets.QLabel('Tool dia:')
        tdlabel.setToolTip(
            "Diameter of the tool to be\n"
            "rendered in the plot."
        )
        grid0.addWidget(tdlabel, 2, 0)
        self.tooldia_entry = LengthEntry()
        grid0.addWidget(self.tooldia_entry, 2, 1)

        # Number of decimals to use in GCODE coordinates
        cdeclabel = QtWidgets.QLabel('Coords decimals:')
        cdeclabel.setToolTip(
            "The number of decimals to be used for \n"
            "the X, Y, Z coordinates in CNC code (GCODE, etc.)"
        )
        grid0.addWidget(cdeclabel, 3, 0)
        self.coords_dec_entry = IntEntry()
        grid0.addWidget(self.coords_dec_entry, 3, 1)

        # Number of decimals to use in GCODE feedrate
        frdeclabel = QtWidgets.QLabel('Feedrate decimals:')
        frdeclabel.setToolTip(
            "The number of decimals to be used for \n"
            "the feedrate in CNC code (GCODE, etc.)"
        )
        grid0.addWidget(frdeclabel, 4, 0)
        self.fr_dec_entry = IntEntry()
        grid0.addWidget(self.fr_dec_entry, 4, 1)

        self.layout.addStretch()


class CNCJobOptPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "CNC Job Options Preferences", parent=None)
        super(CNCJobOptPrefGroupUI, self).__init__(self)

        self.setTitle(str("CNC Job Options"))

        ## Export G-Code
        self.export_gcode_label = QtWidgets.QLabel("<b>Export G-Code:</b>")
        self.export_gcode_label.setToolTip(
            "Export and save G-Code to\n"
            "make this object to a file."
        )
        self.layout.addWidget(self.export_gcode_label)

        # Prepend to G-Code
        prependlabel = QtWidgets.QLabel('Prepend to G-Code:')
        prependlabel.setToolTip(
            "Type here any G-Code commands you would\n"
            "like to add at the beginning of the G-Code file."
        )
        self.layout.addWidget(prependlabel)

        self.prepend_text = FCTextArea()
        self.layout.addWidget(self.prepend_text)

        # Append text to G-Code
        appendlabel = QtWidgets.QLabel('Append to G-Code:')
        appendlabel.setToolTip(
            "Type here any G-Code commands you would\n"
            "like to append to the generated file.\n"
            "I.e.: M2 (End of program)"
        )
        self.layout.addWidget(appendlabel)

        self.append_text = FCTextArea()
        self.layout.addWidget(self.append_text)

        self.layout.addStretch()


class ToolsNCCPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "NCC Tool Options", parent=parent)
        super(ToolsNCCPrefGroupUI, self).__init__(self)

        self.setTitle(str("NCC Tool Options"))

        ## Clear non-copper regions
        self.clearcopper_label = QtWidgets.QLabel("<b>Parameters:</b>")
        self.clearcopper_label.setToolTip(
            "Create a Geometry object with\n"
            "toolpaths to cut all non-copper regions."
        )
        self.layout.addWidget(self.clearcopper_label)

        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)

        ncctdlabel = QtWidgets.QLabel('Tools dia:')
        ncctdlabel.setToolTip(
            "Diameters of the cutting tools, separated by ','"
        )
        grid0.addWidget(ncctdlabel, 0, 0)
        self.ncc_tool_dia_entry = FCEntry()
        grid0.addWidget(self.ncc_tool_dia_entry, 0, 1)

        nccoverlabel = QtWidgets.QLabel('Overlap:')
        nccoverlabel.setToolTip(
            "How much (fraction) of the tool width to overlap each tool pass.\n"
            "Example:\n"
            "A value here of 0.25 means 25% from the tool diameter found above.\n\n"
            "Adjust the value starting with lower values\n"
            "and increasing it if areas that should be cleared are still \n"
            "not cleared.\n"
            "Lower values = faster processing, faster execution on PCB.\n"
            "Higher values = slow processing and slow execution on CNC\n"
            "due of too many paths."
        )
        grid0.addWidget(nccoverlabel, 1, 0)
        self.ncc_overlap_entry = FloatEntry()
        grid0.addWidget(self.ncc_overlap_entry, 1, 1)

        nccmarginlabel = QtWidgets.QLabel('Margin:')
        nccmarginlabel.setToolTip(
            "Bounding box margin."
        )
        grid0.addWidget(nccmarginlabel, 2, 0)
        self.ncc_margin_entry = FloatEntry()
        grid0.addWidget(self.ncc_margin_entry, 2, 1)

        # Method
        methodlabel = QtWidgets.QLabel('Method:')
        methodlabel.setToolTip(
            "Algorithm for non-copper clearing:<BR>"
            "<B>Standard</B>: Fixed step inwards.<BR>"
            "<B>Seed-based</B>: Outwards from seed.<BR>"
            "<B>Line-based</B>: Parallel lines."
        )
        grid0.addWidget(methodlabel, 3, 0)
        self.ncc_method_radio = RadioSet([
            {"label": "Standard", "value": "standard"},
            {"label": "Seed-based", "value": "seed"},
            {"label": "Straight lines", "value": "lines"}
        ], orientation='vertical', stretch=False)
        grid0.addWidget(self.ncc_method_radio, 3, 1)

        # Connect lines
        pathconnectlabel = QtWidgets.QLabel("Connect:")
        pathconnectlabel.setToolTip(
            "Draw lines between resulting\n"
            "segments to minimize tool lifts."
        )
        grid0.addWidget(pathconnectlabel, 4, 0)
        self.ncc_connect_cb = FCCheckBox()
        grid0.addWidget(self.ncc_connect_cb, 4, 1)

        contourlabel = QtWidgets.QLabel("Contour:")
        contourlabel.setToolTip(
            "Cut around the perimeter of the polygon\n"
            "to trim rough edges."
        )
        grid0.addWidget(contourlabel, 5, 0)
        self.ncc_contour_cb = FCCheckBox()
        grid0.addWidget(self.ncc_contour_cb, 5, 1)

        restlabel = QtWidgets.QLabel("Rest M.:")
        restlabel.setToolTip(
            "If checked, use 'rest machining'.\n"
            "Basically it will clear copper outside PCB features,\n"
            "using the biggest tool and continue with the next tools,\n"
            "from bigger to smaller, to clear areas of copper that\n"
            "could not be cleared by previous tool.\n"
            "If not checked, use the standard algorithm."
        )
        grid0.addWidget(restlabel, 6, 0)
        self.ncc_rest_cb = FCCheckBox()
        grid0.addWidget(self.ncc_rest_cb, 6, 1)

        self.layout.addStretch()


class ToolsCutoutPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Cutout Tool Options", parent=parent)
        super(ToolsCutoutPrefGroupUI, self).__init__(self)

        self.setTitle(str("Cutout Tool Options"))

        ## Board cuttout
        self.board_cutout_label = QtWidgets.QLabel("<b>Parameters:</b>")
        self.board_cutout_label.setToolTip(
            "Create toolpaths to cut around\n"
            "the PCB and separate it from\n"
            "the original board."
        )
        self.layout.addWidget(self.board_cutout_label)

        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)

        tdclabel = QtWidgets.QLabel('Tool dia:')
        tdclabel.setToolTip(
            "Diameter of the cutting tool."
        )
        grid0.addWidget(tdclabel, 0, 0)
        self.cutout_tooldia_entry = LengthEntry()
        grid0.addWidget(self.cutout_tooldia_entry, 0, 1)

        marginlabel = QtWidgets.QLabel('Margin:')
        marginlabel.setToolTip(
            "Distance from objects at which\n"
            "to draw the cutout."
        )
        grid0.addWidget(marginlabel, 1, 0)
        self.cutout_margin_entry = LengthEntry()
        grid0.addWidget(self.cutout_margin_entry, 1, 1)

        gaplabel = QtWidgets.QLabel('Gap size:')
        gaplabel.setToolTip(
            "Size of the gaps in the toolpath\n"
            "that will remain to hold the\n"
            "board in place."
        )
        grid0.addWidget(gaplabel, 2, 0)
        self.cutout_gap_entry = LengthEntry()
        grid0.addWidget(self.cutout_gap_entry, 2, 1)

        gapslabel = QtWidgets.QLabel('Gaps Rect:')
        gapslabel.setToolTip(
            "Where to place the gaps when doing a Rectangular Cutout:\n"
            " - 2 (T/B) --> Top/Bottom\n"
            " - 2 (L/R) --> Left/Rigt\n"
            " - 4       --> on each of all 4 sides."
        )
        grid0.addWidget(gapslabel, 3, 0)
        self.gaps_radio = RadioSet([{'label': '2 (T/B)', 'value': 'tb'},
                                    {'label': '2 (L/R)', 'value': 'lr'},
                                    {'label': '4', 'value': '4'}])
        grid0.addWidget(self.gaps_radio, 3, 1)

        gaps_ff_label = QtWidgets.QLabel('Gaps FF:')
        gaps_ff_label.setToolTip(
            "Number of gaps used for the FreeForm cutout.\n"
            "There can be maximum 8 bridges/gaps.\n"
            "The choices are:\n"
            "- lr    - left + right\n"
            "- tb    - top + bottom\n"
            "- 4     - left + right +top + bottom\n"
            "- 2lr   - 2*left + 2*right\n"
            "- 2tb  - 2*top + 2*bottom\n"
            "- 8     - 2*left + 2*right +2*top + 2*bottom"
        )
        grid0.addWidget(gaps_ff_label, 4, 0)
        self.gaps_combo = FCComboBox()
        grid0.addWidget(self.gaps_combo, 4, 1)

        gaps_items = ['LR', 'TB', '4', '2LR', '2TB', '8']
        for it in gaps_items:
            self.gaps_combo.addItem(it)
            self.gaps_combo.setStyleSheet('background-color: rgb(255,255,255)')

        self.layout.addStretch()


class Tools2sidedPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "2sided Tool Options", parent=parent)
        super(Tools2sidedPrefGroupUI, self).__init__(self)

        self.setTitle(str("2Sided Tool Options"))

        ## Board cuttout
        self.dblsided_label = QtWidgets.QLabel("<b>Parameters:</b>")
        self.dblsided_label.setToolTip(
            "A tool to help in creating a double sided\n"
            "PCB using alignment holes."
        )
        self.layout.addWidget(self.dblsided_label)

        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)

        ## Drill diameter for alignment holes
        self.drill_dia_entry = LengthEntry()
        self.dd_label = QtWidgets.QLabel("Drill diam.:")
        self.dd_label.setToolTip(
            "Diameter of the drill for the "
            "alignment holes."
        )
        grid0.addWidget(self.dd_label, 0, 0)
        grid0.addWidget(self.drill_dia_entry, 0, 1)

        ## Axis
        self.mirror_axis_radio = RadioSet([{'label': 'X', 'value': 'X'},
                                     {'label': 'Y', 'value': 'Y'}])
        self.mirax_label = QtWidgets.QLabel("Mirror Axis:")
        self.mirax_label.setToolTip(
            "Mirror vertically (X) or horizontally (Y)."
        )
        # grid_lay.addRow("Mirror Axis:", self.mirror_axis)
        self.empty_lb1 = QtWidgets.QLabel("")
        grid0.addWidget(self.empty_lb1, 1, 0)
        grid0.addWidget(self.mirax_label, 2, 0)
        grid0.addWidget(self.mirror_axis_radio, 2, 1)

        ## Axis Location
        self.axis_location_radio = RadioSet([{'label': 'Point', 'value': 'point'},
                                       {'label': 'Box', 'value': 'box'}])
        self.axloc_label = QtWidgets.QLabel("Axis Ref:")
        self.axloc_label.setToolTip(
            "The axis should pass through a <b>point</b> or cut\n "
            "a specified <b>box</b> (in a Geometry object) in \n"
            "the middle."
        )
        # grid_lay.addRow("Axis Location:", self.axis_location)
        grid0.addWidget(self.axloc_label, 3, 0)
        grid0.addWidget(self.axis_location_radio, 3, 1)

        self.layout.addStretch()


class ToolsPaintPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Paint Area Tool Options", parent=parent)
        super(ToolsPaintPrefGroupUI, self).__init__(self)

        self.setTitle(str("Paint Tool Options"))

        # ------------------------------
        ## Paint area
        # ------------------------------
        self.paint_label = QtWidgets.QLabel('<b>Parameters:</b>')
        self.paint_label.setToolTip(
            "Creates tool paths to cover the\n"
            "whole area of a polygon (remove\n"
            "all copper). You will be asked\n"
            "to click on the desired polygon."
        )
        self.layout.addWidget(self.paint_label)

        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)

        # Tool dia
        ptdlabel = QtWidgets.QLabel('Tool dia:')
        ptdlabel.setToolTip(
            "Diameter of the tool to\n"
            "be used in the operation."
        )
        grid0.addWidget(ptdlabel, 0, 0)

        self.painttooldia_entry = LengthEntry()
        grid0.addWidget(self.painttooldia_entry, 0, 1)

        # Overlap
        ovlabel = QtWidgets.QLabel('Overlap:')
        ovlabel.setToolTip(
            "How much (fraction) of the tool\n"
            "width to overlap each tool pass."
        )
        grid0.addWidget(ovlabel, 1, 0)
        self.paintoverlap_entry = LengthEntry()
        grid0.addWidget(self.paintoverlap_entry, 1, 1)

        # Margin
        marginlabel = QtWidgets.QLabel('Margin:')
        marginlabel.setToolTip(
            "Distance by which to avoid\n"
            "the edges of the polygon to\n"
            "be painted."
        )
        grid0.addWidget(marginlabel, 2, 0)
        self.paintmargin_entry = LengthEntry()
        grid0.addWidget(self.paintmargin_entry, 2, 1)

        # Method
        methodlabel = QtWidgets.QLabel('Method:')
        methodlabel.setToolTip(
            "Algorithm to paint the polygon:<BR>"
            "<B>Standard</B>: Fixed step inwards.<BR>"
            "<B>Seed-based</B>: Outwards from seed."
        )
        grid0.addWidget(methodlabel, 3, 0)
        self.paintmethod_combo = RadioSet([
            {"label": "Standard", "value": "standard"},
            {"label": "Seed-based", "value": "seed"},
            {"label": "Straight lines", "value": "lines"}
        ], orientation='vertical', stretch=False)
        grid0.addWidget(self.paintmethod_combo, 3, 1)

        # Connect lines
        pathconnectlabel = QtWidgets.QLabel("Connect:")
        pathconnectlabel.setToolTip(
            "Draw lines between resulting\n"
            "segments to minimize tool lifts."
        )
        grid0.addWidget(pathconnectlabel, 4, 0)
        self.pathconnect_cb = FCCheckBox()
        grid0.addWidget(self.pathconnect_cb, 4, 1)

        # Paint contour
        contourlabel = QtWidgets.QLabel("Contour:")
        contourlabel.setToolTip(
            "Cut around the perimeter of the polygon\n"
            "to trim rough edges."
        )
        grid0.addWidget(contourlabel, 5, 0)
        self.contour_cb = FCCheckBox()
        grid0.addWidget(self.contour_cb, 5, 1)

        # Polygon selection
        selectlabel = QtWidgets.QLabel('Selection:')
        selectlabel.setToolTip(
            "How to select the polygons to paint."
        )
        grid0.addWidget(selectlabel, 6, 0)
        self.selectmethod_combo = RadioSet([
            {"label": "Single", "value": "single"},
            {"label": "All", "value": "all"},
            # {"label": "Rectangle", "value": "rectangle"}
        ])
        grid0.addWidget(self.selectmethod_combo, 6, 1)

        self.layout.addStretch()


class ToolsFilmPrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Cutout Tool Options", parent=parent)
        super(ToolsFilmPrefGroupUI, self).__init__(self)

        self.setTitle(str("Film Tool Options"))

        ## Board cuttout
        self.film_label = QtWidgets.QLabel("<b>Parameters:</b>")
        self.film_label.setToolTip(
            "Create a PCB film from a Gerber or Geometry\n"
            "FlatCAM object.\n"
            "The file is saved in SVG format."
        )
        self.layout.addWidget(self.film_label)

        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)

        self.film_type_radio = RadioSet([{'label': 'Pos', 'value': 'pos'}, {'label': 'Neg', 'value': 'neg'}])
        ftypelbl = QtWidgets.QLabel('Film Type:')
        ftypelbl.setToolTip(
            "Generate a Positive black film or a Negative film.\n"
            "Positive means that it will print the features\n"
            "with black on a white canvas.\n"
            "Negative means that it will print the features\n"
            "with white on a black canvas.\n"
            "The Film format is SVG."
        )
        grid0.addWidget(ftypelbl, 0, 0)
        grid0.addWidget(self.film_type_radio, 0, 1)

        self.film_boundary_entry = FCEntry()
        self.film_boundary_label = QtWidgets.QLabel("Border:")
        self.film_boundary_label.setToolTip(
            "Specify a border around the object.\n"
            "Only for negative film.\n"
            "It helps if we use as a Box Object the same \n"
            "object as in Film Object. It will create a thick\n"
            "black bar around the actual print allowing for a\n"
            "better delimitation of the outline features which are of\n"
            "white color like the rest and which may confound with the\n"
            "surroundings if not for this border."
        )
        grid0.addWidget(self.film_boundary_label, 1, 0)
        grid0.addWidget(self.film_boundary_entry, 1, 1)

        self.film_scale_entry = FCEntry()
        self.film_scale_label = QtWidgets.QLabel("Scale Stroke:")
        self.film_scale_label.setToolTip(
            "Scale the line stroke thickness of each feature in the SVG file.\n"
            "It means that the line that envelope each SVG feature will be thicker or thinner,\n"
            "therefore the fine features may be more affected by this parameter."
        )
        grid0.addWidget(self.film_scale_label, 2, 0)
        grid0.addWidget(self.film_scale_entry, 2, 1)

        self.layout.addStretch()


class ToolsPanelizePrefGroupUI(OptionsGroupUI):
    def __init__(self, parent=None):
        # OptionsGroupUI.__init__(self, "Cutout Tool Options", parent=parent)
        super(ToolsPanelizePrefGroupUI, self).__init__(self)

        self.setTitle(str("Panelize Tool Options"))

        ## Board cuttout
        self.panelize_label = QtWidgets.QLabel("<b>Parameters:</b>")
        self.panelize_label.setToolTip(
            "Create an object that contains an array of (x, y) elements,\n"
            "each element is a copy of the source object spaced\n"
            "at a X distance, Y distance of each other."
        )
        self.layout.addWidget(self.panelize_label)

        grid0 = QtWidgets.QGridLayout()
        self.layout.addLayout(grid0)

        ## Spacing Columns
        self.pspacing_columns = FCEntry()
        self.spacing_columns_label = QtWidgets.QLabel("Spacing cols:")
        self.spacing_columns_label.setToolTip(
            "Spacing between columns of the desired panel.\n"
            "In current units."
        )
        grid0.addWidget(self.spacing_columns_label, 0, 0)
        grid0.addWidget(self.pspacing_columns, 0, 1)

        ## Spacing Rows
        self.pspacing_rows = FCEntry()
        self.spacing_rows_label = QtWidgets.QLabel("Spacing rows:")
        self.spacing_rows_label.setToolTip(
            "Spacing between rows of the desired panel.\n"
            "In current units."
        )
        grid0.addWidget(self.spacing_rows_label, 1, 0)
        grid0.addWidget(self.pspacing_rows, 1, 1)

        ## Columns
        self.pcolumns = FCEntry()
        self.columns_label = QtWidgets.QLabel("Columns:")
        self.columns_label.setToolTip(
            "Number of columns of the desired panel"
        )
        grid0.addWidget(self.columns_label, 2, 0)
        grid0.addWidget(self.pcolumns, 2, 1)

        ## Rows
        self.prows = FCEntry()
        self.rows_label = QtWidgets.QLabel("Rows:")
        self.rows_label.setToolTip(
            "Number of rows of the desired panel"
        )
        grid0.addWidget(self.rows_label, 3, 0)
        grid0.addWidget(self.prows, 3, 1)

        ## Constrains
        self.pconstrain_cb = FCCheckBox("Constrain within:")
        self.pconstrain_cb.setToolTip(
            "Area define by DX and DY within to constrain the panel.\n"
            "DX and DY values are in current units.\n"
            "Regardless of how many columns and rows are desired,\n"
            "the final panel will have as many columns and rows as\n"
            "they fit completely within selected area."
        )
        grid0.addWidget(self.pconstrain_cb, 4, 0)

        self.px_width_entry = FCEntry()
        self.x_width_lbl = QtWidgets.QLabel("Width (DX):")
        self.x_width_lbl.setToolTip(
            "The width (DX) within which the panel must fit.\n"
            "In current units."
        )
        grid0.addWidget(self.x_width_lbl, 5, 0)
        grid0.addWidget(self.px_width_entry, 5, 1)

        self.py_height_entry = FCEntry()
        self.y_height_lbl = QtWidgets.QLabel("Height (DY):")
        self.y_height_lbl.setToolTip(
            "The height (DY)within which the panel must fit.\n"
            "In current units."
        )
        grid0.addWidget(self.y_height_lbl, 6, 0)
        grid0.addWidget(self.py_height_entry, 6, 1)

        self.layout.addStretch()


class FlatCAMActivityView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setMinimumWidth(200)

        self.icon = QtWidgets.QLabel(self)
        self.icon.setGeometry(0, 0, 16, 12)
        self.movie = QtGui.QMovie("share/active.gif")
        self.icon.setMovie(self.movie)
        # self.movie.start()

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(layout)

        layout.addWidget(self.icon)
        self.text = QtWidgets.QLabel(self)
        self.text.setText("Idle.")

        layout.addWidget(self.text)

    def set_idle(self):
        self.movie.stop()
        self.text.setText("Idle.")

    def set_busy(self, msg):
        self.movie.start()
        self.text.setText(msg)


class FlatCAMInfoBar(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(FlatCAMInfoBar, self).__init__(parent=parent)

        self.icon = QtWidgets.QLabel(self)
        self.icon.setGeometry(0, 0, 12, 12)
        self.pmap = QtGui.QPixmap('share/graylight12.png')
        self.icon.setPixmap(self.pmap)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        self.setLayout(layout)

        layout.addWidget(self.icon)

        self.text = QtWidgets.QLabel(self)
        self.text.setText("Hello!")
        self.text.setToolTip("Hello!")

        layout.addWidget(self.text)

        layout.addStretch()

    def set_text_(self, text):
        self.text.setText(text)
        self.text.setToolTip(text)

    def set_status(self, text, level="info"):
        level = str(level)
        self.pmap.fill()
        if level == "ERROR" or level == "ERROR_NOTCL":
            self.pmap = QtGui.QPixmap('share/redlight12.png')
        elif level == "success":
            self.pmap = QtGui.QPixmap('share/greenlight12.png')
        elif level == "WARNING" or level == "WARNING_NOTCL":
            self.pmap = QtGui.QPixmap('share/yellowlight12.png')
        else:
            self.pmap = QtGui.QPixmap('share/graylight12.png')

        self.icon.setPixmap(self.pmap)
        self.set_text_(text)
# end of file
