from qtpy.QtWidgets import QWidget
from qtpy.QtCore import QPoint
from .enums import TooltipPlacement
from .utils import Utils


class PlacementUtils:

    @staticmethod
    def get_optimal_placement(widget: QWidget, triangle_size: int, border_radius: int) -> TooltipPlacement:
        """Calculate the optimal placement of a tooltip based on the widget,
        triangle size, and border radius.

        :param widget: widget of the tooltip
        :param triangle_size: size of the tooltip triangle
        :param border_radius: border radius of the tooltip
        :return: optimal placement
        """
        top_level_parent = Utils.get_top_level_parent(widget)
        top_level_parent_geometry = top_level_parent.geometry()
        widget_pos = widget.mapToGlobal(QPoint(0, 0))
        widget_center_x = widget_pos.x() + widget.width() // 2

        min_space_required = 2 * triangle_size + border_radius

        # Available space left and right from widget center
        left_space_from_center = widget_center_x - top_level_parent.pos().x()
        right_space_from_center = top_level_parent_geometry.right() - widget_center_x

        # Available space top and bottom
        top_space = widget_pos.y() - top_level_parent.pos().y()
        bottom_space = top_level_parent_geometry.bottom() - widget_pos.y() - widget.height()

        # Available space left and right
        left_space = widget_pos.x() - top_level_parent.pos().x()
        right_space = top_level_parent_geometry.right() - widget_pos.x() - widget.width()

        # Check if top/bottom placement is possible
        can_place_top_bottom = (left_space_from_center > min_space_required and 
                               right_space_from_center > min_space_required)

        # Check if left/right placement is possible
        can_place_left_right = (top_space > min_space_required and 
                               bottom_space > min_space_required)

        if can_place_top_bottom:
            return TooltipPlacement.TOP if top_space >= bottom_space else TooltipPlacement.BOTTOM
        elif can_place_left_right:
            return TooltipPlacement.RIGHT if right_space >= left_space else TooltipPlacement.LEFT
        else:
            # Fallback: choose placement with most available space
            spaces = [
                (TooltipPlacement.LEFT, left_space),
                (TooltipPlacement.RIGHT, right_space),
                (TooltipPlacement.TOP, top_space),
                (TooltipPlacement.BOTTOM, bottom_space)
            ]
            return max(spaces, key=lambda x: x[1])[0]
