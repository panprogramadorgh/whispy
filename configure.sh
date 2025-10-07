#! /bin/sh

# TODO: Use regular cmake environment variables

# Read env vars
BTYPE=$WHISPERPY_CMAKE_BUILD_TYPE
BDIR=$WHISPERPY_CMAKE_BUILD_DIR
COMPILER=$WHISPERPY_CMAKE_CXX_COMPILER

if [ "$BTYPE" = "" ]; then
  BTYPE=Release
fi

if [ "$BDIR" = "" ]; then
  BDIR=cmake-build
fi

if [ "$COMPILER" = "" ]; then
  COMPILER=/usr/bin/g++
fi

cmake . -B $BDIR -DCMAKE_BUILD_TYPE=$BTYPE -DCMAKE_CXX_COMPILER=$COMPILER