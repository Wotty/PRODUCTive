import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';

void main() async {

  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {

    return MaterialApp(

      title: 'Flutter Firebase App',

      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,

      ),
      home: HomePage(),

    );

  }

}

class HomePage extends StatelessWidget {

  @override

  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(

        title: Text('Firebase Integration'),

      ),

      body: Center(

        child: Column(

          mainAxisAlignment: MainAxisAlignment.center,

          children: [

            ElevatedButton(

              onPressed: () {

                // Add your authentication flow here

              },

              child: Text('Sign In'),

            ),

            SizedBox(height: 20),

            ElevatedButton(

              onPressed: () {

                // Add your Firestore database functionality here

              },

              child: Text('Firestore'),

            ),

          ],

        ),

      ),

    );

  }

}