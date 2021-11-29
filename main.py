from ctypes import *


XID = c_ulong
Time = c_ulong
Window = XID
GContext = XID
Colormap = XID
KeySym = XID
Display = c_voidp
XPointer = c_char_p

class _XDisplay(Structure):
    pass


class _XGC(Structure):
    _fields_ = [
        ("ext_data", c_voidp),
        ("gid", GContext)
        ]


GC = POINTER(_XGC)


class XMotionEvent(Structure):
    _fields_ = [
        ("type", c_int),
        ("serial", c_ulong),
        ("send_event", c_bool),
        ("display", c_voidp),
        ("window", Window),
        ("root", Window),
        ("subwindow", Window),
        ("time", Time),
        ("x", c_int),
        ("y", c_int),
        ("x_root", c_int),
        ("y_root", c_int),
        ("state", c_uint),
        ("is_hint", c_char),
        ("same_screen", c_bool)
        ]


class XButtonEvent(Structure):
    _fields_ = [
        ("type", c_int),
        ("serial", c_ulong),
        ("send_event", c_bool),
        ("display", c_voidp),
        ("window", Window),
        ("root", Window),
        ("subwindow", Window),
        ("time", Time),
        ("x", c_int),
        ("y", c_int),
        ("x_root", c_int),
        ("y_root", c_int),
        ("state", c_uint),
        ("button", c_uint),
        ("same_screen", c_bool)
        ]


class XKeyEvent(Structure):
    _fields_ = [
        ("type", c_int),
        ("serial", c_ulong),
        ("send_event", c_bool),
        ("display", c_voidp),
        ("window", Window),
        ("root", Window),
        ("subwindow", Window),
        ("time", Time),
        ("x", c_int),
        ("y", c_int),
        ("x_root", c_int),
        ("y_root", c_int),
        ("state", c_uint),
        ("keycode", c_uint),
        ("same_screen", c_bool)
        ]


class XEvent(Structure):
    _fields_ = [
        ("type", c_int),
        ("serial", c_ulong),
        ("send_event", c_bool),
        ("display", c_voidp),
        ("extension", c_int),
        ("evtype", c_int)
        ]


class Screen(Structure):
    _fields_ = [
        ("ext_data", c_voidp),
        ("display", POINTER(_XDisplay)),
        ("root", Window),
        ("width", c_int),
        ("height", c_int),
        ("mwidth", c_int),
        ("mheight", c_int),
        ("ndepths", c_int),
        ("depths", c_voidp),
        ("root_depth", c_int),
        ("root_visual", c_voidp),
        ("default_gc", GC),
        ("cmap", Colormap),
        ("white_pixel", c_ulong),
        ("black_pixel", c_ulong),
        ("max_maps", c_int),
        ("min_maps", c_int),
        ("backing_store", c_int),
        ("save_unders", c_bool),
        ("root_input_mask", c_long)
        ]



_XDisplay._fields_ = [
        ("ext_data", c_voidp),
        ("private1", c_voidp),
        ("fd", c_int),
        ("private2", c_int),
        ("proto_major_version", c_int),
        ("proto_minor_version", c_int),
        ("vendor", c_char_p),
        ("private3", XID),
        ("private4", XID),
        ("private5", XID),
        ("private6", c_int),
        ("resource_alloc", c_voidp),
        ("byte_order", c_int),
        ("bitmap_unit", c_int),
        ("bitmap_pad", c_int),
        ("bitmap_bit_order", c_int),
        ("nformats", c_int),
        ("pixmap_format", c_voidp),
        ("private8", c_int),
        ("release", c_int),
        ("private9", c_voidp),
        ("private10", c_voidp),
        ("qlen", c_int),
        ("last_request_read", c_ulong),
        ("request", c_ulong),
        ("private11", XPointer),
        ("private12", XPointer),
        ("private13", XPointer),
        ("private14", XPointer),
        ("max_request_size", c_uint),
        ("db", c_voidp),
        ("private15", c_voidp),
        ("display_name", c_char_p),
        ("default_screen", c_int),
        ("nscreens", c_int),
        ("screens", POINTER(Screen)),
        ("motion_buffer", c_ulong),
        ("private16", c_ulong),
        ("min_keycode", c_int),
        ("max_keycode", c_int),
        ("private17", XPointer),
        ("private18", XPointer),
        ("private19", c_int),
        ("xdefaults", c_char_p)
        ]


_XPrivDisplay = POINTER(_XDisplay)


def offsetof(structure, element):
    return getattr(structure, element).offset


def ScreenOfDisplay(d: c_voidp, s: c_uint) -> POINTER(Screen):
    return pointer(cast(d, _XPrivDisplay).contents.screens[s])


def BlackPixel(dsp: c_voidp):
    return ScreenOfDisplay(dsp, DefaultScreen(dsp)).contents.black_pixel


def WhitePixel(dsp: c_voidp):
    return ScreenOfDisplay(dsp, DefaultScreen(dsp)).contents.white_pixel


def DefaultScreen(dsp: c_voidp) -> c_int:
    return cast(dsp, _XPrivDisplay).contents.default_screen


def DefaultRootWindow(dsp: c_voidp) -> POINTER(Screen):
    return ScreenOfDisplay(dsp, DefaultScreen(dsp)).contents.root


def reinterpret(obj, ty):
    return cast(addressof(obj), POINTER(ty)).contents


x11 = CDLL("/usr/lib/libX11.so")

XOpenDisplay = x11.XOpenDisplay
XOpenDisplay.argtypes = [c_char_p]
XOpenDisplay.restype = c_voidp

XCreateSimpleWindow = x11.XCreateSimpleWindow
XCreateSimpleWindow.argtypes = [
        c_voidp, Window, c_int, c_int,
        c_uint, c_uint, c_uint, c_ulong, c_ulong
        ]
XCreateSimpleWindow.restype = Window

XMapWindow = x11.XMapWindow
XMapWindow.argtypes = [Display, Window]
XMapWindow.restype = c_int

XFlush = x11.XFlush
XFlush.argtypes = [Display]
XFlush.restype = c_int

XCreateGC = x11.XCreateGC
XCreateGC.argtypes = [c_voidp, Window, c_ulong, c_voidp]
XCreateGC.restype = GC

XSetForeground = x11.XSetForeground
XSetForeground.argtypes = [c_voidp, GC, c_ulong]
XSetForeground.restype = c_int

XNextEvent = x11.XNextEvent
XNextEvent.argtypes = [c_voidp, c_voidp]
XNextEvent.restype = c_int

XSelectInput = x11.XSelectInput
XSelectInput.argtypes = [c_voidp, Window, c_long]
XSelectInput.restype = c_int

XKeycodeToKeysym = x11.XKeycodeToKeysym
XKeycodeToKeysym.argtypes = [c_voidp, c_uint, c_int]
XKeycodeToKeysym.restype = KeySym

CopyFromParent = 0

MapNotify = 19
ButtonPress = 4
MotionNotify = 6
KeyPress = 2

StructureNotifyMask = 1 << 17
ButtonPressMask = 1 << 2
ButtonReleaseMask = 1 << 3
PointerMotionMask = 1 << 6
KeyPressMask = 1 << 0

if __name__ == "__main__":
    d = XOpenDisplay(None)
    black_color = BlackPixel(d)
    white_color = WhitePixel(d)
    if not d:
        raise Exception
    w = XCreateSimpleWindow(d, DefaultRootWindow(d),
        0, 0, 500, 500, 5, 0, white_color)

    XSelectInput(d, w,
        StructureNotifyMask | PointerMotionMask | ButtonPressMask \
                | KeyPressMask)
    XMapWindow(d, w)
    gc = XCreateGC(d, w, 0, 0)
    XSetForeground(d, gc, white_color)

    while True:
        e = XKeyEvent()
        XNextEvent(d, addressof(e))
        
        if e.type == MotionNotify:
            e = reinterpret(e, XMotionEvent)
        elif e.type == ButtonPress:
            e = reinterpret(e, XButtonEvent)
            print(e.state, e.x, e.y)
        elif e.type == KeyPress:
            e = reinterpret(e, XKeyEvent)
            key = XKeycodeToKeysym(d, e.keycode, 0)
            # TODO: send to keyboard driver as KeySym,
            #       read output from resulting keyboard buffer
            #       as 'char' (assuming ascii)

    XFlush(d)

    input()
