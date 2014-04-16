# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import tank

from tank.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

def show_help_screen(parent, bundle, pixmaps):
    """
    Show help screen window.
    
    :param parent: Parent window. The help screen will be centered on top of this window.
    :param bundle: Bundle object to associate with (app, engine, framework)
    :param pixmaps: List of QPixmap objects, all 650x400 px    
    """
    gui = Dialog(parent, bundle, pixmaps)    
    gui.show()
    # center on top of parent window
    gui.move(gui.parent().window().frameGeometry().center() - gui.window().rect().center())
    gui.repaint()

class Dialog(QtGui.QDialog):
    """
    Simple list widget which hosts a square thumbnail, header text
    and body text. It has a fixed size.
    
    This class is typically used in conjunction with a QT View and the 
    ShotgunDelegate class. 
    """
    
    def __init__(self, parent, bundle, pixmaps):
        """
        Constructor.
        
        :param parent: Parent window. The help screen will be centered on top of this window.
        :param bundle: Bundle object to associate with (app, engine, framework)
        :param pixmaps: List of QPixmap objects, all 650x400 px        
        """
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
        
        self._bundle = bundle

        # set up the UI
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
        if self._bundle.documentation_url is None:
            self.ui.view_documentation.setEnabled(False)
        
        self.ui.view_documentation.clicked.connect(self._on_doc)
        self.ui.close.clicked.connect(self.close)
        
        self.ui.left_arrow.clicked.connect(self._on_left_arrow_click)
        self.ui.right_arrow.clicked.connect(self._on_right_arrow_click)
        
        # make GC happy
        self._widgets = []
        self._pages = []
        
        for p in pixmaps:
            
            if p.width() != 650 or p.height() != 400:
                raise tank.TankError("Images must be 650x400px!")
            
            page = QtGui.QWidget()
            self._pages.append(page)
            layout = QtGui.QVBoxLayout(page)
            layout.setContentsMargins(2, 2, 2, 2)
            label = QtGui.QLabel(page)
            label.setMinimumSize(QtCore.QSize(650, 400))
            label.setMaximumSize(QtCore.QSize(650, 400))
            label.setPixmap(p)
            label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(label)
            self.ui.stackedWidget.addWidget(page)
            self._widgets.extend([p, page, layout, label])
        
        # set first page
        self.ui.stackedWidget.setCurrentIndex(0)
        self._num_images = len(pixmaps)
        
    def _on_left_arrow_click(self):
        """
        User clicks the left arrow
        """
        start_index = self.ui.stackedWidget.currentIndex()
        
        prev_index = start_index-1
        if prev_index < 0:
            prev_index = self._num_images-1
        
        this_page = self._pages[start_index]
        prev_page = self._pages[prev_index]
        
        # rest positions
        prev_page.move(prev_page.x()-650, prev_page.y())
        self.ui.stackedWidget.setCurrentIndex(prev_index)
        this_page.show()
        this_page.raise_()       
        
        self.anim = QtCore.QPropertyAnimation(this_page, "pos")
        self.anim.setDuration(600)
        self.anim.setStartValue(QtCore.QPoint(this_page.x(), this_page.y()))
        self.anim.setEndValue(QtCore.QPoint(this_page.x()+650, this_page.y()))
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self.anim2 = QtCore.QPropertyAnimation(prev_page, "pos")
        self.anim2.setDuration(600)
        self.anim2.setStartValue(QtCore.QPoint(prev_page.x()-650, prev_page.y()))
        self.anim2.setEndValue(QtCore.QPoint(prev_page.x(), prev_page.y()))
        self.anim2.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self.grp = QtCore.QParallelAnimationGroup()
        self.grp.addAnimation(self.anim)
        self.grp.addAnimation(self.anim2)
        self.grp.start()
        
        
        
    def _on_right_arrow_click(self):
        """
        User clicks the left arrow
        """
        start_index = self.ui.stackedWidget.currentIndex()
        
        next_index = (start_index+1) % self._num_images
        
        this_page = self._pages[start_index]
        next_page = self._pages[next_index]
        
        # rest positions
        next_page.move(next_page.x()+650, next_page.y())
        self.ui.stackedWidget.setCurrentIndex(next_index)
        this_page.show()
        this_page.raise_()       
        
        self.anim = QtCore.QPropertyAnimation(this_page, "pos")
        self.anim.setDuration(600)
        self.anim.setStartValue(QtCore.QPoint(this_page.x(), this_page.y()))
        self.anim.setEndValue(QtCore.QPoint(this_page.x()-650, this_page.y()))
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self.anim2 = QtCore.QPropertyAnimation(next_page, "pos")
        self.anim2.setDuration(600)
        self.anim2.setStartValue(QtCore.QPoint(next_page.x()+650, next_page.y()))
        self.anim2.setEndValue(QtCore.QPoint(next_page.x(), next_page.y()))
        self.anim2.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self.grp = QtCore.QParallelAnimationGroup()
        self.grp.addAnimation(self.anim)
        self.grp.addAnimation(self.anim2)
        self.grp.start()
        
    def _on_doc(self):
        """
        Launch doc url.
        """
        self._bundle.log_debug("Opening documentation url %s..." % self._bundle.documentation_url)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self._bundle.documentation_url))
        
        
        
        
        