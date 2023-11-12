import { View, Text, TouchableOpacity, StyleSheet, FlatList } from 'react-native';
import { useVacationContext } from './VacationContext';

const VacationCard = ({ vacation }) => {
    const { vacationName, startDate, endDate, members } = vacation;
  
    return (
      <TouchableOpacity style={styles.card}>
        <Text style={styles.cardTitle}>{vacationName}</Text>
        <Text style={styles.cardText}>{`Start Date: ${startDate}`}</Text>
        <Text style={styles.cardText}>{`End Date: ${endDate}`}</Text>
        {/* <Text style={styles.cardText}>{`Members: ${members.join(', ')}`}</Text> */}
      </TouchableOpacity>
    );
  };

const Main = ({ navigation }) => {
  const { vacationGroups } = useVacationContext();

  const handleAddVacation = () => {
    // Logic to navigate to the page where you can create or join a vacation group
    // You can implement this based on your navigation structure
    // For example, navigation.navigate('CreateVacation');
    navigation.navigate('CreateJoin');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>My Vacations</Text>

      {vacationGroups.length === 0 ? (
        <Text style={styles.noVacationText}>No vacations added. Click the + to create or join a vacation group.</Text>
      ) : (
        <FlatList
          data={vacationGroups}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <VacationCard vacation={item} />}
        />
      )}

      <TouchableOpacity style={styles.addButton} onPress={handleAddVacation}>
        <Text style={styles.addButtonText}>+</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
    container: {
      flex: 1,
      alignItems: 'center', // Center horizontally
      padding: 16,
    },
    header: {
      fontSize: 24,
      marginBottom: 20,
    },
    noVacationText: {
      fontSize: 16,
      textAlign: 'center',
      marginBottom: 20,
    },
    addButton: {
      position: 'absolute',
      bottom: 16,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: 'blue',
      width: 100, // Increase the width
      height: 100, // Increase the height
      borderRadius: 50, // Half of the width/height to make it a circle
    },
    addButtonText: {
      color: 'white',
      fontSize: 50, // Increase the font size
      textAlign: 'center', // Center the text horizontally
      lineHeight: 70, // Center the text vertically
    },
    card: {
        backgroundColor: '#fff',
        padding: 16,
        marginBottom: 16,
        borderRadius: 8,
        borderWidth: 1,
        borderColor: '#ccc',
    },
    cardTitle: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 8,
    },
    cardText: {
        fontSize: 16,
        marginBottom: 6,
    },
  });

export default Main;
