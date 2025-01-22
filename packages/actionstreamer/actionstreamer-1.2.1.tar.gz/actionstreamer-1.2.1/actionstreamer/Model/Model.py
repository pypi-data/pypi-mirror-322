from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class EventStatus(Enum):

    Checked_out = 2
    Complete = 4
    Error = 5
    Pending = 1
    Processing = 3
    Timed_out = 6


class VideoClipStatus(Enum):

    Announced = 1
    Transferring = 2
    Encoding = 3
    FileAvailable = 4
    AnnouncedButMissing = 5
    Highlighted = 6


class VideoClipType(Enum):

    Original_clip = 1
    Concatenated_clip = 2
    Extracted_clip = 3


class EventType:

    class Video(Enum):
        Start_bars = 9
        Follow = 8
        Receive_stream = 5
        Start_recording = 1
        Start_streaming = 3
        Stop_bars = 10
        Stop_receive_stream = 6
        Stop_recording = 2
        Stop_streaming = 4
        Test_event = 7
        Test_stop = 11
        Start_RTMP = 14
        Stop_RTMP = 15
        Join_conference = 24
        Leave_conference = 25

    class Transcoding(Enum):
        Transcode_file = 12
        Concatenate_files = 16
        Extract_video = 23
        Concatenate_files_ext = 26

    class Transfer(Enum):
        Transfer_file = 13

    class Device(Enum):  
        Add_network = 17
        Remove_network = 18
        Update_networks = 19
        Send_network_list = 20
        Update_software = 21
        Update_setting = 22


class Event:

    def __init__(self, key: int, userID: int, deviceID: int, agentTypeID: int, agentID: int, eventTypeID: int, serverEvent: int, eventStatus: str, eventParameters: str, processID: int, result: str, percentComplete: int, priority: int, expirationEpoch: int, attemptNumber: int, maxAttempts: int, checkoutToken: str, tagString: str, tagNumber: int, creationDate: str, createdBy: int, lastModifiedDate: str, lastModifiedBy: int):

        self.eventID = key
        self.userID = userID
        self.deviceID = deviceID
        self.agentTypeID = agentTypeID
        self.agentID = agentID
        self.eventTypeID = eventTypeID
        self.serverEvent = serverEvent
        self.eventStatus = eventStatus
        self.eventParameters = eventParameters
        self.processID = processID
        self.result = result
        self.percentComplete = percentComplete
        self.priority = priority
        self.expirationEpoch = expirationEpoch
        self.attemptNumber = attemptNumber
        self.maxAttempts = maxAttempts
        self.checkoutToken = checkoutToken
        self.tagString = tagString
        self.tagNumber = tagNumber
        self.creationDate = creationDate
        self.createdBy = createdBy
        self.lastModifiedDate = lastModifiedDate
        self.lastModifiedBy = lastModifiedBy


class EventWithNames(Event):

    def __init__(self, key: int, userID: int, deviceID: int, agentTypeID: int, agentID: int, eventTypeID: int, serverEvent: int, eventStatus: int, eventParameters: str, processID: int, result: str, percentComplete: int, priority: int, expirationEpoch: int, attemptNumber: int, maxAttempts: int, checkoutToken: str, tagString: str, tagNumber: int, creationDate: str, createdBy: int, lastModifiedDate: str, lastModifiedBy: int, deviceName: str, eventType: str, agentType: str, version: str, eventStatusName: str, eventStatusDescription: str, agentIndex: int):
        super().__init__(key, userID, deviceID, agentTypeID, agentID, eventTypeID, serverEvent, eventStatus, eventParameters, processID, result, percentComplete, priority, expirationEpoch, attemptNumber, maxAttempts, checkoutToken, tagString, tagNumber, creationDate, createdBy, lastModifiedDate, lastModifiedBy)
        self.deviceName = deviceName
        self.eventType = eventType
        self.agentType = agentType
        self.version = version
        self.eventStatusName = eventStatusName
        self.eventStatusDescription = eventStatusDescription
        self.agentIndex = agentIndex


class RecordingParameters:

    def __init__(self, height: int = 1920, width: int = 1080, fps: float = 30, bitrate: int = 5000000, vflip: int = 0, hflip: int = 0, encoding: str = '', segmentLengthSeconds: float = 0, audio: int = 0, rotationDegrees: int = 0):
        self.height = height
        self.width = width
        self.fps = fps
        self.bitrate = bitrate
        self.vflip = vflip
        self.hflip = hflip
        self.encoding = encoding
        self.segmentLengthSeconds = segmentLengthSeconds
        self.audio = audio
        self.rotationDegrees = rotationDegrees

class RTMPParameters:

    def __init__(self, height: int = 1920, width: int = 1080, fps: float = 30, bitrate: int = 5000000, server: str = '', port: int = 0, streamName: str = '', streamKey: str = '', hflip: int = 0, vflip: int = 0):
        self.height = height
        self.width = width
        self.fps = fps
        self.bitrate = bitrate
        self.server = server
        self.port = port
        self.stream_name = streamName
        self.stream_key = streamKey
        self.hflip = hflip
        self.vflip = vflip


class File:

    def __init__(self, key: int = 0, userID: int = 0, deviceID: int = 0, filename: str = '', fileGUID: str = '', sHA256Hash: str = '', fileLocation: str = '', fileExpiration: str = '', fileSize: int = '', fileInS3: bool = False, creationDate: str = '', createdBy: int = '', lastModifiedDate: str = '', lastModifiedBy: int = 0):
        self.key = key
        self.userID = userID
        self.deviceID = deviceID
        self.filename = filename
        self.fileGUID = fileGUID
        self.sHA256Hash = sHA256Hash
        self.fileLocation = fileLocation
        self.fileExpiration = fileExpiration
        self.fileSize = fileSize
        self.fileInS3 = fileInS3
        self.creationDate = creationDate
        self.createdBy = createdBy
        self.lastModifiedDate = lastModifiedDate
        self.lastModifiedBy = lastModifiedBy


class VideoClip:

    def __init__(self, key: int = 0, userID: int = 0, deviceID: int = 0, fileID: int = 0, tsFileID: int = 0, videoClipTypeID: int = 1, videoClipStatus: int = 0, videoClipParameters: str = '', localFilePath: str = '', height: int = 0, width: int = 0, fileSize: int = 0, framesPerSecond: float = 0, bitrate: int = 0, audioStatus: int = 0, startTime: int = 0, startTimeMs: int = 0, endTime: int = 0, endTimeMs: int = 0, clipLengthInSeconds: float = 0, tagListID: int = 0, creationDate: str = '', createdBy: int = 0, lastModifiedDate: int = '', lastModifiedBy: int = 0):
        self.videoClipID = key
        self.userID = userID
        self.deviceID = deviceID
        self.fileID = fileID
        self.tsFileID = tsFileID
        self.videoClipTypeID = videoClipTypeID
        self.videoClipStatus = videoClipStatus
        self.videoClipParameters = videoClipParameters
        self.localFilePath = localFilePath
        self.height = height
        self.width = width
        self.fileSize = fileSize
        self.framesPerSecond = framesPerSecond
        self.bitrate = bitrate
        self.audioStatus = audioStatus
        self.startTime = startTime
        self.startTimeMs = startTimeMs
        self.endTime = endTime
        self.endTimeMs = endTimeMs
        self.clipLengthInSeconds = clipLengthInSeconds
        self.tagListID = tagListID
        self.creationDate = creationDate
        self.createdBy = createdBy
        self.lastModifiedDate = lastModifiedDate
        self.lastModifiedBy = lastModifiedBy


class TranscodingParameters:

    def __init__(self, fileID: int, source: str, sourceFile: str, targetFile: str, fps: float, codec: str):
        self.fileID = fileID
        self.source = source
        self.sourceFile = sourceFile
        self.targetFile = targetFile
        self.fps = fps
        self.codec = codec


class TransferArgs:

    def __init__(self, fileID: int, videoClipID: int, localFilePath: str, remoteFilename: str, remoteFolderPath: str, url: str, action: str, attemptNumber: int, maxAttempts: int, firstAttemptStartTime: int, maxTimeToTryInSeconds: int):
        self.fileID = fileID
        self.videoClipID = videoClipID
        self.localFilePath = localFilePath
        self.remoteFilename = remoteFilename
        self.remoteFolderPath = remoteFolderPath
        self.url = url,
        self.action = action
        self.attemptNumber = attemptNumber,
        self.maxAttempts = maxAttempts
        self.firstAttemptStartTime = firstAttemptStartTime,
        self.maxTimeToTryInSeconds = maxTimeToTryInSeconds


class ConcatenateClipsArgs:

    def __init__(self, deviceID: int, deviceName: str, startEpoch: int, endEpoch: int, uploadURL: str, postbackURL: str, videoClips: list[VideoClip]):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.startEpoch = startEpoch
        self.endEpoch = endEpoch
        self.uploadURL = uploadURL
        self.postbackURL = postbackURL
        self.videoClips = videoClips


class ConferenceArgs:

    def __init__(self, url: str, roomName: str, displayName: str, videoWidth: int = 1280, videoHeight: int = 720, framerate: float = 30, videoBitrate: int = 1000000, sendVideo: bool = True, sendAudio: bool = True, receiveVideo: bool = True, receiveAudio: bool = True):
        self.url = url
        self.roomName = roomName
        self.displayName = displayName
        self.videoHeight = videoHeight
        self.videoWidth = videoWidth
        self.videoBitrate = videoBitrate
        self.framerate = framerate
        self.sendVideo = sendVideo
        self.sendAudio = sendAudio
        self.receiveVideo = receiveVideo
        self.receiveAudio = receiveAudio


class EpochRange:

    def __init__(self, startEpoch: int, endEpoch: int):
        self.startEpoch = startEpoch
        self.endEpoch = endEpoch


class WifiConnection:

    def __init__(self, ssid: str = '', connectionName: str = '', password: str = '', priority: int = 0):
        self.ssid = ssid
        self.password = password
        self.priority = priority
        self.connection_name = connectionName
       
class NameValuePair:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class EventDetails:
    eventID: int
    eventStatus: int
    eventParameters: str
    result: str
    percentComplete: float
    priority: int
    attemptNumber: int
    maxAttempts: int
    tagString: str
    tagNumber: int

    def __init__(self, eventID: int = None, eventStatus: int = None, eventParameters: str = None, result: str = None, percentComplete: float = None, priority: int = None, attemptNumber: int = None, maxAttempts: int = None, tagString: str = None, tagNumber: int = None):
        self.eventID = eventID
        self.eventStatus = eventStatus
        self.eventParameters = eventParameters
        self.result = result
        self.percentComplete = percentComplete
        self.priority = priority
        self.attemptNumber = attemptNumber
        self.maxAttempts = maxAttempts
        self.tagString = tagString
        self.tagNumber = tagNumber


class StandardResult:

    def __init__(self, code: str, description: str):
        self.code = code
        self.description = description


class DeviceObject:

    def __init__(self, key: int = 0, deviceTypeID: int = 0, userID: int = 0, deviceName: str = '', serialNumber: str = '', deviceDescription: str = '', recentOutput: str = '', cameraStatus: str = '', lastIPAddress: str = '', tunnelIPAddress: str = '', lastHeardFromDate: datetime = datetime.now(), softwareDate: datetime = datetime.now(), location: str = '', setupStatus: int = 0, autoSendFiles: int = 0, runStartupEvent: int = 0, deviceReadyEventPresetID: int = 0, standaloneEventPresetID: int = 0, logHealth: int = 0, audioChannelName: str = '', volume: int = 0, commentListID = 0, isArchived: bool = False, gUID: str = '', creationDate: datetime = datetime.now(), createdBy: int = 0, lastModifiedDate: datetime = datetime.now(), lastModifiedBy: int = 0):
        self.key = key
        self.deviceTypeID = deviceTypeID
        self.userID = userID
        self.deviceName = deviceName
        self.serialNumber = serialNumber
        self.deviceDescription = deviceDescription
        self.recentOutput = recentOutput
        self.cameraStatus = cameraStatus
        self.lastIPAddress = lastIPAddress
        self.tunnelIPAddress = tunnelIPAddress
        self.lastHeardFromDate = lastHeardFromDate
        self.softwareDate = softwareDate
        self.location = location
        self.setupStatus = setupStatus
        self.autoSendFiles = autoSendFiles
        self.runStartupEvent = runStartupEvent
        self.deviceReadyEventPresetID = deviceReadyEventPresetID
        self.standaloneEventPresetID = standaloneEventPresetID
        self.logHealth = logHealth
        self.audioChannelName = audioChannelName
        self.volume = volume
        self.commentListID = commentListID
        self.isArchived = isArchived
        self.gUID = gUID
        self.creationDate = creationDate
        self.createdBy = createdBy
        self.lastModifiedDate = lastModifiedDate
        self.lastModifiedBy = lastModifiedBy


class VideoClip:

    def __init__(self, key: int = 0, userID: int = 0, deviceID: int = 0, fileID: int = 0, tSFileID: int = 0, videoClipStatus: int = 0, videoClipTypeID: int = 0, videoClipParameters: str = '', localFilePath: str = '', height: int = 0, width: int = 0, filesize: int = 0, framesPerSecond: float = 0, bitrate: int = 0, audioStatus: int = 0, startTime: int = 0, startTimeMs: int = 0, endTime: int = 0, endTimeMs: int = 0, clipLengthInSeconds: float = 0, tagListID: int = 0, creationDate: str = '', createdBy: int = 0, lastModifiedDate: int = '', lastModifiedBy: int = 0):
        self.videoClipID = key
        self.userID = userID
        self.deviceID = deviceID
        self.fileID = fileID
        self.tSFileID = tSFileID
        self.videoClipStatus = videoClipStatus
        self.videoClipTypeID = videoClipTypeID
        self.videoClipParameters = videoClipParameters
        self.localFilePath = localFilePath
        self.height = height
        self.width = width
        self.filesize = filesize
        self.framesPerSecond = framesPerSecond
        self.bitrate = bitrate
        self.audioStatus = audioStatus
        self.startTime = startTime
        self.startTimeMs = startTimeMs
        self.endTime = endTime
        self.endTimeMs = endTimeMs
        self.clipLengthInSeconds = clipLengthInSeconds
        self.tagListID = tagListID
        self.creationDate = creationDate
        self.createdBy = createdBy
        self.lastModifiedDate = lastModifiedDate
        self.lastModifiedBy = lastModifiedBy


class CreateVideoClip:

    def __init__(self, deviceID: int = 0, deviceName: str = '', localFilePath: str = '', height: int = 0, width: int = 0, framesPerSecond: float = 0.0, startTime: int = 0, startTimeMs: int = 0, clipLengthInSeconds: float = 0.0, videoClipStatus: int = 0, videoClipTypeID: int = 0, videoClipParameters: str = ''):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.localFilePath = localFilePath
        self.height = height
        self.width = width
        self.framesPerSecond = framesPerSecond
        self.startTime = startTime
        self.startTimeMs = startTimeMs
        self.clipLengthInSeconds = clipLengthInSeconds
        self.videoClipStatus = videoClipStatus
        self.videoClipTypeID = videoClipTypeID
        self.videoClipParameters = videoClipParameters

