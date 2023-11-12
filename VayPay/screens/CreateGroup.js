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

  const handleCreateGroup = () => {
    // Implement logic to handle creating the group with the entered details-
    const newGroup = {
      vacationName,
      startDate,
      endDate,
      groupPassword,
    };

    // Add the new group to the context
    addVacationGroup(newGroup);

    // After creating the group, you can navigate back to the 'Main' screen
    navigation.navigate('Main');
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
