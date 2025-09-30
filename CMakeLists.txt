cmake_minimum_required(VERSION 3.16)
project(whisperpy)

set(TARGET ${PROJECT_NAME})

file(GLOB BACKEND_SOURCES "${CMAKE_SOURCE_DIR}/src/backend/*.cpp")
list(REMOVE_ITEM BACKEND_SOURCES "${CMAKE_SOURCE_DIR}/src/backend/whisper.cpp")
add_library(${TARGET} SHARED ${BACKEND_SOURCES})
add_subdirectory("${CMAKE_SOURCE_DIR}/src/backend/whisper.cpp")

target_compile_features(${TARGET} PUBLIC cxx_std_23)
target_link_libraries(${TARGET} PUBLIC whisper)
# template implementations
target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/src/backend")
target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/include")

# tests

add_subdirectory("${CMAKE_SOURCE_DIR}/tests/low-lvl-api")
