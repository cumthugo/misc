/*************************************************************************
	> File Name: second.cpp
# Author: Zhang Yong
# mail: cumt_zhangyong@163.com
	> Created Time: Îå  8/19 18:45:03 2016
 ************************************************************************/

#include <stdio.h>
#include <string.h>
#include <jni.h>
#include <inttypes.h>
#include <android/log.h>

#define LOGI(...) \
  ((void)__android_log_print(ANDROID_LOG_INFO, "second:", __VA_ARGS__))

extern int first_test();

int second()
{
	printf("printf work?");
	LOGI("my second shared lib");
	return first_test() + 2;
}
