#include <gst/gst.h>
#include <glib.h>

static gboolean bus_call(GstBus* bus, GstMessage* msg, gpointer data)
{
	GMainLoop* loop = (GMainLoop*)data;
	switch (GST_MESSAGE_TYPE(msg))
	{
		case GST_MESSAGE_EOS:
		 g_print("End of stream\n");
		 g_main_loop_quit(loop);
		 break;
		case GST_MESSAGE_ERROR:
		{
			gchar* debug;
			GError* error;
			gst_message_parse_error(msg,&error,&debug);
			g_free(debug);
			g_printerr("ERROR:%s\n",error->message);
			g_error_free(error);
			g_main_loop_quit(loop);
			break;
		}
		default:
			break;
	}
	return TRUE;
}

int main(int argc, char* argv[])
{
	GMainLoop* loop;
	GstElement *pipeline,*source,*decoder,*sink;
	GstBus *bus;
	
	gst_init(&argc,&argv);
	loop = g_main_loop_new(NULL,FALSE);

	if(argc != 2)
	{	
		g_printerr("Usage:%s < map3 filename>\n",argv[0]);
		return -1;
	}

	pipeline = gst_pipeline_new("audio-player");
	source = gst_element_factory_make("filesrc","file-source");
	decoder = gst_element_factory_make("mad","mad-decoder");
	sink = gst_element_factory_make("autoaudiosink","audio-output");

	if(!pipeline || !source || !decoder || !sink){
		g_printerr("One element could not be created. Exiting.\n");
		return -1;
	}
	
	g_object_set(G_OBJECT(source),"location",argv[1],NULL);
	bus = gst_pipeline_get_bus(GST_PIPELINE(pipeline));
	gst_bus_add_watch(bus,bus_call,loop);
	gst_object_unref(bus);
	
	gst_bin_add_many(GST_BIN(pipeline),source,decoder,sink,NULL);

	gst_element_link_many(source,decoder,sink,NULL);
	
	gst_element_set_state(pipeline,GST_STATE_PLAYING);

	g_print("Running\n");

	g_main_loop_run(loop);

	g_print("Return, stopping playback\n");

	gst_element_set_state(pipeline,GST_STATE_NULL);

	return 0;
}
