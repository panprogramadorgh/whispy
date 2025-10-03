cmake_minimum_required(VERSION 3.16)
project(whisperpy)

set(TARGET ${PROJECT_NAME})

# Config whisperpy wrapper
file(GLOB BACKEND_SOURCES "${CMAKE_SOURCE_DIR}/src/backend/*.cpp")
list(REMOVE_ITEM BACKEND_SOURCES "${CMAKE_SOURCE_DIR}/src/backend/whisper.cpp")
add_library(${TARGET} SHARED ${BACKEND_SOURCES})

target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/src/backend")

target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/include")
target_compile_features(${TARGET} PUBLIC cxx_std_23)

set_target_properties(${TARGET} PROPERTIES BUILD_RPATH "$ORIGIN/src/backend/whisper.cpp/src")

# Config whisper.cpp
add_subdirectory("${CMAKE_SOURCE_DIR}/src/backend/whisper.cpp")

set_target_properties(${TARGET} PROPERTIES BUILD_RPATH "$ORIGIN/src/backend/whisper.cpp/src")
set_target_properties(whisper PROPERTIES BUILD_RPATH "$ORIGIN/src/backend/whisper.cpp/ggml/src")

target_link_libraries(${TARGET} PUBLIC whisper)

# Testings

add_subdirectory("${CMAKE_SOURCE_DIR}/tests/low-lvl-api")
