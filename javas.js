function accessBDO() {
  const data = {
    URL: 'https://blackdesertonline.fandom.com/wiki/Black_Desert_Online_Wiki',
    BASE_URL: 'https://blackdesertonline.fandom.com/wiki/'
  };

  fetch('/access', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response data here
      console.log(data.message);
      // Process the rest of the data as needed
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

accessBDO();
