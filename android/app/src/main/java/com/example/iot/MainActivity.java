package com.example.iot;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.ParcelUuid;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.example.iot.databinding.ActivityMainBinding;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {

    ActivityMainBinding binding;

    // Communication
    private OutputStream outputStream;
    private InputStream inputStream;

    // Sensor
    SensorManager sensorManager;
    Sensor accSensor;
    Sensor gravitySensor;
    SensorEventListener sensorEventListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        View view = binding.getRoot();
        setContentView(view);

        sensorManager = (SensorManager)getSystemService(Context.SENSOR_SERVICE);

        accSensor = sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
        gravitySensor = sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY);

        try {
            init();
        } catch (IOException e) {
            e.printStackTrace();
        }

        sensorEventListener = new SensorEventListener() {
            @Override
            public void onSensorChanged(SensorEvent event) {
                String str = "";
                // Accelerator sensor
                if (event.sensor.getType() == Sensor.TYPE_LINEAR_ACCELERATION) {
                    for (int i = 0; i < 2; i++) {
                        str += ("a" + event.values[i] + " ");
                    }
                }
                // Gravity sensor
                if (event.sensor.getType() == Sensor.TYPE_GRAVITY) {
                    str += ("g" + event.values[2]);
                }
                if (System.currentTimeMillis() % 2 == 0) {
                    try {
                        write(str);
                        read();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onAccuracyChanged(Sensor sensor, int accuracy) {

            }
        };
    }

    public void onLeftClick(View v) {
//        Toast.makeText(this, "Left clicked!", Toast.LENGTH_LONG).show();
        sensorManager.registerListener(sensorEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION), SensorManager.SENSOR_DELAY_FASTEST);
        sensorManager.registerListener(sensorEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY), SensorManager.SENSOR_DELAY_FASTEST);

    }

    public void onRightClick(View v) {
//        Toast.makeText(this, "Right clicked!", Toast.LENGTH_LONG).show();
        sensorManager.unregisterListener(sensorEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION));
        sensorManager.unregisterListener(sensorEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY));
        try{
            write("0");
            read();
        }
        catch (IOException e){
            e.printStackTrace();
        }
    }

    public void onScrollClick(View v) {
        Toast.makeText(this, "Scroll clicked!", Toast.LENGTH_LONG).show();
    }

    public void onMacro1Click(View v) {
        Toast.makeText(this, "Macro1 clicked!", Toast.LENGTH_LONG).show();
    }

    public void onMacro2Click(View v) {
        Toast.makeText(this, "Macro2 clicked!", Toast.LENGTH_LONG).show();
    }

    private void init() throws IOException {
        BluetoothAdapter blueAdapter = BluetoothAdapter.getDefaultAdapter();
        if (blueAdapter != null) {
            if (blueAdapter.isEnabled()) {
                Set<BluetoothDevice> bondedDevices = blueAdapter.getBondedDevices();
                if (bondedDevices.size() > 0) {
                    BluetoothDevice device = (BluetoothDevice) bondedDevices.toArray()[2];
                    Log.e("qwe", device.getName());
                    device.fetchUuidsWithSdp();
                    ParcelUuid[] uuids = device.getUuids();
                    Log.e("qwe", uuids[0].getUuid().toString());
                    BluetoothSocket socket = device.createRfcommSocketToServiceRecord(UUID.fromString("00001117-0000-1000-8000-00805F9B34FB"));
                    Log.e("qwe", "before socket connect!!");
                    socket.connect();
                    Log.e("qwe", "after socket connect!!");
                    outputStream = socket.getOutputStream();
                    inputStream = socket.getInputStream();
                }
                Log.e("error", "No appropriate paired devices.");
            } else {
                Log.e("error", "Bluetooth is disabled.");
            }
        }
    }

    public void write(String s) throws IOException {

        // outputStream.write(s.getBytes());
        // Wrap the OutputStream with DataOutputStream


        // Encode the string with UTF-8
        byte[] message = s.getBytes("UTF-8");
        outputStream.write(message);
    }

    public void read() throws IOException{
        byte[] b = new byte[36];
        int len = inputStream.read(b, 0, 36);
        String ack = new String(b);
        ack = ack.substring(0, len);
    }
}