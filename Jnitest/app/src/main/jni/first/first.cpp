/*************************************************************************
	> File Name: first.cpp
# Author: Zhang Yong
# mail: cumt_zhangyong@163.com
	> Created Time: Îå  8/19 18:45:03 2016
 ************************************************************************/

#include <stdio.h>
#include <string.h>
#include <jni.h>
#include <inttypes.h>
#include <android/log.h>

#ifdef __cplusplus
extern "C" {
#endif

#define LOGI(...) \
  ((void)__android_log_print(ANDROID_LOG_INFO, "first:", __VA_ARGS__))

int first_test()
{
	printf("printf work?");
	LOGI("my first shared lib");
	return 5;
}

#ifdef __cplusplus
}
#endif
