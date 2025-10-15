cmake_minimum_required(VERSION 3.16)
project(test_minimp3)

set(TARGET ${PROJECT_NAME})

add_executable(${TARGET} "${CMAKE_SOURCE_DIR}/sandbox/audio_decoding_minimp3/main.cpp")
target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/lib/minimp3")