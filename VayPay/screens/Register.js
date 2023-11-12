// Register.js

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';

// Assuming this code is inside a React Native component or utility function

const flaskServerBaseUrl = 'http://34.132.122.94:5000';

// Example function to make a GET request
const fetchDataFromFlask = async () => {
  try {
    const response = await fetch(`${flaskServerBaseUrl}/api/test`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Data from Flask:', data);

    // Perform further actions with the data as needed
  } catch (error) {
    console.error('Error fetching data from Flask:', error.message);
    // Handle the error
  }
};

// Example function to make a POST request
const postDataToFlask = async (data) => {
  try {
    const response = await fetch(`${flaskServerBaseUrl}/api/addUser`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        data
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();
    console.log('Response from Flask:', responseData);

    // Perform further actions with the response data as needed
  } catch (error) {
    console.error('Error posting data to Flask:', error.message);
    // Handle the error
  }
};

// Call the functions
// fetchDataFromFlask();
// postDataToFlask();



const Register = ({ navigation }) => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [country, setCountry] = useState('');
  const [password, setPassword] = useState('');

  const handleRegistration = async () => {

      const userData = {
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber,
        country: country,
        email: email,
        password_hash: password
      };

      postDataToFlask(userData);
      // fetchDataFromFlask();
      // Add your logic after successful registration
      navigation.navigate('Main');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Registration</Text>

      <TextInput
        style={styles.input}
        placeholder="First Name"
        onChangeText={(text) => setFirstName(text)}
      />

      <TextInput
        style={styles.input}
        placeholder="Last Name"
        onChangeText={(text) => setLastName(text)}
      />

      <TextInput
        style={styles.input}
        placeholder="Email"
        onChangeText={(text) => setEmail(text)}
        keyboardType="email-address"
      />

      <TextInput
        style={styles.input}
        placeholder="Phone Number"
        onChangeText={(text) => setPhoneNumber(text)}
        keyboardType="numeric"
      />

      <TextInput
        style={styles.input}
        placeholder="Country"
        onChangeText={(text) => setCountry(text)}
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        onChangeText={(text) => setPassword(text)}
        secureTextEntry={true}
      />

      <TouchableOpacity style={styles.button} onPress={handleRegistration}>
        <Text style={styles.buttonText}>Register</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    fontSize: 24,
    marginBottom: 20,
  },
  input: {
    width: '80%',
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 20,
    paddingLeft: 10,
  },
  button: {
    backgroundColor: 'blue',
    padding: 10,
    borderRadius: 5,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
  },
});

export default Register;
