#! /bin/sh

BDIR=$CMAKE_BUILD_DIR

if [ "$BDIR" = "" ]; then
  BDIR=cmake-build
fi

cmake --build $BDIR -- -j $(nproc) &&
mkdir -p ./src/whisperpy/lib

cp $BDIR/libwhisperpy.so ./src/whisperpy/lib &&
cp $BDIR/lib/whisper.cpp/src/libwhisper.so ./src/whisperpy/lib &&
cp $BDIR/lib/whisper.cpp/src/libwhisper.so.1 ./src/whisperpy/lib &&
cp $BDIR/lib/whisper.cpp/src/libwhisper.so.1.7.4 ./src/whisperpy/lib &&
cp $BDIR/lib/whisper.cpp/ggml/src/libggml.so ./src/whisperpy/lib &&
cp $BDIR/lib/whisper.cpp/ggml/src/libggml-base.so ./src/whisperpy/lib &&
cp $BDIR/lib/whisper.cpp/ggml/src/libggml-cpu.so ./src/whisperpy/lib