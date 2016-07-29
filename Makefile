all: test tutorial-1

test: 
	gcc test_mp3.c `pkg-config --cflags --libs gstreamer-1.0` -o test_mp3 
tutorial-1:
	gcc tutorial-1.c `pkg-config --cflags --libs gstreamer-1.0` -o tutorial-1 
tutorial-3:
	gcc tutorial-3.c `pkg-config --cflags --libs gstreamer-1.0` -o tutorial-3 
	
clean:
	rm -f test_mp3 tutorial-1
