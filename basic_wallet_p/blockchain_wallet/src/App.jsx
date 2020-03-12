import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [name, setName] = useState('');
  const [sent, setSent] = useState(null);
  const [received, setReceived] = useState(null);

  const handleChange = e => {
    setName(e.target.value);
  };

  const handleSubmit = e => {
    axios.get('http://localhost:5000/chain').then(res => {
      const { chain } = res.data;
      const sentT = [];
      const receivedT = [];
      chain.forEach(node => {
        node.transactions.forEach(transaction => {
          if (transaction.recipient === name) {
            receivedT.push(transaction);
          } else if (transaction.sender === name) {
            sentT.push(transaction);
          }
        });
      });
      setSent(sentT);
      setReceived(receivedT);
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
          {received
            ? `Coins for ${name}: ${received.reduce((acc, curr) => {
                return acc + curr.amount;
              }, 0)}`
            : 'Please enter a name.'}
        </p>
        {(sent || received) && (
          <>
            <h2>Transactions: </h2>
            {sent
              .concat(received)
              .filter(transaction => transaction)
              .map((transaction, index) => (
                <ul key={index}>
                  <li key="sender">
                    Sender:{' '}
                    {transaction.sender === 0 ? 'Mining' : transaction.sender}
                  </li>
                  <li key="recipient">Recipient: {transaction.recipient}</li>
                  <li key="amount">Amount: {transaction.amount}</li>
                </ul>
              ))}
          </>
        )}
      </header>
    </div>
  );
};

export default App;
