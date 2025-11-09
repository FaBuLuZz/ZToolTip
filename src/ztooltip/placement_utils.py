from qtpy.QtWidgets import QWidget, QApplication
from qtpy.QtCore import QRect, QSize, QPoint
from .enums import TooltipPlacement
from .utils import Utils


class PlacementUtils:

    @staticmethod
    def get_optimal_placement(widget: QWidget) -> TooltipPlacement:
        """Calculate the optimal placement of a tooltip based on the widget,
        size and triangle size.

        :param widget: widget of the tooltip
        :return: optimal placement
        """
        top_level_parent = Utils.get_top_level_parent(widget)
        top_level_parent_geometry = top_level_parent.geometry()
        widget_pos = widget.mapToGlobal(QPoint(0, 0))

        spaces = [
            (TooltipPlacement.LEFT, widget_pos.x() - top_level_parent.pos().x()),
            (TooltipPlacement.RIGHT, top_level_parent_geometry.right() - widget_pos.x() - widget.width()),
            (TooltipPlacement.TOP, widget_pos.y() - top_level_parent.pos().y()),
            (TooltipPlacement.BOTTOM, top_level_parent_geometry.bottom() - widget_pos.y() - widget.height())
        ]

        return max(spaces, key=lambda x: x[1])[0]
