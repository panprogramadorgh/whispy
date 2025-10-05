#! /bin/sh

BDIR=$WHISPERPY_CMAKE_BUILD_DIR

if [ "$BDIR" = "" ]; then
  BDIR=cmake-build
fi

cmake --build $BDIR -- -j $(nproc) &&
mkdir -p $BDIR/lib &&
cp $BDIR/libwhisperpy.so $BDIR/lib && 
cp $BDIR/src/backend/whisper.cpp/src/libwhisper.so* $BDIR/lib &&
cp $BDIR/src/backend/whisper.cpp/ggml/src/libggml.so $BDIR/lib &&
cp $BDIR/src/backend/whisper.cpp/ggml/src/libggml-base.so $BDIR/lib &&
cp $BDIR/src/backend/whisper.cpp/ggml/src/libggml-cpu.so $BDIR/lib
