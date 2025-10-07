cmake_minimum_required(VERSION 3.16)
project(whisperpy)

set(CMAKE_BUILD_RPATH "$ORIGIN")

# Config whisperpy wrapper
set(TARGET ${PROJECT_NAME})
file(GLOB BACKEND_SOURCES "${CMAKE_SOURCE_DIR}/src/whisperpy/*.cpp")
add_library(${TARGET} SHARED ${BACKEND_SOURCES})
target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/src/whisperpy")
target_compile_features(${TARGET} PUBLIC cxx_std_23)

# Config whisper.cpp
add_subdirectory("${CMAKE_SOURCE_DIR}/lib/whisper.cpp")
target_link_libraries(${TARGET} PUBLIC whisper)

# C++ Tests

add_subdirectory("${CMAKE_SOURCE_DIR}/tests/low-lvl-api")
