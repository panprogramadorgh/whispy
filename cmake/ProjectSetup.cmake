# ============================================================
#  ProjectSetup.cmake
#  Main compilation configurations
# ============================================================

# --- Explicit CMake Policy ---
if(POLICY CMP0077)
    cmake_policy(SET CMP0077 NEW)  # Allows overriding options by using -D
endif()

# --- File Generator  ---

# --- Adds custom directories for modules ---
list(APPEND CMAKE_MODULE_PATH
    "${CMAKE_SOURCE_DIR}/cmake/functions"
    # "${CMAKE_SOURCE_DIR}/cmake/macros"
    # "${CMAKE_SOURCE_DIR}/cmake/modules"
)

# ============================================================
#  General compiler configuration
# ============================================================

# Simplifies library linking
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/whispy/lib")
set(CMAKE_BUILD_RPATH "$ORIGIN")

# Enforces used version of C/C++
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# --- Compilation options based on configurations ---
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type" FORCE)
endif()

message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

# Generic flags
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(COMMON_C_FLAGS "-Wall -Wextra -Wpedantic")
    set(COMMON_CXX_FLAGS "-Wall -Wextra -Wpedantic")

    set(CMAKE_C_FLAGS_DEBUG   "-O0 -g ${COMMON_C_FLAGS}")
    set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG ${COMMON_C_FLAGS}")
    set(CMAKE_CXX_FLAGS_DEBUG   "-O0 -g ${COMMON_CXX_FLAGS}")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG ${COMMON_CXX_FLAGS}")
elseif(MSVC)
    set(CMAKE_CXX_FLAGS_DEBUG   "/Zi /Od /DDEBUG")
    set(CMAKE_CXX_FLAGS_RELEASE "/O2 /DNDEBUG")
endif()

# ============================================================
#  Project global variables
# ============================================================

set(PROJECT_LIB_DIR "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}") # src/whispy/lib -> python3 package
set(PROJECT_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/include")

file(MAKE_DIRECTORY
    "${PROJECT_OUTPUT_DIR}"
    "${PROJECT_LIB_DIR}"
)

message(STATUS "Compilation environment was correctly initialized.")
