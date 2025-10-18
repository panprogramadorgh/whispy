cmake_minimum_required(VERSION 3.16)
project(generic_audio_decoder)

set(TARGET ${PROJECT_NAME})
add_executable(${TARGET} "${CMAKE_SOURCE_DIR}/sandbox/generic_audio_decoder_libav/main.cpp")
target_link_libraries(${TARGET} PUBLIC whispy)