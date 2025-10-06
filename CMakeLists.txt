cmake_minimum_required(VERSION 3.16)
project(whisperpy)

set(TARGET ${PROJECT_NAME})

# Config whisperpy wrapper
file(GLOB BACKEND_SOURCES "${CMAKE_SOURCE_DIR}/src/whisperpy/*.cpp")
add_library(${TARGET} SHARED ${BACKEND_SOURCES})

target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/src/whisperpy")
target_compile_features(${TARGET} PUBLIC cxx_std_23)

set_target_properties(${TARGET} PROPERTIES BUILD_RPATH "$ORIGIN/../lib")

# Config whisper.cpp
add_subdirectory("${CMAKE_SOURCE_DIR}/lib/whisper.cpp")
set_target_properties(whisper PROPERTIES BUILD_RPATH "$ORIGIN")
set_target_properties(ggml PROPERTIES BUILD_RPATH "$ORIGIN")
set_target_properties(ggml-base PROPERTIES BUILD_RPATH "$ORIGIN")
set_target_properties(ggml-cpu PROPERTIES BUILD_RPATH "$ORIGIN")

target_link_libraries(${TARGET} PUBLIC whisper)

# C++ Tests

add_subdirectory("${CMAKE_SOURCE_DIR}/tests/low-lvl-api")
