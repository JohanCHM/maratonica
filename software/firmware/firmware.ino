/*  Nombre de archivo: main.ino
*   Proyecto: Carbeto
*   Programa principal para el carrito de aldea
*/

//	************************* LIBRARIES ***********************************

#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <TimerOne.h>

#include "src/carbeto.h"

//	************************* VARIABLES ***********************************
enum Estados {
	ESPERA,
	SALVAR,
	DECIDIR,
	ADELANTE,
	IZQUIERDA,
	DERECHA,
	ERROR,
	LEVANTADO
};

Estados estadoCarbeto; //!< Estado actual en el que se encuentra el robot

Adafruit_NeoPixel luces = Adafruit_NeoPixel(LED_COUNT, RGB, NEO_GRB + NEO_KHZ400); //!< objeto para controlar los LEDs

unsigned long tiempo;	//!< variable de almacenamiento de milisegundos

int pwmIzq = 255;	//!< PWM de calibración para el motor izq
int pwmDer = 255;	//!< PWM de calibración para el motor der

char instruc[28];	//!< Cadena para almacenar los caracteres

int banderaTiempo1 = LOW;  //!< bandera para denotar el Timer1
int banderaPrimer = LOW;	//!< bandera para la primer corrida

void setup()
{
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
	
	//Luces
	luces.begin();  // Inicia los LEDs
	ledOff(); //Apaga los LEDs

	//Inicializar estados
	estadoCarbeto = ESPERA;

	//Timers
	Timer1.initialize(100000);
	Timer1.attachInterrupt(finTimer1);

	// ******* ACCIONES INICIALES ************
	
	cambioDeEstado(); //Inicializa las variables de cambio de estado
	
	//Cargar PWMs de la EEPROM
	//pwmDer = EEPROM.read(PWM_A);
	//pwmIzq = EEPROM.read(PWM_B);
	
}

//	************************* PROGRAM ***************************************

void loop() {
	switch (estadoCarbeto) {
	case ESPERA:
		ledGroovy();

		if (Serial.available() > 0) {	//Si hay información en el serial
			estadoCarbeto = SALVAR;
			cambioDeEstado();
		}

		break;

	case SALVAR:
		//Si es la primera vez que entra al estado después de un cambio
		if (banderaPrimer == LOW){
			ledOff();	// Apaga los LEDs
			banderaPrimer = HIGH;
		}
	
		if (Serial.find("S")) {
			// lee y convierte el primer valor hasta la coma:
			int pwmIzq = Serial.parseInt();
			// lee y convierte el segundo valor hasta la coma:
			int pwmDer = Serial.parseInt();

			//Debug---->
			Serial.print("Motor Izq:");
			Serial.print("\t");
			Serial.print(pwmIzq);
			Serial.println();
			Serial.print("Motor Der:");
			Serial.print("\t");
			Serial.print(pwmDer);
			Serial.println();
			

			estadoCarbeto = ADELANTE;
			cambioDeEstado();//<----Debug

		}
		else
		{
			Serial.write("cadena erronea\n");
			estadoCarbeto = ESPERA;
			cambioDeEstado();
		}

		

		break;

	case DECIDIR:

		break;

	case ADELANTE:
		if (banderaPrimer == LOW){
			ledBlanco();	//Color para asegurar que el siguiente se despliegue correctamente
			ledAdelante();
			banderaPrimer = HIGH;
		}
		break;

	case IZQUIERDA:
		if (banderaPrimer == LOW){
			ledBlanco();	//Color para asegurar que el siguiente se despliegue correctamente
			ledIzq();
			banderaPrimer = HIGH;
		}
		break;

	case DERECHA:
		if (banderaPrimer == LOW){
			ledBlanco();	//Color para asegurar que el siguiente se despliegue correctamente
			ledDer();
			banderaPrimer = HIGH;
		}
		break;

	case ERROR:
		if (banderaPrimer == LOW){
			ledBlanco();	//Color para asegurar que el siguiente se despliegue correctamente
			ledDer();
			banderaPrimer = HIGH;
		}
		break;

	case LEVANTADO:
		if (banderaPrimer == LOW){
			ledOff();
			banderaPrimer = HIGH;
		}
		break;

	default:
		//Nunca debe de llegar aquí
		//Lanzar un mensaje de error de HW y ver si SW
		break;

	} //End switch Maq estados

} //End Loop



// ********************FUNCTIONS**********************************************
// LEDS*************

/** Encendido de LEDs en blanco */
void ledBlanco()
{
	for (int i = 0; i < LED_COUNT; i++) {
		luces.setPixelColor(i, 0xFFFFFF);
	}
	luces.show();
	delay(5);
} //End of ledBlanco


/** Encendido de LEDs color adelante */
void ledAdelante()
{
	for (int i = 0; i < LED_COUNT; i++) {
		luces.setPixelColor(i, FRENTE);
	}
	luces.show();
	delay(5);
} //End of ledAdeladnte

/** Encendido de LEDs color adelante y centro repite*/
void ledRepAdelante()
{
	for (int i = 0; i < LED_COUNT; i++) {
		luces.setPixelColor(i, FRENTE);
	}
	luces.setPixelColor(3, REPITE);  //Pone el LED central en morado
	luces.show();
	delay(5);
} // End of ledRepAdelante

/** Encendido de LEDs color izquierda */
void ledIzq()
{
	for (int i = 0; i < LED_COUNT; i++) {
		luces.setPixelColor(i, IZQ);
	}
	luces.show();
	delay(5);
} //End of ledIzq

/** Encendido de LEDs color izquierda y centro repite*/
void ledRepIzq()
{
	for (int i = 0; i < LED_COUNT; i++) {
		luces.setPixelColor(i, IZQ);
	}
	luces.setPixelColor(3, REPITE);  //Pone el LED central en morado
	luces.show();
	delay(5);
} // End of ledRepIzq

/** Encendido de LEDs color derecha */
void ledDer()
{
	for (int i = 0; i < LED_COUNT; i++) {
		luces.setPixelColor(i, DER);		
	}
	luces.show();
	delay(10);
} //End of ledDer

/** Encendido de LEDs color derecha y centro repite*/
void ledRepDer()
{
	for (int i = 0; i < LED_COUNT; i++) {
		luces.setPixelColor(i, DER);
	}
	luces.setPixelColor(3, REPITE);  //Pone el LED central en morado
	luces.show();
	delay(5);
} //End of ledRepDer

/** Encendido de LEDs color error */
void ledError()
{
	for (int i = 0; i < LED_COUNT; i++) {
		luces.setPixelColor(i, CHIN);
	}
	luces.show();
	delay(5);
} //End of ledError

/** Muestra un arcoiris */
void ledGroovy()
{
	static int i; //exp
	rainbow(i);
	
	if (millis() - tiempo >= BARRIDO) {
		i++;
		if (i >= LED_COUNT * 10){
			i = 0;
		}
		tiempo = millis();
	}	

} //End of ledGroovy

/** Apagado de LEDs */
void ledOff()
{
	for (int i = 0; i<LED_COUNT; i++)
	{
		luces.setPixelColor(i, 0);
	}
	luces.show();
	delay(5);
	
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
	for (int i = 0; i<LED_COUNT; i++)
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
void finTimer1(void)
{
	banderaTiempo1 = HIGH;
} //End finTimer1


// ******* ESTADOS ************

/** Acciones al realizar un cambio de estado */
void cambioDeEstado()
{
	banderaPrimer = LOW;
	tiempo = millis();
}