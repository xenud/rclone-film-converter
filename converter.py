import glob, os, subprocess, shlex, json
import shutil

print("Started")
for file in glob.iglob("/home/runner/work/rclone-film-converter/rclone-film-converter/drive/" + '**/*.*', recursive=True):
  print("File found")
  bashCommand = "ffprobe -v quiet -print_format json -show_format -show_streams \"" + file + "\""
  process = subprocess.Popen(shlex.split(bashCommand), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output, error = process.communicate()
  res = json.loads(output)
  video_need_conv = False
  audio_need_conv = False
  try:
    for key in res["streams"]:
      #print(key["codec_type"])
      if(key["codec_type"] == "video"):
        if(key["codec_name"] != "h264"):
          video_need_conv = True
      if(key["codec_type"] == "audio"):
        if(key["codec_name"] != "aac"):
          audio_need_conv = True
    #print(video_need_conv, audio_need_conv)
    base=os.path.basename(file)
    nome_file = os.path.splitext(base)[0] + os.path.splitext(base)[1]
    if not os.path.exists(file.replace("drive/", "drive/🎥 Cineserver (H264 – AAC)/")):
      try:
        os.makedirs(file.replace("drive/", "drive/🎥 Cineserver (H264 – AAC)/").replace(nome_file, ""))
      except:
        print("cartelle esistono")
      if(video_need_conv == True or audio_need_conv == True):
        print("Converto...")
        #print(os.path.splitext(base)[1])
        #print(file.replace(os.path.splitext(base)[0] + os.path.splitext(base)[1], "") + os.path.splitext(base)[0] + ".mkv")
        bashCommand = "ffmpeg -i \"" + file + "\" -map 0 -c:s copy -c:v libx264 -crf 19 -c:a aac -b:a 128k -movflags +faststart -y \"" + file.replace(nome_file, "").replace("drive/", "drive/🎥 Cineserver (H264 – AAC)/") + os.path.splitext(base)[0] + ".mkv\""
        print(bashCommand)
        process = subprocess.Popen(shlex.split(str(bashCommand)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        #if not error:
        #  os.remove(file)
      else:
        print(file)
        print(nome_file)
        print("Copio...")
        shutil.copy(file, file.replace("drive/", "drive/🎥 Cineserver (H264 – AAC)/"))

  
  except Exception as e:
    print("Errore: " + file)
    print(e)
