import unittest
from maze import Maze


class MazeTests(unittest.TestCase):
    def test_reset_cells_visited(self):
        maze = Maze(0, 0, 5, 5, 10, 10, seed=0)

        # Verify all cells are visited after maze generation
        for row in maze._cells:
            for cell in row:
                self.assertTrue(cell.visited, f"Cell at ({cell._x1}, {cell._y1}) should be visited")

        # Call reset and verify all cells are unvisited
        maze._reset_cells_visited()
        for row in maze._cells:
            for cell in row:
                self.assertFalse(cell.visited, f"Cell at ({cell._x1}, {cell._y1}) should not be visited")


if __name__ == "__main__":
    unittest.main()
