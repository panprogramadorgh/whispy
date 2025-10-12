cmake_minimum_required(VERSION 3.16)
project(low-lvl-api)

set(TARGET ${PROJECT_NAME})

add_executable(${TARGET} "./main.cpp")
set_target_properties(${TARGET} PROPERTIES BUILD_RPATH "$ORIGIN/../../lib")
target_link_libraries(${TARGET} whispy)