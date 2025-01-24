#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "astar.hpp"

namespace py = pybind11;

std::shared_ptr<Maze> load_maze(py::array_t<int> array) {
    py::buffer_info buf = array.request();
    if (buf.ndim != 2) {
        throw std::runtime_error("Number of dimensions must be 2");
    }

    size_t rows = buf.shape[0];
    size_t cols = buf.shape[1];
    int* ptr = static_cast<int*>(buf.ptr);

    std::vector<std::vector<int>> grid(rows, std::vector<int>(cols));
    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            grid[i][j] = ptr[i * cols + j];
        }
    }

    return std::make_shared<Maze>(grid);
}

std::optional<std::vector<std::pair<int, int>>> find_path_wrapper(
    std::shared_ptr<Maze> maze,
    std::pair<int, int> start,
    std::pair<int, int> goal
) {
    if (!maze->isValid(start.first, start.second) || !maze->isValid(goal.first, goal.second)) {
        throw std::runtime_error("Start or goal position is out of bounds");
    }
    if (!maze->isWalkable(start.first, start.second) || !maze->isWalkable(goal.first, goal.second)) {
        throw std::runtime_error("Start or goal position is not walkable");
    }

    AStar pathfinder(*maze);
    return pathfinder.findPath(start, goal);
}

PYBIND11_MODULE(stara_cpp, m) {
    m.doc() = "A* pathfinding algorithm implementation in C++";

    py::class_<Maze, std::shared_ptr<Maze>>(m, "Maze")
        .def(py::init<const std::vector<std::vector<int>>&>())
        .def("is_valid", &Maze::isValid)
        .def("is_walkable", &Maze::isWalkable)
        .def("get_cell_neighbours", &Maze::getCellNeighbours)
        .def("get_width", &Maze::getWidth)
        .def("get_height", &Maze::getHeight);

    py::class_<AStar>(m, "AStar")
        .def(py::init<const Maze&>())
        .def("manhattan_distance", &AStar::manhattanDistance)
        .def("find_path", &AStar::findPath);

    m.def("load_maze", &load_maze, "Load maze from numpy array",
          py::arg("array").noconvert());
    
    m.def("find_path", &find_path_wrapper, "Find path using A* algorithm",
          py::arg("maze"),
          py::arg("start"),
          py::arg("goal"));
} 