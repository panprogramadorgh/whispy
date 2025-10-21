# ============================================================
#  PrepareFFMPEG
#  Provides a cmake function in charge of configuring, compiling and linking some essential ffmpeg libraries.
# ============================================================

include(ExternalProject)
include("WHISPY_RunpathUtils")

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
	add_dependencies(${target} ffmpeg)

	# --- Links the libraries ---
	foreach(LIB_PATH IN ITEMS ${FFMPEG_LIBS})
		get_filename_component(LIB_NAME ${LIB_PATH} NAME_WE)
		string(REPLACE "lib" "" LIB_NAME ${LIB_NAME})	
		set(IMPORTED_TARGET "ffmpeg_${LIB_NAME}")

		# Imported library target
		add_library(${IMPORTED_TARGET} SHARED IMPORTED)
		set_target_properties(${IMPORTED_TARGET} PROPERTIES
			IMPORTED_LOCATION ${LIB_PATH}	
		)

		target_link_libraries(${target} PRIVATE ${IMPORTED_TARGET})
	endforeach()

	# Header files
	target_include_directories(${target} PRIVATE "${CMAKE_SOURCE_DIR}/lib/ffmpeg")

	# Modifies libraries' RUNPATH configuration
	add_runpath_to_binaries(${FFMPEG_LIBS} "\$ORIGIN")

endfunction()