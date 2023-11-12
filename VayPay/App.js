// App.js

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Register from './screens/Register';
import Login from './screens/Login';
import Main from './screens/Main';
import CreateJoin from './screens/CreateJoin';
import CreateGroup from './screens/CreateGroup';
import { VacationProvider } from './screens/VacationContext';


const Stack = createStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <VacationProvider>
        <Stack.Navigator initialRouteName="Login">
          <Stack.Screen name="Register" component={Register} />
          <Stack.Screen name="Login" component={Login} />
          <Stack.Screen name="Main" component={Main} />
          <Stack.Screen name="CreateJoin" component={CreateJoin} />
          <Stack.Screen name="CreateGroup" component={CreateGroup} />
        </Stack.Navigator>
      </VacationProvider>
    </NavigationContainer>
  );
};

export default App;
