import android.content.Context
import android.content.Intent
import android.service.voice.VoiceInteractionService
import android.service.voice.VoiceInteractionSession
import android.os.Bundle
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugins.GeneratedPluginRegistrant
import io.flutter.plugin.common.MethodChannel

class ETVoiceInteractionService : VoiceInteractionService() {
    override fun onNewSession(args: Bundle?): VoiceInteractionSession {
        return ETVoiceInteractionSession(applicationContext)
    }
}
