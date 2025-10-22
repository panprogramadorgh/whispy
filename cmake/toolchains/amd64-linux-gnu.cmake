# ============================================================================
# Basic toolchain file for Linux systems.
# Highly compatible and adaptable to both, cross and local compilation.
# Usage:
#   ./configure amd64-linux-gnu
# ============================================================================

# --- Target System -----------------------------------------------------------
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

# --- Compilers ---------------------------------------------------------------
# Use default system compilers if there aren't any defined
# You may substitute by some absolute paths if it isn't cross-compilation
set(CMAKE_C_COMPILER   gcc)
set(CMAKE_CXX_COMPILER g++)

# --- Compiler Flags ---
set(CMAKE_C_FLAGS_INIT "")
set(CMAKE_C_CXX_FLAGS_INIT "")

# --- Enlaces y librerías -----------------------------------------------------
# Puedes ajustar rutas personalizadas si tu entorno lo requiere
set(CMAKE_EXE_LINKER_FLAGS_INIT "")
set(CMAKE_SHARED_LINKER_FLAGS_INIT "")

# --- Generic definitions --------------------------------------------------
# Ensures consistency between different builds
add_compile_definitions(
    LINUX
    UNIX
)

# --- Mensaje de confirmación -------------------------------------------------
message(STATUS "Using basic Linux toolchain file")
message(STATUS "  Compiler C:   ${CMAKE_C_COMPILER}")
message(STATUS "  Compiler C++: ${CMAKE_CXX_COMPILER}")
message(STATUS "  Target:       ${CMAKE_SYSTEM_PROCESSOR} (${CMAKE_SYSTEM_NAME})")
