from PIL import Image, ImageMath


def LSB(openpoint,mode):
    print(openpoint)
    if(mode):
        watermark=Image.open(r"images/logi.jpg")
        original=Image.open(openpoint)
        watermark=watermark.resize(original.size)
        red, green, blue = original.split()
        wred, wgreen, wblue = watermark.split()
        red2 = ImageMath.eval("convert(a&0xFE|b&0x1,'L')", a=red, b=wred)
        green2 = ImageMath.eval("convert(a&0xFE|b&0x1,'L')", a=green, b=wgreen)
        blue2 = ImageMath.eval("convert(a&0xFE|b&0x1,'L')", a=blue, b=wblue)
        out = Image.merge("RGB", (red2, green2, blue2))
        out.save(r"images/LSB-watermarked.png")
        return "images/LSB-watermarked.png"

    else:
        #print("a")
        stegged=Image.open(openpoint)
        red, green, blue = stegged.split()
        watermark1=ImageMath.eval("((a&0x01)*255)",a=red)
         # convert to 0 or 255
        watermark1=watermark1.convert("L")
        watermark2=ImageMath.eval("((a&0x01)*255)",a=green)
         # convert to 0 or 255
        watermark2=watermark1.convert("L")
        watermark3=ImageMath.eval("((a&0x01)*255)",a=blue)
         # convert to 0 or 255
        watermark3=watermark1.convert("L")
        watermark= Image.merge("RGB", (watermark1,watermark2,watermark3))
        watermark.save(r"images/extracted-watermark.png")
        return "images/extracted-watermark.png"
