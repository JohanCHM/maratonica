/*  Nombre de archivo: main.ino
*   Proyecto: Carbeto
*   Programa principal para el carrito de aldea
*/

//	************************* LIBRARIES ***********************************
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <TimerOne.h>

#include "carbeto.h"

//	************************* VARIABLES ***********************************
enum Estados {
  ESPERA,
  GUARDAR,
  DECIDIR,
  ADELANTE,
  IZQUIERDA,
  DERECHA,
  ERROR,
  LEVANTADO
};

Estados estadoCarbeto; //!< Estado actual en el que se encuentra el robot

Adafruit_NeoPixel luces = Adafruit_NeoPixel(LED_COUNT, RGB, NEO_GRB + NEO_KHZ400); //!< objeto para controlar los LEDs

int banderaTiempo1 = LOW;  //!< bandera para denotar el Timer1

// ********************FUNCTIONS**********************************************
// LEDS*************

/** Encendido de LEDs color adelante */
void ledAdelante()
{
  for (int i = 0; i < LED_COUNT; i++) {
    luces.setPixelColor(i, FRENTE);
  }
  luces.show();

} //End of ledAdeladnte

/** Encendido de LEDs color adelante y centro repite*/
void ledRepAdelante()
{
  for (int i = 0; i < LED_COUNT; i++) {
    luces.setPixelColor(i, FRENTE);
  }
  luces.setPixelColor(3, REPITE);  //Pone el LED central en morado
  luces.show();
} // End of ledRepAdelante

/** Encendido de LEDs color izquierda */
void ledIzq()
{
  for (int i = 0; i < LED_COUNT; i++) {
    luces.setPixelColor(i, IZQ);
  }
  luces.show();
} //End of ledIzq

/** Encendido de LEDs color izquierda y centro repite*/
void ledRepIzq()
{
  for (int i = 0; i < LED_COUNT; i++) {
    luces.setPixelColor(i, IZQ);
  }
  luces.setPixelColor(3, REPITE);  //Pone el LED central en morado
  luces.show();
} // End of ledRepIzq

/** Encendido de LEDs color derecha */
void ledDer()
{
  for (int i = 0; i < LED_COUNT; i++) {
    luces.setPixelColor(i, DER);
  }
  luces.setPixelColor(3, REPITE);  //Pone el LED central en morado
  luces.show();
} //End of ledDer

/** Encendido de LEDs color derecha y centro repite*/
void ledRepDer()
{
  for (int i = 0; i < LED_COUNT; i++) {
    luces.setPixelColor(i, DER);
  }
  luces.show();
} //End of ledRepDer

/** Encendido de LEDs color error */
void ledError()
{
  for (int i = 0; i < LED_COUNT; i++) {
    luces.setPixelColor(i, CHIN);
  }
  luces.show();
} //End of ledError

/** Muestra un arcoiris */
void ledGroovy()
{
  static int i=0; //exp
  rainbow(i);
  delay(100);  // Delay between rainbow slides
  //if (banderaTiempo1) {
    i++;
    if (i>=LED_COUNT*10){
      i=0;

    }
    //reiniciarTimer1();
  //}


} //End of ledGroovy

/** Apagado de LEDs */
void ledOff()
{
  for (int i=0; i<LED_COUNT; i++)
  {
    luces.setPixelColor(i, 0);
  }
  luces.show();
} //End of ledOff

/** Muestra un arcoiris en todos los LEDs
* \param startPosition posiscion inicial del arcoiris
*/
void rainbow(byte startPosition)
{
  // Need to scale our rainbow. We want a variety of colors, even if there
  // are just 10 or so pixels.
  int rainbowScale = 192 / LED_COUNT;

  // Next we setup each pixel with the right color
  for (int i=0; i<LED_COUNT; i++)
  {
    // There are 192 total colors we can get out of the rainbowOrder function.
    // It'll return a color between red->orange->green->...->violet for 0-191.
    luces.setPixelColor(i, rainbowOrder((rainbowScale * (i + startPosition)) % 192));
  }
  // Finally, actually turn the LEDs on:
  luces.show();
}

/* Input a value 0 to 191 to get a color value.
* The colors are a transition red->yellow->green->aqua->blue->fuchsia->red...
*  Adapted from Wheel function in the Adafruit_NeoPixel library example sketch
* \return color value
*/
uint32_t rainbowOrder(byte position)
{
  // 6 total zones of color change:
  if (position < 31)  // Red -> Yellow (Red = FF, blue = 0, green goes 00-FF)
  {
    return luces.Color(0xFF, position * 8, 0);
  }
  else if (position < 63)  // Yellow -> Green (Green = FF, blue = 0, red goes FF->00)
  {
    position -= 31;
    return luces.Color(0xFF - position * 8, 0xFF, 0);
  }
  else if (position < 95)  // Green->Aqua (Green = FF, red = 0, blue goes 00->FF)
  {
    position -= 63;
    return luces.Color(0, 0xFF, position * 8);
  }
  else if (position < 127)  // Aqua->Blue (Blue = FF, red = 0, green goes FF->00)
  {
    position -= 95;
    return luces.Color(0, 0xFF - position * 8, 0xFF);
  }
  else if (position < 159)  // Blue->Fuchsia (Blue = FF, green = 0, red goes 00->FF)
  {
    position -= 127;
    return luces.Color(position * 8, 0, 0xFF);
  }
  else  //160 <position< 191   Fuchsia->Red (Red = FF, green = 0, blue goes FF->00)
  {
    position -= 159;
    return luces.Color(0xFF, 0x00, 0xFF - position * 8);
  }
}

// ******* TIMERS ************

/** Acción para la interrupción al final del timer1 */
void finTimer1()
{
  banderaTiempo1 = HIGH;
  Timer1.detachInterrupt();
  Timer1.stop();
  Serial.print("no ");
} //End finTimer1

void reiniciarTimer1()
{
  banderaTiempo1 = LOW;
  Timer1.attachInterrupt (finTimer1);
  Timer1.start();
} //End reiniciarTimer1


//	************************* SETUP ***************************************

void setup() {
  //Entradas
  pinMode(PISO, INPUT);
  pinMode(CHOQUE, OUTPUT);

  //Salidas
  pinMode(RGB, OUTPUT);
  pinMode(BUZZ, OUTPUT);

  pinMode(PWM_A, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);

  pinMode(PWM_B, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);

  //COMUNICACIÓN SERIAL
  Serial.begin(9600);
  Serial.print("hola ");

  //Luces
  luces.begin();  // Inicia los LEDs
  ledOff(); //Apaga los LEDs

  //Inicializar estados
  estadoCarbeto = ESPERA;

  //Timers
  Timer1.initialize (100000);
  Timer1.attachInterrupt (finTimer1);
}

//	************************* PROGRAM ***************************************

void loop() {
  switch (estadoCarbeto) {
    case ESPERA:
      ledGroovy();
      break;

    case GUARDAR:
      break;

    case DECIDIR:

      break;

    case ADELANTE:
      break;

    case IZQUIERDA:
      break;

    case DERECHA:
      break;

    case ERROR:
      break;

    case LEVANTADO:
      break;

    default:
      //Nunca debe de llegar aquí
      //Lanzar un mensaje de error de HW y ver si SW
      break;

  } //End switch Maq estados

} //End Loop
