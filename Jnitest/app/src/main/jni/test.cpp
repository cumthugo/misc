//
// Created by 张勇 on 16/8/27.
//
#include <jni.h>
#include <stdio.h>
#include <android/log.h>
#include <pthread.h>
#include <unistd.h>

#define LOGI(...) \
  ((void)__android_log_print(ANDROID_LOG_INFO, "test.cpp:", __VA_ARGS__))

#ifdef __cplusplus
extern "C" {
#endif

extern int second();


void *mythreadproc(void* arg);

jstring Java_hugo_jnitest_MainActivity_jni_1get(JNIEnv *env, jobject thiz){
	int sec_ret;
    char ss[50];
    printf("invoke get in c++\n");
	sec_ret = second();
	LOGI("second return value = %d",sec_ret);
    sprintf(ss,"Hello from Jni in libjni-test.so, second = %d",sec_ret);


    pthread_t id;
    int ret = pthread_create(&id,NULL,mythreadproc,NULL);
    if(ret != 0)
    {
        LOGI("create thread failed!");
    }
    else
    {
        LOGI("Thread create success!");
    }

    jclass clazz = env->FindClass("hugo/jnitest/MainActivity");
    if (clazz != NULL)
    {
        LOGI("clazz is not null");
        jmethodID id = env->GetMethodID(clazz,"callByJni","(I)V");
        if(id != NULL)
        {
            LOGI("method id not null, call");
            jint s = 66;
            env->CallVoidMethod(thiz,id,s);

        }
        else
        {
            LOGI("method is null, cancelled");
        }

    }
    else
    {
        LOGI("clazz is null");
    }

    return env->NewStringUTF(ss);
}

void Java_hugo_jnitest_MainActivity_jni_1set(JNIEnv *env, jobject thiz, jstring string){
    printf("invoke set in c++\n");
    char* str = (char*)env->GetStringUTFChars(string,NULL);
    printf("%s\n",str);
    env->ReleaseStringUTFChars(string,str);
}



void *mythreadproc(void* arg)
{
    int a;
    while(++a < 20)
    {
        LOGI("my thread run! oh yeah");
        sleep(1);
    }
}

#ifdef __cplusplus
}
#endif
