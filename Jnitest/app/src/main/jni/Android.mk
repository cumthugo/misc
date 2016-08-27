MY_LOCAL_PATH := $(call my-dir)
LOCAL_PATH := $(MY_LOCAL_PATH)

include $(LOCAL_PATH)/first/Android.mk


LOCAL_PATH := $(MY_LOCAL_PATH)
include $(LOCAL_PATH)/second/Android.mk


LOCAL_PATH := $(MY_LOCAL_PATH)
include $(CLEAR_VARS)

LOCAL_MODULE := jni-test
LOCAL_SRC_FILES := test.cpp
LOCAL_LDLIBS := -llog
LOCAL_SHARED_LIBRARIES := second
include $(BUILD_SHARED_LIBRARY)
