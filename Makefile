test: test_mp3.c
	gcc test_mp3.c `pkg-config --cflags --libs gstreamer-1.0` -o test_mp3 
clean:
	rm test_mp3
