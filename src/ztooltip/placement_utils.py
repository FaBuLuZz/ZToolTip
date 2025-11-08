from qtpy.QtWidgets import QWidget, QApplication
from qtpy.QtCore import QRect, QSize, QPoint
from .enums import TooltipPlacement
from .utils import Utils


class PlacementUtils:

    @staticmethod
    def get_optimal_placement(widget: QWidget, size: QSize, triangle_size: int) -> TooltipPlacement:
        """Calculate the optimal placement of a tooltip based on the widget,
        size and triangle size.

        :param widget: widget of the tooltip
        :param size: size of the tooltip
        :param triangle_size: size of the triangle
        :return: optimal placement
        """

        top_level_parent = Utils.get_top_level_parent(widget)
        top_level_parent_pos = top_level_parent.pos()
        top_level_parent_geometry = top_level_parent.geometry()
        widget_pos = widget.mapToGlobal(QPoint(0, 0))

        # Calculate available space for placements
        left_space = widget_pos.x() - top_level_parent_pos.x()
        right_space = top_level_parent_geometry.right() - (widget_pos.x() + widget.width())
        top_space = widget_pos.y() - top_level_parent_pos.y()
        bottom_space = top_level_parent_geometry.bottom() - (widget_pos.y() + widget.height())
        space_placement_map = {
            right_space:  TooltipPlacement.RIGHT,
            left_space:   TooltipPlacement.LEFT,
            top_space:    TooltipPlacement.TOP,
            bottom_space: TooltipPlacement.BOTTOM
        }

        # Return most optimal placement that also fits on screen
        optimal_placement = None
        for space, placement in sorted(space_placement_map.items(), reverse=True):
            if not optimal_placement:
                optimal_placement = placement

            tooltip_rect = PlacementUtils.__get_tooltip_rect(
                widget, placement, size, triangle_size
            )
            if PlacementUtils.__rect_contained_by_screen(tooltip_rect):
                return placement

        return optimal_placement

    @staticmethod
    def __rect_contained_by_screen(rect: QRect) -> bool:
        """Check if a rect is fully contained by a single screen

        :param rect: rect that should be checked
        :return: whether the rect is contained by a screen
        """

        for screen in QApplication.screens():
            if screen.geometry().contains(rect):
                return True
        return False

    @staticmethod
    def __get_tooltip_rect(widget: QWidget, placement: TooltipPlacement, size: QSize,
                           triangle_size: int) -> QRect:
        """Get the rect of a tooltip based on the widget position,
        placement, size and triangle size of the tooltip

        :param widget: widget of the tooltip
        :param placement: placement of the tooltip
        :param size: size of the tooltip
        :param triangle_size: size of the triangle
        :return: rect of the tooltip
        """

        widget_pos = widget.mapToGlobal(QPoint(0, 0))
        rect = QRect()

        # Calculate rect depending on placement
        if placement == TooltipPlacement.TOP:
            rect.setX(int(widget_pos.x() + widget.width() / 2 - size.width() / 2))
            rect.setY(widget_pos.y() - size.height() - triangle_size)
            rect.setRight(rect.x() + size.width())
            rect.setBottom(rect.y() + size.height() + triangle_size)
        elif placement == TooltipPlacement.BOTTOM:
            rect.setX(int(widget_pos.x() + widget.width() / 2 - size.width() / 2))
            rect.setY(widget_pos.y() + widget.height())
            rect.setRight(rect.x() + size.width())
            rect.setBottom(rect.y() + size.height() + triangle_size)
        elif placement == TooltipPlacement.LEFT:
            rect.setX(widget_pos.x() - size.width() - triangle_size)
            rect.setY(int(widget_pos.y() + widget.height() / 2 - size.width() / 2))
            rect.setRight(rect.x() + size.width() + triangle_size)
            rect.setBottom(rect.y() + size.height())
        elif placement == TooltipPlacement.RIGHT:
            rect.setX(widget_pos.x() + widget.width())
            rect.setY(int(widget_pos.y() + widget.height() / 2 - size.width() / 2))
            rect.setRight(rect.x() + size.width() + triangle_size)
            rect.setBottom(rect.y() + size.height())

        return rect
