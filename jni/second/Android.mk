LOCAL_PATH := $(call my-dir)

include $(CLEAR_VAR)
LOCAL_MODULE := second
LOCAL_MODULE_FILENAME := libsecond
LOCAL_SRC_FILES := second.cpp
LOCAL_LDLIBS := -llog
include $(BUILD_SHARED_LIBRARY)

