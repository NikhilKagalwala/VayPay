// CreateGroup.js

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { useVacationContext } from './VacationContext';

const CreateGroup = ({ navigation }) => {
  const { addVacationGroup } = useVacationContext();

  const [vacationName, setVacationName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [groupPassword, setGroupPassword] = useState('');

  const flaskServerBaseUrl = 'http://34.132.122.94:5000';

  const generateUniqueID = () => {
    const timestamp = new Date().getTime();
    const random = Math.floor(Math.random() * 1000000);
    return `${timestamp}-${random}`;
  };


  const handleCreateGroup = async () => {
    try {
      const newGroup = {
        id: generateUniqueID(),
        vacationName,
        startDate,
        endDate,
        groupPassword,
      };

      const groupData = {
        vacation_title: vacationName,
        group_password: groupPassword,
        vacation_start_datetime: startDate,
        vacation_end_datetime: endDate,
      };

      console.log('Sending data to server:', groupData);

  
      // Send data to your Flask server
      const response = await fetch(`${flaskServerBaseUrl}/api/addGroup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(groupData),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const responseData = await response.json();
      console.log('Response from Flask:', responseData);
  
      addVacationGroup(newGroup);
      navigation.navigate('Main');
    } catch (error) {
      console.error('Error creating group:', error.message);
    }
  };
  


  return (
    <View style={styles.container}>
      <Text style={styles.header}>Create Vacation Group</Text>

      <TextInput
        style={styles.input}
        placeholder="Vacation Name"
        onChangeText={(text) => setVacationName(text)}
      />

      <TextInput
        style={styles.input}
        placeholder="Start Date"
        onChangeText={(text) => setStartDate(text)}
      />

      <TextInput
        style={styles.input}
        placeholder="End Date"
        onChangeText={(text) => setEndDate(text)}
      />

      <TextInput
        style={styles.input}
        placeholder="Group Password"
        onChangeText={(text) => setGroupPassword(text)}
        secureTextEntry={true}
      />

      <TouchableOpacity style={styles.createButton} onPress={handleCreateGroup}>
        <Text style={styles.buttonText}>Create Group</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  header: {
    fontSize: 20,
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
  createButton: {
    backgroundColor: 'green',
    padding: 15,
    borderRadius: 8,
    width: 200,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
  },
});

export default CreateGroup;
