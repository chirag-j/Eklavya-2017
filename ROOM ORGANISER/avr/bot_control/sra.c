
/*---------------------------------------------------------
Revised sra.c : PWM frequency changed to 3KHz
				ADC is 10bit
				USART functions changed. Working with cp2102
 ---------------------------------------------------------
/*

/* I N C L U D E S */
#include<avr/io.h>
#include<stdlib.h>
#include<compat/deprecated.h>
#include<util/delay.h>
#include<avr/eeprom.h>
#include<io.h>
#include <inttypes.h>
/* E N D S */

unsigned char min[sensor_num],max[sensor_num],threshold[sensor_num];
unsigned char sensorbyte=0;

//PORT INITIALIZE
void port_init(void)
{
	DDRA = 0xFF;
	PORTA = 0X00;
	DDRB = 0xFF;
	DDRC = 0x00;
	PORTC = 0xFF;
	DDRD = 0xFF;
	PORTD = 0x00;
}

//PWM1 INITIALIZE
void pwm1_init(void)
{
 PWM1A_DIR=1;
 PWM1B_DIR=1;
 TCCR1B = 0x00; //stop
 TCNT1H = 0x00; //setup
 TCNT1L = 0x00;
 OCR1AH = 0x00;
 OCR1AL = 0x00;
 OCR1BH = 0x00;
 OCR1BL = 0x00;
 ICR1H  = 0x02; //for 3khz frequency
 ICR1L  = 0x9A;
 TCCR1A = 0xA2; //prescalar set to 8
 TCCR1B = 0x1A; //start Timer
}

void pwm2_init()
{
TCCR2 = 0x69;
}

void pwm0_init()
{
TCCR0 = 0x69;
}

//ADC INITIALIZE
void adc_init(void)
{
 ADC_DIR=0X00;
 ADCSRA=0X00;
 ADMUX=0X40;//0x40 for 10 bits
 ADCSRA=0X87;
 ACSR=0X80;
}

//ADC START
unsigned int adc_start(unsigned char channel)
{

	ADMUX &= 0B11111000;
	ADMUX |= channel;
	ADCSRA &= 0b11111000;
	ADCSRA |= 0b01001100;
	while(!(ADCSRA & (1<<ADIF)));       // wait for conv. to complete
	
	return (ADCL + (ADCH & 0b00000011) * 256);
}

//DELAY FUNCTIONS
void delay_sec(int x)
{
 unsigned char i,j;
 for(i=0;i<x;i++)
  for(j=0;j<4;j++)
   _delay_ms(250);
}

void delay_millisec(int n)
{
	_delay_ms(n);
}

void delay_microsec(int n)
{
	_delay_us(n);
}

//CHECK THE SENSOR VALUES
void check_sensors(void)
{
sensorbyte=0;

unsigned char i,temp[sensor_num];

	 for(i=0;i<sensor_num;i++)
	 {
	 
	  temp[i]=adc_start(i);
	  if(temp[i]>threshold[i])
	  sensorbyte|=(1<<i);
	 
	 } 
}
 
 //CALIBRATE FOR BLACK SURFACE
 void calibrate_black(void)
{
	unsigned char j,i,temp[sensor_num];

	for(j=0;j<sensor_num;j++) 
	 {
		  max[j]=adc_start(j);
		  
		  for(i=0;i<10;i++)
		 {
			  temp[i]=adc_start(j);
			  
			  if(temp[i]>max[j])
			  {
			  max[j]=temp[i];
			  }
			  
		 }
	 
	}

		
}

//CALIBRATE FOR WHITE SURFACE
void calibrate_white(void)
{

	unsigned char j,i,temp[sensor_num];
	 
	 for(j=0;j<sensor_num;j++) 
	 {
		  min[j]=adc_start(j);
		  
		  for(i=0;i<10;i++)
		 {
			  temp[i]=adc_start(j);
			  
			 if(temp[i]<min[j])
			  {
			  min[j]=temp[i];
			  }
		  
		 }
	 
	}

		
}

//SET THRESHOLD VALUE
void set_threshold(void)
{

	unsigned char i,eeprom_addr=0x0000;
	char diff;
	
	
	 for(i=0;i<sensor_num;i++)
	 {
	 
		 diff=abs(max[i]-min[i]);	
		 threshold[i]=max[i]+(diff>>1);
		  
	 }
	 
	 for(int i=0;i<sensor_num;i++)
	{
		eeprom_write_byte(eeprom_addr,threshold[i]);
		eeprom_addr++;
	}
	 
}

//LED FLICKER FUNCTION
void flick (void)
{
unsigned int i=0;

	for(i=0;i<5;i++)
	{
		LED=0xff;
		delay_millisec(100);
		LED=0x00;
		delay_millisec(100);
	}

}

//SET PWM1A
void set_pwm1a(int a)
{
OCR1A=a;
}

//SET PWM1B
void set_pwm1b(int b)
{
OCR1B=b;
}
void set_pwm0(int c)
{
OCR0=c;
}

//SET PWM1B
void set_pwm2(int d)
{
OCR2=d;
}

//LCD FUNCTIONS

//LCD DEFINITIONS

#define LCD_DATA_PORT 	PORT(LCD_DATA)
#define LCD_E_PORT 		PORT(LCD_E)
#define LCD_RS_PORT 		PORT(LCD_RS)
#define LCD_RW_PORT 		PORT(LCD_RW)

#define LCD_DATA_DDR 	DDR(LCD_DATA)
#define LCD_E_DDR 		DDR(LCD_E)
#define LCD_RS_DDR 		DDR(LCD_RS)
#define LCD_RW_DDR 		DDR(LCD_RW)

#define LCD_DATA_PIN		PIN(LCD_DATA)

#define SET_E() (LCD_E_PORT|=(1<<LCD_E_POS))
#define SET_RS() (LCD_RS_PORT|=(1<<LCD_RS_POS))
#define SET_RW() (LCD_RW_PORT|=(1<<LCD_RW_POS))

#define CLEAR_E() (LCD_E_PORT&=(~(1<<LCD_E_POS)))
#define CLEAR_RS() (LCD_RS_PORT&=(~(1<<LCD_RS_POS)))
#define CLEAR_RW() (LCD_RW_PORT&=(~(1<<LCD_RW_POS)))

#define blink 	    0B00000001
#define underline 0B00000010

#define lcd_cmd(c) (lcd_byte(c,0))
#define lcd_data(d) (lcd_byte(d,1))

#define lcd_clear()	lcd_cmd (0b00000001)
#define lcd_home()	lcd_cmd (0b00000010);

#define _CONCAT(a,b) a##b
 #define PORT(x) _CONCAT(PORT,x)
 #define PIN(x) _CONCAT(PIN,x)
 #define DDR(x) _CONCAT(DDR,x)


//LCD FUNCTIONS
void lcd_byte(uint8_t c,uint8_t isdata)
{
uint8_t hn,ln;			//Nibbles
uint8_t temp;
hn=c>>4;
ln=(c & 0x0F);
if(isdata==0)
	CLEAR_RS();
else
	SET_RS();
_delay_us(0.500);		//tAS
SET_E();
temp=(LCD_DATA_PORT & 0XF0)|(hn);
LCD_DATA_PORT=temp;
_delay_us(1);			//the
CLEAR_E();
_delay_us(1);
SET_E();
temp=(LCD_DATA_PORT & 0XF0)|(ln);
LCD_DATA_PORT=temp;
_delay_us(1);			//tEH
CLEAR_E();
_delay_us(1);			//tEL
lcd_busy_loop();
}

void lcd_busy_loop(void)
{
	uint8_t busy,status=0x00,temp;
	LCD_DATA_DDR&=0xF0;
	SET_RW();		//Read mode
	CLEAR_RS();		//Read status
	_delay_us(0.5);		//tAS
	do
	{

		SET_E();
		_delay_us(0.5);
		status=LCD_DATA_PIN;
		status=status<<4;
		_delay_us(0.5);
		CLEAR_E();
		_delay_us(1);	//tEL
		SET_E();
		_delay_us(0.5);
		temp=LCD_DATA_PIN;
		temp&=0x0F;
		status=status|temp;
		busy=status & 0b10000000;
		_delay_us(0.5);
		CLEAR_E();
		_delay_us(1);	//tEL
	}while(busy);
CLEAR_RW();		//write mode
	//Change Port to output
	LCD_DATA_DDR|=0x0F;

}

void lcd_init(uint8_t style)
{
	
_delay_ms(30);
	
	//Set IO Ports
	LCD_DATA_DDR|=(0x0F);
	LCD_E_DDR|=(1<<LCD_E_POS);
	LCD_RS_DDR|=(1<<LCD_RS_POS);
	LCD_RW_DDR|=(1<<LCD_RW_POS);

	LCD_DATA_PORT&=0XF0;
	CLEAR_E();
	CLEAR_RW();
	CLEAR_RS();
	_delay_us(0.3);	//tAS
	SET_E();
	LCD_DATA_PORT|=(0b00000010);
	_delay_us(1);
	CLEAR_E();
	_delay_us(1);
	lcd_busy_loop();                                    //[B] Forgot this delay
	lcd_cmd (0b00001100|style);	//Display On
	lcd_cmd (0b00101000);			//function set 4-bit,2 line 5x7 dot format
}
void lcd_write_string(const char *msg)
{
while(*msg!='\0')
 {
	lcd_data (*msg);
	msg++;
 }
}

void lcd_write_int(int val,unsigned int field_length)
{
	char str[5]={0,0,0,0,0};
	int i=4,j=0;
	while(val)
	{
	str[i]=val%10;
	val=val/10;
	i--;
	}
	if(field_length==-1)
		while(str[j]==0) j++;
	else
		j=5-field_length;

	if(val<0) lcd_data ('-');
	for(i=j;i<5;i++)
	{
	lcd_data (48+str[i]);
	}
}
void lcd_goto_xy(uint8_t x,uint8_t y)
{
 if(x<40)
 {
  if(y) x|=0b01000000;
  x|=0b10000000;
  lcd_cmd (x);
  }
}
void lcd_write_string_xy(int x,int y,char *msg)
 {
 lcd_goto_xy(x,y);
 lcd_write_string(msg);
}

void lcd_write_int_xy(int x,int y,int val,int fl) {
 lcd_goto_xy(x,y);
 lcd_write_int(val,fl);
}

//This function is used to initialize the USART
//at a given UBRR value
void SerialBegin(long baud_rate)
{

   //Set Baud rate
   uint16_t ubrr_value = (1000000/baud_rate) - 1;
   UBRRL = ubrr_value;
   UBRRH = (ubrr_value>>8);

   ///Set Frame Format
   //Asynchronous mode
   //No Parity
   //1 StopBit
   //char size 8


   UCSRC=(1<<URSEL)|(3<<UCSZ0);


   //Enable The receiver and transmitter

   UCSRB=(1<<RXEN)|(1<<TXEN);


}

//-----------------------------------------------------
//USART functions

/* Functions for Serial communication(UART) .for using CP2102 too.
Call SerialBegin(long baudrate) to initialise the UART.
Call SerialWriteChar(char x) to print single character.
Call SerialWriteString(char x[]) to print string. Pass string in double inverted commas.
Call SerialWriteInt(int x) to print integer(signed only)
Call SerialWriteLong(unsigned long int x) to print unsigned long integers.

*/

//This function is used to read the available data
//from USART. This function will wait untill data is
//available.
char SerialReadChar()
{
   //Wait untill a data is available

   while(!(UCSRA & (1<<RXC)))
   {
		;
      //Do nothing
   }
   //Data recieved in USART
   return UDR;
}


//This fuction prints a single character.
void SerialWriteChar(char data)
{
   //Wait untill the transmitter is ready

   while(!(UCSRA & (1<<UDRE)))
   {
      //Do nothing
   }

   //Now write the data to USART buffer

   UDR=data;
}


//This function prints a string. Pass in double inverted commas or a character array.
void SerialWriteString(char string[])
{
	for (int i=0; i<strlen(string); i++) 
	{
			SerialWriteChar(string[i]);
	}
		
		
}

//This function prints a signed integer.
void SerialWriteInt(int data)
{
	int i = 0, count = 0;
	
	if(data<0)
	{
		SerialWriteChar('-');
		data*=-1;
	}
	
	int x = data;
	
	//count number of digits
	while(x)
	{
		count++;
		x = x/10;
	}
	
   int temp[count];
   
   //store each digit in temp array
   while(data)
   {
	temp[i] = data%10;
	data = data/10;
	i++;
   }
   
   
   //print each digit by typecasting to character
   for(i = count-1; i>=0 ; i--)
   {
		SerialWriteChar(temp[i]+'0');
   }

  
}

//This function prints an unsigned long int.
void SerialWriteLong(unsigned long int data)
{
	int i = 0, count = 0;	
	unsigned long x = data;
	
	//count number of digits
	while(x)
	{
		count++;
		x = x/10;
	}
	
   int temp[count];
   
   //store each digit in temp array
   while(data)
   {
	temp[i] = data%10;
	data = data/10;
	i++;
   }
   
   
   //print each digit by typecasting to character
   for(i = count-1; i>=0 ; i--)
   {
		SerialWriteChar(temp[i]+'0');
   }
}
//----------------------------------------------------


//BOT MOTIONS
void bot_motion_init(void)
{
DDRC=0xff;
}
void bot_left_forward(void)
{
	MOTOR1A=0;
	MOTOR1B=0;
	
	MOTOR2A=1;
	MOTOR2B=0;
	
	MOTOR3A=0;
	MOTOR3B=0;
	
	MOTOR4A=1;
	MOTOR4B=0;
}
void bot_left_backward(void)
{
	MOTOR1A=0;
	MOTOR1B=0;
	
	MOTOR2A=0;
	MOTOR2B=1;
	
	MOTOR3A=0;
	MOTOR3B=0;
	
	MOTOR4A=0;
	MOTOR4B=1;
}
void bot_right_forward(void)
{
	MOTOR1A=1;
	MOTOR1B=0;
	
	MOTOR2A=0;
	MOTOR2B=0;
	
	MOTOR3A=1;
	MOTOR3B=0;
	
	MOTOR4A=0;
	MOTOR4B=0;
}

void bot_left(void)
{
 bot_right_forward();
}

void bot_right(void)
{
 bot_left_forward();
}

void bot_right_backward(void)
{
	MOTOR1A=0;
	MOTOR1B=1;
	
	MOTOR2A=0;
	MOTOR2B=0;

	MOTOR3A=0;
	MOTOR3B=1;
	
	MOTOR4A=0;
	MOTOR4B=0;
}
void bot_forward(void)
{
	MOTOR1A=1;
	MOTOR1B=0;
	
	MOTOR2A=1;
	MOTOR2B=0;
	
	MOTOR3A=1;
	MOTOR3B=0;
	
	MOTOR4A=1;
	MOTOR4B=0;

}
void bot_backward(void)
{
	MOTOR1A=0;
	MOTOR1B=1;
	
	MOTOR2A=0;
	MOTOR2B=1;
	
	MOTOR3A=0;
	MOTOR3B=1;
	
	MOTOR4A=0;
	MOTOR4B=1;
}
void bot_spot_left(void)
{
	MOTOR1A=1;
	MOTOR1B=0;
	
	MOTOR2A=0;
	MOTOR2B=1;
	
	MOTOR3A=1;
	MOTOR3B=0;
	
	MOTOR4A=0;
	MOTOR4B=1;
}

void bot_spot_right(void)
{
	MOTOR1A=0;
	MOTOR1B=1;
	
	MOTOR2A=1;
	MOTOR2B=0;
	
	MOTOR3A=0;
	MOTOR3B=1;
	
	MOTOR4A=1;
	MOTOR4B=0;
}
void bot_stop(void)
{
	MOTOR1A=0;
	MOTOR1B=0;
	
	MOTOR2A=0;
	MOTOR2B=0;
	
	MOTOR3A=0;
	MOTOR3B=0;
	
	MOTOR4A=0;
	MOTOR4B=0;
}
void bot_brake(void)
{
	MOTOR1A=1;
	MOTOR1B=1;
	
	MOTOR2A=1;
	MOTOR2B=1;
	
	MOTOR3A=1;
	MOTOR3B=1;
	
	MOTOR4A=1;
	MOTOR4B=1;
}

void switch_init(void)
{
PORTD|=0x0F;
DDRD&=0xF0;
}

int pressed_switch0(void)
{
if(bit_is_clear(PIND,0))
return 1;
else
return 0;
}

int pressed_switch1(void)
{
if(bit_is_clear(PIND,1))
return 1;
else
return 0;
}

int pressed_switch2(void)
{
if(bit_is_clear(PIND,2))
return 1;
else
return 0;
}

int pressed_switch3(void)
{
if(bit_is_clear(PIND,3))
return 1;
else
return 0;
}

/*EEPROM FUNCTIONS*/
//Variabes

void retrieve_threshold(void)
{
	unsigned char eeprom_addr=0x0000;
	for(int i=0;i<sensor_num;i++)
	{
		threshold[i]=eeprom_read_byte(eeprom_addr);
		eeprom_addr++;
	}
}

