LOCAL_PATH := $(call my-dir)

include $(CLEAR_VAR)
LOCAL_MODULE := first
LOCAL_MODULE_FILENAME := libfirst
LOCAL_SRC_FILES := first.cpp
LOCAL_EXPORT_LDLIBS := -llog
include $(BUILD_STATIC_LIBRARY)

