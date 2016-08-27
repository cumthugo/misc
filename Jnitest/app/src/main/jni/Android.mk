MY_LOCAL_PATH := $(call my-dir)
LOCAL_PATH := $(MY_LOCAL_PATH)

include $(LOCAL_PATH)/first/Android.mk


LOCAL_PATH := $(MY_LOCAL_PATH)
include $(LOCAL_PATH)/second/Android.mk

LOCAL_PATH := $(MY_LOCAL_PATH)
include $(CLEAR_VARS)
LOCAL_MODULE := foo-prebuilt
LOCAL_SRC_FILES := libprotobuf/$(TARGET_ARCH_ABI)/libprotobuf.so
include $(PREBUILT_SHARED_LIBRARY)

LOCAL_PATH := $(MY_LOCAL_PATH)
include $(CLEAR_VARS)

LOCAL_MODULE := jni-test
LOCAL_SRC_FILES := test.cpp person.pb.cc
LOCAL_CPP_EXTENSION := .cpp .cc
LOCAL_CFLAGS += -I/Users/zhangyong/Desktop/work/Carlife/source/protobuf-2.5.0/build/include
LOCAL_CFLAGS += -I/Users/zhangyong/Desktop/work/Carlife/source/protobuf-2.5.0/build/include/google/protobuf/io

LOCAL_CPP_FEATURES := rtti
LOCAL_SHARED_LIBRARIES := foo-prebuilt
LOCAL_SHARED_LIBRARIES += second
include $(BUILD_SHARED_LIBRARY)
