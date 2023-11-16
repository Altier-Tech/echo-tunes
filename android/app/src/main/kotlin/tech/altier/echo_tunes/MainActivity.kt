package tech.altier.echo_tunes

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugins.GeneratedPluginRegistrant
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        GeneratedPluginRegistrant.registerWith(flutterEngine)

        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "your_channel_name")
            .setMethodCallHandler { call, result ->
                if (call.method == "launchMusicPlayer") {
                    launchMusicPlayer()
                    result.success(null) 
                } else {
                    result.notImplemented()
                }
            }
    }

    private fun launchMusicPlayer() {
        val packageName = "tech.altier.echo_tunes" 
        val intent = packageManager.getLaunchIntentForPackage(packageName)
    
        if (intent != null) {
            startActivity(intent)
        } else {
            // TODO: The music player app is not installed
        }
    }
    
}
