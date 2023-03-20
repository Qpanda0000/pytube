from pytube import YouTube
from pytube import Playlist
import pytube.exceptions
import subprocess
import os
import time

path = ''

nowtime=time.localtime()
errorlog_fname=str(nowtime.tm_year) + '{:0>2d}'.format(nowtime.tm_mon) + '{:0>2d}'.format(nowtime.tm_mday) +', '+ '{:0>2d}'.format(nowtime.tm_hour)+ '_' + '{:0>2d}'.format(nowtime.tm_min)+ '_' + '{:0>2d}'.format(nowtime.tm_sec)
f=open('./log/'+ errorlog_fname +'.txt','w')

#----gettime----
def gettime():
    nowtime=time.localtime()
    return str(nowtime.tm_year) + '{:0>2d}'.format(nowtime.tm_mon) + '{:0>2d}'.format(nowtime.tm_mday) +','+ '{:0>2d}'.format(nowtime.tm_hour)+ ':' + '{:0>2d}'.format(nowtime.tm_min)+ ':' + '{:0>2d}'.format(nowtime.tm_sec) + '\t'

#----getname----
def getname(url):
    for i in range(10):
        try:
            name = YouTube(url).title
            return name
        except:
            continue
    f.write(gettime() + url + '\t' + 'get name error\n')
    return('get name error %s' %(url))

#----download mp4----
def downloadmp4(url):
    yt = YouTube(url)
    name = getname(url)
    characters = ':/\\\'\"*;~!$&>@?|.'
    for i in range(len(characters)):
        name = name.replace(characters[i],'')
    try:
        yt.streams.filter(mime_type="audio/mp4").last().download(filename='audio.mp3')
        yt.streams.filter(res='1080p').first().download(filename='video.mp4')
    except pytube.exceptions.VideoUnavailable:
        f.write(gettime() + url + '\t' + 'download mp4 error -- video is unavailable')
        return('download mp4 error -- video is unavailable')
    except pytube.exceptions.RegexMatchError:
        f.write(gettime() + url + '\t' + 'download mp4 error -- regex match error')
        return('download mp4 error -- regex match error')
    except pytube.exceptions.PytubeError:
        f.write(gettime() + url + '\t' + 'download mp4 error -- pytube error')
        return('download mp4 error -- pytube error')
    except:
        f.write(gettime() + url + '\t' + 'download mp4 error')
        return('download mp4 error')
    try:
        subprocess.call('ffmpeg -y -i ./video.mp4 -i ./audio.mp3 -c copy tem.mp4',shell=True)
    except:
        f.write(gettime() + url + '\t' + 'ffmpeg error')
        return('ffmpeg error')
    try:
        if not os.path.exists('./'+path+'/mp4/'):
            os.makedirs('./'+path+'/mp4/')
        os.rename('tem.mp4',name+'.mp4')
        os.replace('./'+name+'.mp4','./'+path+'/mp4/'+name +'.mp4')
    except OSError as e:
        f.write(gettime() + url + '\t' + 'replace mp4 file error -- %s - %s' %(e.filename,e.strerror))
        os.remove(name+'.mp4')
        print('replace mp4 file error -- %s - %s' %(e.filename,e.strerror))
    try:
        os.remove('./audio.mp3')
    except OSError as e:
        f.write(gettime() + url + '\t' + 'remove audio error -- %s - %s' %(e.filename,e.strerror))
        return('remove audio error -- %s - %s' %(e.filename,e.strerror))
    try:
        os.remove('./video.mp4')
    except OSError as e:
        f.write(gettime() + url + '\t' + 'remove video error -- %s - %s' %(e.filename,e.strerror))
        return('remove video error -- %s - %s' %(e.filename,e.strerror))
    return('download mp4 done')

#----download mp3----
def downloadmp3(url):
    yt=YouTube(url)
    name = getname(url)
    characters = ':/\\\'\"*;~!$&>@?|'
    for i in range(len(characters)):
        name = name.replace(characters[i],'')
    try:
        yt.streams.filter(mime_type="audio/mp4").last().download('./'+path,filename=name + '.mp3')
        return('download mp3 done')
    except pytube.exceptions.VideoUnavailable:
        f.write(gettime() + url + '\t' + 'download mp3 error -- video is unavailable')
        return('download mp3 error -- video is unavailable')
    except pytube.exceptions.RegexMatchError:
        f.write(gettime() + url + '\t' + 'download mp3 error -- regex match error')
        return('download mp3 error -- regex match error')
    except pytube.exceptions.PytubeError:
        f.write(gettime() + url + '\t' + 'download mp3 error -- pytube error')
        return('download mp3 error -- pytube error')
    except:
        f.write(gettime() + url + '\t' + 'download mp3 error')
        return('download mp3 error')

#----main----
url = input('input youtube url: ')
while True:
    type = input('enter "a" to download mp3 enter "b" to download mp4: ')
    if type == 'a' or type == 'b':
        break
    else:
        continue

if 'list' in url:
    print('playlist')
    plurl = Playlist(url)
    for i in plurl.video_urls:
        name = getname(i)
        if type == 'a':
            print(name+'\t'+downloadmp3(i))
        elif type == 'b':
            print(name+'\t'+downloadmp4(i))
else:
    print('not playlist')
    name = getname(url)
    if type == 'a':
        print(name+'\t'+downloadmp3(url))
    elif type == 'b':
        print(name+'\t'+downloadmp4(url))
f.write('--------------------------------------------------\n'+gettime()+'\t'+'done')
f.close()