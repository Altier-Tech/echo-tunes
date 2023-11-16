import android.content.Context
import android.content.Intent
import android.service.voice.VoiceInteractionService
import android.service.voice.VoiceInteractionSession
import android.os.Bundle

class ETVoiceInteractionService : VoiceInteractionService() {
    override fun onNewSession(args: Bundle?): VoiceInteractionSession {
        return ETVoiceInteractionSession(applicationContext)
    }
}
