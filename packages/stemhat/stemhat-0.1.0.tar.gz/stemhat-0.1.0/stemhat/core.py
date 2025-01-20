import smbus


STEMHAT_ADDRESS         = 0x08   #Stemhat Address
OLED_ADDRESS            = 0x38   #OLED    Address
AHT20_ADDRESS           = 0x3c   #AHT20   Address 

I2C_REG_FIRMWARE_REV    = 0x00
I2C_REG_SRV1            = 0x00
I2C_REG_SRV2            = 0x02
I2C_REG_SRV3            = 0x03
I2C_REG_SRV4            = 0x04
I2C_REG_M1A             = 0x05
I2C_REG_M1B             = 0x06
I2C_REG_M2A             = 0x07
I2C_REG_M2B             = 0x08
I2C_REG_R0              = 0x09  #implemented
I2C_REG_G0              = 0x0A  #implemented
I2C_REG_B0              = 0x0B  #implemented
I2C_REG_R1              = 0x0C  #implemented
I2C_REG_G1              = 0x0D  #implemented
I2C_REG_B1              = 0x0E  #implemented
I2C_REG_AN0             = 0x0F
I2C_REG_AN1             = 0x10
I2C_REG_LIGHT           = 0x11
I2C_REG_VIN             = 0x12
I2C_REG_BUZZER          = 0x13
I2C_REG_RST             = 0x14

bus = smbus.SMBus(1)

def SetLED(led,red,blue,green):
    if led not in [0, 1]:
        raise ValueError("LED must be 0 or 1")
    if not (0 <= red <= 255):
        raise ValueError("Red value must be between 0 and 255")
    if not (0 <= blue <= 255):
        raise ValueError("Blue value must be between 0 and 255")
    if not (0 <= green <= 255):
        raise ValueError("Green value must be between 0 and 255")
    
    if led == 0:
        bus.write_byte_data(STEMHAT_ADDRESS,I2C_REG_R0,red)
        bus.write_byte_data(STEMHAT_ADDRESS,I2C_REG_B0,blue)
        bus.write_byte_data(STEMHAT_ADDRESS,I2C_REG_G0,green)
    else:
        bus.write_byte_data(STEMHAT_ADDRESS,I2C_REG_R1,red)
        bus.write_byte_data(STEMHAT_ADDRESS,I2C_REG_B1,blue)
        bus.write_byte_data(STEMHAT_ADDRESS,I2C_REG_G1,green)

