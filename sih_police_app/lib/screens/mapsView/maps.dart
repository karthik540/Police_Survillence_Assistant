import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:sih_policebot/globals.dart' as globals;

class MapScreen extends StatefulWidget{
  //final List<Map<String, String>> locations;
  //MapScreen({@required this.locations});
  @override
  MapScreenState createState() => MapScreenState();
}

class MapScreenState extends State<MapScreen>{
  Completer<GoogleMapController> _controller = Completer();
  Set<Marker> markers = {};
  @override
  void initState(){
    super.initState();
    setState(() => markers = getMarkers());
  }

  @override
  Widget build(BuildContext context){
    return Stack(
      children: <Widget>[
        //Center(child: Text("MapView"))
        _mapView(context)
      ],
    );
  }

  Set<Marker> getMarkers(){
    Map<String, LatLng> loc = {
      "Tambaram": LatLng(12.9249, 80.1000),
      "Avadi": LatLng(13.1067, 80.0970),
      "Egmore": LatLng(13.0732, 80.2609)
    };
    
    //List<Marker> out = List();
    //this.widget.locations.forEach((k, v) => out.add(new Marker(markerId: )));
    var out = globals.locations.map((Map i) => Marker(
      markerId: MarkerId(i["location"]),
      position: loc[i["location"]],
      infoWindow: InfoWindow(title: globals.suspect + ", Last seen: " + i["time"]),
      icon: BitmapDescriptor.defaultMarkerWithHue(
        BitmapDescriptor.hueOrange
      )
    )).toSet();
    print(out);
    return out;
  }

  Widget _mapView(BuildContext context){
    return Container(
      height: MediaQuery.of(context).size.height,
      width: MediaQuery.of(context).size.width,
      child: GoogleMap(
        mapType: MapType.normal,
        initialCameraPosition: CameraPosition(
          target: LatLng(13.0317, 80.1817),
          zoom: 11
        ),
        onMapCreated: (GoogleMapController controller){
          _controller.complete(controller);
        },
        markers: markers
      ),
    );
  }
}

/*Marker marker1 = Marker(
  markerId: MarkerId("marker1"),
  position: LatLng(37.42796133580664, -122.015749655962),
  infoWindow: InfoWindow(title: "Place 1"),
  icon: BitmapDescriptor.defaultMarkerWithHue(
    BitmapDescriptor.hueOrange
  )
);

Marker marker2 = Marker(
  markerId: MarkerId("marker2"),
  position: LatLng(37.42796133580664, -122.06),
  infoWindow: InfoWindow(title: "Place 2"),
  icon: BitmapDescriptor.defaultMarkerWithHue(
    BitmapDescriptor.hueBlue
  ),
  draggable: true
);

Marker marker3 = Marker(
  markerId: MarkerId("marker3"),
  position: LatLng(37.35796133580664, -122.09),
  infoWindow: InfoWindow(title: "Place 3"),
  icon: BitmapDescriptor.defaultMarkerWithHue(
    BitmapDescriptor.hueViolet
  ),
  draggable: true
);

Marker marker4 = Marker(
  markerId: MarkerId("marker4"),
  position: LatLng(37.47796133580664, -122.06),
  infoWindow: InfoWindow(title: "Place 4"),
  icon: BitmapDescriptor.defaultMarkerWithHue(
    BitmapDescriptor.hueRed
  ),
  draggable: true
);

Set<Marker> markers = new Set.from([marker1, marker2, marker3, marker4]);*/