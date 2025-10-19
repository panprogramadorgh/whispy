# ============================================================
#  PrepareFFMPEG
#  Provides a cmake function in charge of configuring, compiling and linking some essential ffmpeg libraries.
# ============================================================

include(ExternalProject)

function(prepare_ffmpeg target)

# Output ffmpeg libraries
set(FFMPEG_LIBS
	"${PROJECT_LIB_DIR}/libavutil/libavutil.so"	
	"${PROJECT_LIB_DIR}/libswresample/libswresample.so"	
	"${PROJECT_LIB_DIR}/libavcodec/libavcodec.so"	
	"${PROJECT_LIB_DIR}/libavformat/libavformat.so"	
)

# --- FFMPEG configuration  ---
ExternalProject_Add(ffmpeg 
	SOURCE_DIR "${CMAKE_SOURCE_DIR}/lib/ffmpeg"
	CONFIGURE_COMMAND 
		bash -c "
			cd ${CMAKE_SOURCE_DIR}/lib/ffmpeg && \
			env CC=gcc CFLAGS=\"-std=c11 -O3\" ./configure \
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
add_dependencies(${target} ffmpeg)

# Links the libraries and makes them visible
target_link_libraries(${target} PRIVATE ${FFMPEG_LIBS})
target_include_directories(${target} PRIVATE "${CMAKE_SOURCE_DIR}/lib/ffmpeg")

# --- Modifies libraries' RUNPATH configuration ---
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
# TODO: Finish

elseif(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    message(STATUS "Compiling Windows environment")
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    message(STATUS "Compiling macOS environment")
endif()

endfunction()