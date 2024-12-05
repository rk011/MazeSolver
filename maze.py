import random
from tkinter import Tk, BOTH, Canvas
import time


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Randomized Maze Solver")
        self.__root.geometry(f"{width}x{height}")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)


class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win

        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self.visited = False

    def draw(self):
        if not self._win:
            return  # Skip drawing if no window is provided

        # Overwrite removed walls with background color
        if not self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "#d9d9d9")
        if not self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "#d9d9d9")
        if not self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "#d9d9d9")
        if not self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "#d9d9d9")

        # Draw existing walls
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "black")

    def draw_move(self, to_cell, undo=False):
        fill_color = "red" if not undo else "gray"
        from_x = (self._x1 + self._x2) // 2
        from_y = (self._y1 + self._y2) // 2
        to_x = (to_cell._x1 + to_cell._x2) // 2
        to_y = (to_cell._y1 + to_cell._y2) // 2
        self._win.draw_line(Line(Point(from_x, from_y), Point(to_x, to_y)), fill_color)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def _create_cells(self):
        for i in range(self._num_rows):
            row = []
            for j in range(self._num_cols):
                row.append(self._create_cell(i, j))
            self._cells.append(row)

    def _create_cell(self, i, j):
        x1 = self._x1 + j * self._cell_size_x
        y1 = self._y1 + i * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        cell = Cell(x1, y1, x2, y2, self._win)
        if self._win:
            cell.draw()
        return cell

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        entrance.draw()

        exit_cell = self._cells[-1][-1]
        exit_cell.has_bottom_wall = False
        exit_cell.draw()

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            directions = []

            if i > 0 and not self._cells[i - 1][j].visited:  # Up
                directions.append(("up", i - 1, j))
            if i < self._num_rows - 1 and not self._cells[i + 1][j].visited:  # Down
                directions.append(("down", i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:  # Left
                directions.append(("left", i, j - 1))
            if j < self._num_cols - 1 and not self._cells[i][j + 1].visited:  # Right
                directions.append(("right", i, j + 1))

            if not directions:
                return

            direction, next_i, next_j = random.choice(directions)

            if direction == "up":
                current_cell.has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif direction == "down":
                current_cell.has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False
            elif direction == "left":
                current_cell.has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif direction == "right":
                current_cell.has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False

            self._break_walls_r(next_i, next_j)

    def _animate(self):
        if self._win:
            self._win.redraw()
            time.sleep(0.05)

    def solve(self):
        self._reset_cells_visited()
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True  # Reached the end

        directions = [
            ("up", i - 1, j, current_cell.has_top_wall),
            ("down", i + 1, j, current_cell.has_bottom_wall),
            ("left", i, j - 1, current_cell.has_left_wall),
            ("right", i, j + 1, current_cell.has_right_wall),
        ]

        for direction, next_i, next_j, has_wall in directions:
            if 0 <= next_i < self._num_rows and 0 <= next_j < self._num_cols:
                next_cell = self._cells[next_i][next_j]
                if not has_wall and not next_cell.visited:
                    current_cell.draw_move(next_cell)
                    if self._solve_r(next_i, next_j):
                        return True
                    current_cell.draw_move(next_cell, undo=True)

        return False  # Dead end

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

if __name__ == "__main__":
    win = Window(800, 800)
    maze = Maze(10, 10, 10, 10, 50, 50, win)
    maze.solve()
    win.wait_for_close()
