# ============================================================
#  Whispy
#  Speech to text library
# ============================================================

# --- Minimum version of CMake allowd by the project ---
cmake_minimum_required(VERSION 3.26)

# --- Declares the name and the used languages for the project ---
project(whispy LANGUAGES C CXX)

# --- Includes ---
include("cmake/ProjectSetup.cmake")
include("WHISPY_DetectTools")
include("WHISPY_PrepareFFMPEG")

# --- Creating whispy target ---
set(TARGET ${PROJECT_NAME})
file(GLOB BACKEND_SOURCES "${CMAKE_SOURCE_DIR}/src/whispy/*.cpp")
add_library(${TARGET} SHARED ${BACKEND_SOURCES})
target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/src/whispy")
target_compile_features(${TARGET} PUBLIC cxx_std_23)

# --- Configuring whispy dependencies ---

# whisper.cpp
add_subdirectory("${CMAKE_SOURCE_DIR}/lib/whisper.cpp")
target_link_libraries(${TARGET} PUBLIC whisper)

# ffmpeg
prepare_ffmpeg(${TARGET})

# --- C++ Tests & Sandbox envs ---
add_subdirectory("${CMAKE_SOURCE_DIR}/tests/low-lvl-api")
add_subdirectory("${CMAKE_SOURCE_DIR}/sandbox")