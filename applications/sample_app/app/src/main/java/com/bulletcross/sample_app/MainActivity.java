package com.bulletcross.sample_app;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import org.tensorflow.lite.Interpreter;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final Interpreter interpreter;
    }
}
