import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import 'voiceIO.dart';

class VoiceChatScreen extends StatefulWidget{
  final String ip;
  VoiceChatScreen({@required this.ip});
  @override
  _VoiceChatScreenState createState() => _VoiceChatScreenState();
}

class _VoiceChatScreenState extends State<VoiceChatScreen> {

  bool _permissionGranted = false;
  
  @override
  void initState(){
    super.initState();
    getRequiredPermission();
  }

  void getRequiredPermission() async{
    final PermissionHandler permissionHandler = new PermissionHandler();
    var res = await permissionHandler.requestPermissions([PermissionGroup.microphone]);
    if(res[PermissionGroup.microphone] == PermissionStatus.granted)
      setState(() => _permissionGranted = true);
  }

  @override
  Widget build(BuildContext context){
    return _permissionGranted ? voiceChat(context, this.widget.ip) : grantPermission(getRequiredPermission);
  }
}

Widget voiceChat(BuildContext context, String ip){
  return ConstrainedBox(
      constraints: BoxConstraints(maxHeight: MediaQuery.of(context).size.height),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Container(
            width: 150,
            height: 150,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              image: DecorationImage(
                  fit: BoxFit.cover,
                  image: AssetImage("assets/durai_singam_crp.jpg")
                )
            )
          ),
          VoiceIO(ip: ip)
        ],
      )
    );
    //), physics: AlwaysScrollableScrollPhysics(),);
}

Widget grantPermission(Function getRequiredPermission){
  return Container(
    color: Colors.black,
    child: Center(
      child: RaisedButton(
        child: Text("Grant Microphone Permission", style: TextStyle(fontSize: 20),),
        color: Colors.red,
        textColor: Colors.black,
        splashColor: Colors.green,
        onPressed: getRequiredPermission,
      )
    ),
  );
} 

