import spydaap, spydaap.parser.mp3, spydaap.parser.ogg, spydaap.parser.flac

spydaap.parsers = [spydaap.parser.mp3.Mp3Parser(), 
                   spydaap.parser.flac.FlacParser(), 
                   spydaap.parser.ogg.OggParser()]

#to process .mov files
#from spydaap.parser import mp3,mov

#spydaap.server_name = "spydaap"
#spydaap.port = 3689

#top path to scan for media
#spydaap.media_path = "media"

#spydaap.cache_dir = 'cache'
