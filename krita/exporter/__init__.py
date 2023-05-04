from krita import DockWidgetFactory, DockWidgetFactoryBase
from .exporter import Exporter

dock_widget_factory = DockWidgetFactory("exporter", DockWidgetFactoryBase.DockRight, Exporter)
Krita.instance().addDockWidgetFactory(dock_widget_factory)
