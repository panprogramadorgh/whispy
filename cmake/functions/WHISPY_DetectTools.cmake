# ============================================================
#  DetectTools
#  Detects necessary tools to configure, compile and link the project.
# ============================================================

if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    find_program(PATCHELF_EXE patchelf)
    if("${PATCHELF_EXE}" STREQUAL "")
        message(FATAL_ERROR "patchelf command line tool is not available")
    endif()
elseif(CMAKE_SYSTEM_NAME STREQUAL "Windows")

    # ============================================================
    #  Windows DLLs behave as if they would already have a $ORIGIN token in RUNPATH. So aditional linking information will not be necesary to be provided fo ffmpeg libraries.
    # ============================================================

elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    find_program(INSTALL_NAME_TOOL_EXEC install_name_tool)
    if("${INSTALL_NAME_TOOL_EXEC}" STREQUAL "")
        message(FATAL_ERROR "install_name_tool command line tool is not available")
    endif()
endif()