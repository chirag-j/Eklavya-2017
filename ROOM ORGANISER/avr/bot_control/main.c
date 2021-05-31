#include "sra.c"

void main()
{
	unsigned char data;
	SerialBegin(9600);
	bot_motion_init();
	pwm1_init();
	int pwm = 399;
	while(1)
	{
		
		data = SerialReadChar();
		if(data == 'f')
		{
			set_pwm1a(pwm);    
			set_pwm1b(pwm);
			bot_forward();
			delay_millisec(100);
		}
		else if(data == 'b')
		{
			set_pwm1a(pwm);
			set_pwm1b(pwm);
			bot_backward();
			delay_millisec(300);
		}
		else if(data == 'r')
		{
			set_pwm1a(pwm);
			set_pwm1b(pwm);
			bot_spot_right();
			delay_millisec(100);
		}
		else if(data == 'l')
		{
			set_pwm1a(pwm);
			set_pwm1b(pwm);
			bot_spot_left();
			delay_millisec(100);
		}
		else if(data == 's')
		{
			bot_stop();
		}
		else if(data == 'a')
		{
			set_pwm1a(pwm);
			set_pwm1b(pwm);
			bot_left();
			delay_millisec(100);
		
		}
		else if(data == 'd')
		{
			set_pwm1a(pwm);
			set_pwm1b(pwm);
			
			bot_right();
			delay_millisec(100);
		
		}
		else if((int)data == 200)
		{
			flick();
			SerialWriteInt((int)data);
			
		}
		
		else 
		{
			bot_stop();
		}
	}
}