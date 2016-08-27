MY_LOCAL_PATH := $(call my-dir)
LOCAL_PATH := $(MY_LOCAL_PATH)

#NDK_MODULE_PATH := $(LOCAL_PATH)
#
#$(call import-module,first)
#$(call import-module,second)

include $(call all-subdir-makefiles)


LOCAL_PATH := $(MY_LOCAL_PATH)
