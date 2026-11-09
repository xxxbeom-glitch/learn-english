package com.seongbeom.sidea;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
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
}
