import android.content.Context
import android.content.Intent
import android.service.voice.VoiceInteractionSession

class ETVoiceInteractionSession(context: Context) : VoiceInteractionSession(context) {
    override fun onLaunchVoiceAssistFromKeyguard() {
        // TODO Handle the voice command to launch the app
        val intent = Intent(context, MainActivity::class.java) // TODO fix
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        context.startActivity(intent)
        finish()
    }
}
