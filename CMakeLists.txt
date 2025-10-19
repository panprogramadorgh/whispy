include("cmake/ProjectSetup.cmake")
include("PrepareFFMPEG")


# Checks the library ext name.
set(LIB_EXTNAME)
if (${CMAKE_SYSTEM_NAME} STREQUAL "Linux")
	set(LIB_EXTNAME "so")
elseif(${CMAKE_SYSTEM_NAME} STREQUAL "Windows")
	set(LIB_EXTNAME "dll")
elseif(${CMAKE_SYSTEM_NAME} STREQUAL "Darwin")
	set(LIB_EXTNAME "dylib")
else()
	message(FATAL_ERROR "Unsupported operating system")
endif()


# ---

# Configuring whispy wrapper
set(TARGET ${PROJECT_NAME})
file(GLOB BACKEND_SOURCES "${CMAKE_SOURCE_DIR}/src/whispy/*.cpp")
add_library(${TARGET} SHARED ${BACKEND_SOURCES})
target_include_directories(${TARGET} PUBLIC "${CMAKE_SOURCE_DIR}/src/whispy")
target_compile_features(${TARGET} PUBLIC cxx_std_23)

# Configuring whisper.cpp
add_subdirectory("${CMAKE_SOURCE_DIR}/lib/whisper.cpp")
target_link_libraries(${TARGET} PUBLIC whisper)

# Configuring + Building ffmpeg
ExternalProject_Add(ffmpeg 
	SOURCE_DIR "${CMAKE_SOURCE_DIR}/lib/ffmpeg"
	CONFIGURE_COMMAND 
		bash -c "
			cd ${CMAKE_SOURCE_DIR}/lib/ffmpeg && \
			env CC=gcc CFLAGS=\"-std=c11 -O3\" ./configure \
				--disable-x86asm \
				--enable-shared \
				--disable-static \
				--disable-programs \
				--disable-doc \
				--disable-avdevice \
				--disable-swscale \
				--enable-swresample \
				--disable-debug \
				--disable-gpl \
				--disable-nonfree \
				--enable-avformat \
				--enable-avcodec \
				--enable-avutil \
				--enable-demuxer='wav,flac,mp3,ogg' \
				--enable-parser='mpegaudio,flac,opus' \
				--enable-decoder='pcm_f32le,flac,opus,vorbis,mp3'"

	BUILD_COMMAND
		bash -c "cd ${CMAKE_SOURCE_DIR}/lib/ffmpeg && make -j 4"

	INSTALL_COMMAND ""
)
add_dependencies(${TARGET} ffmpeg)

# Coping and linking ffmpeg manually

set(FFMPEG_LIBS
	"libavutil"
	"libswresample"
	"libavcodec"
	"libavformat"
)
foreach(LIB_NAME IN ITEMS ${FFMPEG_LIBS})
  # Copy
  file(GLOB LIB_PATH_ALL "${CMAKE_SOURCE_DIR}/lib/ffmpeg/${LIB_NAME}/${LIB_NAME}.${LIB_EXTNAME}*")
  file(COPY ${LIB_PATH_ALL} DESTINATION "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
  # Link
  set(LIB_PATH "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${LIB_NAME}.${LIB_EXTNAME}")
  target_link_libraries(${TARGET} PUBLIC ${LIB_PATH})
endforeach()

# Adding ffmpeg headers
target_include_directories(${TARGET} PUBLIC
  "${CMAKE_SOURCE_DIR}/lib/ffmpeg"
)

# C++ Tests

add_subdirectory("${CMAKE_SOURCE_DIR}/tests/low-lvl-api")

# C++ Sandbox

add_subdirectory("${CMAKE_SOURCE_DIR}/sandbox")