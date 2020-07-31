import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:speech_recognition/speech_recognition.dart';
import 'package:flutter_tts/flutter_tts.dart';
//import 'package:translator/translator.dart';
import 'package:http/http.dart' as http;
//import 'package:dio/dio.dart';
import 'textSection.dart';
import 'package:sih_policebot/globals.dart' as globals;

class VoiceIO extends StatefulWidget {
  final String ip;
  final bool voiceInput;
  VoiceIO({@required this.ip, @required this.voiceInput});
  @override
  _VoiceIOState createState() => _VoiceIOState();
}

class _VoiceIOState extends State<VoiceIO> {
  BuildContext _context;
  SpeechRecognition _speechRecognition;
  FlutterTts _flutterTts;
  //GoogleTranslator _translator;
  bool _isAvailable;
  bool _isListening = false;
  bool _isSpeaking = false;
  bool _requested = false;
  String _inputText = "";
  String _resultText = "";

  @override
  void initState() {
    super.initState();
    initialize();
  }

  void initialize() {
    if (this.widget.voiceInput) {
      _speechRecognition = SpeechRecognition();
      _speechRecognition.setAvailabilityHandler(
          (bool status) => setState(() => _isAvailable = status));
      _speechRecognition.setRecognitionStartedHandler(() => setState(() {
            _requested = false;
            _isListening = true;
            _inputText = "";
            _resultText = "";
          }));

      _speechRecognition.setRecognitionResultHandler((String result) {
        setState(() => _inputText = result);
      });

      _speechRecognition.setRecognitionCompleteHandler(() async {
        setState(() => _isListening = false);
        print(_inputText);
        if (!_requested && !_isSpeaking) {
          await makeRequest(_inputText);
        }
      });
      //_speechRecognition.noSuchMethod(invocation)
      _speechRecognition
          .activate()
          .then((status) => setState(() => _isAvailable = status));
    }

    _flutterTts = FlutterTts();
    _flutterTts.setStartHandler(() => setState(() => _isSpeaking = true));
    _flutterTts.setCompletionHandler(() => setState(() {
          _isSpeaking = false;
        }));
    _flutterTts
        .setErrorHandler((err) => showErrorMessage("TTS: " + err.toString()));
    //_translator = GoogleTranslator();
  }

  Future<void> makeRequest(String msg) async {
    print("Making req");

    try {
      print("x" + msg + "x");
      //_translator.translate(_inputText, from: "hi", to: "en").then((res) => print(res));
      if (msg.contains(" ")) {
        if (!_requested) setState(() => _requested = true);
        print("here");
        //if(_inputText.contains("scene"))
        //onResponse("Analyzing");
        //globals.locations = [{"location":"Chennai","time":"10:21"}, {"location":"Delhi","time":"10:20"}, {"location":"Mumbai","time":"10:20"}];
        http.post("http://" + this.widget.ip + ":5000/botResponse",
            body: {"utext": _inputText}).then((http.Response res) {
          if (res.statusCode == 200) {
            if (msg.contains("track")) {
              globals.suspect = _inputText.split(" ")[1];
              setLocations(jsonDecode(res.body)["response"]);
              onResponse("Locations fetched!");
            } else
              onResponse(jsonDecode(res.body)["response"]);
          } else if (res.statusCode != 500) {
            showErrorMessage("Status code: " + res.statusCode.toString());
          }
          setState(() {
            _requested = false;
            //_inputText = "";
          });
          print("Done");
        });
        /*setState(() {
          _requested = false;
          _inputText = "";
        });*/
        //setState(() => _requested = false);
        //}
      }
    } catch (err) {
      setState(() => _requested = false);
      showErrorMessage(err.toString());
    }
  }

  void setLocations(String res) {
    var lm = List<Map<String, String>>();
    var lists = jsonDecode(res);
    for (var l in lists) {
      Map<String, String> m = {"location": l["location"], "time": l["time"]};
      print(l["location"] + l["time"]);
      lm.add(m);
    }
    Map<String, String> m1 = {
      "location": "Avadi",
      "time": "22 Feb 2020, 14:20pm"
    };
    lm.add(m1);
    globals.locations = lm;
  }

  Future onResponse(String response) async {
    setState(() => _resultText = response);
    await _flutterTts.speak(_resultText);
  }

  Future stopReading() async {
    await _flutterTts.stop();
    setState(() => _isSpeaking = false);
  }

  void showErrorMessage(String message) {
    showDialog(
        context: _context,
        builder: (_) => AlertDialog(
              title: Text("Error"),
              content: Text(message),
              elevation: 24.0,
            ));
  }

  @override
  Widget build(BuildContext context) {
    _context = context;
    return ConstrainedBox(
        constraints:
            BoxConstraints(minHeight: MediaQuery.of(context).size.height * 0.5),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            this.widget.voiceInput
                ? TextSection(Text(
                    _inputText,
                    style: TextStyle(fontSize: 18),
                  ))
                : TextSection(
                    Padding(
                      padding: EdgeInsets.all(20),
                      child: TextField(
                        //controller: controller,
                        onChanged: (text) => setState(() => _inputText = text),
                        decoration: InputDecoration(
                          hintText: "Enter a message",
                        ),
                        style: TextStyle(fontSize: 18),
                      ),
                    ),
                  ),
            TextSection(Text(
              _resultText,
              style: TextStyle(fontSize: 18),
            )),
            this.widget.voiceInput
                ? FloatingActionButton(
                    child: Icon(_isListening
                        ? Icons.hearing
                        : _isSpeaking ? Icons.stop : Icons.keyboard_voice),
                    backgroundColor: _isListening
                        ? Colors.green
                        : _isSpeaking ? Colors.red : Colors.blue,
                    onPressed: () {
                      if (_isSpeaking)
                        stopReading();
                      else if (_isAvailable && !_isListening)
                        _speechRecognition
                            .listen(locale: "en_IN")
                            .then((result) => print("Result: " + result));
                    },
                  )
                : FloatingActionButton(
                    onPressed: () => makeRequest(_inputText),
                    child: Icon(Icons.send),
                  ),
          ],
        ));
  }
}
