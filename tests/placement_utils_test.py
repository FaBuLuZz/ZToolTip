from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtCore import QPoint, QSize
from src.ztooltip import TooltipPlacement
from src.ztooltip.placement_utils import PlacementUtils


def test_get_optimal_placement(qtbot):
    """Test getting the optimal placement"""

    window = QMainWindow()
    button = QPushButton(window)
    qtbot.addWidget(window)
    qtbot.addWidget(button)

    # Left placement
    window.setFixedSize(500, 250)
    button.move(400, 100)
    placement = PlacementUtils.get_optimal_placement(button)
    assert placement == TooltipPlacement.LEFT

    # Right placement
    button.move(0, 100)
    placement = PlacementUtils.get_optimal_placement(button)
    assert placement == TooltipPlacement.RIGHT

    # Top placement
    button.move(250, 250)
    placement = PlacementUtils.get_optimal_placement(button)
    assert placement == TooltipPlacement.TOP

    # Bottom placement
    button.move(250, 0)
    placement = PlacementUtils.get_optimal_placement(button)
    assert placement == TooltipPlacement.BOTTOM
