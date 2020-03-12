import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [name, setName] = useState('');
  const [transactions, setTransactions] = useState(null);

  const handleChange = e => {
    setName(e.target.value);
  };

  const handleSubmit = e => {
    axios.get('http://localhost:5000/chain').then(res => {
      const { chain } = res.data;
      const userTransactions = [];
      chain.forEach(node => {
        node.transactions.forEach(transaction => {
          if (transaction.recipient === name) {
            userTransactions.push(transaction);
          }
        });
      });
      setTransactions(userTransactions);
    });
    e.preventDefault();
  };

  return (
    <div className="App">
      <header className="App-header">
        <form onSubmit={handleSubmit}>
          <label htmlFor="name">
            Name:
            <input
              type="text"
              name="name"
              value={name}
              onChange={handleChange}
            />
          </label>
          <input type="submit" value="Submit" />
        </form>
        <p>
          {transactions
            ? `Coins for ${name}: ${transactions.length}`
            : 'Please enter a name.'}
        </p>
      </header>
    </div>
  );
};

export default App;
