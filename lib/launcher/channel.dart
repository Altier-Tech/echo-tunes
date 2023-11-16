import 'package:flutter/services.dart';

const platform = MethodChannel('echo_tunes');

Future<void> launchMusicPlayer() async {
  try {
    await platform.invokeMethod('launchMusicPlayer');
  } on PlatformException catch (e) {
    print("Failed to launch music player: ${e.message}");
  }
}
