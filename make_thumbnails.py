import os
import sys
from PIL import Image

print('\n')
print(sys.version)

class FourChannelImage(Exception):
    """ in case you get RGBA images.  """


#path = 'f:\\Invasives\\Photos'
#path = 'F:\\Richie\\PhotoSessionsRS'
path = 'F:\\PhotoSessions\\2023'

for family in os.listdir(path):
    family_path = os.path.join(path, family)
    if os.path.isdir(family_path):
        for species in os.listdir(family_path):
            species_path = os.path.join(family_path, species)
            if os.path.isdir(species_path):
                for filename in os.listdir(species_path):
                    # print(filename)
                    if filename.lower().endswith(('.jpg', '.jpeg')):
                        full_path = os.path.join(species_path, filename)
                        thumbs_path = os.path.join(species_path, 'Thumbs')
                        if not os.path.isdir(thumbs_path):
                            os.makedirs(thumbs_path)
                        thumb_file = os.path.join(thumbs_path, filename)
                        if not os.path.exists(thumb_file):
                            try:
                                with Image.open(full_path) as img:
                                    img.thumbnail((480, 480))
                                    if img.mode == 'RGBA':
                                        raise(FourChannelImage)
                                    img.save(thumb_file)
                                    print(f'Generated a thumb for {filename}')
                            except FourChannelImage as exc:
                                print(f"4 Channel Image detected {full_path}")
                                # Log to logfile
                            except OSError as exc:
                                print(f"Unknown OS Error occured with {full_path}  ")
                                # Print to log file here. include path name
                            except Exception as e:
                                print("exception occured")
                                print(sys.exc_info())
                                print(e)
                                # Print to log file here.



