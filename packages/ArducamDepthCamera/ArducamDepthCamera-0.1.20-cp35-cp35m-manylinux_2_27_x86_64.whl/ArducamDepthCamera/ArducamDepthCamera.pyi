from __future__ import annotations
import numpy
import typing
__all__ = ['ArducamCamera', 'CameraInfo', 'Connection', 'Control', 'DepthData', 'DeviceType', 'Frame', 'FrameFormat', 'FrameType', 'RawData', 'TofErrorCode', 'TofFrameWorkMode', 'TofWorkMode']
class Frame:
    @property
    def data(self) -> dict:
        """
        Frame data
        """
    @data.setter
    def data(self, arg1: typing.Any) -> None:
        ...
    @property
    def format(self) -> FrameFormat:
        """
        Frame data format
        """
    @format.setter
    def format(self, arg1: FrameFormat) -> None:
        ...
class ArducamCamera:
    def __init__(self) -> None:
        ...
    def close(self) -> TofErrorCode:
        """
        Close the camera
        """
    def getCameraInfo(self) -> CameraInfo:
        """
        Get camera information.
        """
    def getControl(self, ctrl: Control) -> int:
        """
        Get camera parameters.
        """
    def open(self, mode: Connection, index: int = 0) -> TofErrorCode:
        """
        Initialize the camera configuration and turn on the camera, set the initialization frame according to the mode.
        
        - mode Specify the connection method.
        - index Device node, the default value is video0.
        """
    def openWithFile(self, path: str, index: int = 0) -> TofErrorCode:
        """
        Initialize the camera configuration and turn on the camera, set the initialization frame according to the mode.
        
        - path Specify the config file path.
        - index Device node, the default value is video0.
        """
    def releaseFrame(self, frame: Frame) -> TofErrorCode:
        """
        Free the memory space of the frame.
        """
    def requestFrame(self, timeout: int) -> Frame:
        """
        Request a frame of data from the frame processing thread.
        """
    def setControl(self, ctrl: Control, value: int) -> TofErrorCode:
        """
        Set camera parameters.
        """
    def start(self, type: FrameType) -> TofErrorCode:
        """
        Start the camera stream and start processing.
        """
    def stop(self) -> TofErrorCode:
        """
        Stop camera stream and processing.
        """
class CameraInfo:
    bit_width: int
    bpp: int
    connect: Connection
    device_type: DeviceType
    height: int
    index: int
    type: FrameType
    width: int
class Connection:
    """
    Members:
    
      CSI
    
      USB
    """
    CSI: typing.ClassVar[Connection]  # value = <Connection.CSI: 0>
    USB: typing.ClassVar[Connection]  # value = <Connection.USB: 1>
    __members__: typing.ClassVar[dict[str, Connection]]  # value = {'CSI': <Connection.CSI: 0>, 'USB': <Connection.USB: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Control:
    """
    Members:
    
      RANGE
    
      FMT_WIDTH
    
      FMT_HEIGHT
    
      MODE
    
      FRAME_MODE
    
      EXPOSURE
    
      FRAME_RATE
    
      SKIP_FRAME
    
      SKIP_FRAME_LOOP
    
      AUTO_FRAME_RATE
    
      INTRINSIC_FX
    
      INTRINSIC_FY
    
      INTRINSIC_CX
    
      INTRINSIC_CY
    
      DENOISE
    
      HFLIP
    
      VFLIP
    
      CONFIG_DIR_EXT
    
      LOAD_CALI_DATA
    
      SAVE_CALI_DATA
    
      I2C_BY_PASS
    
      I2C_BUS_NUM
    """
    AUTO_FRAME_RATE: typing.ClassVar[Control]  # value = <Control.AUTO_FRAME_RATE: 9>
    CONFIG_DIR_EXT: typing.ClassVar[Control]  # value = <Control.CONFIG_DIR_EXT: 256>
    DENOISE: typing.ClassVar[Control]  # value = <Control.DENOISE: 14>
    EXPOSURE: typing.ClassVar[Control]  # value = <Control.EXPOSURE: 5>
    FMT_HEIGHT: typing.ClassVar[Control]  # value = <Control.FMT_HEIGHT: 2>
    FMT_WIDTH: typing.ClassVar[Control]  # value = <Control.FMT_WIDTH: 1>
    FRAME_MODE: typing.ClassVar[Control]  # value = <Control.FRAME_MODE: 4>
    FRAME_RATE: typing.ClassVar[Control]  # value = <Control.FRAME_RATE: 6>
    HFLIP: typing.ClassVar[Control]  # value = <Control.HFLIP: 15>
    I2C_BUS_NUM: typing.ClassVar[Control]  # value = <Control.I2C_BUS_NUM: 260>
    I2C_BY_PASS: typing.ClassVar[Control]  # value = <Control.I2C_BY_PASS: 259>
    INTRINSIC_CX: typing.ClassVar[Control]  # value = <Control.INTRINSIC_CX: 12>
    INTRINSIC_CY: typing.ClassVar[Control]  # value = <Control.INTRINSIC_CY: 13>
    INTRINSIC_FX: typing.ClassVar[Control]  # value = <Control.INTRINSIC_FX: 10>
    INTRINSIC_FY: typing.ClassVar[Control]  # value = <Control.INTRINSIC_FY: 11>
    LOAD_CALI_DATA: typing.ClassVar[Control]  # value = <Control.LOAD_CALI_DATA: 257>
    MODE: typing.ClassVar[Control]  # value = <Control.MODE: 3>
    RANGE: typing.ClassVar[Control]  # value = <Control.RANGE: 0>
    SAVE_CALI_DATA: typing.ClassVar[Control]  # value = <Control.SAVE_CALI_DATA: 258>
    SKIP_FRAME: typing.ClassVar[Control]  # value = <Control.SKIP_FRAME: 7>
    SKIP_FRAME_LOOP: typing.ClassVar[Control]  # value = <Control.SKIP_FRAME_LOOP: 8>
    VFLIP: typing.ClassVar[Control]  # value = <Control.VFLIP: 16>
    __members__: typing.ClassVar[dict[str, Control]]  # value = {'RANGE': <Control.RANGE: 0>, 'FMT_WIDTH': <Control.FMT_WIDTH: 1>, 'FMT_HEIGHT': <Control.FMT_HEIGHT: 2>, 'MODE': <Control.MODE: 3>, 'FRAME_MODE': <Control.FRAME_MODE: 4>, 'EXPOSURE': <Control.EXPOSURE: 5>, 'FRAME_RATE': <Control.FRAME_RATE: 6>, 'SKIP_FRAME': <Control.SKIP_FRAME: 7>, 'SKIP_FRAME_LOOP': <Control.SKIP_FRAME_LOOP: 8>, 'AUTO_FRAME_RATE': <Control.AUTO_FRAME_RATE: 9>, 'INTRINSIC_FX': <Control.INTRINSIC_FX: 10>, 'INTRINSIC_FY': <Control.INTRINSIC_FY: 11>, 'INTRINSIC_CX': <Control.INTRINSIC_CX: 12>, 'INTRINSIC_CY': <Control.INTRINSIC_CY: 13>, 'DENOISE': <Control.DENOISE: 14>, 'HFLIP': <Control.HFLIP: 15>, 'VFLIP': <Control.VFLIP: 16>, 'CONFIG_DIR_EXT': <Control.CONFIG_DIR_EXT: 256>, 'LOAD_CALI_DATA': <Control.LOAD_CALI_DATA: 257>, 'SAVE_CALI_DATA': <Control.SAVE_CALI_DATA: 258>, 'I2C_BY_PASS': <Control.I2C_BY_PASS: 259>, 'I2C_BUS_NUM': <Control.I2C_BUS_NUM: 260>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class DepthData(Frame):
    @property
    def amplitude_data(self) -> numpy.ndarray[typing.Any, numpy.dtype[numpy.float32]]:
        """
        Frame data(amplitude data)
        """
    @amplitude_data.setter
    def amplitude_data(self, arg1: typing.Any) -> None:
        ...
    @property
    def confidence_data(self) -> numpy.ndarray[typing.Any, numpy.dtype[numpy.float32]]:
        """
        Frame data(confidence data)
        """
    @confidence_data.setter
    def confidence_data(self, arg1: typing.Any) -> None:
        ...
    @property
    def data(self) -> dict:
        """
        Frame data
        """
    @data.setter
    def data(self, arg1: typing.Any) -> None:
        ...
    @property
    def depth_data(self) -> numpy.ndarray[typing.Any, numpy.dtype[numpy.float32]]:
        """
        Frame data(depth data)
        """
    @depth_data.setter
    def depth_data(self, arg1: typing.Any) -> None:
        ...
    @property
    def format(self) -> FrameFormat:
        """
        Frame data format
        """
    @format.setter
    def format(self, arg1: FrameFormat) -> None:
        ...
class DeviceType:
    """
    Members:
    
      VGA
    
      HQVGA
    """
    HQVGA: typing.ClassVar[DeviceType]  # value = <DeviceType.HQVGA: 1>
    VGA: typing.ClassVar[DeviceType]  # value = <DeviceType.VGA: 0>
    __members__: typing.ClassVar[dict[str, DeviceType]]  # value = {'VGA': <DeviceType.VGA: 0>, 'HQVGA': <DeviceType.HQVGA: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class FrameFormat:
    height: int
    timestamp: int
    type: FrameType
    width: int
class FrameType:
    """
    Members:
    
      RAW
    
      DEPTH
    
      CONFIDENCE
    
      AMPLITUDE
    
      CACHE
    """
    AMPLITUDE: typing.ClassVar[FrameType]  # value = <FrameType.AMPLITUDE: 3>
    CACHE: typing.ClassVar[FrameType]  # value = <FrameType.CACHE: 4>
    CONFIDENCE: typing.ClassVar[FrameType]  # value = <FrameType.CONFIDENCE: 1>
    DEPTH: typing.ClassVar[FrameType]  # value = <FrameType.DEPTH: 2>
    RAW: typing.ClassVar[FrameType]  # value = <FrameType.RAW: 0>
    __members__: typing.ClassVar[dict[str, FrameType]]  # value = {'RAW': <FrameType.RAW: 0>, 'DEPTH': <FrameType.DEPTH: 2>, 'CONFIDENCE': <FrameType.CONFIDENCE: 1>, 'AMPLITUDE': <FrameType.AMPLITUDE: 3>, 'CACHE': <FrameType.CACHE: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class RawData(Frame):
    @property
    def data(self) -> dict:
        """
        Frame data
        """
    @data.setter
    def data(self, arg1: typing.Any) -> None:
        ...
    @property
    def format(self) -> FrameFormat:
        """
        Frame data format
        """
    @format.setter
    def format(self, arg1: FrameFormat) -> None:
        ...
    @property
    def raw_data(self) -> numpy.ndarray[typing.Any, numpy.dtype[numpy.int16]]:
        """
        Frame data(raw data)
        """
    @raw_data.setter
    def raw_data(self, arg1: typing.Any) -> None:
        ...
class TofErrorCode:
    """
    Members:
    
      ArducamSuccess
    
      ArducamInvalidParameter
    
      ArducamNoCache
    
      ArducamUnkownDevice
    
      ArducamNotImplemented
    
      ArducamSkipFrame
    
      ArducamSystemError
    
      ArducamUnkownError
    """
    ArducamInvalidParameter: typing.ClassVar[TofErrorCode]  # value = <TofErrorCode.ArducamInvalidParameter: 1>
    ArducamNoCache: typing.ClassVar[TofErrorCode]  # value = <TofErrorCode.ArducamNoCache: 2>
    ArducamNotImplemented: typing.ClassVar[TofErrorCode]  # value = <TofErrorCode.ArducamNotImplemented: 4>
    ArducamSkipFrame: typing.ClassVar[TofErrorCode]  # value = <TofErrorCode.ArducamSkipFrame: 240>
    ArducamSuccess: typing.ClassVar[TofErrorCode]  # value = <TofErrorCode.ArducamSuccess: 0>
    ArducamSystemError: typing.ClassVar[TofErrorCode]  # value = <TofErrorCode.ArducamSystemError: -2>
    ArducamUnkownDevice: typing.ClassVar[TofErrorCode]  # value = <TofErrorCode.ArducamUnkownDevice: 3>
    ArducamUnkownError: typing.ClassVar[TofErrorCode]  # value = <TofErrorCode.ArducamUnkownError: -1>
    __members__: typing.ClassVar[dict[str, TofErrorCode]]  # value = {'ArducamSuccess': <TofErrorCode.ArducamSuccess: 0>, 'ArducamInvalidParameter': <TofErrorCode.ArducamInvalidParameter: 1>, 'ArducamNoCache': <TofErrorCode.ArducamNoCache: 2>, 'ArducamUnkownDevice': <TofErrorCode.ArducamUnkownDevice: 3>, 'ArducamNotImplemented': <TofErrorCode.ArducamNotImplemented: 4>, 'ArducamSkipFrame': <TofErrorCode.ArducamSkipFrame: 240>, 'ArducamSystemError': <TofErrorCode.ArducamSystemError: -2>, 'ArducamUnkownError': <TofErrorCode.ArducamUnkownError: -1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    def str(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class TofFrameWorkMode:
    """
    Members:
    
      SINGLE_FREQ_2PHASE
    
      SINGLE_FREQ_4PHASE
    
      SINGLE_FREQ_4PHASE_GRAY
    
      SINGLE_FREQ_4PHASE_BG
    
      SINGLE_FREQ_4PHASE_4BG
    
      SINGLE_FREQ_4PHASE_GRAY_5BG
    
      SINGLE_FREQ_GRAY_BG_4PHASE_GRAY_BG
    
      SINGLE_FREQ_GRAY_BG_4PHASE_BG
    
      SINGLE_FREQ_BG_GRAY_BG_4PHASE
    
      SINGLE_FREQ_BG_4PHASE_BG_GRAY
    
      DOUBLE_FREQ_4PHASE
    
      DOUBLE_FREQ_4PHASE_GRAY_4PHASE_BG
    
      DOUBLE_FREQ_4PHASE_4BG
    
      DOUBLE_FREQ_4PHASE_GRAY_5BG
    
      TRIPLE_FREQ_4PHASE
    
      TRIPLE_FREQ_4PHASE_GRAY_4PHASE_GRAY_4PHASE_BG
    
      QUAD_FREQ_4PHASE
    
      QUAD_FREQ_4PHASE_GRAY_4PHASE_BG_4PHASE_GRAY_4PHASE_BG
    
      BG_OUTDOOR
    
      GRAY_ONLY
    
      CUSTOM
    """
    BG_OUTDOOR: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.BG_OUTDOOR: 18>
    CUSTOM: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.CUSTOM: 20>
    DOUBLE_FREQ_4PHASE: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.DOUBLE_FREQ_4PHASE: 10>
    DOUBLE_FREQ_4PHASE_4BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.DOUBLE_FREQ_4PHASE_4BG: 12>
    DOUBLE_FREQ_4PHASE_GRAY_4PHASE_BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.DOUBLE_FREQ_4PHASE_GRAY_4PHASE_BG: 11>
    DOUBLE_FREQ_4PHASE_GRAY_5BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.DOUBLE_FREQ_4PHASE_GRAY_5BG: 13>
    GRAY_ONLY: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.GRAY_ONLY: 19>
    QUAD_FREQ_4PHASE: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.QUAD_FREQ_4PHASE: 16>
    QUAD_FREQ_4PHASE_GRAY_4PHASE_BG_4PHASE_GRAY_4PHASE_BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.QUAD_FREQ_4PHASE_GRAY_4PHASE_BG_4PHASE_GRAY_4PHASE_BG: 17>
    SINGLE_FREQ_2PHASE: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_2PHASE: 0>
    SINGLE_FREQ_4PHASE: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_4PHASE: 1>
    SINGLE_FREQ_4PHASE_4BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_4PHASE_4BG: 4>
    SINGLE_FREQ_4PHASE_BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_4PHASE_BG: 3>
    SINGLE_FREQ_4PHASE_GRAY: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_4PHASE_GRAY: 2>
    SINGLE_FREQ_4PHASE_GRAY_5BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_4PHASE_GRAY_5BG: 5>
    SINGLE_FREQ_BG_4PHASE_BG_GRAY: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_BG_4PHASE_BG_GRAY: 9>
    SINGLE_FREQ_BG_GRAY_BG_4PHASE: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_BG_GRAY_BG_4PHASE: 8>
    SINGLE_FREQ_GRAY_BG_4PHASE_BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_GRAY_BG_4PHASE_BG: 7>
    SINGLE_FREQ_GRAY_BG_4PHASE_GRAY_BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.SINGLE_FREQ_GRAY_BG_4PHASE_GRAY_BG: 6>
    TRIPLE_FREQ_4PHASE: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.TRIPLE_FREQ_4PHASE: 14>
    TRIPLE_FREQ_4PHASE_GRAY_4PHASE_GRAY_4PHASE_BG: typing.ClassVar[TofFrameWorkMode]  # value = <TofFrameWorkMode.TRIPLE_FREQ_4PHASE_GRAY_4PHASE_GRAY_4PHASE_BG: 15>
    __members__: typing.ClassVar[dict[str, TofFrameWorkMode]]  # value = {'SINGLE_FREQ_2PHASE': <TofFrameWorkMode.SINGLE_FREQ_2PHASE: 0>, 'SINGLE_FREQ_4PHASE': <TofFrameWorkMode.SINGLE_FREQ_4PHASE: 1>, 'SINGLE_FREQ_4PHASE_GRAY': <TofFrameWorkMode.SINGLE_FREQ_4PHASE_GRAY: 2>, 'SINGLE_FREQ_4PHASE_BG': <TofFrameWorkMode.SINGLE_FREQ_4PHASE_BG: 3>, 'SINGLE_FREQ_4PHASE_4BG': <TofFrameWorkMode.SINGLE_FREQ_4PHASE_4BG: 4>, 'SINGLE_FREQ_4PHASE_GRAY_5BG': <TofFrameWorkMode.SINGLE_FREQ_4PHASE_GRAY_5BG: 5>, 'SINGLE_FREQ_GRAY_BG_4PHASE_GRAY_BG': <TofFrameWorkMode.SINGLE_FREQ_GRAY_BG_4PHASE_GRAY_BG: 6>, 'SINGLE_FREQ_GRAY_BG_4PHASE_BG': <TofFrameWorkMode.SINGLE_FREQ_GRAY_BG_4PHASE_BG: 7>, 'SINGLE_FREQ_BG_GRAY_BG_4PHASE': <TofFrameWorkMode.SINGLE_FREQ_BG_GRAY_BG_4PHASE: 8>, 'SINGLE_FREQ_BG_4PHASE_BG_GRAY': <TofFrameWorkMode.SINGLE_FREQ_BG_4PHASE_BG_GRAY: 9>, 'DOUBLE_FREQ_4PHASE': <TofFrameWorkMode.DOUBLE_FREQ_4PHASE: 10>, 'DOUBLE_FREQ_4PHASE_GRAY_4PHASE_BG': <TofFrameWorkMode.DOUBLE_FREQ_4PHASE_GRAY_4PHASE_BG: 11>, 'DOUBLE_FREQ_4PHASE_4BG': <TofFrameWorkMode.DOUBLE_FREQ_4PHASE_4BG: 12>, 'DOUBLE_FREQ_4PHASE_GRAY_5BG': <TofFrameWorkMode.DOUBLE_FREQ_4PHASE_GRAY_5BG: 13>, 'TRIPLE_FREQ_4PHASE': <TofFrameWorkMode.TRIPLE_FREQ_4PHASE: 14>, 'TRIPLE_FREQ_4PHASE_GRAY_4PHASE_GRAY_4PHASE_BG': <TofFrameWorkMode.TRIPLE_FREQ_4PHASE_GRAY_4PHASE_GRAY_4PHASE_BG: 15>, 'QUAD_FREQ_4PHASE': <TofFrameWorkMode.QUAD_FREQ_4PHASE: 16>, 'QUAD_FREQ_4PHASE_GRAY_4PHASE_BG_4PHASE_GRAY_4PHASE_BG': <TofFrameWorkMode.QUAD_FREQ_4PHASE_GRAY_4PHASE_BG_4PHASE_GRAY_4PHASE_BG: 17>, 'BG_OUTDOOR': <TofFrameWorkMode.BG_OUTDOOR: 18>, 'GRAY_ONLY': <TofFrameWorkMode.GRAY_ONLY: 19>, 'CUSTOM': <TofFrameWorkMode.CUSTOM: 20>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    @typing.overload
    def __int__(self) -> int:
        ...
    @typing.overload
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class TofWorkMode:
    """
    Members:
    
      SINGLE_FREQ
    
      DOUBLE_FREQ
    
      TRIPLE_FREQ
    
      QUAD_FREQ
    
      DISTANCE
    
      HDR
    
      AE
    
      BG_OUTDOOR
    
      GRAY_ONLY
    
      CUSTOM1
    
      CUSTOM2
    
      CUSTOM3
    """
    AE: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.AE: 6>
    BG_OUTDOOR: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.BG_OUTDOOR: 7>
    CUSTOM1: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.CUSTOM1: 9>
    CUSTOM2: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.CUSTOM2: 10>
    CUSTOM3: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.CUSTOM3: 11>
    DISTANCE: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.DISTANCE: 4>
    DOUBLE_FREQ: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.DOUBLE_FREQ: 1>
    GRAY_ONLY: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.GRAY_ONLY: 8>
    HDR: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.HDR: 5>
    QUAD_FREQ: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.QUAD_FREQ: 3>
    SINGLE_FREQ: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.SINGLE_FREQ: 0>
    TRIPLE_FREQ: typing.ClassVar[TofWorkMode]  # value = <TofWorkMode.TRIPLE_FREQ: 2>
    __members__: typing.ClassVar[dict[str, TofWorkMode]]  # value = {'SINGLE_FREQ': <TofWorkMode.SINGLE_FREQ: 0>, 'DOUBLE_FREQ': <TofWorkMode.DOUBLE_FREQ: 1>, 'TRIPLE_FREQ': <TofWorkMode.TRIPLE_FREQ: 2>, 'QUAD_FREQ': <TofWorkMode.QUAD_FREQ: 3>, 'DISTANCE': <TofWorkMode.DISTANCE: 4>, 'HDR': <TofWorkMode.HDR: 5>, 'AE': <TofWorkMode.AE: 6>, 'BG_OUTDOOR': <TofWorkMode.BG_OUTDOOR: 7>, 'GRAY_ONLY': <TofWorkMode.GRAY_ONLY: 8>, 'CUSTOM1': <TofWorkMode.CUSTOM1: 9>, 'CUSTOM2': <TofWorkMode.CUSTOM2: 10>, 'CUSTOM3': <TofWorkMode.CUSTOM3: 11>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    @typing.overload
    def __int__(self) -> int:
        ...
    @typing.overload
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
__version__: str = '0.1.20'