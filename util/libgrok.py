import ctypes

class GrokT(ctypes.Structure):
	_fields_ = [
		("pattern", ctypes.c_char_p),
		("pattern_len", ctypes.c_int),
		("full_pattern", ctypes.c_char_p),
		("full_pattern_len", ctypes.c_int),
		("patterns", ctypes.c_void_p),
		("re", ctypes.c_void_p),
		("pcre_capture_venctor", ctypes.POINTER(ctypes.c_int)),
		("pcre_num_capture", ctypes.c_int),
		("captures_by_id", ctypes.c_void_p),
		("captures_by_name", ctypes.c_void_p),
		("captures_by_subname", ctypes.c_void_p),
		("captures_by_capture_number", ctypes.c_void_p),
		("max_capture_num", ctypes.c_int),
		("pcre_errptr", ctypes.c_char_p),
		("pcre_erroffset", ctypes.c_int),
		("pcre_errno", ctypes.c_int),
		("logmask", ctypes.c_uint),
		("logdepth", ctypes.c_uint),
		("errstr", ctypes.c_char_p)
	]

class MatchResult(ctypes.Structure):
	_fields_ = [
		("grok", ctypes.POINTER(GrokT)),
		("subject", ctypes.c_char_p),
		("start", ctypes.c_int),
		("end", ctypes.c_int)
	]

_libgrok = ctypes.cdll.LoadLibrary('libgrok.so')
_libtcab = ctypes.cdll.LoadLibrary('libtokyocabinet.so')

# void grok_match_walk_init(const grok_match_t *gm);
_grok_match_walk_init = _libgrok.grok_match_walk_init
_grok_match_walk_init.argtypes = [ ctypes.POINTER(MatchResult) ]

# int grok_match_walk_next(const grok_match_t *gm,
#                          char **name, int *namelen,
#                          const char **substr, int *substrlen);

_grok_match_walk_next = _libgrok.grok_match_walk_next
_grok_match_walk_next.argtypes = [ ctypes.POINTER(MatchResult), ctypes.POINTER(ctypes.c_char_p), 
		ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_int) ]
_grok_match_walk_next.restype = ctypes.c_int

# void grok_match_walk_end(const grok_match_t *gm);

_grok_match_walk_end = _libgrok.grok_match_walk_end
_grok_match_walk_end.argtypes = [ ctypes.POINTER(MatchResult) ]


_grok_new = _libgrok.grok_new
_grok_new.argtypes = []
_grok_new.restype = ctypes.c_void_p

_grok_free = _libgrok.grok_free
_grok_free.argtypes = [ctypes.c_void_p]

_grok_compile = _libgrok.grok_compile
_grok_compile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_grok_compile.restype = ctypes.c_int

_grok_exec = _libgrok.grok_exec
_grok_exec.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(MatchResult)]
_grok_exec.restype = ctypes.c_int

_grok_pattern_add = _libgrok.grok_pattern_add
_grok_pattern_add.argtypes = [ctypes.c_void_p,
                              ctypes.c_char_p, ctypes.c_size_t,
                              ctypes.c_char_p, ctypes.c_size_t]
_grok_pattern_add.restype = ctypes.c_int

_grok_patterns_import_from_file = _libgrok.grok_patterns_import_from_file
_grok_patterns_import_from_file.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_grok_patterns_import_from_file.restype = ctypes.c_int


class Grok(object):

    def __init__(self):
        self._grok = _grok_new()

    def __del__(self):
        _grok_free(self._grok)

    def add_pattern(self, name, pattern):
        _grok_pattern_add(self._grok, name, len(name), pattern, len(pattern))

    def add_patterns_from_file(self, filename):
        _grok_patterns_import_from_file(self._grok, filename)

    def compile(self, pattern):
        _grok_compile(self._grok, pattern)

    def __call__(self, text, result):
        return _grok_exec(self._grok, text, result)

    def parse(self, match):
	parsed = {}
	_grok_match_walk_init(ctypes.byref(match))
	while True:
		name = (ctypes.c_char * 100)()
		nameptr = ctypes.cast(name, ctypes.c_char_p)
		namelen = ctypes.c_int()
		substr = (ctypes.c_char * 100)()
		substrptr = ctypes.cast(substr, ctypes.c_char_p)
		substrlen = ctypes.c_int()
		result = _grok_match_walk_next(ctypes.byref(match), ctypes.byref(nameptr), ctypes.byref(namelen), ctypes.byref(substrptr), ctypes.byref(substrlen))

		if result != 0:
			break

		names = nameptr.value[0:namelen.value].split(':')
		value = substrptr.value[0:substrlen.value]
		key = names[0]
		if len(names) == 2:
			key = names[1]
		print "key: %s" % key
		print "value: %s" % value

		if key in parsed:
			values = parsed[key]
			values.append(value)
		else:
			values = [value]
		parsed[key] = values
	
	_grok_match_walk_end(ctypes.byref(match))

	return parsed

