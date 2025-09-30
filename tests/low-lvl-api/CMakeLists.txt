cmake_minimum_required(VERSION 3.16)
project(low-lvl-api)

set(TARGET ${PROJECT_NAME})

add_executable(${TARGET} "./main.cpp")
target_link_libraries(${TARGET} whisperpy)