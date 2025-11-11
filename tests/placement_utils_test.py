from PyQt6.QtWidgets import QMainWindow, QPushButton
from src.ztooltip import TooltipPlacement
from src.ztooltip.placement_utils import PlacementUtils


def test_get_optimal_placement(qtbot):
    """Test getting the optimal placement"""

    window = QMainWindow()
    button = QPushButton(window)
    qtbot.addWidget(window)
    qtbot.addWidget(button)

    button.setFixedSize(10, 10)
    window.setFixedSize(20, 20)

    # Left placement
    button.move(5, 5)
    placement = PlacementUtils.get_optimal_placement(button, 5, 2)
    assert placement == TooltipPlacement.LEFT

    # Right placement
    button.move(0, 5)
    placement = PlacementUtils.get_optimal_placement(button, 5, 2)
    assert placement == TooltipPlacement.RIGHT

    # Top placement
    button.move(5, 10)
    placement = PlacementUtils.get_optimal_placement(button, 5, 2)
    assert placement == TooltipPlacement.TOP

    # Bottom placement
    button.move(5, 0)
    placement = PlacementUtils.get_optimal_placement(button, 5, 2)
    assert placement == TooltipPlacement.BOTTOM
