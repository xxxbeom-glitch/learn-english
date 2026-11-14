package com.seongbeom.sidea;

import android.Manifest;
import android.app.PendingIntent;
import android.app.PictureInPictureParams;
import android.app.RemoteAction;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.graphics.drawable.Icon;
import android.media.AudioManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Rational;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.getcapacitor.BridgeActivity;
import java.util.ArrayList;

public class MainActivity extends BridgeActivity {
    // 이어폰을 빼거나 블루투스 이어폰 연결이 끊기면 안드로이드가 '곧 스피커로 소리가 난다'(BECOMING_NOISY)고 알린다.
    // 스포티파이처럼 이때 멈추도록 웹 코드에 sidea-noisy 이벤트를 보낸다(template.html이 받아 일시정지). 2026-11-11 성범 제보
    private final BroadcastReceiver noisy = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (AudioManager.ACTION_AUDIO_BECOMING_NOISY.equals(intent.getAction()) && getBridge() != null) {
                getBridge().getWebView().evaluateJavascript("window.dispatchEvent(new Event('sidea-noisy'))", null);
            }
        }
    };

    // PIP(작은 창): 재생 중에 홈으로 나가면 유튜브처럼 작은 창이 뜨고, 창에는 지금 배우는 가사 줄만 보인다(template.html의 #pip).
    // 창 안은 직접 누를 수 없어서 이전, 재생/멈춤, 다음 단추를 안드로이드에 맡긴다. 누르면 웹 코드에 sidea-pip-act 이벤트로 알린다. 2026-11-12 성범 요청
    private static final String PIP_ACT = "com.seongbeom.sidea.PIP_ACT";
    private boolean playing = false;
    private final BroadcastReceiver pipAct = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String act = intent.getStringExtra("act");
            if (act != null && act.matches("[a-z]+") && getBridge() != null) {
                getBridge().getWebView().evaluateJavascript("window.dispatchEvent(new CustomEvent('sidea-pip-act',{detail:'" + act + "'}))", null);
            }
        }
    };

    private RemoteAction pipButton(int icon, String label, String act, int code) {
        Intent i = new Intent(PIP_ACT).setPackage(getPackageName()).putExtra("act", act);
        PendingIntent pi = PendingIntent.getBroadcast(this, code, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        return new RemoteAction(Icon.createWithResource(this, icon), label, label, pi);
    }

    // 창 비율은 유튜브와 같은 16:9. 단추는 안드로이드가 그려서 크기와 자리를 못 바꾼다. 처음 2:1은 창이 낮아 단추가 가사를 다 가렸다(2026-11-12 성범 지적). 재생 중일 때만 홈으로 나갈 때 저절로 작은 창이 된다(안드로이드 12 이상).
    private PictureInPictureParams pipParams() {
        ArrayList<RemoteAction> acts = new ArrayList<>();
        acts.add(pipButton(R.drawable.ic_pip_prev, "Previous", "previoustrack", 1));
        acts.add(playing ? pipButton(R.drawable.ic_pip_pause, "Pause", "pause", 2) : pipButton(R.drawable.ic_pip_play, "Play", "play", 3));
        acts.add(pipButton(R.drawable.ic_pip_next, "Next", "nexttrack", 4));
        PictureInPictureParams.Builder b = new PictureInPictureParams.Builder().setAspectRatio(new Rational(16, 9)).setActions(acts);
        if (Build.VERSION.SDK_INT >= 31) b.setAutoEnterEnabled(playing);
        return b.build();
    }

    // 웹 코드가 재생/멈춤이 바뀔 때마다 알려 준다(window.SideAPip.setPlaying).
    private class PipBridge {
        @JavascriptInterface
        public void setPlaying(boolean on) {
            runOnUiThread(() -> {
                playing = on;
                if (Build.VERSION.SDK_INT >= 26) {
                    try { setPictureInPictureParams(pipParams()); } catch (RuntimeException ignored) { }
                }
            });
        }
    }

    // 안드로이드 8~11은 저절로 들어가는 기능이 없어서, 홈으로 나가는 순간 직접 작은 창으로 바꾼다.
    @Override
    public void onUserLeaveHint() {
        super.onUserLeaveHint();
        if (playing && Build.VERSION.SDK_INT >= 26 && Build.VERSION.SDK_INT < 31) {
            try { enterPictureInPictureMode(pipParams()); } catch (RuntimeException ignored) { }
        }
    }

    // 작은 창이 되거나 원래 화면으로 돌아오면 웹 코드에 알려 화면을 바꾼다.
    @Override
    public void onPictureInPictureModeChanged(boolean inPip, Configuration newConfig) {
        super.onPictureInPictureModeChanged(inPip, newConfig);
        if (getBridge() != null) {
            getBridge().getWebView().evaluateJavascript("window.dispatchEvent(new CustomEvent('sidea-pip',{detail:" + inPip + "}))", null);
        }
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ContextCompat.registerReceiver(this, pipAct, new IntentFilter(PIP_ACT), ContextCompat.RECEIVER_NOT_EXPORTED);
        getBridge().getWebView().addJavascriptInterface(new PipBridge(), "SideAPip");
        // 앱을 내려 둔 채 들을 때도 받아야 하므로 onPause가 아니라 onDestroy에서 푼다
        ContextCompat.registerReceiver(this, noisy, new IntentFilter(AudioManager.ACTION_AUDIO_BECOMING_NOISY), ContextCompat.RECEIVER_NOT_EXPORTED);
        // 화면 폭을 Figma 시안과 같은 360으로 잡는 viewport 설정(index.html)을 WebView가 따르게 한다.
        // 기본값은 이 설정을 무시해서, 폭이 411인 폰에서 화면이 시안보다 작게 보였다(2026-11-09 성범 지적).
        WebSettings s = getBridge().getWebView().getSettings();
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        // 맨 위에서 당길 때 WebView 전체(미니 바 포함)가 늘어나던 안드로이드 기본 효과를 끈다.
        // 당김 반응은 페이지 안에서 화면 내용에만 준다(template.html).
        getBridge().getWebView().setOverScrollMode(View.OVER_SCROLL_NEVER);
        // 재생 알림과 잠금 화면 재생 버튼이 보이려면 안드로이드 13 이상에서 알림 권한을 한 번 물어야 한다.
        if (Build.VERSION.SDK_INT >= 33
            && ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[] { Manifest.permission.POST_NOTIFICATIONS }, 1);
        }
    }

    // 화면이 꺼지거나 앱을 내려도 WebView 소리와 다음 화 넘김(자바스크립트)이 멈추지 않게,
    // 액티비티가 멈출 때 WebView 타이머를 멈추지 않는다. 앱을 살려 두는 건 미디어 재생 서비스가 한다.
    @Override
    public void onPause() {
        super.onPause();
        getBridge().getWebView().onResume();
        getBridge().getWebView().resumeTimers();
    }

    @Override
    public void onDestroy() {
        try { unregisterReceiver(noisy); } catch (IllegalArgumentException ignored) { }
        try { unregisterReceiver(pipAct); } catch (IllegalArgumentException ignored) { }
        super.onDestroy();
    }
}
