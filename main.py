import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math

def round_odd_int(x):
	if x%2 == 0:
		return math.ceil(x)
	else:
		return math.floor(x)

# Config

# qr_data = 'Know the pulse of your business'
qr_data = 'F9IkkR3V6TnP'
logo_path = 'img\\hp_logo3.png'

# QRcolor = 'Black'
QRcolor = (30, 68, 150) # HP Blue for location QRs
# QRcolor = (168, 204, 60) # HP Green, nooooo
QRback_color = "white"
# QRback_color = (102, 101, 99) # HP Gray

dpi = 300

# QR v2, 25x25 modules
qr_min_version = 4

if qr_min_version == 2:
	qr_box_size = int(dpi/25)
elif qr_min_version == 4:
	qr_box_size = int(dpi/33)
else:
	qr_box_size = 10

# Create QR
QRcode = qrcode.QRCode(
	error_correction=qrcode.constants.ERROR_CORRECT_H,
	border=0,
	box_size=qr_box_size,
	version=qr_min_version
	# v2 -> 25x25 module grid
	# v4 # 33x33 modules, might need this to go with dynamic QRs
	# HP admin panels looks to be 21x21 which is v1?  Does this change with adding the logo?
)
QRcode.add_data(qr_data)

# Add qr color
QRimg = QRcode.make_image(
	fill_color=QRcolor, back_color=QRback_color, ).convert('RGB')
	# fill_color = QRback_color, back_color = QRcolor).convert('RGB')
# QRimg.show()
pass

# Logo
logo = Image.open(logo_path)

# taking base width
# logo_dim_modules = QRcode.modules_count-16
logo_dim_modules = round_odd_int( QRcode.modules_count*0.36)
logo_dim_px = int(logo_dim_modules*qr_box_size)

# adjust image size
# wpercent = (basewidth/float(logo.size[0]))
# hsize = int((float(logo.size[1])*float(wpercent)))
# logo = logo.resize((basewidth, hsize), Image.LANCZOS)
logo = logo.resize( (logo_dim_px, logo_dim_px), Image.LANCZOS)

# add logo
pos = ((QRimg.size[0] - logo.size[0]) // 2,
	(QRimg.size[1] - logo.size[1]) // 2)
QRimg.paste(logo, pos)
QRimg = QRimg.resize((dpi,dpi))
# QRimg.show()
pass

# add text
message = '12345678901234567890'
txt_img = Image.new( 'RGB', size=(QRimg.size[0], int(dpi*3/32)), color=(256,256,256))
draw = ImageDraw.Draw(txt_img)
font = ImageFont.truetype('segoeui.ttf', 27)
_, _, w, h = draw.textbbox((0, 0), message, font=font)
loc = ((txt_img.size[0]-w)/2, -7)
# loc = (0,-7)
draw.text(xy=loc, text=message, font=font, fill=QRcolor)
# txt_img.show()
# QRimg.show()
txt_pos = (0, QRimg.size[1])
QRimg = ImageOps.expand( QRimg, border=(0,0,0,txt_img.size[1]), fill=(256,256,256))
# QRimg.show()
QRimg.paste(txt_img, txt_pos)

QRimg.show()
pass

# save the QR code generated
QRimg.save('QRs\\gfg_QR.png')

# print('QR code generated!')
