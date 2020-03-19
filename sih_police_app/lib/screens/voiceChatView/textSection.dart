import 'package:flutter/material.dart';

class TextSection extends StatelessWidget{
  final String text;

  TextSection(this.text);
  
  @override
  Widget build(BuildContext context) {
    return Container(
      width: MediaQuery.of(context).size.width * 0.8,
      height: MediaQuery.of(context).size.height * 0.1,
      child: Center(
        child: Text(
          text,
          style: TextStyle(
            fontSize: 18
          ),
        )
      ),
      decoration: BoxDecoration(
        color: Colors.grey,
        borderRadius: BorderRadius.circular(10.0) 
      ),
    );
  }

}