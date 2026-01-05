# Amphibious-Delivery-Robot
ADR repo page
This project is provided for educational and experimental purposes.  
Feel free to adapt or build upon the design.

I have attached all the STL files needed to print this project yourself. Any common 3D printer settings work, however I would recommend to
use an increased wall strenght since the flotation devices are hallow this allows for less play. I used PLA to do all of this but would recommend at least 
PETG fillament since PLA does not do too well in water. Something I unfortunately learned...

As for the coding and BOM. Transmitter_0.py goes into an Adafruit RP2040 feather and the receiver_1.py goes into the onboard Raspberry Pico W.
Although I have attached this BOM, if interested in adapting and building upon this design, I would highly recommend moving to a sprocket and chain system
as the water and land conversion can physically wear the bot's timing belt system causing loss of tension on the belts.

Best of luck! Thanks for stopping by my Github. If any questions rise please feel free to reach out to me on LinkedIn @ www.linkedin.com/in/josuesgarcia  :)

~ Josue S. Garcia

BOM:

Receiver/ADR bot:
- 1 x Raspberry Pico W
- 2 x L298N Motor drivers
- 1 x 12V 2800 mAh rechargeable Li-ion battery 
- 1 x Junction box ABS IP65 electrical enclosure box
- 1 x Freenove breakout board for Raspberry Pico W
- 1 x LM2596S buck converter
- 2 x 5mm bore idler pulleys for 6 mm width timing belt (toothless)
- 2 x 5mm bore idler pulleys for 6 mm width timing belt (toothed)
- 2 x Aluminum timing belt pulley 20&60 teeth 5 mm bore
- 1 x 433 Mhz gmrs Antenna 
- 1 x Adafruit rfm69hcw
- 1 x premium robot tracked car chassis kit (used tracks, motors, and chassis as the refence for ADR chassis design)

Transmitter/controller:
- 1 x Adafruit RP2040 Feather
- 1 x Analog Joystick
- 1 x Lipo battery
- 1 x 433 Mhz gmrs Antenna 
- 1 x Adafruit rfm69hcw
