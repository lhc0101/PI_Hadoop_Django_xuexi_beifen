#include <reg52.h>
#include <intrins.h>
#define uint unsigned int
#define uchar unsigned char
#define lcd P0
///MQ－5天然气传感器
///hei51板上的ADC0804是为了量化漏泄浓度,1602显示
sbit adc_cs=P2^0;
sbit adc_rd=P3^7;
sbit adc_wr=P3^6; 
sbit en=P3^4;
sbit rw=P2^7;
sbit rs=P3^5;
sbit busybit=P0^7;
sbit beep=P2^2;
sbit P26=P2^6;
sbit P27=P2^7;
sbit P24=P2^4;
bit beep_flag;
bit adc_flag;
bit adc_start;
uchar tab[]="0123456789";
//////
void lcd_init(void);
//////////
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
 lcd_init();
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
 if(temp==20)
 {
  temp=0;
  adc_start=1;
 } 
}
void testbusy(void)//read com
{
 busybit=1;
 en=0;
 rs=0;
 rw=1;
 delay(5);
 en=1;
 delay(5);
 while (busybit);
 en=0;
}
void wr_dat(uchar dat,busyflag)
{
 if(busyflag)
 testbusy();
 en=0;
 rs=1;
 rw=0;
 lcd=dat;
 delay(5);
 en=1;
 delay(5);
 en=0;
}
void wr_com(uchar com,busyflag)
{
 if(busyflag)
 testbusy();
 en=0;
 rs=0;
 rw=0;
 lcd=com;
 delay(5);
 en=1;
 delay(5);
 en=0;
}
void lcd_init(void)
{
 delay(1650);//time
 wr_com(0x38,0);
 delay(550);//time
 wr_com(0x38,0);
 delay(550);
 wr_com(0x38,0);
 wr_com(0x38,1);
 wr_com(0x08,1);
 wr_com(0x01,1);
 wr_com(0x06,1);
 wr_com(0x0c,1);
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
  wr_com(0x80,1);
  wr_dat('M',1);
  delay(3);
  wr_dat('Q',1);
  delay(3);
  wr_dat('-',1);
  delay(3);
     wr_dat('5',1);
  delay(3);
  wr_dat(':',1);
  delay(3);
     wr_com(0xc0,1);
  wr_dat(tab[bei],1);
  delay(3);
  wr_dat(tab[shi],1);
  delay(3);
  wr_dat(tab[ge],1);
  delay(3);    
 } 
}