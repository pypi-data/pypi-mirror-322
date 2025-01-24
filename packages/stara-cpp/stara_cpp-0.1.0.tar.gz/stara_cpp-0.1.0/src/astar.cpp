#include "astar.hpp"
#include <algorithm>
#include <iostream>
std::pair<int, int> AStar::getLowestFScoreNode(
    const std::unordered_map<std::pair<int, int>, int, PairHash>& fScores,
    const std::unordered_set<std::pair<int, int>, PairHash>& openSet
) {
    if (openSet.empty()) {
        throw std::runtime_error("Cannot get lowest f-score from empty set");
    }

    return *std::min_element(
        openSet.begin(), 
        openSet.end(),
        [&fScores](const auto& a, const auto& b) {
            return fScores.at(a) < fScores.at(b);
        }
    );
}

std::optional<std::vector<std::pair<int, int>>> AStar::findPath(
    const std::pair<int, int>& start,
    const std::pair<int, int>& goal
) {
    // Pre-allocate containers with reasonable initial sizes
    std::unordered_map<std::pair<int, int>, int, PairHash> gScores;
    gScores.reserve(maze_.getWidth() * maze_.getHeight());
    gScores[start] = 0;

    std::unordered_map<std::pair<int, int>, int, PairHash> fScores;
    fScores.reserve(maze_.getWidth() * maze_.getHeight());
    fScores[start] = manhattanDistance(start, goal);

    std::unordered_map<std::pair<int, int>, std::pair<int, int>, PairHash> cameFrom;
    cameFrom.reserve(maze_.getWidth() * maze_.getHeight());

    std::unordered_set<std::pair<int, int>, PairHash> openSet;
    openSet.reserve(maze_.getWidth() * maze_.getHeight());
    openSet.insert(start);

    std::unordered_set<std::pair<int, int>, PairHash> closedSet;
    closedSet.reserve(maze_.getWidth() * maze_.getHeight());

    try {
        while (!openSet.empty()) {
            auto currentPos = getLowestFScoreNode(fScores, openSet);
            openSet.erase(currentPos);

            if (closedSet.find(currentPos) != closedSet.end()) {
                continue;
            }

            if (currentPos == goal) {
                std::vector<std::pair<int, int>> path;
                path.reserve(gScores[currentPos]); // Reserve space for the expected path length
                auto current = currentPos;
                while (cameFrom.find(current) != cameFrom.end()) {
                    path.push_back(current);
                    current = cameFrom[current];
                }
                path.push_back(start);
                std::reverse(path.begin(), path.end());
                return path;
            }

            closedSet.insert(currentPos);

            auto neighbors = maze_.getCellNeighbours(currentPos.first, currentPos.second);
            for (const auto& next : neighbors) {
                auto nextPos = std::make_pair(std::get<0>(next), std::get<1>(next));
                int value = std::get<2>(next);

                if (value == 0 || closedSet.find(nextPos) != closedSet.end()) {
                    continue;
                }

                int tentativeG = gScores[currentPos] + 1;

                if (gScores.find(nextPos) == gScores.end() || tentativeG < gScores[nextPos]) {
                    cameFrom[nextPos] = currentPos;
                    gScores[nextPos] = tentativeG;
                    fScores[nextPos] = tentativeG + manhattanDistance(nextPos, goal);
                    openSet.insert(nextPos);
                }
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return std::nullopt;
    }

    return std::nullopt;
} 