import ctypes

lib = ctypes.CDLL('target/release/libwasi_lib.dylib')

s = "calculator.add".encode("UTF-8")
lib.run.restype = ctypes.c_char_p
lib.run.argtypes = [ctypes.c_char_p]
lib.run(s)