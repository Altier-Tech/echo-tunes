

class ETVoiceInteractionService : VoiceInteractionService() {
    override fun onNewSession(args: Bundle?): VoiceInteractionSession {
        return ETVoiceInteractionSession(applicationContext)
    }
}
