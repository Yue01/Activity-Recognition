package dev.edmt.takepicturecamera;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.StrictMode;
import android.provider.MediaStore;
import android.speech.tts.TextToSpeech;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.Date;
import java.util.Locale;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

public class MainActivity extends AppCompatActivity {
    private TextToSpeech mTTS;
    ImageView imageView;
    Toast toast;
    JSONObject json;
    String machine = "0"; // representing the machine id
    String text = "";
    String time = "";
    String request = "in";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
        imageView = (ImageView)findViewById(R.id.imageView);
        final Button mButtonpicture = (Button)findViewById(R.id.btnCamera);
        final Button mButtonspeak = (Button)findViewById(R.id.speakbutton);
        final Button mButtonsend = (Button)findViewById(R.id.sendbutton);


        mTTS = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    int result = mTTS.setLanguage(Locale.US);

                    if (result == TextToSpeech.LANG_MISSING_DATA
                            || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Log.e("TTS", "Language not supported");
                    } else {
                        mButtonspeak.setEnabled(true);
                    }
                } else {
                    Log.e("TTS", "Initialization failed");
                }
            }
        });

        //speak function
        mButtonspeak.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                request="word_out";
                String url = "http://54.183.26.41/message_server/servlet/Fetch?machine="+machine+"&time="+time+"&request="+request;
                JsonObjectRequest sr = new JsonObjectRequest(Request.Method.GET, url,json,

                        new Response.Listener<JSONObject>() {
                            @Override
                            public void onResponse(JSONObject response) {
                                String text = null;
                                try {
                                    text = response.getString("info");
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                    text = "Please wait! Thank you!";
                                }
                                speak(text);
                            }
                        },
                        new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                Log.i("Response", "ERROR");
                                Toast.makeText(getApplication(), "Unable to connect to server", Toast.LENGTH_SHORT).show();
                            }
                        }
                );
                Volley.newRequestQueue(getApplicationContext()).add(sr);
            }
        });

        //send function
        mButtonsend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String result = (machine+","+time+","+text).toString();
                Toast.makeText(getApplication(), result, Toast.LENGTH_SHORT).show();
                try{
                    Socket s = new Socket("169.234.40.126",7778);
                    OutputStreamWriter writer = new OutputStreamWriter(s.getOutputStream());
                    writer.write(result);
                    writer.flush();
                    writer.close();
                    s.close();
                }catch(IOException e) {
                    e.printStackTrace();
                }
            }
        });

        // picture capturing
        mButtonpicture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent photo = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(photo,0);
            }
        });

    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {

        super.onActivityResult(requestCode, resultCode, data);
        try {
            Bitmap bitmap = (Bitmap)data.getExtras().get("data");
//            Bitmap bitmap = Bitmap.createScaledBitmap(orimap,800,800,true);
            imageView.setImageBitmap(bitmap);
            Date date = new Date();
            time = date.toString();
            time = time.replaceAll(" ","");
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.PNG,100,baos);
            byte[] b = baos.toByteArray();
            text = Base64.encodeToString(b,Base64.DEFAULT);

        }catch (Exception e) {
            Toast.makeText(getApplication(), "No Picture!", Toast.LENGTH_SHORT).show();
            e.printStackTrace();
        }
    }

    private void speak(String text) {
        mTTS.speak(text, TextToSpeech.QUEUE_FLUSH, null);
    }

}
