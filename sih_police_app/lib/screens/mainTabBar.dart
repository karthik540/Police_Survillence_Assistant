import 'package:flutter/material.dart';
//import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:sih_policebot/main.dart';
import 'mapsView/maps.dart';
import 'textChatView/textChat.dart';
import 'voiceChatView/voiceChat.dart';
import 'package:sih_policebot/globals.dart' as globals;

class MainTabBar extends StatefulWidget{
  @override
  _MainTabBarState createState() => _MainTabBarState();
}

class _MainTabBarState extends State<MainTabBar> with SingleTickerProviderStateMixin{
  TabController _controller;
  String _ip = "172.16.40.230";
  bool _isGranted = false;
  //List<Map<String, String>> {[{"Chennai": "10:20"}, {"Chennai": "10:20"}, {"Chennai": "10:20"}]};
  //static final _voiceChatKey = new GlobalKey<_voiceChatKeyState>();
  //var l = [{"location":"Chennai","time":"10:20"}, {"location":"Delhi","time":"10:20"}, {"location":"Mumbai","time":"10:20"}];

  @override
  void initState(){
    super.initState();
    _controller = TabController(
      length: 3,
      vsync: this,
      initialIndex: 1
    )..addListener(() => setState(() => {}));
  }
  @override
  void dispose(){
    _controller.dispose();
    //_textController.dispose();
    super.dispose();
  }
  void setIp(BuildContext context) async{
    final TextEditingController controller = TextEditingController();
    await showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Center(child: Text("Current IP: " + _ip)),
        contentPadding: EdgeInsets.all(16.0),
        content: TextField(
              controller: controller,
              autofocus: true,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(hintText: "Enter new IP"),
        ),
        actions: <Widget>[
          FlatButton(
            child: Text("Cancel"),
            onPressed: () => Navigator.pop(context),
          ),
          FlatButton(
            child: Text("Set"),
            onPressed: () {
              setState(() => _ip = controller.text);
              print("Done");
              Navigator.pop(context);
            },
          )
        ],
        elevation:  24.0,
      )
    );
    //controller.dispose();
  }
  Future<void> getPermission() async{
    final PermissionHandler permissionHandler = new PermissionHandler();
    var status = await permissionHandler.checkPermissionStatus(PermissionGroup.camera);
    if(status != PermissionStatus.granted){
      var res = await permissionHandler.requestPermissions([PermissionGroup.camera]);
      if(res[PermissionGroup.camera] == PermissionStatus.granted)
        setState(() => _isGranted = true);
    }
  }
  void translateImage() async{
    await getPermission();

    //var image = await ImagePicker.pickImage(source: ImageSource.camera);
    //print(image);
  }
  @override
  Widget build(BuildContext context){
    return DefaultTabController(
      length: 3,
      initialIndex: 1,
      child: Scaffold(
        appBar: AppBar(
          elevation: 6.0,
          bottom: TabBar(
            controller: _controller,
            tabs: <Widget>[
              Tab(icon: Icon(Icons.map)),
              Tab(icon: Icon(Icons.record_voice_over)),
              Tab(icon: Icon(Icons.chat))
            ],
          ),
          title: Text("Singam"),
          centerTitle: true,
          actions: <Widget>[
            IconButton(
              icon: Icon(Icons.settings),
              onPressed: (){
                setIp(context);
              },
            )
          ],
        ),
        body: TabBarView(
          controller: _controller,
          physics: NeverScrollableScrollPhysics(),
          children: <Widget>[
            MapScreen(),
            VoiceChatScreen(ip: _ip),
            TextChatScreen()
          ],
        ),
        floatingActionButton: _controller.index == 1 ? ImageTranslator(translate: translateImage) : null,
        resizeToAvoidBottomPadding: false,
      ),
    );
  }
}

class ImageTranslator extends StatelessWidget {
  final Function translate;
  ImageTranslator({this.translate});
  @override
  Widget build(BuildContext context){
    return FloatingActionButton(
      onPressed: () => translate(),
      tooltip: "Capture an image for images to translated text",
      child: Icon(Icons.camera)
    );
  }
}