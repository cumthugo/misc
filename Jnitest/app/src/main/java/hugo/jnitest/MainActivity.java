package hugo.jnitest;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    static {
        System.loadLibrary("second");
        System.loadLibrary("jni-test");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView textView = (TextView) findViewById(R.id.msg);
        textView.setText(jni_get());
        jni_set("hello world from jni test app");
    }

    public void callByJni(int v){
        Log.i("test.cpp","java: callByJni invoked!");
        TextView textView = (TextView) findViewById(R.id.resultView);
        textView.setText("this value is from jni, result = " + v);
    }


    public native String jni_get();
    public native void jni_set(String str);
}
