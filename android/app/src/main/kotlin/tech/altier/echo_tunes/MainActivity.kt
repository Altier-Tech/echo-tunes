package tech.altier.echo_tunes

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugins.GeneratedPluginRegistrant
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        GeneratedPluginRegistrant.registerWith(flutterEngine)

        // Set up method channel
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "your_channel_name")
            .setMethodCallHandler { call, result ->
                if (call.method == "launchMusicPlayer") {
                    // Handle the method call, e.g., launch the music player
                    launchMusicPlayer()
                    result.success(null) // You can send a result back to Dart if needed
                } else {
                    result.notImplemented()
                }
            }
    }

    private fun launchMusicPlayer() {
        // Implement the logic to launch the music player
    }
}
