import filecmp
import sys

from siaskynet import Skynet

# upload a file

SRC_FILE = "./LICENSE.txt"

print("Uploading file "+SRC_FILE)
skylink = Skynet.upload_file(SRC_FILE)
print("File upload successful, skylink: " + skylink)

# download a file

DST_FILE = "./dst.txt"

print("Downloading to "+DST_FILE)
skylink = skylink[len(Skynet.uri_skynet_prefix()):]
Skynet.download_file(DST_FILE, skylink)
if not filecmp.cmp(SRC_FILE, DST_FILE):
    sys.exit("ERROR: Downloaded file at "+DST_FILE +
             " did not equal uploaded file "+SRC_FILE)
print("File download successful")

# upload a directory

SRC_DIR = "./siaskynet"

print("Uploading dir "+SRC_DIR)
skylink = Skynet.upload_directory(SRC_DIR)
print("Dir upload successful, skylink: " + skylink)
