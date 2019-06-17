#include <stdio.h>
#include <stdlib.h> 

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define TEMP_PATH "/sys/class/thermal/thermal_zone0/temp"
#define MAX_SIZE 32
//读取CPU温度
int main(void) 
{
    int fd;
    double temp = 0;
    char buf[MAX_SIZE];
    
    // 打开/sys/class/thermal/thermal_zone0/temp
    fd = open(TEMP_PATH, O_RDONLY);
    if (fd < 0) {
        fprintf(stderr, "failed to open thermal_zone0/temp\n");
        return -1;
    }
    
    // 读取内容
    if (read(fd, buf, MAX_SIZE) < 0) {
        fprintf(stderr, "failed to read temp\n");
        return -1;
    }
    
    // 转换为浮点数打印
    temp = atoi(buf) / 1000.0;
    printf("Your Pi's current temperature : %.2f ℃: %.2f\n", temp);
    
    // 关闭文件
    close(fd);
}
//编译链接：
//$gcc -o cpu_temp cpu_temp.c
//执行：
//$./cpu_temp