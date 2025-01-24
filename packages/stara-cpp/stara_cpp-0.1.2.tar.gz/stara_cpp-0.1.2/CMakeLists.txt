cmake_minimum_required(VERSION 3.15)
project(stara_cpp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Add the C++ library
pybind11_add_module(stara_cpp 
    src/stara_cpp.cpp
    src/astar.cpp
)

# Include directories
target_include_directories(stara_cpp PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Install the module into the Python package directory
install(TARGETS stara_cpp DESTINATION stara_cpp) 