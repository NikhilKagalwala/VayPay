// VacationContext.js

import React, { createContext, useContext, useState } from 'react';

const VacationContext = createContext();

const VacationProvider = ({ children }) => {
  const [vacationGroups, setVacationGroups] = useState([]);

  const addVacationGroup = (newGroup) => {
    setVacationGroups((prevGroups) => [...prevGroups, newGroup]);
  };

  return (
    <VacationContext.Provider value={{ vacationGroups, addVacationGroup }}>
      {children}
    </VacationContext.Provider>
  );
};

const useVacationContext = () => {
  return useContext(VacationContext);
};

export { VacationProvider, useVacationContext };
