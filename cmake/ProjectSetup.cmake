# ============================================================
#  ProjectSetup.cmake
#  Main compilation configurations
# ============================================================

# --- Minimum version of CMake allowd by the project ---
cmake_minimum_required(VERSION 3.16)

# --- Explicit CMake Policy ---
if(POLICY CMP0077)
    cmake_policy(SET CMP0077 NEW)  # Allows overriding options by using -D
endif()

# --- Declares the name and the used languages for the project ---
project(whispy LANGUAGES C CXX)

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
set(CMAKE_BUILD_RPATH "$ORIGIN") # TODO: External project doesn't configure RUNPATH for ffmpeg libraries.

# Enforces used version of C/C++
set(CMAKE_C_STANDARD 23)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# --- Compilation options based on configurations ---
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type" FORCE)
endif()

message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

# Generic flags
set(COMMON_C_FLAGS "-Wall -Wextra -Wpedantic")
set(COMMON_CXX_FLAGS "-Wall -Wextra -Wpedantic")

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_CXX_FLAGS_DEBUG   "-O0 -g ${COMMON_CXX_FLAGS}")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG ${COMMON_CXX_FLAGS}")
elseif(MSVC)
    set(CMAKE_CXX_FLAGS_DEBUG   "/Zi /Od /DDEBUG")
    set(CMAKE_CXX_FLAGS_RELEASE "/O2 /DNDEBUG")
endif()

# ============================================================
#  Platform and toolchain detection
# ============================================================

if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    message(STATUS "Compiling Linux environment")
elseif(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    message(STATUS "Compiling Windows environment")
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    message(STATUS "Compiling macOS environment")
endif()

# Ejemplo: Include specific toolchain script if it exists
# if(DEFINED TARGET_ARCH AND EXISTS "${CMAKE_SOURCE_DIR}/cmake/toolchains/${TARGET_ARCH}.cmake")
#     include("${CMAKE_SOURCE_DIR}/cmake/toolchains/${TARGET_ARCH}.cmake")
# endif()

# ============================================================
#  Including project utilitaty functions 
# ============================================================

# include(Utils OPTIONAL)
# include(AddExternalLibrary OPTIONAL)
# include(ConfigureBuildOptions OPTIONAL)

# ============================================================
#  External dependencies configuration
# ============================================================

# if(EXISTS "${CMAKE_SOURCE_DIR}/lib")
#     message(STATUS "Configuting external dependencies...")
#     include(ExternalProject)
    # Ejemplo: A function created by us in charge of handling external dependencies
    # if(COMMAND setup_external_dependencies)
    #     setup_external_dependencies()
    # endif()
# endif()

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
