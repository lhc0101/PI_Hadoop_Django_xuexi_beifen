#include <reg52.h>
#include <intrins.h>
#define uint unsigned int
#define uchar unsigned char
//开发板+数码管 燃气报警
//MQ－5有4脚，VCC，GND，AOUT,DOUT
//VCC,GND分别接51hei单片机开发板的+5V与……DOUT接外部中断1（P3.3），
//中断则报警……AOUT接ADC0804的VIN+，也就是hei板J2的3脚，J2的1脚接外部中断0（P3.2），
//在ADC0804转换中用，转换与显示……注意电源供电，否则工作不正常……
uchar code tab[]={0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71};
sbit adc_cs=P2^0;
sbit adc_rd=P3^7;
sbit adc_wr=P3^6; 
sbit beep=P2^2;
sbit P26=P2^6;
sbit P27=P2^7;
sbit P24=P2^4;
bit beep_flag;
bit adc_flag;
bit adc_start;
void delay(uint temp)
{
 while(temp--);
}
void init(void)
{
 P24=0;
 P27=1;
 P0=0xff;
 P27=0;
 P26=1;
 P0=0x00;
 P26=0;
 TMOD=0x01;
 TH0=0x3c;
 TL0=0xb0;
 ET0=1;
 TR0=1;
 IT1=0;
 EX1=1;
 IT0=1;
 EX0=1;
 EA=1;
}        
void  int0_srv() interrupt 0
{
 adc_flag=1;
}
void int1_srv() interrupt 2
{  
 beep_flag=1;  
}
void timer0_srv() interrupt 1
{
 uchar temp;
 TH0=0x3c;
 TL0=0xb0;
 temp++;
 if(temp==40)
 {
  temp=0;
  adc_start=1;
 } 
}
uchar adc_change(void)
{
 uchar value;
 adc_cs=1;
 adc_wr=1;
 delay(2);
 adc_cs=0;
 delay(2);
 adc_wr=0;
 delay(10);
 adc_wr=1;
 delay(2);
 adc_cs=1;
 while(!adc_flag);
 adc_flag=0;
 adc_rd=1;
 _nop_();
 adc_cs=0;
 delay(2);
 adc_rd=0;
 _nop_();
 value=P1;
 _nop_();
 adc_rd=1;
 delay(2);
 adc_cs=1;
 return value;
}
void main()
{
 uchar adc_value;
 uchar ge,shi,bei;
 uint i;
 init();
 while(1)
 {
  if(beep_flag)
  {
   beep_flag=0;
   beep=0;
   delay(10000);
   beep=1;
   delay(10000);
  }
  if(adc_start)
  {
   adc_start=0;
   adc_value=adc_change();
   bei=adc_value/100;
   adc_value=adc_value%100;
   shi=adc_value/10;
   ge=adc_value%10;
  }
  for(i=0;i<100;i++)/////////
  {
   P27=1;
   P0=0xfe;      
   P27=0;
   
   P26=1;
   P0=tab[bei];
   delay(50);
   P0=0x00;      
   P26=0;
     
      P27=1;
   P0=0xfd;      
   P27=0;
   
   P26=1;
   P0=tab[shi];
   delay(50);
   P0=0x00;      
   P26=0;
   
   P27=1;
   P0=0xfb;      
   P27=0;
   
   P26=1;
   P0=tab[ge];
   delay(50);
   P0=0x00;      
   P26=0; 
  } 
 } 
}
