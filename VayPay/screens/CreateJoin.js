// CreateJoin.js

import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';

const CreateJoin = () => {
    const navigation = useNavigation();

  const handleCreate = () => {
    // Handle logic for creating a vacation group
    console.log('Create button clicked');
    navigation.navigate('CreateGroup');

  };

  const handleJoin = () => {
    // Handle logic for joining a vacation group
    console.log('Join button clicked');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Create or Join a Vacation Group</Text>

      <TouchableOpacity style={styles.createButton} onPress={handleCreate}>
        <Text style={styles.buttonText}>Create</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.joinButton} onPress={handleJoin}>
        <Text style={styles.buttonText}>Join</Text>
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
  createButton: {
    backgroundColor: 'green',
    padding: 15,
    borderRadius: 8,
    marginBottom: 16,
    width: 200,
    alignItems: 'center',
  },
  joinButton: {
    backgroundColor: 'blue',
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

export default CreateJoin;
