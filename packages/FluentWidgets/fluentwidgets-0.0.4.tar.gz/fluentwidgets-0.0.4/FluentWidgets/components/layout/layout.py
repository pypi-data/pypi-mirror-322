# coding:utf-8
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLayout


class HBoxLayout(QHBoxLayout):
    """ horizontal layout """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

    def addWidgets(self, widgets: List[QWidget], stretch=0, alignment=Qt.AlignmentFlag(0)):
        """ add stretch default is 0, alignment default is None widgets"""
        for widget in widgets:
            self.addWidget(widget, stretch=stretch, alignment=alignment)

    def addLayouts(self, layouts: List[QLayout], stretch=0):
        """ add stretch default is 0 layouts"""
        for layout in layouts:
            self.addLayout(layout, stretch)

    def addWidgets_(
            self, widgets: List[QWidget], stretch: List[int] | int = 1,
            alignment: List[Qt.AlignmentFlag] | Qt.AlignmentFlag = Qt.AlignmentFlag(0)
    ):
        """ add custom stretch alignment widgets"""
        stretch = [stretch for _ in range(len(widgets))] if type(stretch) is not list else stretch
        alignment = [alignment for _ in range(len(widgets))] if type(alignment) is not list else alignment
        for w, s, a in zip(widgets, stretch, alignment):
            self.addWidget(w, s, a)

    def addLayouts_(self, layouts: List[QLayout], stretches: List[int] | int = 1):
        """ add custom stretch alignment layouts"""
        stretches = [stretches for _ in range(len(layouts))] if type(stretches) is not list else stretches
        for l, s in zip(layouts, stretches):
            self.addLayout(l, s)


class VBoxLayout(QVBoxLayout, HBoxLayout):
    """ vertical layout """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)