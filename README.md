# WhatsappImgDater
A python program that imports date information to your whatsapp images.
U will need to install piexif and Pillow libraries to use program.

Normally whatsapp images have a name like IMG-20230820-WA0001.jpg and they dont have any shot date metadata in it. This program splits the file name with "-" symbol and splits the second part to three parts.
First one is year, second one is month, third one is day.
And it inserts this information to photos and videos.
Shot hour would be a constant random hour.\
\
It also supports videos too. You will need to install ffmpeg to your computer for video.

Use it with a bat/cmd file. \
python X/main.py X/yourfolder \
Enjoy it.
