# ============================================================
#  RunpathUtils
#  Helps writing specific paths to binaries' RUNPATH label
# ============================================================

# --- Converts Linux $ORIGIN token target's RUNPATH to @loader_path ---
function(parse_to_darwin_rpath input_rpath output_rpath)
  if(${input_rpath} STREQUAL "$ORIGIN")
    set(${output_rpath} "@loader_path")
  endif()
endfunction()

function(add_runpath_to_binaries binaries new_runpath)
  if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    find_program(PATCHELF_EXE patchelf)

    foreach(BIN in ${binaries})
      execute_process(
          COMMAND "${PATHELF_EXEC} --add-rpath ${new_runpath} ${BIN}"
          RESULT_VARIABLE FIND_RESULT
          ERROR_VARIABLE FIND_STDERR
      )
      if ("${FIND_RESULT}" AND NOT STREQUAL "0")
        message(FATAL_ERROR "patchelf failed:\n${FIND_STDERR}")
      endif()
    endforeach()

  elseif(CMAKE_SYSTEM_NAME STREQUAL "Windows")
  
    # ============================================================
    #  Windows DLLs behave as if they would already have a $ORIGIN token in RUNPATH. So aditional linking information will not be necesary to be provided fo ffmpeg libraries.
    # ============================================================

  elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    find_program(INSTALL_NAME_TOOL_EXE install_name_tool)
    parse_to_darwin_rpath(${new_runpath} DARWIN_RPATH)

    foreach(BIN in ${binaries})
      execute_process(
          COMMAND "${INSTALL_NAME_TOOL_EXE} -add_rpath ${DARWIN_RPATH} ${BIN}"
          RESULT_VARIABLE FIND_RESULT
          ERROR_VARIABLE FIND_STDERR
      )
      if ("${FIND_RESULT}" AND NOT STREQUAL "0")
          message(FATAL_ERROR "install_name_tool failed:\n${FIND_STDERR}")
      endif()
    endforeach()

  endif()
endfunction()
