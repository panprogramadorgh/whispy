# ============================================================
#  RunpathUtils
#  Helps writing specific paths to binaries' RUNPATH label
# ============================================================

function(add_runpath_to_binaries binaries new_runpath)
  if(CMAKE_SYSTEM_NAME STREQUAL "Linux")

    foreach(BIN in ${binaries})
      execute_process(
          COMMAND "patchelf --add-rpath ${new_runpath} ${BIN}"
          RESULT_VARIABLE FIND_RESULT
          ERROR_VARIABLE FIND_STDERR
      )

      if(${FIND_RESULT} NOT EQUAL 0)
          message(FATAL_ERROR "patchelf failed:\n${FIND_STDERR}")
      endif()
    endforeach()

  elseif(CMAKE_SYSTEM_NAME STREQUAL "Windows")
  
    # ============================================================
    #  Windows DLLs behave as if they would already have a $ORIGIN token in RUNPATH. So aditional linking information will not be necesary to be provided fo ffmpeg libraries.
    # ============================================================

  elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")

    # Ensures the same linux $ORIGIN token semantic in mac.
    set(DARWIN_PARSED_RUNPATH "${new_runpath}")
    if("${new_runpath}" STREQUAL "$ORIGIN")
      set(DARWIN_PARSED_RUNPATH "@loader_path") 
    endif()

    foreach(BIN in ${binaries})
      execute_process(
          COMMAND "install_name_tool -add_rpath ${DARWIN_PARSED_RUNPATH} ${BIN}"
          RESULT_VARIABLE FIND_RESULT
          ERROR_VARIABLE FIND_STDERR
      )

      if(${FIND_RESULT} NOT EQUAL 0)
          message(FATAL_ERROR "patchelf failed:\n${FIND_STDERR}")
      endif()
    endforeach()

  endif()
endfunction()
