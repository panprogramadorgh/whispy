cmake_minimum_required(VERSION 3.16)
project(whispy)

set(CMAKE_BUILD_RPATH "$ORIGIN")

# Config whispy wrapper
set(TARGET ${PROJECT_NAME})
file(GLOB BACKEND_SOURCES "${CMAKE_SOURCE_DIR}/src/whispy/*.cpp")
add_library(${TARGET} SHARED ${BACKEND_SOURCES})
target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/src/whispy")
target_compile_features(${TARGET} PUBLIC cxx_std_23)

# Config whisper.cpp
add_subdirectory("${CMAKE_SOURCE_DIR}/lib/whisper.cpp")
target_link_libraries(${TARGET} PUBLIC whisper)

# Config minimp3
# target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/lib/minimp3")

# C++ Tests

add_subdirectory("${CMAKE_SOURCE_DIR}/tests/low-lvl-api")

# C++ Sandbox

add_subdirectory("${CMAKE_SOURCE_DIR}/sandbox/audio_decoding_minimp3")