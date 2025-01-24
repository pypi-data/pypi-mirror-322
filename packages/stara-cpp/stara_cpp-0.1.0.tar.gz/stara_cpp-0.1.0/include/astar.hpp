#pragma once
#include <vector>
#include <queue>
#include <unordered_set>
#include <unordered_map>
#include <cmath>
#include <memory>
#include <optional>

class Maze {
public:
    explicit Maze(std::vector<std::vector<int>>&& grid) noexcept 
        : grid_(std::move(grid)) {
        height_ = grid_.size();
        width_ = height_ > 0 ? grid_[0].size() : 0;
    }

    // Copy constructor for grid
    explicit Maze(const std::vector<std::vector<int>>& grid)
        : grid_(grid) {
        height_ = grid_.size();
        width_ = height_ > 0 ? grid_[0].size() : 0;
    }

    // Rule of five
    Maze(const Maze&) = default;
    Maze& operator=(const Maze&) = default;
    Maze(Maze&&) noexcept = default;
    Maze& operator=(Maze&&) noexcept = default;
    ~Maze() = default;

    [[nodiscard]] bool isValid(int x, int y) const noexcept {
        return x >= 0 && x < width_ && y >= 0 && y < height_;
    }

    [[nodiscard]] bool isWalkable(int x, int y) const noexcept {
        return isValid(x, y) && grid_[y][x] >= 1;
    }

    [[nodiscard]] std::vector<std::tuple<int, int, int>> getCellNeighbours(int x, int y) const {
        std::vector<std::tuple<int, int, int>> neighbours;
        neighbours.reserve(4);  // Pre-allocate for 4 possible neighbors
        static const std::vector<std::pair<int, int>> directions = {
            {0, 1}, {1, 0}, {0, -1}, {-1, 0}  
        };

        for (const auto& dir : directions) {
            int newX = x + dir.first;
            int newY = y + dir.second;
            if (isValid(newX, newY)) {
                neighbours.emplace_back(newX, newY, grid_[newY][newX]);
            }
        }
        return neighbours;
    }

    [[nodiscard]] int getWidth() const noexcept { return width_; }
    [[nodiscard]] int getHeight() const noexcept { return height_; }

private:
    std::vector<std::vector<int>> grid_;
    int width_;
    int height_;
};

class AStar {
public:
    struct PairHash {
        template <class T1, class T2>
        [[nodiscard]] std::size_t operator()(const std::pair<T1, T2>& p) const noexcept {
            auto h1 = std::hash<T1>{}(p.first);
            auto h2 = std::hash<T2>{}(p.second);
            return h1 ^ (h2 << 1);
        }
    };

    explicit AStar(const Maze& maze) noexcept : maze_(maze) {}

    // Rule of five (though we only need the default implementations)
    AStar(const AStar&) = default;
    AStar& operator=(const AStar&) = default;
    AStar(AStar&&) noexcept = default;
    AStar& operator=(AStar&&) noexcept = default;
    ~AStar() = default;

    [[nodiscard]] static int manhattanDistance(
        const std::pair<int, int>& pos1,
        const std::pair<int, int>& pos2
    ) noexcept {
        return std::abs(pos1.first - pos2.first) + std::abs(pos1.second - pos2.second);
    }

    [[nodiscard]] static std::pair<int, int> getLowestFScoreNode(
        const std::unordered_map<std::pair<int, int>, int, PairHash>& fScores,
        const std::unordered_set<std::pair<int, int>, PairHash>& openSet
    );

    [[nodiscard]] std::optional<std::vector<std::pair<int, int>>> findPath(
        const std::pair<int, int>& start,
        const std::pair<int, int>& goal
    );

private:
    const Maze& maze_;
}; 