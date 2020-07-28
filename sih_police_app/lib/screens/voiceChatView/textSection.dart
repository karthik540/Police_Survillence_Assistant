import 'package:flutter/material.dart';

class TextSection extends StatelessWidget {
  final Widget widget;

  TextSection(this.widget);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: MediaQuery.of(context).size.width * 0.8,
      height: MediaQuery.of(context).size.height * 0.1,
      child: Center(child: widget),
      decoration: BoxDecoration(
          color: Colors.grey, borderRadius: BorderRadius.circular(10.0)),
    );
  }
}
