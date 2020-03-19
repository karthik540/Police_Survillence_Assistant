import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:http/http.dart' as http;
import 'msg.dart';

class TextChatScreen extends StatefulWidget{
  @override
  _TextChatScreenState createState() => _TextChatScreenState();
}

class _TextChatScreenState extends State<TextChatScreen> with TickerProviderStateMixin{
  final TextEditingController _controller = new TextEditingController();
  final List<Msg> _messages = <Msg>[];
  bool _isWriting = false;

  @override
  void initState(){
    super.initState();
  }

  @override
  Widget build(BuildContext context){
    return Column(
      children: <Widget>[
        Flexible(
          child: ListView.builder(
            itemBuilder: (_, int index) => _messages[index],
            itemCount: _messages.length,
            reverse: true,
            padding: EdgeInsets.all(5.0),
          ),
        ),
        Divider(height: 1.0,),
        Container(
          child: inputField(),
          decoration: BoxDecoration(color: Theme.of(context).cardColor),
        )
      ],
    );
  }
  Widget inputField(){
    return IconTheme(
      data: IconThemeData(color: Theme.of(context).accentColor),
      child: Container(
        margin: EdgeInsets.symmetric(horizontal: 8.0),
        child: Row(
          children: <Widget>[
            Flexible(
              child: TextField(
                controller: _controller,
                onChanged: (String txt) => setState(() => _isWriting = txt.length > 0),
                onSubmitted: submitMessage,
                decoration: InputDecoration.collapsed(hintText: "Enter some text!"),
              ),
            ),
            Container(
              padding: EdgeInsets.symmetric(horizontal: 3.0),
              child: IconButton(
                icon: Icon(Icons.send),
                onPressed: _isWriting ? () => submitMessage(_controller.text) : null
              )
            )
          ],
        ),
      ),
    );
  }

  void submitMessage(String message) async{
    _controller.clear();
    setState(() => _isWriting = false);
    Msg msg = new Msg(txt: message, animationController: new AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 500)
    ));
    setState(() => _messages.insert(0, msg));
    
    msg.animationController.forward();
    await makeRequest(message);
  }

  Future<void> makeRequest(_inputText) async {
    print("Making req");
    /*await http.post("http://192.168.43.69:5000/botResponse", body: {"utext": "hello"}).then((http.Response res){
      if(res.statusCode == 200){
        print(res.body);
      }else{
        print(res.statusCode);
      }
    }).catchError((err) => print(err));*/
    print("Done");
  }

  @override
  void dispose(){
    for(Msg msg in _messages){
      msg.animationController.dispose();
    }
    super.dispose(); 
  }
}

