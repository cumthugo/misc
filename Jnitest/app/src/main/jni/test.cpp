//
// Created by 张勇 on 16/8/27.
//
#include <jni.h>
#include <stdio.h>
#include <android/log.h>

#define LOGI(...) \
  ((void)__android_log_print(ANDROID_LOG_INFO, "test.cpp:", __VA_ARGS__))

#ifdef __cplusplus
extern "C" {
#endif

extern int second();

jstring Java_hugo_jnitest_MainActivity_jni_1get(JNIEnv *env, jobject thiz){
	int sec_ret;
    char ss[50];
    printf("invoke get in c++\n");
	sec_ret = second();
	LOGI("second return value = %d",sec_ret);
    sprintf(ss,"Hello from Jni in libjni-test.so, second = %d",sec_ret);
    return env->NewStringUTF(ss);
}

void Java_hugo_jnitest_MainActivity_jni_1set(JNIEnv *env, jobject thiz, jstring string){
    printf("invoke set in c++\n");
    char* str = (char*)env->GetStringUTFChars(string,NULL);
    printf("%s\n",str);
    env->ReleaseStringUTFChars(string,str);
}


#ifdef __cplusplus
}
#endif
