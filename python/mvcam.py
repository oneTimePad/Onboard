
from ctypes import *

class dvpFrame(Structure):
	_fields_=[
		("format", c_int),
		("bits",   c_int),
		("uBytes", c_uint),
		("iWidth", c_int),
		("iHeight",c_int),
		("uFrameID",c_uint64),
		("uTimestamp",c_uint64),
		("fExposure", c_double),
		("fAGain",    c_float),
		("reserved",  c_uint*32)
		
	]

class mvCamImage(Structure):
	_fields_ = [
		("frame",dvpFrame),
		("image_buffer",c_void_p),
		("image_name", c_char*10000)
	]

class mvExposure(Structure):
	_fields_ = [
		("mvexp_aflick",c_int),
		("mvexp_shutter",c_double),
		("mvexp_aemode", c_int),
		("mvexp_aeop",   c_int),
		("mvexp_aetarget",c_uint),
		("mvexp_awop", c_int),
		("mvexp_gain",c_float)
	]

class mvStrobe(Structure):
	_fields_ = [
		("mvstrb_duration",c_double),
		("mvstrb_output",c_int),
		("mvstrb_driver",c_int),
		("mvstrb_delay",c_double)
	]


class MvStrobe(object):
	def __init__(self,duration,output,driver,delay):
		self.strb = mvStrobe()
		self.strb.mvstrb_duration = c_double(duration)
		self.strb.mvstrb_output = c_int(output)
		self.strb.mvstrb_driver = c_int(driver)
		self.strb.mvstrb_delay = c_double(delay)
		self._as_parameter_ = self.strb
class MvExposure(object):
	def __init__(self, aflick = 0, shutter = 400, aemode =0, aeop= 0, aetarget
              = 0, awop = 0,gain =32.0):
		self.exp = mvExposure()
		self.exp.mvexp_aflick = c_int(aflick)
		self.exp.mvexp_shutter = c_double(shutter)
		self.exp.mvexp_aemode = c_int(aemode)
		self.exp.mvexp_aeop = c_int(aeop)
		self.exp.mvexp_aetarget = c_uint(aetarget)
		self.exp.mvexp_awop = c_int(awop)
		self.exp.mvexp_gain = c_float(gain)
		self._as_parameter_ = self.exp
class MvCamImage(object):
	def __init__(self,image):
		self._as_parameter_ = image
	def set_name(self,image_name):
		self._as_parameter_.image_name = image_name

class MvStrobeDriver(object):
	def __init__(self):
		self.FRAME_DURATION = 0
		self.TIMER_LOGIC = 1
		self.SENSOR_STROBE = 2

class MvStrobeOutput(object):
	def __init__(self):
		self.STROBE_OUT_OFF = 0
		self.STROBE_OUT_LOW = 1
		self.STROBE_OUT_HIGH = 2

class MvAeMode(object):
	def __init__(self):
		self.AE_MODE_AE_AG = 0
		self.AE_MODE_AG_AE = 1
		self.AE_MODE_AE_ONLY = 2
		self.AE_MODE_AG_ONLY = 3

class MvAeOp(object):
	def __init__(self):
		self.AE_OP_OFF = 0
		self.AE_OP_ONCE = 1
		self.AE_OP_CONTINUOUS = 2


class MachineVision:
	def __init__(self,libPath,imageStorage):
		self.libHandle = cdll.LoadLibrary(libPath)
		self.dvpStatus = c_uint()
		self.dvpHandle = c_uint()
		self.fps = None
		self.imageStorage = imageStorage
	def getStatus(self):
		return int(self.dvpStatus)
	def open_cam(self):
		return int(self.libHandle.mvCamOpenDef(byref(self.dvpHandle),byref(self.dvpStatus)))
	def set_exposure(self,exp):
		return int(self.libHandle.mvCamSetExposure(byref(self.dvpHandle),exp,byref(self.dvpStatus)))
	def set_strobe(self,strb):
		return int(self.libHandle.mvCamSetStrobe(byref(self.dvpHandle),strb,byref(self.dvpStatus)))

	def start_cam(self,loop,delay):
		delay = c_double(delay)
		loop = c_float(loop)
		return int(self.libHandle.mvCamStartTrigger(byref(self.dvpHandle),loop,delay,byref(self.dvpStatus)))
	def get_image(self,timeout):
		image = mvCamImage()
		ctimeout = c_uint(timeout)
		retVal = int(self.libHandle.mvCamGetImage(byref(self.dvpHandle), byref(image),ctimeout,byref(self.dvpStatus)))
		return MvCamImage(image),retVal
	def save_image(self,image,quality):
		cquality = c_int(quality)
		return int(self.libHandle.mvCamSaveImage(byref(self.dvpHandle),byref(image._as_parameter_),cquality,byref(self.dvpStatus)))
	def stop_cam(self):
		return int(self.libHandle.mvCamStopTrigger(byref(self.dvpHandle),byref(self.dvpStatus)))
	def close_cam(self):
		return int(self.libHandle.mvCamDestroy(byref(self.dvpHandle),byref(self.dvpStatus)))


