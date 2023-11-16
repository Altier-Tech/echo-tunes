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
        // TODO Implement the logic to launch the music player
    }
}
