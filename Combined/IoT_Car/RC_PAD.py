from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5 import QtSql
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from google.cloud import speech
import time
import os
import re # 정규표현식 모듈
import sys

from google.cloud import speech
import pyaudio  # 파이썬에서 오디오 입력 사용
import queue

# Audio recording parameters
STREAMING_LIMIT = 60000
RATE = 16000
#RATE = 48000
CHUNK = int(RATE / 10)  

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/black-radius-332505-32929f26700c.json"

before_str = ""
th = None
pThread = None
mThread = None
stop_list = ["정지","스탑","스톱","멈춰","그만","stop"]
go_list = ["출발","고","go","전진","앞으로","직진"]
back_list = ["뒤로","back","후진","후퇴"]
left_list = ["왼쪽","left","좌측","왼"]
right_list = ["오른쪽","오른","right","우측"]
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL',"mainWindow")
        self.db.setHostName("ec2-3-36-129-200.ap-northeast-2.compute.amazonaws.com")
        self.db.setDatabaseName("2-3")
        self.db.setUserName("ssafy2_3")
        self.db.setPassword("ssafy1234")
        ok = self.db.open()
        print(ok)
        
        self.query = QtSql.QSqlQuery(self.db)
        self.query.exec("truncate command_1")
        #self.timer = QTimer()
        #self.timer.setInterval(1000)
        #self.timer.timeout.connect(self.pollingQuery)
        #self.timer.start()
        loadUi("test.ui",self)
        global th
        global pThread
        global mThread
        self.setWindowTitle("RC-Car PAD")
        th = QMyThread(self.label)
        th.start(QThread.LowestPriority)
        pThread = QPollingThread(self.text,self.lcdNumber,self.lcdNumber_2)
        pThread.textSignal.connect(self.textSignalEmitted)
        pThread.start(QThread.LowestPriority)
        mThread = QMicThread()
        mThread.stopSignal.connect(self.clickedMid)
        mThread.goSignal.connect(self.clickedGo)
        mThread.backSignal.connect(self.clickedBack)
        mThread.leftSignal.connect(self.clickedLeft)
        mThread.rightSignal.connect(self.clickedRight)
        mThread.start()
        #pThread.start()
    def textSignalEmitted(self,text):
        self.text.appendPlainText(text)
        
    def clickedRight(self):
        self.commandQuery("right","1 sec")
    def clickedLeft(self):
        self.commandQuery("left","1 sec")
    def clickedGo(self):
        self.commandQuery("go","1 sec")
    def clickedBack(self):
        self.commandQuery("back","1 sec")
    def clickedMid(self):
        self.commandQuery("mid","1 sec")
    def pollingQuery(self):
        result = self.query.exec("select * from command_1 order by time desc limit 1");
        
        if self.query.next():
        
            self.record = self.query.record()
            str = "%10s | %10s | %4d" % (self.record.value(1),self.record.value(2), self.record.value(3))
                
                
        result = self.query.exec("select * from sensing_1 order by time desc limit 1");
        if self.query.next():
            record = self.query.record()
            self.lcdNumber.display(record.value(2)*100)
            self.lcdNumber_2.display(record.value(3)*100)
    def commandQuery(self, cmd, arg):
        self.query.prepare("insert into command_1 (time, cmd_string, arg_string, is_finish) values(:time, :cmd, :arg, :finish)")
        time = QDateTime().currentDateTime()
        self.query.bindValue(":time", time)
        self.query.bindValue(":cmd", cmd)
        self.query.bindValue (":arg",arg)
        self.query.bindValue(":finish", 0)
        self.query.exec()
    def leftPress(self):
        self.commandQuery("leftside","press")
    def leftRelease(self):
        self.commandQuery("leftside","release")
    def rightPress(self):
        self.commandQuery("rightside","press")
    def rightRelease(self):
        self.commandQuery("rightside","release")
    def frontPress(self):
        self.commandQuery("front","press")
    def frontRelease(self):
        self.commandQuery("front","release")

class QMyThread(QThread):
    def __init__(self,label):
        super().__init__()
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL',"thread")
        self.db.setHostName("ec2-3-36-129-200.ap-northeast-2.compute.amazonaws.com")
        self.db.setDatabaseName("2-3")
        self.db.setUserName("ssafy2_3")
        self.db.setPassword("ssafy1234")
        ok = self.db.open()
        self.query = QtSql.QSqlQuery(self.db)
        self.label = label
    def run(self):
        while True:            
            result = self.query.exec("select * from test_blob");
            if self.query.next():            
                pixmap = QPixmap() 
                pixmap.loadFromData(self.query.record().value(0));
                self.label.setPixmap(pixmap)

class QPollingThread(QThread):
    textSignal = pyqtSignal(str)
    def __init__(self,text,lcd1,lcd2):
        super().__init__()
        self.text = text
        self.lcd1 = lcd1
        self.lcd2 = lcd2
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL',"PollingThread")
        self.db.setHostName("ec2-3-34-192-207.ap-northeast-2.compute.amazonaws.com")
        self.db.setDatabaseName("2-3")
        self.db.setUserName("ssafy2_3")
        self.db.setPassword("ssafy1234")
        ok = self.db.open()
        self.query = QtSql.QSqlQuery(self.db)
        self.before_str = None
    def run(self):
        while True:
            result = self.query.exec("select * from command_1 order by time desc limit 1");
            
            if self.query.next():
                #self.text.clear()
                #while (self.query.next()):
                
                record = self.query.record()
                str = "%10s | %10s | %4d" % (record.value(1),record.value(2), record.value(3))
                    #self.text.appendPlainText(str)
                if not self.before_str:
                    self.before_str = str
                    #self.text.appendPlainText(str)
                    self.textSignal.emit(str)
                else:
                    if self.before_str != str:
                        #self.text.appendPlainText(str)
                        self.textSignal.emit(str)
                        self.before_str = str
                    
                    
            result = self.query.exec("select * from sensing_1 order by time desc limit 1");
            if self.query.next():
                #while (self.query.next()):
                record = self.query.record()
                #str += "%s | %10s | %10s | %10s n" % (self.record.value(0).toString(),
                #s elf.record.value(1), self.record.value(2), self.record.value(3))
                #self.text2.setPlainText(str)
                self.lcd1.display(record.value(2)*100)
                self.lcd2.display(record.value(3)*100)

                
def get_current_time():
    """Return Current Time in MS."""

    return int(round(time.time() * 1000))


class ResumableMicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk_size):
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        self.start_time = get_current_time()
        self.restart_counter = 0
        self.audio_input = []
        self.last_audio_input = []
        self.result_end_time = 0
        self.is_final_end_time = 0
        self.final_request_end_time = 0
        self.bridging_offset = 0
        self.last_transcript_was_final = False
        self.new_stream = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

    def __enter__(self):

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, *args, **kwargs):
        """Continuously collect data from the audio stream, into the buffer."""

        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Stream Audio from microphone to API and to local buffer"""

        while not self.closed:
            data = []
            
            """
            THE BELOW 'IF' STATEMENT IS WHERE THE ERROR IS LIKELY OCCURRING
            This statement runs when the streaming limit is hit and a new request is made.
            """
            if self.new_stream and self.last_audio_input:

                chunk_time = STREAMING_LIMIT / len(self.last_audio_input)

                if chunk_time != 0:

                    if self.bridging_offset < 0:
                        self.bridging_offset = 0

                    if self.bridging_offset > self.final_request_end_time:
                        self.bridging_offset = self.final_request_end_time

                    chunks_from_ms = round(
                        (self.final_request_end_time - self.bridging_offset)
                        / chunk_time
                    )

                    self.bridging_offset = round(
                        (len(self.last_audio_input) - chunks_from_ms) * chunk_time
                    )

                    for i in range(chunks_from_ms, len(self.last_audio_input)):
                        data.append(self.last_audio_input[i])

                self.new_stream = False

            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            self.audio_input.append(chunk)

            if chunk is None:
                return
            data.append(chunk)
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)

                    if chunk is None:
                        return
                    data.append(chunk)
                    self.audio_input.append(chunk)

                except queue.Empty:
                    break

            yield b"".join(data)


def listen_print_loop(responses,stream,stopSignal,goSignal,backSignal,leftSignal,rightSignal):
    global stop_list
    global go_list
    global before_str
    global back_list
    global left_list
    global right_list
    global before_str
    target_str = ""
    for response in responses:

        if get_current_time() - stream.start_time > STREAMING_LIMIT:
            stream.start_time = get_current_time()
            break

        if not response.results:
            continue

        result = response.results[0]

        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        result_seconds = 0
        result_micros = 0

        if result.result_end_time.seconds:
            result_seconds = result.result_end_time.seconds

        if result.result_end_time.microseconds:
            result_micros = result.result_end_time.microseconds

        stream.result_end_time = int((result_seconds * 1000) + (result_micros / 1000))

        corrected_time = (
            stream.result_end_time
            - stream.bridging_offset
            + (STREAMING_LIMIT * stream.restart_counter)
        )
        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        
        if result.is_final:

            sys.stdout.write("FINAL RESULT @ ")
            sys.stdout.write(str(corrected_time/1000) + ": " + transcript + "\n")

            stream.is_final_end_time = stream.result_end_time
            stream.last_transcript_was_final = True

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                sys.stdout.write("Exiting...\n")
                stream.closed = True
                break

        else:
            sys.stdout.write("INTERIM RESULT @ ")
            sys.stdout.write(str(corrected_time/1000) + ": " + transcript + "\r")

            stream.last_transcript_was_final = False
        
        if before_str != transcript:
            target_str = transcript
            if len(before_str) < len(transcript):
                target_str = transcript[len(before_str):]
            before_str = transcript
            for stop in stop_list:
                if stop in target_str:
                    stopSignal.emit()
                    break
            for go in go_list:
                if go in target_str:
                    goSignal.emit()
                    break
            for back in back_list:
                if back in target_str:
                    backSignal.emit()
                    break;
            for left in left_list:
                if left in target_str:
                    leftSignal.emit()
                    break;
            for right in right_list:
                if right in target_str:
                    rightSignal.emit()
                    break;
                
        
            
                
            
    

class QMicThread(QThread):
    stopSignal = pyqtSignal()
    goSignal = pyqtSignal()
    backSignal = pyqtSignal()
    leftSignal = pyqtSignal()
    rightSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        
    def run(self):
        language_code = 'ko-KR'  # a BCP-47 language tag

        client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding='LINEAR16', # enums.RecognitionConfig.AudioEncoding.LINEAR16
            sample_rate_hertz=RATE,
            max_alternatives=1, # 가장 가능성 높은 1개 alternative만 받음.
            language_code=language_code)
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True) # 해석완료되지 않은(is_final=false) 중도값도 사용.

        mic_manager = ResumableMicrophoneStream(RATE, CHUNK)
        print(mic_manager.chunk_size)
        sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')
        sys.stdout.write("End (ms)       Transcript Results/Status\n")
        sys.stdout.write("=====================================================\n")

        with mic_manager as stream:

            while not stream.closed:
                sys.stdout.write(
                    "\n" + str(STREAMING_LIMIT * stream.restart_counter) + ": NEW REQUEST\n"
                )

                stream.audio_input = []
                audio_generator = stream.generator()

                requests = (
                    speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator
                )

                responses = client.streaming_recognize(streaming_config, requests)

                # Now, put the transcription responses to use.
                listen_print_loop(responses, stream,self.stopSignal,self.goSignal,self.backSignal,self.leftSignal,self.rightSignal)

                if stream.result_end_time > 0:
                    stream.final_request_end_time = stream.is_final_end_time
                stream.result_end_time = 0
                stream.last_audio_input = []
                stream.last_audio_input = stream.audio_input
                stream.audio_input = []
                stream.restart_counter = stream.restart_counter + 1

                if not stream.last_transcript_was_final:
                    sys.stdout.write("\n")
                stream.new_stream = True
        

app = QApplication([])
win = MyApp()
win.show()
app.exec()
