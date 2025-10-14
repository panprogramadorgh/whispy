import ctypes


# User-defined types

class nullptr:
  """Emulates C/C++ null pointers.
  """

  def __init__(self):
    _as_parameter_ = 0

class whispy_transcript_context(ctypes.Structure):
  _fields_ = [
    ("last_error_code", ctypes.c_uint8),
    ("last_error_message", ctypes.c_char_p),
    ("model_context", ctypes.c_void_p)
  ]

class whisper_ahead(ctypes.Structure):
  _fields_ = [
    ("n_text_layer", ctypes.c_int),
    ("n_head", ctypes.c_int)
  ]

class whisper_aheads(ctypes.Structure):
  _fields_ = [
    ("n_heads", ctypes.c_uint64),
    ("heads", ctypes.POINTER(whisper_ahead))
  ]

class whisper_context_params(ctypes.Structure):
  _fields_ = [
    ("use_gpu", ctypes.c_bool),
    ("flash_attn", ctypes.c_bool),
    ("gpu_device", ctypes.c_int),
    ("dtw_token_timestamps", ctypes.c_bool),
    ("dtw_aheads_preset", ctypes.c_int),
    ("dtw_n_top", ctypes.c_int),
    ("dtw_aheads", whisper_aheads),
    ("dtw_mem_size", ctypes.c_uint64)
  ]

class whisper_token_data(ctypes.Structure):
  _fields_ = [
    ("id", ctypes.c_int32),
    ("tid", ctypes.c_int32),
    ("p", ctypes.c_float),
    ("plog", ctypes.c_float),
    ("pt", ctypes.c_float),
    ("ptsum", ctypes.c_float),
    ("t0", ctypes.c_int64),
    ("t1", ctypes.c_int64),

    # [EXPERIMENTAL] Token-level timestamps with DTW
    # do not use if you haven't computed token-level timestamps
    # with dtw. Roughly corresponds to the moment in audio in
    # which the token was output  
    ("t_dtw", ctypes.c_int64),

    ("vlen", ctypes.c_float)
  ]

whisper_new_segment_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)

whisper_progress_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)

whisper_encoder_begin_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)

whisper_encoder_begin_callback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)

ggml_abort_callback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)

whisper_logits_filter_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(whisper_token_data), ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_void_p)

class whisper_full_params(ctypes.Structure):
  _fields_ = [
    ("strategy", ctypes.c_int),
    ("n_threads", ctypes.c_int),
    ("n_max_text_ctx", ctypes.c_int),
    ("offset_ms", ctypes.c_int),
    ("duration_ms", ctypes.c_int),

    ("translate", ctypes.c_bool),
    ("no_context", ctypes.c_bool),
    ("no_timestampts", ctypes.c_bool),
    ("single_segment", ctypes.c_bool),
    ("print_special", ctypes.c_bool),
    ("print_progress", ctypes.c_bool),
    ("print_realtime", ctypes.c_bool),
    ("print_timestampts", ctypes.c_bool),

    # [EXPERIMENTAL] token-level timestampts
    ("token_timestampts", ctypes.c_bool),
    ("thold_pt", ctypes.c_float),
    ("thold_ptsum", ctypes.c_float),
    ("max_len", ctypes.c_int),
    ("split_on_word", ctypes.c_bool),
    ("max_tokens", ctypes.c_int),

    # [EXPERIMENTAL]    
    ("debug_mode", ctypes.c_bool),
    ("audio_ctx", ctypes.c_int),

    # [EXPERIMENTAL]
    ("tdrz_enable", ctypes.c_bool),

    ("suppress_regex", ctypes.c_char_p),
    ("initial_prompt", ctypes.c_char_p),
    ("prompt_tokens", ctypes.POINTER(ctypes.c_int32)),
    ("prompt_n_tokens", ctypes.c_int),

    ("language", ctypes.c_char_p),
    ("detect_language", ctypes.c_bool),

    ("suppress_blank", ctypes.c_bool),
    ("suppress_nst", ctypes.c_bool),

    ("temperature", ctypes.c_float),
    ("max_initial_ts", ctypes.c_float),
    ("length_penalty", ctypes.c_float),

    ("temperature_inc", ctypes.c_float),
    ("entropy_thold", ctypes.c_float),
    ("logprob_thold", ctypes.c_float),
    ("no_speech_thold", ctypes.c_float),

    ("new_segment_callback", whisper_new_segment_callback),
    ("new_segment_callback_user_data", ctypes.c_void_p),

    ("progress_callback", whisper_progress_callback),
    ("new_segment_callback_user_data", ctypes.c_void_p),

    ("encoder_begin_callback", whisper_encoder_begin_callback),
    ("encoder_begin_callback_user_data", ctypes.c_void_p),

    ("abort_callback", ggml_abort_callback),
    ("abort_callback_user_data", ctypes.c_void_p),

    ("logits_filter_callback", whisper_logits_filter_callback),
    ("logits_filter_callback_user_data", ctypes.c_void_p),

    ("grammar_rules", ctypes.POINTER(ctypes.c_void_p)),
    ("n_grammar_rules", ctypes.c_uint64),
    ("i_start_rule", ctypes.c_uint64),
    ("grammar_penalty", ctypes.c_float)
  ]


# Library prototyping

def bind_c_api(dll: ctypes.CDLL):
    dll.whispy_tc_make.argtypes = [ctypes.POINTER(whispy_transcript_context), ctypes.c_char_p, whisper_context_params]
    dll.whispy_tc_make.restype = ctypes.c_int

    dll.whispy_tc_free.argtypes = [ctypes.POINTER(whispy_transcript_context)]
    dll.whispy_tc_free.restype = None

    dll.whispy_speech_to_text.argtypes = [ctypes.c_char_p, ctypes.c_uint64, ctypes.POINTER(whispy_transcript_context), ctypes.c_char_p, whisper_full_params]
    dll.whispy_speech_to_text.restype = ctypes.c_int

    # whisper.cpp

    ## params
    dll.whisper_context_default_params.argtypes = []
    dll.whisper_context_default_params.restype = whisper_context_params

    dll.whisper_full_default_params.argtypes = [ctypes.c_int]
    dll.whisper_full_default_params.restype = whisper_full_params

    ## segments
    dll.whisper_full_n_segments.argtypes = [ctypes.c_void_p]
    dll.whisper_full_n_segments.restype = ctypes.c_int

    dll.whisper_full_get_segment_text.argtypes = [ctypes.c_void_p, ctypes.c_int]
    dll.whisper_full_get_segment_text.restype = ctypes.c_char_p