const mysql = require('mysql');

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'root1234',
  database: 'testdb',
});

connection.connect((error) => {
  if (error) {
    console.error('Error connecting to MySQL database:', error.message);
    process.exit(1);
  }

  console.log('Successfully connected to MySQL database.');
  connection.end((endError) => {
    if (endError) {
      console.error('Error closing MySQL connection:', endError.message);
      process.exit(1);
    }
  });
});
