cmake_minimum_required(VERSION 3.16)
project(whisperpy)

set(TARGET ${PROJECT_NAME})

add_library(${TARGET} SHARED "./whisperpy.cpp")
add_subdirectory("./whisper.cpp")

target_compile_features(${TARGET} PUBLIC cxx_std_23)
target_link_libraries(${TARGET} PUBLIC whisper)
